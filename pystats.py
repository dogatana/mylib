""" Python コードのメトリクス計測

* 空白行、コメント行（単一行、複数行）は削除
* radon を使用し、次の項目を計測する
    * ファイルの MI Score
    * function, class, method の行数、Cyclomatic Complexity
* ファイルもしくはフォルダを指定
* フォルダ指定時は、フォルダ直下の *.py を対象とする
"""

import glob
import os.path
import re
import sys
from collections import namedtuple

import radon.visitors
from radon.complexity import cc_rank, cc_visit
from radon.metrics import mi_rank, mi_visit

from csvutil import to_csvline
from miscutil import expand_files


Stat = namedtuple("Stat", "file mi cc")


class CCStats(namedtuple("CCStatsBase", "type name loc complexity")):
    def to_a(self):
        return [self.type, self.name, self.loc, self.complexity]


def main(paths):
    stats = anayalize(globbed(paths))
    if stats:
        print_result(stats)


def globbed(paths):
    result = []
    for path in paths:
        result.extend(glob.glob(path))
    return result


def anayalize(paths):
    stats = []
    for path in paths:
        if os.path.isfile(path):
            stats.append(Stat(path, *get_metrics(path)))
        elif os.path.isdir(path):
            for file in glob.glob(os.path.join(path, "*.py")):
                stats.append(Stat(file, *get_metrics(file)))
        else:
            print("# invalid target", path)
    return stats


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


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: pystats.py file|dir [file|dir...]")
        exit()
    args = expand_files(sys.argv[1:])
    main(args)
