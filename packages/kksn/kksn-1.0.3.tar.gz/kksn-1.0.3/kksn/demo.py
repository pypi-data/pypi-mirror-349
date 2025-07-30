# -*- coding: utf-8 -*-
from client import Monitor


def run():
    print('Hello world')


if __name__ == '__main__':
    Monitor(target=run, pwd='123')
