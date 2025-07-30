'''Generates variations of a dataset using a pool of feature engineering
techniques. Used for training ensemble models.'''

import logging
from pathlib import Path
from random import choice, shuffle

import h5py
import numpy as np
import pandas as pd

import ensembleset.feature_engineerings as engineerings
import ensembleset.feature_methods as fm

logging.captureWarnings(True)


class DataSet:
    '''Dataset generator class.'''

    def __init__(
            self,
            label: str,
            train_data: pd.DataFrame,
            test_data: pd.DataFrame = None,
            string_features: list = None,
            data_directory: str = 'ensembleset_data',
            ensembleset_name: str = 'ensembleset.h5'
        ):

        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())

        # Check user argument types
        type_check = self._check_argument_types(
            label=label,
            train_data=train_data,
            test_data=test_data,
            string_features=string_features,
            data_directory=data_directory,
            ensembleset_name=ensembleset_name
        )

        # If the type check passed, assign arguments to attributes
        if type_check is True:
            self.label = label
            self.train_data = train_data.copy()

            if test_data is not None:
                self.test_data = test_data.copy()

            else:
                self.test_data = None

            self.string_features = string_features
            self.data_directory = data_directory
            self.ensembleset_name = ensembleset_name

        # Get the init logger
        logger.info("Training label: '%s'", self.label)
        logger.info('Training data: %s', type(self.train_data))
        logger.info('Testing data: %s', type(self.test_data))
        logger.info('String features: %s', self.string_features)
        logger.info('Data directory: %s', self.data_directory)
        logger.info('Ensembleset name: %s', self.ensembleset_name)

        # Enforce string type on DataFrame columns
        self.train_data.columns = self.train_data.columns.astype(str)

        if self.test_data is not None:
            self.test_data.columns = self.test_data.columns.astype(str)

        # Retrieve and assign the training labels, set NAN if they don't exist
        # then remove them from the training data
        if self.label in self.train_data.columns:
            self.train_labels=np.array(self.train_data[label])
            self.train_data.drop(self.label, axis=1, inplace=True)

        else:
            self.train_labels=[np.nan] * len(self.train_data)

        # Retrieve and assign the testing labels, set NAN if they don't exist
        # then remove them from the training data
        if self.test_data is not None:
            if self.label in self.test_data.columns:
                self.test_labels=np.array(self.test_data[label])
                self.test_data.drop(self.label, axis=1, inplace=True)

            else:
                self.test_labels=[np.nan] * len(self.test_data)

        else:
            self.test_labels = None

        # Create the HDF5 output
        Path(self.data_directory).mkdir(parents=True, exist_ok=True)

        # Create groups for training and testing datasets
        with h5py.File(f'{self.data_directory}/{self.ensembleset_name}', 'a') as hdf:

            _ = hdf.require_group('train')

            if self.test_data is not None:
                _ = hdf.require_group('test')

        # Add the training and testing labels
        with h5py.File(f'{self.data_directory}/{self.ensembleset_name}', 'w') as hdf:

            _ = hdf.create_dataset('train/labels', data=self.train_labels)

            if self.test_data is not None:
                _ = hdf.create_dataset('test/labels', data=self.test_labels)

        # Define the feature engineering pipeline methods
        self.string_encodings=engineerings.STRING_ENCODINGS
        self.numerical_methods=engineerings.NUMERICAL_METHODS


    def make_datasets(self, n_datasets:int, frac_features:int, n_steps:int):
        '''Makes n datasets with different feature subsets and pipelines.'''

        logger = logging.getLogger(__name__ + '.make_datasets')
        logger.addHandler(logging.NullHandler())

        logger.info('Will make %s datasets', n_datasets)
        logger.info('Running %s feature engineering steps per dataset', n_steps)
        logger.info('Selecting %s percent of features for each step', round(frac_features * 100))

        with h5py.File(f'{self.data_directory}/{self.ensembleset_name}', 'a') as hdf:

            # Generate n datasets
            for n in range(n_datasets):

                logger.info('Generating dataset %s of %s', n+1, n_datasets)
                logger.info('Input training data shape: %s', self.train_data.shape)

                # Take a copy of the training and test data
                train_df = self.train_data.copy()

                if self.test_data is not None:
                    test_df = self.test_data.copy()
                    logger.info('Input testing data shape: %s', self.test_data.shape)

                else:
                    test_df = None

                # Generate a data pipeline
                pipeline = self._generate_data_pipeline(n_steps)

                # Set input n features for first round
                input_n_features = int(len(train_df.columns.to_list()) * frac_features)
                input_n_features = max([input_n_features, 1])

                # Loop on and apply each method in the pipeline
                for method, arguments in pipeline.items():

                    func = getattr(fm, method)

                    if method in self.string_encodings:

                        logger.info('Applying %s to %s' , method, self.string_features)

                        train_df, test_df = func(
                            train_df,
                            test_df,
                            self.string_features,
                            arguments
                        )

                    else:

                        n_features = int(len(train_df.columns.to_list()) * frac_features)
                        n_features = max([n_features, 1])
                        n_features = min([n_features, 2 * input_n_features])
                        input_n_features = n_features

                        features = self._select_features(n_features, train_df)

                        logger.info('Applying %s to %s features' , method, len(features))

                        train_df, test_df = func(
                            train_df,
                            test_df,
                            features,
                            arguments
                        )

                        logger.info('New training data shape: %s', train_df.shape)

                        if test_df is not None:
                            logger.info('New testing data shape: %s', test_df.shape)

                # Save the results to HDF5 output
                _ = hdf.create_dataset(f'train/{n}', data=np.array(train_df).astype(np.float64))

                if test_df is not None:
                    _ = hdf.create_dataset(f'test/{n}', data=np.array(test_df).astype(np.float64))


    def _select_features(self, n_features:int, data_df:pd.DataFrame):
        '''Selects a random subset of features.'''

        features = data_df.columns.to_list()
        shuffle(features)
        features = features[:n_features]

        return features


    def _generate_data_pipeline(self, n_steps:int):
        '''Generates one random sequence of feature engineering operations. Starts with
        a string encoding method if we have string features.'''

        pipeline={}

        # Choose a string encoding method, if needed
        if self.string_features is not None:
            options = list(self.string_encodings.keys())
            selection = choice(options)
            pipeline[selection] = self.string_encodings[selection]

        # Construct a random sequence of numerical feature engineering methods
        methods = list(self.numerical_methods.keys())
        shuffle(methods)
        methods = methods[:n_steps]

        for method in methods:

            pipeline[method] = {}
            parameters = self.numerical_methods[method]

            for parameter, values in parameters.items():

                value = choice(values)
                pipeline[method][parameter] = value

        return pipeline


    def _check_argument_types(
            self,
            label: str,
            train_data: pd.DataFrame,
            test_data: pd.DataFrame,
            string_features: list,
            data_directory: str,
            ensembleset_name: str
    ) -> bool:

        '''Checks user argument types, returns true or false for all passing.'''

        check_pass = False

        if isinstance(label, str):
            check_pass = True

        else:
            raise TypeError('Label is not a string.')

        if isinstance(train_data, pd.DataFrame):
            check_pass = True

        else:
            raise TypeError('Train data is not a Pandas DataFrame.')

        if isinstance(test_data, pd.DataFrame) or test_data is None:
            check_pass = True

        else:
            raise TypeError('Test data is not a Pandas DataFrame.')

        if isinstance(string_features, list) or string_features is None:
            check_pass = True

        else:
            raise TypeError('String features is not a list.')

        if isinstance(data_directory, str):
            check_pass = True

        else:
            raise TypeError('Data directory is not a string.')

        if isinstance(ensembleset_name, str):
            check_pass = True

        else:
            raise TypeError('Ensembleset name is not a string.')

        return check_pass
