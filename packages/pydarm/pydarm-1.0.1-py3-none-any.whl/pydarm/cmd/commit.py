from pathlib import Path
from subprocess import run

import git

from ._log import logger, CMDError
from . import _args
from ._report import Report


def add_args(parser):
    _args.add_report_argument(parser)
    parser.add_argument(
        '--diff', '-d', action='store_true',
        help="show uncommited report diffs and exit"
    )
    parser.add_argument(
        '--valid', action='store_true',
        help="tag report version as 'valid' after committing"
    )
    parser.add_argument(
        '--message', required=True,
        help="commit message"
    )


def main(args):
    """commit report version

    This commits any changes to the report in to an internal git repo
    for tracking.  This must be done before exporting.

    """
    try:
        report = Report.find(args.report)
    except FileNotFoundError as e:
        raise CMDError(e)
    logger.info(f"report found: {report.path}")

    ##########
    # initial report git configuration
    #
    # always do this so that we make sure the repo has the most
    # up-to-date configuration

    # this initializes the repo if it doesn't exist
    repo = git.Repo.init(report.path, initial_branch='main')

    # files to ignore
    with open(Path(report.path, '.gitignore'), 'wt') as f:
        f.write('*~\n')
    repo.git.add('.gitignore')

    # FIXME: should we use git-lfs to track the data files?
    # repo.git.lfs('install')
    # # purge old lfs config
    # Path(report.gen_path('.gitattributes')).unlink(missing_ok=True)
    # # FIXME: the measurement files should be specified as
    # # '--lockable', but we need a way to distinguish the chain hdf5
    # # files to be lockable because they might need to be updated
    # repo.git.lfs('track', '*.hdf5', '*.xml')
    # repo.git.lfs('track', '*.hdf5', '*.png', '*.json', '*.npz', '*.pdf')
    # # HACK: need to sort the .gitattributes file because the order is
    # # otherwise non-deterministic
    # gap = report.gen_path('.gitattributes')
    # with open(gap) as f:
    #     lines = f.readlines()
    # with open(gap, 'wt') as f:
    #     for line in sorted(lines):
    #         f.write(line)
    # repo.git.add('.gitattributes')

    ##########

    # if marking commit as valid make sure we remove any old-style
    # valid tags
    if args.valid:
        Path(report.gen_path('tags', 'valid')).unlink(missing_ok=True)

    # add all files in the report to the index.
    # use the git command directly because for some reason it adds
    # cleaner and faster
    repo.git.add('*')

    if args.diff:
        p = run(
            ['git', 'diff', '--cached'],
            cwd=report.path,
        )
        raise SystemExit(p.returncode)

    else:
        print(repo.git.status())

    if repo.is_dirty():
        # this is kind of annoying, but invoke git directly because it
        # allows for the editor to pass through to the tty
        cmd = ['git', 'commit', '-a']
        if args.message:
            cmd += ['-m', args.message]
        p = run(
            cmd,
            cwd=report.path,
        )
        if p.returncode:
            raise SystemExit(p.returncode)

    if args.valid:
        logger.info(f"tagging as valid report commit {repo.head.commit.hexsha}")
        repo.create_tag(
            'valid',
            message=f"pydarm marked report {report.id} as valid.",
            force=True,
        )
