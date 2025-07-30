#!/usr/bin/python

import platform
import sys
sys.path.append(".")
from cnutils import cutils

def is_win_file_path(file_path):
    if len(file_path) <= 2:
        return False
    if file_path[0].isalpha() and file_path[1:].startswith(":\\"): # windwos path
        return True
    return False

def wsl_path_to_linux_path(file_path):
    wsl_path_keyword = r'\\wsl.localhost\Ubuntu-20.04'
    if 'wsl.localhost' in file_path and 'home' in file_path:
        result1 = file_path.replace('\\', '/')
        result2 = '/home' + cutils.get_target_str(result1, '/home', '')
        return result2

    if file_path.startswith(wsl_path_keyword):
        new_file_path = file_path.replace(wsl_path_keyword, '').replace('\\', '/')
        print('path_convert: [%s]\n -----------> [%s]' % (file_path, new_file_path))
        file_path = new_file_path
        return file_path
    return None

def to_linux_path(file_path):
    if is_win_file_path(file_path):
        file_path = file_path.replace("\\", "/")
        return "/mnt/" + file_path[0].lower() + file_path[2:]
    wsl_path = wsl_path_to_linux_path(file_path)
    if wsl_path:
        return wsl_path
        
    return file_path

def path_refine(file_path):
    if cutils.is_windows():
        return file_path
    return to_linux_path(file_path)


def main(arg):
    test_path="H:\\test\\document\\211015_002.cfa"
    test = to_linux_path(test_path)
    print(test)
    pass

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])