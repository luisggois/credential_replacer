import unittest
import os
import pathlib
import Replacer
import shutil
import logging


class TestReplacerInit(unittest.TestCase):

    '''
    Keyword arguments expected
    ----------
    file_directory - **str**
    parsed_destination - **str**
    encrypted_user - **str**
    encrypted_password - **str**

    Kwargs validation
    ----------
    :raises AttributeError - keyword introduced is not valid
    :raises TypeError - kwarg is not of type str
    :raises FileNotFoundError - provided path directory does not exist
    :raises AttributeError - not all mandatory keywords were set

    '''

    @classmethod
    def setUpClass(cls):
        ''' 
        Create two dirs for testing, one with files to encrypt, the other where encrypted
        files will be placed. setUpClass is being used because only __init__ method is 
        being tested, so no changes will be done to the folders created during testing 

        '''
        logging.disable(logging.CRITICAL)

        os.mkdir('./ssh_files')
        pathlib.Path('./ssh_files/test_file.txt').touch()
        os.mkdir('./parsed_files')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('./ssh_files')
        shutil.rmtree('./parsed_files')
        logging.disable(logging.NOTSET)

    # When all kwargs are provided, all values have the correct type and all the provided dir paths exist
    def test_init_ok(self):

        obj = Replacer.Replacer(file_directory='ssh_files', parsed_destination='parsed_files',
                                encrypted_password='pass123', encrypted_user='user123')

        self.assertEqual(obj.file_directory, os.path.abspath('ssh_files'))
        self.assertEqual(obj.parsed_destination, os.path.abspath('parsed_files'))
        self.assertEqual(obj.encrypted_password, 'pass123')
        self.assertEqual(obj.encrypted_user, 'user123')

    # Wrong types of args
    def test_init_wrong_val_types(self):

        with self.assertRaises(TypeError):
            Replacer.Replacer(file_directory=1, parsed_destination='parsed_files',
                              encrypted_password='pass123', encrypted_user='user123')

        with self.assertRaises(TypeError):
            Replacer.Replacer(file_directory='ssh_files', parsed_destination='parsed_files',
                              encrypted_password=True, encrypted_user='user123')

    # Invalid kwargs
    def test_init_invalid_kwargs(self):

        with self.assertRaises(AttributeError):
            Replacer.Replacer(file_directory='ssh_files', parsed_destination='parsed_files',
                              encrypted_password='pass123', encrypted_user='user123', wrong_keyword='foo')

        with self.assertRaises(AttributeError):
            Replacer.Replacer(file_directory='ssh_files', wrong_keyword='bar', parsed_destination='parsed_files',
                              encrypted_password='pass123', encrypted_user='user123')

    # Not all mandatory kwargs were set
    def test_init_invalid_attr_setting(self):

        with self.assertRaises(AttributeError):
            Replacer.Replacer(new_file_directory='ssh_files')

        with self.assertRaises(AttributeError):
            Replacer.Replacer(file_directory='ssh_files', parsed_destination='parsed_files',
                              encrypted_password='pass123')
