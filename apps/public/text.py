# coding: utf-8

from collections import defaultdict


class PoFilter(object):
    """ 对指定的敏感词做替换

    参照 http://code.google.com/p/smallgfw/
    对算法进行优化, 尽最大可能的减少循环次数

    首先统计出敏感词列表中最小长度为最小步长, 以这个步长检查是否有命中便移库中的
    的数据，并从大到少遍历组成新的词块去敏感词库中查找

    Attributes:
       total_terms: 要过滤的全部敏感词库
       offsets: 词块需要扩展到指定的长度列表
       chunk_len: 要过滤敏感中，词的最小长度
    """
    def __init__(self):
        self.total_terms = set()
        self.offsets = {}
        self.chunk_len = 0

    def init(self, terms):
        """ 初指化敏感词库

        Args:
           terms: 敏感词列表
        """
        chunk_len = len(min(terms, key=len))
        offsets = defaultdict(set)

        for term in terms:
            term_len = len(term)
            diff = term_len - chunk_len

            if diff > 0:
                offsets[term[0:chunk_len]].add(diff)
            else:
                offsets[term] = (0,)

            self.total_terms.add(term)

        self.chunk_len = chunk_len
        self.offsets = dict(((chunk, tuple(sorted(offsets, reverse=True))) \
                             for chunk, offsets in offsets.iteritems()))
        offsets = None

    def replace(self, text, to):
        """ 查找敏感词，并进行替换

        Args:
           text: 要查找的文本
           to: 替换敏感词的内容

        Returns:
           替换过敏感词的文本
        """
        result = []
        text_len = len(text)
        step, chunk_len = 0, self.chunk_len

        while step < text_len:
            chunk = text[step:chunk_len]
            offsets = self.offsets.get(chunk)

            if not offsets:
                result.append(text[step])
                step += 1
            else:
                for value in offsets:
                    new_chunk_len = chunk_len + value

                    if text[step:new_chunk_len] in self.total_terms:
                        result.append(to)
                        break

                step = new_chunk_len

            chunk_len = step + self.chunk_len

        return ''.join(result)


if __name__ == '__main__':
    pof = PoFilter()
    pof.init(("迷药", "嗑药", "买真枪", "二代身份证", "卖肾", "出售器官"))
    data = """
迷药
嗑药
买真枪盗取qq盗取密码盗取卡号嗑药
"""

    print pof.replace(data, '*')
