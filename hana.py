#!/usr/bin/env python3

import sys
from typing import *


class EncodingTree:
    pass


class Leaf(EncodingTree):
    leaf: chr

    def __init__(self, lf):
        self.leaf = lf


class Node(EncodingTree):
    children: Dict[chr, EncodingTree]
    encoding_table: Dict[chr, chr]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __init__(self, children=None):
        if children is None:
            self.children = {}
        else:
            self.children = children
        self.encoding_table = {}

    def __setitem__(self, key: str, value: EncodingTree):
        if len(key) == 1:
            self.children[key] = value
        else:
            child = self.children[key[0]]
            if isinstance(child, Node):
                child[key[1:]] = value
            else:
                raise Exception("cannot add a child to a leaf")

    def __getitem__(self, item: str) -> EncodingTree:
        if item == '':
            return self
        else:
            return self[item[1:]]

    def build_encoding_table(self) -> Dict:
        for key, child in self.children.items():
            if isinstance(child, Leaf):
                self.encoding_table[child.leaf] = key
            elif isinstance(child, Node):
                sub_table = child.build_encoding_table()
                for c in sub_table.keys():
                    self.encoding_table[c] = key
        return self.encoding_table

    def hanafy(self, text: str) -> str:
        return ''.join(self.hanafy_chr(c) for c in text)

    def hanafy_chr(self, c: chr) -> str:
        key = self.encoding_table[c]
        child = self.children[key]
        if isinstance(child, Leaf):
            return key
        elif isinstance(child, Node):
            return key + child.hanafy_chr(c)

    def dehana(self, hanaspeak: str) -> str:
        return self.__dehana(hanaspeak, self)

    def __dehana(self, hanaspeak: str, root: 'Node') -> str:
        if len(hanaspeak) == 0:
            return ""
        child = self.children[hanaspeak[0]]
        if isinstance(child, Leaf):
            return child.leaf + root.dehana(hanaspeak[1:])
        elif isinstance(child, Node):
            return child.__dehana(hanaspeak[1:], root)


def build_tree() -> Node:
    root = Node()

    with Node() as S:
        root['S'] = S

        S['K'] = Leaf('a')

        with Node() as H:
            S['H'] = H

            H['J'] = Leaf('e')
            H['M'] = Leaf('t')
            H['K'] = Leaf(' ')

        with Node() as J:
            S['J'] = J

            J['J'] = Leaf('o')
            J['D'] = Leaf('i')
            J['H'] = Leaf('n')

        with Node() as M:
            S['M'] = M

            M['H'] = Leaf('s')
            M['A'] = Leaf('r')
            M['D'] = Leaf('h')

    with Node() as J:
        root['J'] = J

        J['S'] = Leaf('d')

        with Node() as D:
            J['D'] = D

            D['A'] = Leaf('l')
            D['N'] = Leaf('u')
            D['J'] = Leaf('\'')

    with Node() as H:
        root['H'] = H

        H['M'] = Leaf('c')

        with Node() as H2:
            H['H'] = H2

            H2['S'] = Leaf('m')
            H2['J'] = Leaf('f')
            H2['K'] = Leaf('y')

    with Node() as K:
        root['K'] = K

        K['S'] = Leaf('w')

        with Node() as J:
            K['J'] = J

            with Node() as J2:
                J['J'] = J2

                J2['K'] = Leaf('g')
                J2['M'] = Leaf('p')
                J2['S'] = Leaf('b')
    root['D'] = Leaf('v')
    root['A'] = Leaf('k')
    root['M'] = Leaf('x')
    root['G'] = Leaf('q')
    root['L'] = Leaf('j')
    root['E'] = Leaf('z')

    root.build_encoding_table()
    return root


if __name__ == "__main__":
    hana = build_tree()

    maybe_hana = sys.argv[1]
    if maybe_hana.islower():
        print(hana.hanafy(maybe_hana))
    else:
        print(hana.dehana(maybe_hana))
