# setgraphviz

[![Python](https://img.shields.io/pypi/pyversions/setgraphviz)](https://img.shields.io/pypi/pyversions/setgraphviz)
[![Pypi](https://img.shields.io/pypi/v/setgraphviz)](https://pypi.org/project/setgraphviz/)
[![Docs](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/setgraphviz/)
[![LOC](https://sloc.xyz/github/erdogant/setgraphviz/?category=code)](https://github.com/erdogant/setgraphviz/)
[![Downloads](https://static.pepy.tech/personalized-badge/setgraphviz?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/setgraphviz)
[![Downloads](https://static.pepy.tech/personalized-badge/setgraphviz?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/setgraphviz)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/setgraphviz/blob/master/LICENSE)
[![Forks](https://img.shields.io/github/forks/erdogant/setgraphviz.svg)](https://github.com/erdogant/setgraphviz/network)
[![Issues](https://img.shields.io/github/issues/erdogant/setgraphviz.svg)](https://github.com/erdogant/setgraphviz/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
![GitHub Repo stars](https://img.shields.io/github/stars/erdogant/setgraphviz)
![GitHub repo size](https://img.shields.io/github/repo-size/erdogant/setgraphviz)
[![Donate](https://img.shields.io/badge/Support%20this%20project-grey.svg?logo=github%20sponsors)](https://erdogant.github.io/setgraphviz/pages/html/Documentation.html#)
<!---[![BuyMeCoffee](https://img.shields.io/badge/buymea-coffee-yellow.svg)](https://www.buymeacoffee.com/erdogant)-->
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->


* ``setgraphviz`` is Python package

# 
**Star this repo if you like it! ⭐️**
#

setgraphviz is to set the path for graphviz for Windows environments.
Based on the operating system, it will download graphviz and include the paths into the system environment.
There are multiple steps that are taken to set the Graphviz path in the system environment.
The first two steps are automatically skipped if already present.


Step 1. Downlaod Graphviz.

Step 2. Store Graphviz files on disk in temp-directory or the provided dirpath.

Step 3. Add the /bin directory to environment.


### Installation

```bash
pip install setgraphviz            # normal install
pip install --upgrade setgraphviz # or update if needed
```

#### Import setgraphviz package
```python
from setgraphviz import setgraphviz
setgraphviz()
```


#### References
* https://github.com/erdogant/setgraphviz

### Contribute
* All kinds of contributions are welcome!
* If you wish to buy me a <a href="https://www.buymeacoffee.com/erdogant">Coffee</a> for this work, it is very appreciated :)

### Licence
See [LICENSE](LICENSE) for details.
