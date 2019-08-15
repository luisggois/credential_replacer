# How to run

    Demonstration in the the demo package, just click and run the example.py

# Mandatory kwargs user needs to provide:

|       keyword      |      value type      |
| -------------- --- | -------------------- |
|   file_directory   |        **str**       | 
| parsed_destination |        **str**       |
|   encrypted_user   |        **str**       |
| encrypted_password |        **str**       |   

# Tests

    Tests need to be executed from the parent directory:
    >> python -m unittest

# Files expected

    Only files with extension .txt, .cfg and .log will be taking into consideration
    for parsing. Additionally, only files in the selected directory will be taking
    into consideration, subdirectories will not be taking into account.

# Replace all user values

    Keywords we expect to see on the left side of the user value 
    -------------
    key: 'local-user'
    key: 'user'
    key: 'usm-user v3'

    # Ex: local-user go4l0c9l

# Replace all password values

    ** PATTERN 1 **

    Keywords we expect to see on the left side of the password value 
    ----------
    key: 'cipher'
    
    # Ex: cipher %^%#ixA^3ddhhhwM)*:/I=^a

    ** PATTERN 2 **

    Characters we expect to see on a multi-char password 
    ----------
    key: '%' 
    key: '#'
    key: '$'
    key: '@'
    key: '^'
    key: '!' 

    # Ex: %^%#ixAwM)*:/I,-$y=^a8*{C1J%^%#fghfghfghfgh35345345sfsd

