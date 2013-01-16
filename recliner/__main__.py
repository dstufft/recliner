import argparse
import codecs
import locale
import sys

from . import render


locale.setlocale(locale.LC_ALL, "")


def main():
    parser = argparse.ArgumentParser(description="renders reStructuredText")
    parser.add_argument("source",
        nargs="?",
        help="file to open and render",
    )

    args = parser.parse_args()

    if args.source:
        with codecs.open(args.source, "r", "utf-8") as fp:
            text = fp.read()
    else:
        text = sys.stdin.read()

    rendered = render(text)

    sys.stdout.write(rendered.encode("utf-8"))
    sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(main())
