"""Script for patching and then building label_studio PyInstaller executable.

"""

import logging
import pathlib
import shutil
import site
import subprocess
import sys


def clean_build_dist():
    """Cleans up build and dist directories."""

    build = pathlib.Path('build')
    dist = pathlib.Path('dist')
    if build.exists():
        shutil.rmtree(str(build))
    if dist.exists():
        shutil.rmtree(str(dist))


def apply_patch(reverse: bool = False):
    """Applies patch to label_studio package to support bundling.

    Args:
        reverse: ``True`` if the patch should be reversed rather than applied.
    """

    site_packages = pathlib.Path(site.getsitepackages()[-1])
    label_studio = site_packages.joinpath('label_studio')
    patch = pathlib.Path('C:/Program Files/Git/usr/bin/patch.exe')
    assert patch.exists(), 'Cannot find patch executable, aborting'

    cmd = [str(patch), '-p1']
    if reverse:
        cmd.insert(1, '-R')
    with open('ls.patch') as patchf:
        subprocess.run(cmd, cwd=str(label_studio), stdin=patchf)


def run_pyinstaller():
    """Runs pyinstaller to bundle label_studio."""

    pyinstaller = shutil.which('pyinstaller')
    assert pyinstaller is not None, 'Cannot find pyinstaller, aborting'

    cmd = ['pyinstaller', 'pyinstaller.spec']
    subprocess.run(cmd)


def main() -> int:
    """Runs the script.

    Returns:
        ``0`` if successful, ``1`` otherwise.
    """

    logging.basicConfig(level='INFO')

    logging.info('Cleaning build and dist directories')
    clean_build_dist()
    logging.info('Patching label_studio for bundling')
    apply_patch()
    try:
        logging.info('Running pyinstaller')
        run_pyinstaller()
    except Exception as exc:
        logging.exception('Caught exception: %s', exc)
        return 1
    finally:
        logging.info('Reversing label_studio patch')
        apply_patch(reverse=True)

    return 0


if __name__ == '__main__':
    sys.exit(main())
