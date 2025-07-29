import git

from ._log import CMDError


def check_report_git_status(report, check_valid=False):
    try:
        repo = git.Repo(report.path)
    except git.exc.InvalidGitRepositoryError:
        raise CMDError("report is not a valid git repo, 'commit' report first.")

    if repo.is_dirty():
        print(repo.git.status())
        raise CMDError("report repo is dirty, 'commit' changes first.")

    if check_valid and not report.is_valid():
        raise CMDError("report has not been marked as valid, only valid reports can be exported.  report can be marked valid with 'commit --valid' command.")  # noqa E501
