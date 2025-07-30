import logging
from setgraphviz.setgraphviz import (
    setgraphviz,
    get_platform,
    wget,
    check_logger,
    )


__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '1.0.3'

# Setup root logger
_logger = logging.getLogger('setgraphviz')
_log_handler = logging.StreamHandler()
_fmt = '[{asctime}] [{name}] [{levelname}] {msg}'
_formatter = logging.Formatter(fmt=_fmt, style='{', datefmt='%d-%m-%Y %H:%M:%S')
_log_handler.setFormatter(_formatter)
_log_handler.setLevel(logging.DEBUG)
_logger.addHandler(_log_handler)
_logger.propagate = False

# module level doc-string
__doc__ = """
setgraphviz
=====================================================================

setgraphviz is to set the path for graphviz for windows machines.
Based on the operating system, it will download graphviz and include the paths into the system environment.
There are multiple steps that are taken to set the Graphviz path in the system environment.
The first two steps are automatically skipped if already present.

Step 1. Downlaod Graphviz.
Step 2. Store Graphviz files on disk in temp-directory or the provided dirpath.
Step 3. Add the /bin directory to environment.

Example
-------
>>> from setgraphviz import setgraphviz
>>> setgraphviz()

References
----------
https://github.com/erdogant/setgraphviz

"""
