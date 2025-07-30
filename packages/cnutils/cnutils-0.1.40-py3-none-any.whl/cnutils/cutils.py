#!/usr/bin/python
from ast import keyword
import sys
import os

from pathlib import Path
sys.path.append(os.path.dirname(Path(__file__).absolute()))
sys.path.append('.')

import binascii
import datetime
from cnutils import fs_lib

import colorama

class FColor:
    RED = "31m"
    GREEN = "32m"
    YELLOW = "33m"
    BLUE = "34m"
    MAGENTA = "35m"
    CYAN = "36m"
    WHITE = "37m"

def print_color(s, fcolor=FColor.RED):
    ESC = "\033["
    RESET = "0m" 
    fcolor = FColor.BLUE
    print(ESC + fcolor + str(s) + ESC + RESET)
def printc(s, fcolor=FColor.RED):
    ESC = "\033["
    RESET = "0m" 
    print(ESC + fcolor + str(s) + ESC + RESET)

def print_ts(tag=""):
    print("%s: %s" % (str(datetime.datetime.now())[:-3], tag))

def clipboard_set(my_str):
    import clipboard
    clipboard.copy(my_str)
    
    #import pandas.io.clipboard as clip
    #clip.copy(my_str)

def clipboard_get():
    #print_ts()
    import pandas.io.clipboard as clip
    #print_ts()
    s = clip.paste()
    #print_ts()
    return s

def sorted_version(verion_list, reverse=False):
    """
    按字符串最后一个字段的数值从小到大排序（支持点分隔的版本号格式）
    :param str_list: 输入字符串列表（如 ["1.3.0.1", "1.3.0.10", "1.3.0.2"]）
    :return: 排序后的列表
    """
    def parse_last_field(s):
        """提取最后一个字段并转为整数，非数字字段默认视为0"""
        parts = s.split('.')
        last_part = parts[-1] if parts else ''
        try:
            return int(last_part)  # 转为整数（适用于数值型字段）
        except ValueError:
            return 0  # 非数字字段（如字母）默认排到最前面
    
    # 使用自定义解析函数作为排序键
    result = sorted(verion_list, key=parse_last_field, reverse = reverse)
    return result

def is_windows():
    return sys.platform.find("win") != -1

def print_byte_array(byte_array, slice_char="", ending="\n"):
    for val in byte_array:
        print("%02X%s" % (val, slice_char), end="")
    print(ending, end="")


def str_contain(line, target_str):
    return line.find(target_str) != -1


def get_target_val(input_str, start_str, end_str, target_type = int, inc_val=10):
    val_str = get_target_str(input_str, start_str,
                             end_str).strip().replace(' ', '')
    #print("line = [%s]\nstart_str=[%s], end_str = [%s], val_str = [%s]" % (input_str, start_str, end_str, val_str))
    if val_str == "":
        # return 0xDEADBEEF
        return 0xFFFFFFFF
    if target_type == int:
        return target_type(val_str, inc_val)
    try:
        return target_type(val_str)
    except:
        return 0.0


def get_target_str(input_str, start_str, end_str=''):
    start_offset = input_str.find(start_str)
    if start_offset == -1:
        return ""
    start_offset += len(start_str)
    if end_str == "":
        end_offset = len(input_str) - start_offset
    else:
        end_offset = input_str[start_offset:].find(end_str)
    if end_offset == -1:
        return ""
    result = input_str[start_offset: start_offset + end_offset]
    return result


