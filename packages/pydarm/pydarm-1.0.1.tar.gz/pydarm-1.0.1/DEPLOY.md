# Deploying pydarm at the LIGO sites

`pydarm` is deployed at the LIGO sites in a custom conda environment.
The conda environment is create from the included
[conda/environment.yaml](conda/environment.yaml), and then the
production release of the pydarm source is installed into that
environment with pip.

The location of the pydarm conda environments at both the Hanford (H1)
and Livingston (L1) sites is at the following locations:
* control room: `/ligo/groups/cal/conda/pydarm`
* site LDAS cluster: `~cal/conda/pydarm`


## deployment procedure

### production tag

Once a version of pydarm is ready for production release and
deployment, it must first be tagged with a production tag.  Production
tags are of the [CalVer](https://calver.org/) form `<YYYYMMDD>.<I>`,
where `<YYYYMMDD>` is the release date (month/day zero-padded), and
`<I>` is a release index starting at zero.  An example production tag
is:

    20240323.0

The release manager should check out the version of pydarm to be
released, create the appropriate release tag, and then push the
release tag to the main repo, e.g.:

    git tag -m "release" 20240323.0
    git push --tags origin

See the full [list of pydarm
tags](https://git.ligo.org/Calibration/pydarm/-/tags).


### production deploy

Once a production release tag has been made, the release needs to be
deployed at all the LIGO sites, both in the control room and to the
`~cal` account at the site LDAS cluster.

*NOTE:* When upgrading a particular site be sure to upgrade both the
control room and site LDAS cluster installs.

The included [`deploy`](scripts/deploy) script is installed at all deployment
location:
* control room: `/ligo/groups/cal/deploy`
* site LDAS cluster: `~cal/bin/deploy`

To update the deployment, SSH to the appropriate location and simply
run the deploy script, e.g.:
```shell
$ ssh <opsportal>
$ /ligo/groups/cal/deploy
```
or:
```shell
$ ssh cal@<calib1>
$ ~/bin/deploy
```

The deployment script will:

* download the latest production tag from the pydarm source repo
* update the site conda install from the included environment.yaml
  file
* pip install pydarm into the conda environment
