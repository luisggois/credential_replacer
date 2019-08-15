import sys
import os
from tkinter import filedialog, Tk, messagebox

sys.path.append('.')
import Replacer as rp

if __name__ == '__main__':

    try:
        root = Tk()
        root.withdraw()

        file_dir = filedialog.askdirectory(parent=root, initialdir="/", title='Please select the directory with the ssh files!')
        if not file_dir:
            raise ValueError('Directory invalid. Execution has been stopped.')

        new_file_dir = filedialog.askdirectory(parent=root, initialdir="/",
                                               title='Please select a directory where you want to place the new encrypted files!')
        if not new_file_dir:
            raise ValueError('Directory invalid. Execution has been stopped.')

        replace = rp.Replacer(file_directory=file_dir, parsed_destination=new_file_dir, encrypted_password='yyy', encrypted_user='xxx')
        replace.encrypt()

        messagebox.showinfo('Information', 'Execution finished.')

    except Exception as e:
        messagebox.showerror('Error', e)
