# coding: utf-8

import string
import random

BASE_USER_SEQ = [97, 97, 97, 0, 0, 0]
USER_SEQ_FACTOR = [26 * 26 * 1000, 26 * 1000, 1000, 100, 10]

chars = string.ascii_letters + string.digits


def salt_generator(size=6):
    return ''.join(random.choice(chars) for x in xrange(size))

def trans_uid(uid, server_token, unique_token):
    """
    """
    seqs = [unique_token, server_token]
    shang, mod = 0, int(uid)

    for i, factor in enumerate(USER_SEQ_FACTOR):
        shang, mod = divmod(mod, factor)

        if i < 3:
            seqs.append(chr(shang + BASE_USER_SEQ[i]))
        else:
            seqs.append(str(shang + BASE_USER_SEQ[i]))

    seqs.append(str(mod))

    return ''.join(seqs)


def decompress_uid(uid):
    """ 把uid转换成数字

    一些平台只支持纯数字型用户ID, 所以需要把字母型uid转换成纯数字

    Args:
        uid: 用户6位ID(aaa001)

    Returns:
        转换后的数字
    """
    number = 0

    for i in xrange(0, 5):
        if i < 3:
            factor = ord(uid[i])
        else:
            factor = int(uid[i])

        number += (factor - BASE_USER_SEQ[i]) * USER_SEQ_FACTOR[i]

    i += 1
    number += int(uid[i])

    return number


if __name__ == '__main__':
    print salt_generator()
