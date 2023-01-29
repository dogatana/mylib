import os.path
import subprocess
from argparse import ArgumentParser
from glob import glob

JAVA11 = r"c:\pleiades\java\11\bin\java.exe"

def minify(js_files, out_file, verbose):
    args = init_env()
    args = [JAVA11, "-jar", JAR]
    if verbose:
        args.extend(["-W", "VERBOSE"])
    args.extend(js_files)
    args.extend(["--js_output_file", out_file])

    output = subprocess.run(args, capture_output=True)
    for text in [output.stdout.decode("utf-8"), output.stderr.decode("utf-8")]:
        if text:
            print(text)


def init_env():
    if not os.path.exists(JAVA11):
        print("error:", JAVA11, "not found")
        exit()
    jars = glob(os.path.join(os.path.dirname(__file__), "closure-compiler*.jar"))
    if not jars:
        print("error: closure-compiler*.jar not found")
        exit()
    return [JAVA11, jars[-1]]


def parse_args():
    parser = ArgumentParser(description="minify js")
    parser.add_argument("--output", "-o", help="output file", required=True)
    parser.add_argument("files", nargs="+", help="input file(s)")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_const",
        const=True,
        default=False,
        help="verbose output",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    minify(args.files, args.output, args.verbose)
