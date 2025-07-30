#!/usr/bin/python

class cnumb(object):
    @staticmethod
    def hex_str_to_bytes(hex_str):
        return bytes.fromhex(hex_str)

    @staticmethod
    def hex_str_to_int(str_val):
        return int(str(str_val).lower().replace("0x", ""), 16)

    @staticmethod
    def hex_str_to_int_list(hex_str):
        return list(map(cnumb.str_2_hex, hex_str.split(' ')))

    @staticmethod
    def to_int(str_val):
        s = str(str_val).lower()
        base = 10
        if '0x' in s:
            s = s.replace("0x", "")
            base = 16
        return int(s, base)
