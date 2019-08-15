import unittest
import os
import pathlib
import Replacer
import shutil
import logging


class TestReplacerRegexPatterns(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
        Create two dirs for testing, one with files to encrypt, the other where encrypted
        files will be placed. setUpClass is being used because we are only testing the static methods
        that provide the regex patterns, so no changes will be done to the folders created during testing

        '''
        logging.disable(logging.CRITICAL)

        os.mkdir('./ssh_files')
        pathlib.Path('./ssh_files/test_file.txt').touch()
        os.mkdir('./parsed_files')

        # Instantiate Replacer class with required kwargs
        cls.obj = Replacer.Replacer(file_directory='ssh_files', parsed_destination='parsed_files',
                                    encrypted_password='pass123', encrypted_user='user123')

        # Get regex pattern to replace users
        cls.user_pattern = cls.obj.get_user_pattern()
        # Get regex patterns to replace passwords
        cls.password_pattern_one = cls.obj.get_password_pattern_one()
        cls.password_pattern_two = cls.obj.get_password_pattern_two()

    @classmethod
    def tearDownClass(cls):
        del cls.obj
        shutil.rmtree('./ssh_files')
        shutil.rmtree('./parsed_files')
        logging.disable(logging.NOTSET)

    def test_username_replacer(self):
        '''
        Pattern used to find user values

        Keywords we expect to see on the left side of the user value # Ex: local-user go4l0c9l
        ----------
        key: 'local-user'
        key: 'user'
        key: 'usm-user v3'

        Returns
        -------
        <class 're.Pattern'>

        '''

        self.assertIsNot(self.user_pattern.search(" ff local-user dasjd354hkhfdf35345"), None)
        self.assertIsNot(self.user_pattern.search("c local-user dasjd354hkhfdf35345"), None)
        self.assertIsNot(self.user_pattern.search("usm-user v3 dasjd354hkhfdf35345"), None)
        self.assertIsNot(self.user_pattern.search("rtuzrtzrtz usm-user v3 dasjd354hkhfdf35345"), None)
        self.assertIsNot(self.user_pattern.search("dasdasd user v3 dasjd354hkhfdf35345"), None)

        self.assertIsNone(self.user_pattern.search("l2tp-user radius-force"))
        self.assertIsNone(self.user_pattern.search("config password dasjd354hkhfdf35345"))
        self.assertIsNone(self.user_pattern.search("usd-user v3 dasjd354hkhfdf35345"))

    def test_password_replacer_pattern_one(self):
        '''
        Pattern number one used to find password values

        Keywords we expect to see on the left side of the password value
        ----------
        key: 'cipher'

        Returns
        -------
        <class 're.Pattern'>

        '''

        self.assertIsNot(self.password_pattern_one.search("cipher dasjd354hkhfdf35345"), None)
        self.assertIsNot(self.password_pattern_one.search("dasdasd dasd \n cipher dasjd354hkhfdf35345"), None)
        self.assertIsNot(self.password_pattern_one.search("\n\ncipher dasjd354hkhfdf35345"), None)

        self.assertIsNone(self.password_pattern_one.search(" ff local-user dasjd354hkhfdf35345"))
        self.assertIsNone(self.password_pattern_one.search(" password dasjd354hkhfdf35345"))

    def test_password_replacer_pattern_two(self):
        '''
        Pattern number two used to find password values

        Characters we expect to see on a multi-char password
        ----------
        key: '%'
        key: '#'
        key: '$'
        key: '@'
        key: '^'
        key: '!'

        Returns
        -------
        <class 're.Pattern'>

        '''

        self.assertIsNot(self.password_pattern_two.search("cipher %^%#ixA^3ddhhhwM)*:/I=^a"), None)
        self.assertIsNot(self.password_pattern_two.search("cipher \n\n%^%#ixA^3ddhhhwM)*:/I=^a"), None)
        self.assertIsNot(self.password_pattern_two.search("password %^%#ixA^3ddhhhwM)*:/I=^a"), None)

        self.assertIsNone(self.password_pattern_two.search("password dadas4646456456 "))
        self.assertIsNone(self.password_pattern_two.search("password dadas4646456456 "))
