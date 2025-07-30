# %%
# import setgraphviz
# print(dir(setgraphviz))
# print(setgraphviz.__version__)

# %%
from setgraphviz import setgraphviz
setgraphviz()

# %%
from setgraphviz import check_logger

check_logger(verbose='debug')
check_logger(verbose='info')
check_logger(verbose='warning')
check_logger(verbose='error')
check_logger(verbose=None)
