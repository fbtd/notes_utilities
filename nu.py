#!/usr/bin/env python3

import sys

TAB_CHAR   = '\t'
POINT_CHAR = '-'

def _get_indent(line):
    line_len = len(line)
    indent = 0
    while indent <= line_len and line[indent] in (TAB_CHAR, POINT_CHAR):
        indent += 1
    return indent

def enlist(lines_iter):
    """
    arrange lines in a recursive list of tuples (item, [sub-items-touples])
    """
    result = list()
    list_stack = [result, None]

    indent = 0
    for line in lines_iter:
        l = []
        t = (line, l)
        line_indent = _get_indent(line)
        if line_indent > indent:    # dealing with the first sub-item
            list_stack.append(l)
            list_stack[-2].append(t)
        elif line_indent == indent: # same level
            list_stack[-1] = l
            list_stack[-2].append(t)
        else:                       # 1+ lists to close
            list_stack = list_stack[:(line_indent - indent - 1)]
            list_stack.append(l)
            list_stack[-2].append(t)
        indent = line_indent
    return result

def deepsort(l):
    """
    Recursively sort in place each list
    """
    l.sort(key=lambda e:e[0])
    for elem in l:
        deepsort(elem[1])

def delist(l, result=None):
    """
    returns touple of lines from the recursive list of tuples (item, [sub-items-touples])
    """
    if not result: result = []
    for line, sub in l:
        result.append(line)
        delist(sub, result=result)
    return tuple(result)

def main():
    l = enlist(sys.stdin)
    deepsort(l)
    for line in delist(l):
        if _get_indent(line) == 0:
            print()
        print(line, end='')

if __name__ == '__main__':
    exit(main())
