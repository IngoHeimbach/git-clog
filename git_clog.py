#!/usr/bin/env python3

import locale
import os
import subprocess
import re
import sys
from typing import List, Optional, Tuple  # noqa: F401  # pylint: disable=unused-import

__author__ = "Ingo Heimbach"
__email__ = "IJ_H@gmx.de"
__license__ = "MIT"
__version_info__ = (0, 1, 1)
__version__ = ".".join(map(str, __version_info__))

COMMIT_CHAR_ASCII = "*"
COMMIT_CHAR_UNICODE = "●"


def is_locale_utf8() -> bool:
    local_encoding = locale.getlocale()[1]
    return local_encoding is not None and local_encoding.lower() == "utf-8"


def get_pager_with_options() -> List[str]:
    pager = None  # type: Optional[str]
    pager_options = []  # type: List[str]
    try:
        pager = subprocess.check_output(["git", "config", "--get", "core.pager"], universal_newlines=True)
    except subprocess.CalledProcessError:
        pass
    if not pager:
        for env_variable in ("GITPAGER", "PAGER"):
            if env_variable in os.environ:
                pager = os.environ[env_variable]
                if pager:
                    break
        else:
            pager = "less"
    if pager in ("less", "more"):
        pager_options = ["-R"]
    return [pager] + pager_options


def get_git_log() -> str:
    git_log_output = subprocess.check_output(
        ["git", "log", "--color=always", "--all", "--decorate", "--graph", "--oneline"], universal_newlines=True
    )  # type: str
    return git_log_output


def colorize_git_log_output(git_log_output: str) -> str:
    colorized_output_lines = []  # type: List[str]
    commit_char = COMMIT_CHAR_UNICODE if is_locale_utf8() else COMMIT_CHAR_ASCII
    line_regex = re.compile(r"([^\*]*)\*(.*\x1b[^m]*m)([0-9a-f]+)(\x1b[^m]*m.*)")
    for line in git_log_output.split("\n"):
        line = line.strip()
        if not line:
            continue
        match_obj = line_regex.match(line)
        if match_obj is not None:
            line_start, before_commit_hash, commit_hash, rest_of_line = match_obj.groups()
            color_rgb_tuple = tuple(int(commit_hash[i : i + 2], base=16) for i in range(0, 6, 2))
            true_color_escape_sequence = "\x1b[38;2;{r:d};{g:d};{b:d}m".format(
                r=color_rgb_tuple[0], g=color_rgb_tuple[1], b=color_rgb_tuple[2]
            )
            colored_line = "".join(
                [
                    line_start,
                    true_color_escape_sequence,
                    commit_char,
                    "\x1b[m",
                    before_commit_hash,
                    commit_hash,
                    rest_of_line,
                ]
            )
            colorized_output_lines.append(colored_line)
        else:
            colorized_output_lines.append(line)
    return "\n".join(colorized_output_lines)


def print_git_log(colorized_log_output: str) -> None:
    pager_with_options = get_pager_with_options()
    encoding = locale.getlocale()[1]
    if encoding is None:
        encoding = "ascii"
    pager_process = subprocess.Popen(pager_with_options, stdin=subprocess.PIPE)
    pager_process.communicate(input=colorized_log_output.encode(encoding))


def print_version() -> None:
    print("git clog version {}".format(__version__))


def main() -> None:
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-V", "--version"):
            print_version()
            sys.exit()
        else:
            print('Unknown command line argument "{}"'.format(sys.argv[1]))
            sys.exit(1)
    try:
        git_log_output = get_git_log()
        colorized_log_output = colorize_git_log_output(git_log_output)
        print_git_log(colorized_log_output)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    sys.exit()


if __name__ == "__main__":
    main()
