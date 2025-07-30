# SPDX-FileCopyrightText: 2025 The Rockstor Project <support@rockstor.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
import logging

from .zyppchangelog import get_zypper_changelog

logger = logging.getLogger(__name__)


def main():
    """
    Command line invocation: non-boolean arguments are None by default.
    All boolean types are False by default.
    All defaults (no arguments) requests changelogs for all pending updates.
    All options (except '--all-available' & '--debug') filter the above function.
    """
    warning_text = ("Note: '--all-available' alone is extreme: it retrieves rpm headers for\n"
                    "the latest version (per repo) of all available packages - taking no account of\n"
                    "what packages are installed. '--all-available' still heeds the filters\n"
                    "of '--packages' & '--repos' if specified, but the changelogs presented are\n"
                    "full default length: not a difference to any incidentally installed packages.")
    parser = argparse.ArgumentParser(
        prog='zyppchangelog',
        description='Changelogs for installable pending updates,'
                    ' or available/uninstalled packages (requires options).\n\n' + warning_text,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--packages", dest="packages",
        help="Comma separated list (no spaces) of package names to consider.\nDefault is all installed packages."
    )
    parser.add_argument(
        "-r", "--repos", dest="repos",
        help="Comma separated list (no spaces) of repository aliases to consider.\nDefault is all enabled repositories."
    )
    parser.add_argument(
        "-of", "--output-format", dest="outf",
        help="Options: 'json' - formatted single print.\nDefault is line-by-line prints."
    )
    parser.add_argument(
        '-d', '--debug', dest='debug', default=False, action='store_true',
        help='Enable debug mode.'
    )
    parser.add_argument(
        '-t', '--titles-only', dest='titles_only', default=False, action='store_true',
        help='List only the changelog titles.'
    )
    parser.add_argument(
        '-re', '--regex', dest='regex', default=False, action='store_true',
        help='Enable regular expression in package names.'
    )
    parser.add_argument(
        "-AA", "--all-available", dest="all", default=False, action='store_true',
        help="Changelogs for all available packages (latest versions only): USE WITH CAUTION."
    )

    args = parser.parse_args()

    loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG
    # No `stream=` defaults to sys.stderr which works for us.
    logging.basicConfig(level=loglevel)

    pkg_list = []
    if args.packages:
        pkg_list = args.packages.split(",")
    repo_list = []
    if args.repos:
        repo_list = args.repos.split(",")

    get_zypper_changelog(repo_list=repo_list, pkg_list=pkg_list, only_updates=not args.all,
                         titles_only=args.titles_only, regex_enabled=args.regex, output_format=args.outf)


if __name__ == "__main__":
    main()
