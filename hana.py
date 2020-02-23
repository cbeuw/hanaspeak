import sys
from typing import *


class EncodingTree:
    leaf: chr
    children: Dict[chr, 'EncodingTree']
    encoding_table: Dict[chr, chr]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __init__(self, lf='', children=None):
        self.leaf = lf
        if children is None:
            self.children = {}
        else:
            self.children = children
        self.encoding_table = {}

    def __setitem__(self, key: str, value: 'EncodingTree'):
        if len(key) == 1:
            self.children[key] = value
        else:
            if self.leaf is not '':
                raise Exception('node cannot have leaf value')
            self.children[key[0]][key[1:]] = value

    def __getitem__(self, item: str) -> chr:
        if item == "":
            return self.leaf
        else:
            return self[item[1:]]

    def build_encoding_table(self) -> Dict:
        for key, child in self.children.items():
            if child.leaf != '':
                self.encoding_table[child.leaf] = key
            else:
                sub_table = child.build_encoding_table()
                for c in sub_table.keys():
                    self.encoding_table[c] = key
        return self.encoding_table

    def hanafy(self, text: str) -> str:
        return ''.join(self.hanafy_chr(c) for c in text)

    def hanafy_chr(self, c: chr) -> str:
        if self.leaf == c:
            return ""
        else:
            key = self.encoding_table[c]
            return key + self.children[key].hanafy_chr(c)

    def dehana(self, hanaspeak: str) -> str:
        return self.__dehana(hanaspeak, self)

    def __dehana(self, hanaspeak: str, root: 'EncodingTree') -> str:
        if len(hanaspeak) == 0:
            return ""
        cur = hanaspeak[0]
        child = self.children[cur]
        if child.leaf != '':
            return child.leaf + root.dehana(hanaspeak[1:])
        else:
            return child.__dehana(hanaspeak[1:], root)


def build_tree() -> EncodingTree:
    root = EncodingTree()

    with EncodingTree() as S:
        root['S'] = S

        S['K'] = EncodingTree('a')

        with EncodingTree() as H:
            S['H'] = H

            H['J'] = EncodingTree('e')
            H['M'] = EncodingTree('t')
            H['K'] = EncodingTree(' ')

        with EncodingTree() as J:
            S['J'] = J

            J['J'] = EncodingTree('o')
            J['D'] = EncodingTree('i')
            J['H'] = EncodingTree('n')

        with EncodingTree() as S2:
            S['S'] = S2

            S2['H'] = EncodingTree('s')
            S2['A'] = EncodingTree('r')
            S2['D'] = EncodingTree('h')

    with EncodingTree() as J:
        root['J'] = J

        J['S'] = EncodingTree('d')

        with EncodingTree() as D:
            J['D'] = D

            D['A'] = EncodingTree('l')
            D['N'] = EncodingTree('u')
            D['J'] = EncodingTree('\'')

    with EncodingTree() as H:
        root['H'] = H

        H['K'] = EncodingTree('c')

        with EncodingTree() as H2:
            H['H'] = H2

            H2['S'] = EncodingTree('m')
            H2['J'] = EncodingTree('f')
            H2['K'] = EncodingTree('y')

    with EncodingTree() as K:
        root['K'] = K

        K['S'] = EncodingTree('w')

        with EncodingTree() as J:
            K['J'] = J

            with EncodingTree() as J2:
                J['J'] = J2

                J2['K'] = EncodingTree('g')
                J2['M'] = EncodingTree('p')
                J2['S'] = EncodingTree('b')
    root['D'] = EncodingTree('v')
    root['A'] = EncodingTree('k')
    root['M'] = EncodingTree('x')
    root['G'] = EncodingTree('q')
    root['L'] = EncodingTree('j')
    root['E'] = EncodingTree('z')

    root.build_encoding_table()
    return root


if __name__ == "__main__":
    hana = build_tree()

    maybe_hana = sys.argv[1]
    if maybe_hana.islower():
        print(hana.hanafy(maybe_hana))
    else:
        print(hana.dehana(maybe_hana))