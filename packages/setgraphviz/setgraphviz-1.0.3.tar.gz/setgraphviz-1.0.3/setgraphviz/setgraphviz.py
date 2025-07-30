"""Set graphiz path
# Name        : setgraphviz.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/setgraphviz
# Licence     : See licences
"""

import os
import sys
import requests
import logging
import zipfile
import tempfile
import shutil
logger = logging.getLogger(__name__)


# %% Get graphiz path and include into local PATH
def setgraphviz(dirpath=None, verify_certificate: bool = True, verbose: [str, int] = 'info'):
    """Set the graphviz path.

    There are multiple steps that are taken to set the Graphviz path in the system environment for windows machines.
    The first two steps are automatically skipped if already present.

    1. Downlaod Graphviz.
    2. Store Graphviz files on disk in temp-directory or the provided dirpath.
    3. Add the /bin directory to environment.

    Parameters
    ----------
    dirpath : String, optional
        Pathname of directory to save graphviz files.
    verify_certificate : bool (default: True)
        True: Verify the certificates
        False: Do not verify
    verbose : [str, int], optional
        Set the verbose messages using string or integer values.

    Returns
    -------
    None.

    """
    # Set the logger
    set_logger(verbose=verbose)
    URL = 'https://erdogant.github.io/datasets/graphviz-2.38.zip'

    finPath=''
    if get_platform() == "windows":
        # Download from github
        gfile, curpath = download_graphviz(URL, dirpath=dirpath, verify_certificate=verify_certificate)

        # curpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GRAPHVIZ')
        # filesindir = os.listdir(curpath)[0]
        idx = gfile[::-1].find('.') + 1
        dirname = gfile[:-idx]
        getPath = os.path.abspath(os.path.join(curpath, dirname))
        getZip = os.path.abspath(os.path.join(curpath, gfile))

        # Count files (excluding subdirectories): There should be 103 files
        file_count = sum(len(files) for _, _, files in os.walk(getPath))

        # Unzip if path does not exists
        if not os.path.isdir(getPath) or file_count != 103:
            if os.path.exists(finPath) and os.path.isdir(finPath):
                shutil.rmtree(finPath)
                logger.info(f"Deleting existing corrupt directory: {finPath}")

            logger.info('Extracting graphviz files.')
            pathname, _ = os.path.split(getZip)
            # Unzip
            zip_ref = zipfile.ZipFile(getZip, 'r')
            zip_ref.extractall(pathname)
            zip_ref.close()
            getPath = os.path.join(pathname, dirname)

        # Point directly to the bin
        finPath = os.path.abspath(os.path.join(getPath, 'release', 'bin'))
    else:
        logger.info('The OS is not supported to automatically set Graphviz in the system env.')
        pass
        # sudo apt install python-pydot python-pydot-ng graphviz
        # dpkg -l | grep graphviz
        # call(['dpkg', '-l', 'grep', 'graphviz'])
        # call(['dpkg', '-s', 'graphviz'])

    # Add to system
    if finPath not in os.environ["PATH"]:
        logger.info('Set Graphviz path in environment.')
        os.environ["PATH"] += os.pathsep + finPath
    else:
        logger.info('Graphviz path found in environment.')

    return finPath


# %%
def get_platform():
    platforms = {
        'linux1':'linux',
        'linux2':'linux',
        'darwin':'osx',
        'win32':'windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    logger.info(f'System found: {platforms[sys.platform]}')
    return platforms[sys.platform]


# %% Import example dataset from github.
def download_graphviz(url, dirpath=None, verify_certificate=True):
    """Import example dataset from github.

    Parameters
    ----------
    url : str, optional
        url-Link to graphviz. The default is 'https://erdogant.github.io/datasets/graphviz-2.38.zip'.
    verify_certificate : bool (default: True)
        True: Verify the certificates
        False: Do not verify

    Returns
    -------
    tuple : (gfile, dirpath).
        gfile : filename
        dirpath : currentpath

    """
    if dirpath is None:
        dirpath = os.path.join(tempfile.gettempdir(), 'GRAPHVIZ')
    elif dirpath=='workingdir':
        dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GRAPHVIZ')

    gfile = wget.filename_from_url(url)
    PATH_TO_DATA = os.path.join(dirpath, gfile)
    if not os.path.isdir(dirpath):
        logger.info(f'Create graphviz directory: {dirpath}')
        os.makedirs(dirpath, exist_ok=True)

    # Check file exists.
    if not os.path.isfile(PATH_TO_DATA):
        # Download data from URL
        logger.info('Downloading graphviz..')
        wget.download(url, dirpath, verify_certificate=verify_certificate)

    return gfile, dirpath


# %% Retrieve files files.
class wget:
    """Retrieve file from url."""

    def filename_from_url(url):
        """Return filename."""
        return os.path.basename(url)

    def download(url, writepath, verify_certificate=True):
        """Download.

        Parameters
        ----------
        url : str.
            Internet source.
        writepath : str.
            Directory to write the file.
        verify : bool (default: True)
            True: Verify
            False: Do not verify

        Returns
        -------
        None.

        """
        filename = wget.filename_from_url(url)
        # Ensure the directory exists
        os.makedirs(os.path.dirname(writepath), exist_ok=True)
        writepath = os.path.join(writepath, filename)
        # Set the folder to write mode (read, write, and execute)
        r = requests.get(url, stream=True, verify=verify_certificate)
        # Check for HTTP errors (e.g., 404, 500)
        r.raise_for_status()
        # Write to disk
        with open(writepath, "wb") as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

# %%
def get_logger():
    return logger.getEffectiveLevel()


# %%
def set_logger(verbose: [str, int] = 'info'):
    """Set the logger for verbosity messages.

    Parameters
    ----------
    verbose : [str, int], default is 'info' or 20
        Set the verbose messages using string or integer values.
        * [0, 60, None, 'silent', 'off', 'no']: No message.
        * [10, 'debug']: Messages from debug level and higher.
        * [20, 'info']: Messages from info level and higher.
        * [30, 'warning']: Messages from warning level and higher.
        * [50, 'critical']: Messages from critical level and higher.

    Returns
    -------
    None.

    > # Set the logger to warning
    > set_logger(verbose='warning')
    > # Test with different messages
    > logger.debug("Hello debug")
    > logger.info("Hello info")
    > logger.warning("Hello warning")
    > logger.critical("Hello critical")

    """
    # Set 0 and None as no messages.
    if (verbose==0) or (verbose is None):
        verbose=60
    # Convert str to levels
    if isinstance(verbose, str):
        levels = {'silent': 60,
                  'off': 60,
                  'no': 60,
                  'debug': 10,
                  'info': 20,
                  'warning': 30,
                  'error': 50,
                  'critical': 50}
        verbose = levels[verbose]

    # Configure root logger if no handlers exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = '[{asctime}] [{name}] [{levelname}] {msg}'
        formatter = logging.Formatter(fmt=fmt, style='{', datefmt='%d-%m-%Y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Show examples
    logger.setLevel(verbose)


def check_logger(verbose: [str, int] = 'info'):
    """Check the logger."""
    set_logger(verbose)
    logger.debug('DEBUG')
    logger.info('INFO')
    logger.warning('WARNING')
    logger.critical('CRITICAL')

# %% Main
if __name__ == "__main__":
    pass
