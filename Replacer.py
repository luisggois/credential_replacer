import os
import re
from contextlib import contextmanager
import logging
from io import StringIO

''' Set logging for the module '''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s')

file_handler = logging.FileHandler('Replacer.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class Replacer:

    # Mandatory settings
    file_directory: str
    parsed_destination: str
    encrypted_user: str
    encrypted_password: str

    def __init__(self, **kwargs):
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

        logger.debug(f'{__class__.__name__} class has been initiated')

        self.validate_kwargs(kwargs)

    @staticmethod
    def get_user_pattern():
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

        keyword_1, keyword_2, keyword_3 = ('local-user', 'user', 'usm-user v3')
        pattern = re.compile(rf'((\s|^)({keyword_1}|{keyword_2}|{keyword_3})\s)([A-Za-z0-9_-]+)')

        return pattern

    @staticmethod
    def get_password_pattern_one():
        '''
        Pattern number one used to find password values

        Keywords we expect to see on the left side of the password value
        ----------
        key: 'cipher'

        Returns
        -------
        <class 're.Pattern'>

        '''
        keyword_1 = 'cipher'
        pattern = re.compile(rf'({keyword_1}\s)[^\s]+')

        return pattern

    @staticmethod
    def get_password_pattern_two():
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

        pattern = re.compile(r'[^\s]+(?=[%#$@^!])[^\s]+')

        return pattern

    def encrypt(self):
        '''
        Perform file encryption

        Flow
        --------
        1 - Get regex patterns to find user values and password values
        2 - Change to directory containing the ssh text files
        3 - Process each text file one by one:
            - Read a chunk of content(max n characters) from every file at each time to not overload memory 
            - Encrypt each chunk at a time and save the encrypted content to a string buffer (muttable type)
            - Save the new content to directory where parsed files will stay

        '''

        logger.debug(f'{__class__.__name__}.encrypt() has been initiated')
        logger.debug("Retrieving regex patterns for encryption")

        self.user_pattern = self.get_user_pattern()
        self.password_pattern_one = self.get_password_pattern_one()
        self.password_pattern_two = self.get_password_pattern_two()

        with self.change_dir(self.file_directory):
            extensions_supported = (".txt", ".log", ".cfg")
            accepted_files = (file for file in os.listdir() if file.lower().endswith(extensions_supported))
            for accepted_file in accepted_files:
                try:
                    logger.debug(f"Processing {accepted_file!r} for encryption")
                    with open(accepted_file, 'r', encoding='utf-8') as f:
                        with self.string_buffer() as bf:
                            while True:
                                logger.debug(f"Current stream position: {f.tell()!r}")
                                content = f.read(10000)
                                if not content:
                                    output = bf.getvalue()
                                    break
                                else:
                                    encrypted_content = self.exec_encryption(content)
                                    bf.write(encrypted_content)

                except Exception as e:
                    logger.exception(e)
                else:
                    self.save(accepted_file, output)

        logger.debug(f'{__class__.__name__}.encrypt() closing down...')

    def exec_encryption(self, content):
        ''' Replace user and password values using regex patterns'''

        # replace user values
        encrypted = self.user_pattern.sub(rf'\1{self.encrypted_user}', content)
        # replace pass values that match pattern 1
        encrypted = self.password_pattern_one.sub(rf'\1{self.encrypted_password}', encrypted)
        # replace pass values that match pattern 2
        encrypted = self.password_pattern_two.sub(rf'{self.encrypted_password}', encrypted)

        return encrypted

    def save(self, file_name, new_content):
        ''' Save new encrypted file '''

        try:
            logger.debug(f"Saving encrypted file {file_name!r}...")
            path_new_file = os.path.join(self.parsed_destination, file_name)
            with open(path_new_file, 'w', encoding='utf-8') as nf:
                nf.write(new_content)
        except Exception as e:
            logger.exception(e)
            logger.critical(f'Parsed content from {file_name!r} could not be saved')

    def validate_kwargs(self, kwargs):
        '''
        Validating and setting attributes

        :param attrs: dictionary of kwargs from Replacer.__init__
        :type attrs: dict

        '''

        logger.debug('Validating and setting attributes...')

        mandatory_keys = ['file_directory', 'parsed_destination', 'encrypted_user', 'encrypted_password']

        if not all(mk in kwargs.keys() for mk in mandatory_keys):
            logger.error(f'Not all mandatory attributtes were set')
            raise AttributeError(f'Not all mandatory attributtes were set')

        for key, value in kwargs.items():
            if key in mandatory_keys:
                if isinstance(value, str):
                    if key == 'file_directory' or key == 'parsed_destination':
                        if not os.path.isdir(value):
                            logger.error(f'Directory {value!r} does not exist')
                            raise FileNotFoundError(f'Directory {value!r} does not exist')
                        else:
                            setattr(self, key, os.path.abspath(value))
                            logger.debug(f'Attribute {key!r} has been set with value ===> {os.path.abspath(value)!r}')
                            continue
                    setattr(self, key, value)
                    logger.debug(f'Attribute {key!r} has been set with value ===> {value!r}')
                else:
                    logger.error(f'Value from attribute {key!r} is not type str as expected')
                    raise TypeError(f'Value from attribute {key!r} is not type str as expected')
            else:
                logger.error(f'Attribute {key!r} is not valid')
                raise AttributeError(f'Attribute {key!r} is not valid')

    @staticmethod
    @contextmanager
    def change_dir(destination):
        try:
            cwd = os.getcwd()
            os.chdir(destination)
            logger.debug(f"Directory has been changed to {destination!r}")
            yield
        except Exception as e:
            logger.exception(e)
        finally:
            os.chdir(cwd)
            logger.debug(f"Directory has been changed back to {cwd!r}")

    @staticmethod
    @contextmanager
    def string_buffer():
        try:
            buffer = StringIO()
            yield buffer
        except Exception as e:
            logger.exception(e)
        finally:
            buffer.close()
