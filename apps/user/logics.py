# coding: utf-8

import hashlib
import itertools


def build_signature(*args):
    """对变量进行sha1签名

    按变量的传入顺序组合生成sha1签名, 变量必须可转为字符串

    Args:
        *args: 要签名的变量们
    """
    sign_key = '|'.join(itertools.imap(str, args))

    return hashlib.sha1(sign_key).hexdigest()

