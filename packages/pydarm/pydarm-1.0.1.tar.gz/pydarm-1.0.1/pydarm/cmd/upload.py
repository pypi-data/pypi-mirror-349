import logging
from pathlib import Path
from subprocess import run

import git

from ._log import logger, CMDError
from . import _args
from . import _util
from ._report import Report
from ._git import check_report_git_status


def git_init_report_remote(host, repo_path):
    """initialize a report remote git repo

    create the bare repo, install the post-update hook to keep the
    server info up-to-date, then run it to prep the repo to recieve
    pushes.

    """
    cmd = ['bash', '-s']
    capture_output = True
    if logger.handlers[0].level == logging.DEBUG:
        cmd += ['-x']
        capture_output = False
    if host:
        logger.debug(f"remote host: {host}")
        cmd = ['ssh', host] + cmd

    # this is a shell command executed on the remote system to setup
    # the archive report repo
    remote_cmd = f"""
git init --initial-branch main {repo_path}
(cd {repo_path} && git config receive.denyCurrentBranch updateInstead)
cat <<EOF >{repo_path}/.git/hooks/post-update
#!/bin/sh
exec git-update-server-info
EOF
chmod 755 {repo_path}/.git/hooks/post-update
(cd {repo_path} && git update-server-info)
"""

    logger.debug("executing remote initialization command...")
    run(
        cmd,
        input=remote_cmd,
        text=True,
        capture_output=capture_output,
        check=True,
    )


def upload_report(report, config_file=None):
    """upload report to archive

    The archive is specified in the config `archive_location` field.
    If a config file is not specified the report's config file will be
    used.

    """
    if not config_file:
        config_file = report.config_file

    config = _util.load_config(config_file)

    # parse the archive specification
    archive_location = config['Common']['archive_location']
    hostpath = archive_location.split(':')
    if len(hostpath) == 1:
        host = None
        archive_root = hostpath[0]
        remote_url = ''
    else:
        host, archive_root = hostpath
        remote_url = f"{host}:"
    archive_repo_path = Path(archive_root, 'reports', report.id)
    remote_url += str(archive_repo_path)

    repo = git.Repo(report.path)

    git_init_report_remote(host, archive_repo_path)

    if 'archive' in repo.remotes:
        remote = repo.remotes['archive']
        remote.set_url(remote_url)
    else:
        remote = repo.create_remote('archive', remote_url)

    urls = ' '.join(remote.urls)
    logger.info(f"pushing to archive remote: {urls}")
    # use the git command directly so that we can see the progress
    # output
    run(
        ['git', 'push', '--mirror', '--progress'],
        cwd=report.path,
        check=True,
    )


def add_args(parser):
    _args.add_report_argument(parser)


def main(args):
    """push report to archive

    """
    try:
        report = Report.find(args.report)
    except FileNotFoundError as e:
        raise CMDError(e)
    logger.info(f"report found: {report.path}")

    check_report_git_status(report)

    upload_report(report, config_file=args.config)
