""" Python コードのメトリクス計測

* 空白行、コメント行（単一行、複数行）は削除
* radon を使用し、次の項目を計測する
    * ファイルの MI Score
    * function, class, method の行数、Cyclomatic Complexity
* ファイルもしくはフォルダを指定
* フォルダ指定時は、フォルダ直下の *.py を対象とする
"""

import re
import sys
from argparse import ArgumentParser, BooleanOptionalAction
from collections import namedtuple
from glob import glob

import radon.visitors
from radon.complexity import cc_rank, cc_visit
from radon.metrics import mi_rank, mi_visit

from csvutil import to_csvline

Stat = namedtuple("Stat", "file mi cc")


class CCStats(namedtuple("CCStatsBase", "type name loc complexity")):
    def to_a(self):
        return [self.type, self.name, self.loc, self.complexity]


def main(files):
    stats = [Stat(file, *get_metrics(file)) for file in files]
    if stats:
        print_result(stats)


def print_result(stats):
    print("file,metrics,name,loc,complexity,rank")
    for stat in stats:
        print(to_csvline([stat.file, "mi score", "", "", stat.mi, mi_rank(stat.mi)]))
        for cc in stat.cc:
            print(to_csvline([stat.file] + cc.to_a() + [cc_rank(cc.complexity)]))


def get_metrics(file):
    print("#", file, file=sys.stderr)
    text = read_text(file)
    # print(text)

    cc_stats = []
    for cc in cc_visit(text):
        if isinstance(cc, radon.visitors.Function):
            cc_stats.append(
                CCStats(
                    "method" if cc.is_method else "function",
                    f"{cc.classname}.{cc.name}" if cc.is_method else cc.name,
                    cc.endline - cc.lineno + 1,
                    cc.complexity,
                )
            )
        elif isinstance(cc, radon.visitors.Class):
            cc_stats.append(
                CCStats(
                    "class", cc.name, cc.endline - cc.lineno + 1, cc.real_complexity
                )
            )
        else:
            raise NotImplementedError(repr(cc))

    mi = mi_visit(text, False)

    return mi, cc_stats


def read_text(file):
    lines = []
    comment = ""
    in_literal = False
    for line in open(file, encoding="utf-8"):
        if line.strip() == "":
            pass
        elif re.sub(r"\s*#.*$", "", line) == "":
            pass
        elif comment == "" and not in_literal and re.match(r'\s*"""', line):
            comment = line.rstrip() + " "
        elif comment == "" and not in_literal and '"""' in line:
            lines.append(line)
            in_literal = True
        elif comment == "":
            lines.append(line)
        elif comment != "" and re.search(r'"""\s*$', line):
            lines.append(comment + line)
            comment = ""
        elif comment != "":
            pass
        elif in_literal and '"""' in line:
            lines.append(line)
            in_literal = False
        elif in_literal:
            pass
        else:
            raise Exception(line)
    return "".join(lines)


def parse_args():
    parser = ArgumentParser(description="calculate metrics for python")
    parser.add_argument(
        "--recursive",
        "-r",
        help="search file recursively",
        action=BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("target", help="target file(s) or foler(s)", nargs="+")
    return parser.parse_args()


def get_files(args, recursive):
    target = []
    for arg in args:
        target.extend(glob(arg, recursive=recursive))
    return target


if __name__ == "__main__":
    args = parse_args()
    files = get_files(args.target, args.recursive)
    main(files)
