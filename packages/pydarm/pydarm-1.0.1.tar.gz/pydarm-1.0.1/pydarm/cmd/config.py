import subprocess

from ._log import logger, CMDError
from ._const import (
    CAL_CONFIG_ROOT,
    DEFAULT_CONFIG_PATH,
    DEFAULT_MODEL_PATH,
)
from . import _util


def git_cmd(*args):
    """run arbitrary git command in CAL_CONFIG_ROOT"""
    cmd = ['git'] + list(args)
    cmdstr = ' '.join(cmd)
    logger.debug(f"git command: {cmdstr}")
    subprocess.run(
        cmd,
        cwd=CAL_CONFIG_ROOT,
    )


def add_args(parser):
    cgroup = parser.add_mutually_exclusive_group()
    cgroup.add_argument(
        '--edit-model', '-em', action='store_const', dest='edit', const='model',
        help="edit model INI file")
    cgroup.add_argument(
        '--edit-cmd', '--edit-config', '-ec', action='store_const', dest='edit', const='config',
        help="edit cmd config YAML file")
    cgroup.add_argument(
        '--diff', '-d', action='store_const', dest='git', const='diff',
        help="show git diff of files in config repo")
    cgroup.add_argument(
        '--commit', '-c', action='store_const', dest='git', const='commit',
        help="commit change in repo")
    cgroup.add_argument(
        '--tag', '-t', nargs=2, metavar=("TAG", "MSG"), dest='tag',
        help="tag the repo")
    cgroup.add_argument(
        '--push', '-p', action='store_const', dest='git', const='push',
        help="push changes to the remote")
    cgroup.add_argument(
        '--git', '-g', dest='git', nargs='*',
        help="run raw git command")
    # parser.add_argument(
    #     'args', nargs='*',
    #     help="optional additional arguments to git")


def main(args):
    """edit and maintain system config files

    The system config files live in a git repo the CAL_CONFIG_ROOT
    directory.  The commands here act on those files.

    When editing a file, an editor will be opened with the desired
    file.  Once the file is edited and closed, you will be prompted to
    provide a git commit message for your changes.  The standard
    format of a git commit message is a one line summary, followed by
    a blank line, followed by a more in-depth description of the
    changes.  Once the commit is made, the changes will also be pushed
    to the main repo in gitlab.

    Any additional arguments provided will be passed to the git
    comand.

    """
    if not CAL_CONFIG_ROOT:
        raise CMDError("CAL_CONFIG_ROOT not defined.")

    logger.info(f"CAL_CONFIG_ROOT: {CAL_CONFIG_ROOT}")

    if args.edit:
        if args.edit == 'model':
            edit_file = DEFAULT_MODEL_PATH

        elif args.edit == 'config':
            edit_file = DEFAULT_CONFIG_PATH

        logger.info(f"editing {args.edit} file: {edit_file} ...")
        _util.edit_file(edit_file)

    elif args.git == 'diff':
        git_cmd('diff')

    elif args.git == 'commit':
        git_cmd('commit')

    elif args.tag:
        git_cmd('tag', *args.tag)

    elif args.git:
        git_cmd(*args.git)

    else:
        git_cmd('status')
