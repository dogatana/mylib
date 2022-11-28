""" 指定フォルダのファイル一覧 Excel ファイルを作成 """
import os
import os.path
import sys

import excel


def main(dir):
    print("# dir", dir)
    lst = []
    parse(dir, lst)

    create_book(lst)


def parse(root, lst):
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            parse(path, lst)
        else:
            lst.append(path)


def create_book(filelist):
    xls = excel.excel()
    book = xls.Workbooks.Add()
    sheet = book.Worksheets(1)
    for row, path in enumerate(filelist, start=1):
        cell = sheet.Range(f"A{row}")
        cell.Value = path
        sheet.Hyperlinks.Add(Anchor=cell, Address=os.path.abspath(path))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
