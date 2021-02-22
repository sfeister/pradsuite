# pradsuite (Scott's Particle Radiography Suite)

**pradsuite** is a set of Python tools related to the particle radiography data pipeline. They were originally designed for Scott's personal use, but you might still find them useful.

## Setup

### Dependencies
This module requires **Python 3.7+**. Installation requires **git**.

* [`numpy`](http://www.numpy.org/)
* [`scipy`](https://www.scipy.org/)
* [`astropy`](https://www.astropy.org/)
* [`matplotlib`](https://matplotlib.org/)
* [`h5py`](https://www.h5py.org/)
* [`plasmapy`] (https://www.plasmapy.org/)
* [`pradformat`] (https://scott.cikeys.com/prad/)

The dependencies may be installed according to the directions on their webpages. Please install **PlasmaPy** from its **GitHub source code**, so that it includes the Proton Radiography software written by Peter Heuer (merged into the PlasmaPy source code on February 22, 2021).

### Installation
After installing the required packages, we may install **pradsuite**.

One way to install **pradsuite** is via
```bash
pip install "git+https://github.com/phyzicist/pradsuite.git"
```

To update **pradsuite** at a later date
```bash
pip install --upgrade "git+https://github.com/phyzicist/pradsuite.git"
```

An alternative way to install **pradsuite** is via
```bash
git clone https://github.com/phyzicist/pradsuite.git
python setup.py install
```

### General Usage
```python
import pradsuite
```
I didn't write any formal documentation for this package, since it's mostly meant for personal use. Please explore the source code.

Here are some potentially useful functions accessible in the main namespace:
| Function Name | Description |
|---|---|
| pradsuite.load_prf_grid(...)  | Loads PlasmaPy grids object from pradformat SimpleFields File
| pradsuite.save_prf_grid(...)  | Saves pradformat SimpleFields File from PlasmaPy grids object
 
## Uninstalling

To uninstall **pradsuite**
```shell
pip uninstall pradsuite
```