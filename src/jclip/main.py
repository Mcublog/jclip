#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from pathlib import Path

from alive_progress import alive_bar
from colorama import Fore as Clr
from jira import JIRA, Issue
from pylogus import logger_init

from jclip.version import VERSION

log = logger_init(__name__, logging.INFO)

NAME = 'JClip'

JIRA_TOKEN_VARIABLE = 'JIRA_TOKEN'
JIRA_SERVER = 'https://crystals.atlassian.net'

DESCRIPTION = f'{NAME} {Clr.GREEN}v{VERSION}{Clr.RESET}'

def jira_auth_with_token(username: str, token: str) -> JIRA | None:
    try:
        return JIRA(JIRA_SERVER, basic_auth=(username, token))
    except Exception as e:
        log.debug(e)
        log.error(f'Could not authenticate {username}')


def jira_get_issue(jira: JIRA, issue: str) -> Issue | None:
    try:
        return jira.issue(issue)
    except Exception as e:
        log.debug(e)
        log.error(f'Could not get issue {issue} from JIRA')


def jira_attach_file(jira: JIRA, issue: Issue, path: Path) -> bool:
    if not path.exists():
        log.error(f'File: {path} is not exists')
        return False
    if not path.is_file():
        log.error(f'File: {path} is directory')
        return False
    # jira.add_attachment(issue=issue, attachment=f'{path}')
    return True


def main():
    parser = argparse.ArgumentParser(prog=NAME, description=f"{DESCRIPTION}")
    parser.add_argument(f'-u',
                        '--username',
                        type=str,
                        help=f'Email address of the user',
                        required=True)
    parser.add_argument(f'-i',
                        '--issue',
                        type=str,
                        help=f'Number of issue or task (KKT-some_number)',
                        required=True)
    parser.add_argument(f'-f',
                        '--file',
                        type=str,
                        help=f'Path to attachment file',
                        required=True)
    parser.add_argument(
        f'-t',
        '--token',
        type=str,
        help=f'JIRA token or use system environment variable {JIRA_TOKEN_VARIABLE}')

    try:
        args = parser.parse_args()
    except Exception as e:
        log.debug(e)
        sys.exit(1)

    with alive_bar(4) as bar:
        token = args.token if args.token else os.getenv(JIRA_TOKEN_VARIABLE)
        if not token:
            log.error(f'JIRA token not specified, use sys ENV variable {JIRA_TOKEN_VARIABLE} or -t key')
            sys.exit(1)
        bar()
        if (jira := jira_auth_with_token(args.username, token)) is None:
            sys.exit(1)
        bar()
        if (issue := jira_get_issue(jira, args.issue)) is None:
            sys.exit(1)
        bar()
        file = Path(args.file)
        if not jira_attach_file(jira, issue, file):
            sys.exit(1)
        bar(1.)
        log.info(f"{file} is successfully attached to {issue})


if __name__ == '__main__':
    main()