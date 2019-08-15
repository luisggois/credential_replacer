import unittest
from unittest.mock import patch
import os
import pathlib
import Replacer
import shutil
import logging


class TestReplacerRegexPatterns(unittest.TestCase):

    def setUp(self):
        ''' 
        Create two dirs for testing, one with files to encrypt, the other where encrypted
        files will be placed. The directory with files to encrypt will contain several different
        types of files extension and also subdirectories with files
        '''
        logging.disable(logging.CRITICAL)

        os.mkdir('./ssh_files')
        pathlib.Path('./ssh_files/test_file.txt').touch()
        pathlib.Path('./ssh_files/test_file.log').touch()
        pathlib.Path('./ssh_files/test_file.cfg').touch()
        pathlib.Path('./ssh_files/test_file.pdf').touch()
        os.mkdir('./ssh_files/extra_files')
        pathlib.Path('./ssh_files/extra_files/test_file_2.txt').touch()

        os.mkdir('./parsed_files')

        # Instantiate Replacer class with required kwargs
        self.obj = Replacer.Replacer(file_directory='ssh_files', parsed_destination='parsed_files',
                                     encrypted_password='pass123', encrypted_user='user123')

        # Get regex pattern to replace users
        self.user_pattern = self.obj.get_user_pattern()
        # Get regex patterns to replace passwords
        self.password_pattern_one = self.obj.get_password_pattern_one()
        self.password_pattern_two = self.obj.get_password_pattern_two()

    def tearDown(self):
        del self.obj
        shutil.rmtree('./ssh_files')
        shutil.rmtree('./parsed_files')
        logging.disable(logging.NOTSET)

    def test_file_acceptance_and_saving(self):
        '''
        Only files with extension .txt, .cfg and .log
        will be taking into consideration for parsing.
        Additionally, only files in the selected directory will be
        taking into consideration, subdirectories will
        not be taking into account

        '''

        self.obj.encrypt()

        self.assertTrue(os.path.exists('./parsed_files/test_file.txt'))
        self.assertTrue(os.path.exists('./parsed_files/test_file.log'))
        self.assertTrue(os.path.exists('./parsed_files/test_file.cfg'))

        self.assertFalse(os.path.exists('./parsed_files/test_file.pdf'))
        self.assertFalse(os.path.exists('./parsed_files/test_file_2.txt'))
