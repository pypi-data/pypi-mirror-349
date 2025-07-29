import subprocess

from ._log import logger
from ._const import IFO


SSH_USER = 'dmtexec'

DMT_HOST_PORT_MAP = {
    'dmt1': 3001,
    'dmt2': 3002,
    'dmt3': 3003,
}

SSH_PRIVATE_KEY = '/var/lib/dmt_proxy/id_ed25519_dmt'


def ssh_cmd(host, *args):
    SSH_HOST = f'{IFO.lower()}guardian1'
    SSH_CMD = [
        'ssh',
        '-t',
        '-o=PubkeyAuthentication=yes',
        '-i', SSH_PRIVATE_KEY,
        '-p', str(DMT_HOST_PORT_MAP[host]),
        '{}@{}'.format(SSH_USER, SSH_HOST),
        '--',
    ]
    SSH_CMD += args
    try:
        logger.debug("cmd: "+' '.join(SSH_CMD))
        subprocess.run(
            SSH_CMD,
            check=True,
        )
    except subprocess.CalledProcessError:
        raise SystemExit("ERROR: GDS SSH command exited with an error.")


def add_args(parser):
    parser.add_argument(
        'command', choices=['status', 'log', 'restart'],
        help="command to execute")
    parser.add_argument(
        'host', nargs='*', default=['dmt1', 'dmt2'],
        help="host (default: dmt1 dmt2)")


def main(args):
    """GDS pipeline status and control

    Execute a restricted set of commands on the site DMT systems to
    control and get status of the calibration "GDS" pipeline.  The
    available commands are:

      status: print status of the pipeline, including config, filter
      file checksum, and service status

      log: show the last 100 lines of the journal log of the pipeline
      service

      restart: pull in the lastest config and GDS filter and restart
      the pipeline service

    By default, the commands are executed on both the dmt1 and dmt2
    systems, which run the prodocution pipeline services.  The dmt3
    host can be specified as well to update/restart the running code
    on the test dmt3 ssytem.

    """

    if not IFO:
        raise SystemExit("ERROR: IFO not specified.")

    for host in args.host:
        logger.info(f"==================== {host} {args.command} ====================")
        ssh_cmd(host, args.command)
        logger.info("========================================")