def read_file_binary(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            lines = f.read()
            return lines
    else:
        print("file [%s] does not exist." % (file_path))

    return None


def write_file_binary(file_path, content):
    with open(file_path, "wb") as f:
        f.write(content)

def list_trim(tlist, trim_item):
    if not len(tlist):
        return []
    result = []
    for item in tlist:
        t_item = item
        if isinstance(item, str):
            item = item.strip()
        if item == trim_item:
            break
        result.append(t_item)
    return result

def read_file_lines(file_path, rstrip = False, lstrip = False):
    lines = []
    file_path = fs_lib.path_refine(file_path)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
    else:
        print("file [%s] does not exist." % (file_path))
    result = []
    try:
        if lstrip or rstrip:
            for line in lines:
                if rstrip:
                    line = line.rstrip()

                if lstrip:
                    line = line.lstrip()
                #result.append(line.decode('UTF-8'))
                result.append(line)
        else:
            result = lines
    except:
        raise
    return result


def write_file_lines(file_path, lines):
    file_path = fs_lib.path_refine(file_path)
    with open(file_path, "w") as f:
        f.writelines(lines)


def display_bytes(bytes, max_len=0):
    if max_len == 0:
        max_len = len(bytes)
    elif max_len > len(bytes):
        max_len = len(bytes)

    for i in range(max_len):
        if i > 0 and i % 16 == 0:
            print()
        print("%02X" % (bytes[i]), end=" ")
    print()


def search_binary(big_bytes, small_bytes):
    len_small = len(small_bytes)
    len_big = len(big_bytes)
    if len_small > len_big:
        return -1

    for i in range(0, len_big - len_small + 1):
        matched = True
        for k in range(len_small):
            if big_bytes[i + k] != small_bytes[k]:
                matched = False
                print("index = %d, k = %d. (%X, %X)" %
                      (i, k, big_bytes[i + k], small_bytes[k]))
                break
            #print("index = %d, k = %d. (%X, %X)" %(i, k, big_bytes[i + k], small_bytes[k]))

        if matched:
            return i
    return -1


def line_contain_str(line, keywords):
    line = line.strip()
    if line == "" or len(keywords) == 0:
        return False

    if type(keywords) == str:
        return line.find(keywords) != -1

    if type(keywords) == list:
        for keyword in keywords:
            result = line_contain_str(line, keyword)
            if result:
                # found target
                return True

    return False

def line_startswith_str(line, keywords):
    line = line.strip()
    if line == "" or len(keywords) == 0:
        return False

    if type(keywords) == str:
        return line.startswith(keywords)

    if type(keywords) == list:
        for keyword in keywords:
            result = line_startswith_str(line, keyword)
            if result:
                # found target
                return True

    return False

def get_filtered_lines(line_list, keywords_list):
    result = []
    for line in line_list:
        if line_contain_str(line, keywords_list):
            result.append(line)
            #print(line)
    return result


def make_printable(my_string):
    return ''.join(c for c in my_string if c.isprintable())

# def clipboard_get_text():
#     QApplication.clipboard().text()

# def clipboard_set_text(text):
#     QApplication.clipboard().setText(text)


def get_time_now():
    import datetime
    return datetime.datetime.now()
    # ts = str(datetime.datetime.now())
    # return ts if long_ts else ts[11:]

last_ts = 0
def time_delta(reset = 0):
    global last_ts
    if reset:
        if last_ts == 0:
            last_ts = get_time_now()
        print("now: %s delta: %d" % (last_ts, 0))
    else:
        now = get_time_now()
        print("now: %s - %s delta: %s" % (now, str(last_ts)[11:], now - last_ts))

class StatDict():
    def __init__(self, key_list=None):
        self.obj={}
        if key_list:
            for item in key_list:
                self.obj[item] = 0
    
    def inc(self, key):
        if key in self.obj.keys():
            self.obj[key] += 1
        else:
            self.obj[key] = 1
    def show(self):
        total = 0
        for key in sorted(self.obj.keys()):
            print('%s %s %d' % (key, ' '*(20 - len(key)), self.obj[key]))
            total += self.obj[key]
        print('----------------------------')
        print('total                 %s, item cnt = %d.' % (total, len(self.obj.keys())))

def list_files_and_folders(target_path, full_path=True):
    from pathlib import Path
    path_obj = Path(target_path)
    
    # Use .iterdir() to iterate through all items in the directory
    folders = [str(item) if full_path else os.path.basename(item) for item in path_obj.iterdir() if item.is_dir()]
    files = [str(item) if full_path else os.path.basename(item) for item in path_obj.iterdir() if item.is_file()]
    
    return files, folders

def list_files(target_path, full_path=True):
    files, folders = list_files_and_folders(target_path, full_path)
    return files

def list_folders(target_path, full_path=True):
    files, folders = list_files_and_folders(target_path, full_path)
    return folders

def get_longest_prefix(str_list):
    if not str_list:
        return ""
    if len(str_list) == 1:
        return str_list
    result = ""
    for i in range(1, len(str_list[0])):
        error = False
        for s in str_list:
            if not s.startswith(str_list[0][:i]):
                error = True
                break
        if not error:
            result = str_list[0][:i]

    return result

def get_longest_appendix(str_list):
    if not str_list:
        return ""
    if len(str_list) == 1:
        return str_list
    result = ""
    for i in range(1, len(str_list[0])):
        error = False
        ss = str_list[0][-i:]
        for s in str_list[1:]:
            if not s.endswith(ss):
                error = True
                break
        if not error:
            result = str_list[0][-i:]

    return result

from colorama import init, Fore, Back, Style
class Color(object):
    def red(s):
        return Color.do_color(Fore.LIGHTRED_EX,s)
    def green(s):
        return Color.do_color(Fore.LIGHTGREEN_EX, s)
    def yellow(s):
        return Color.do_color(Fore.LIGHTYELLOW_EX, s)
    def white(s):
        return Color.do_color(Fore.LIGHTWHITE_EX, s)
    def blue(s):
        return Color.do_color(Fore.LIGHTBLUE_EX, s)

    def do_color(color, value):
        #print(type(value))
        if type(value) == type([]):
            #return [color + x + Fore.Reset for x in value]
            result = []
            for x in value:
                result.append(color + x + Style.RESET_ALL)
            return result
        return color + value + Style.RESET_ALL

class ZipFile:
    def __init__(self, zip_file):
        import zipfile
        # file path or object are both OK
        self.zf = zipfile.ZipFile(zip_file)

    def get_name_list(self):
        return self.zf.namelist()

    def get_file(self, file_name):
        #return self.zf.read(file_name).decode('utf-8')
        return self.zf.read(file_name).decode('utf-8', errors='ignore')

class ZipArtifact(ZipFile):
    def __init__(self, zip_file):
        ZipFile.__init__(self, zip_file)
    
    def _get_log(self, key_name):
        for name in self.get_name_list():
            if 'ckv' in name:
                continue
            #print(zf.get_file(name))
            if key_name in name:
                return self.get_file(name)
        return ''

    def get_master_log(self):
        return self._get_log('mst')

    def get_master_log_lines(self):
        return self.get_master_log().splitlines()
    def get_slave_log(self):
        return self._get_log('slv')
    def get_slave_log_lines(self):
        return self.get_slave_log().splitlines()
    
    def get_smoke_lines(self):
        return self._get_log('smoke').splitlines()

class Kconfig(object):
    def __init__(self, config_file_path):
        self.kv_dict = {}
        self.ks_dict = {}
        self.load_config(config_file_path)

    def load_config(self, file_path):
        lines = read_file_lines(file_path)

        last_section_name = ''
        for i, line in enumerate(lines):
            line = line.strip()
            # #print(line)
            # if i > 20:
            #     break
            if i+2 < len(lines):
                print('%2d |%s'%(i, line))
                if line == '#' and len(lines[i+1].strip()) and lines[i+2].strip() == '#':
                    last_section_name = lines[i+1][2:].strip()
                    #print('cdbg:'+last_section_name)

            start_str = "# CONFIG_"
            end_str = " is not set"
            if line.startswith(start_str) and line.endswith(end_str):
                key = get_target_str(line, "# ", end_str)
                self.kv_dict[key] = 'n'
                self.ks_dict[key] = last_section_name
                continue
            start_str = "CONFIG_"
            if line.startswith(start_str):
                result = line.split('=')
                self.kv_dict[result[0]] = result[1]
                self.ks_dict[result[0]] = last_section_name
                continue

    def show(self, arg_list = []):
        y_cnt = 0
        n_cnt = 0
        o_cnt = 0
        for k,v in self.kv_dict.items():
            if v == 'y':
                y_cnt += 1
            elif v == 'n':
                n_cnt += 1
            else:
                o_cnt += 1

            if '-n' in arg_list:
                if v != 'y':
                    print('%s - %s - %s' % (k.rjust(40), v.ljust(10), self.ks_dict[k]))
            elif '-y' in arg_list:
                if v != 'n':
                    print('%s - %s - %s' % (k.rjust(40), v.ljust(10), self.ks_dict[k]))
            else:
                print('%s - %s - %s' % (k.rjust(40), v.ljust(10), self.ks_dict[k]))
        print('toatal item %d. y %d, n %d, o %d.' % (len(self.kv_dict), y_cnt, n_cnt, o_cnt))
    
    def is_configed(self, key):
        return key in self.kv_dict.keys()

    def is_disabled(self, key):
        return self.kv_dict.get(key, '-') != '$'

    def get_config(self, key):
        return self.kv_dict.get(key, '-')

class CutilsBase():
    def __init__(self):
        pass