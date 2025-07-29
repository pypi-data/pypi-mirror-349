# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['planetequil', 'planetequil.scripts', 'planetequil.tests']

package_data = \
{'': ['*'], 'planetequil.tests': ['data/config.yml', 'data/raw/*']}

install_requires = \
['black>=25.1.0,<26.0.0',
 'datasets>=3.3.2,<4.0.0',
 'h5py>=3.13.0,<4.0.0',
 'ipykernel>=6.29.5,<7.0.0',
 'lightning>=2.5.1.post0,<3.0.0',
 'matplotlib>=3.10.1,<4.0.0',
 'mypy>=1.15.0,<2.0.0',
 'numpy>=2.0.2,<3.0.0',
 'pandas>=2.2.3,<3.0.0',
 'plotly>=6.0.0,<7.0.0',
 'poetry>=2.1.1,<3.0.0',
 'pytest>=8.3.5,<9.0.0',
 'scikit-learn>=1.6.1,<2.0.0',
 'scipy>=1.15.2,<2.0.0',
 'torch>=2.7.0,<3.0.0',
 'torchinfo>=1.8.0,<2.0.0',
 'tqdm>=4.67.1,<5.0.0',
 'wandb>=0.19.10,<0.20.0']

setup_kwargs = {
    'name': 'planet-equil',
    'version': '0.1.0',
    'description': 'PlaNet: reconstruction of plasma equilibrium and separatrix using convolutional physics-informed neural operator. See https://doi.org/10.1016/j.fusengdes.2024.114193',
    'long_description': '# PlaNet: plasma equilibrium reconstruction using physics-informed neural operator.\nThis is the official repository if the `planet` package. It is a PyTorch implementation of PlaNet (PLAsma equilibrium reconstruction NETwork), a convolutional physics-informed neural operator for performing plasma equilibrium reconstruction using magnetic and non-magnetic measurements.\n\nFor any kind of reference on the model architecture or the mathematical formulation, see [this paper](https://www.sciencedirect.com/science/article/abs/pii/S0920379624000474). The original work was developed using TensorFlow, as mentioned in the paper. This is a polished and optimized version, using modern PyTorch and PyTorch Lightning. \n\n# Installation\nFirst, create a virtual environment using `venv`\n```shell\npython3.10 -m venv venv \nsource venv/bin/activate\n```\nthen install the package and all the dependencies using `poetry`\n```shell\npip3 install poetry==1.8.3\npoetry config virtualenvs.create false\npoetry install\n```\n\n## Data\nTo train and test PlaNet you can use the dataset available at [this repo](https://github.com/matteobonotto/ITERlike_equilibrium_dataset.git), containing ~85k equilibria of an ITER-like devices. All the equilibria have been computed numerically using the free-boundary Grad-Shafranov solver FRIDA, which is publicly available [here](https://github.com/matteobonotto/frida).\n\n\n## Tutorials\nThere are tutorial notebooks available to get started with `planet`:\n- [1_dataset_creation.ipynb](notebooks/1_dataset_creation.ipynb): show how to create and format your data to perform trainign and inference using the PlaNet model.\n- [2_model_training.ipynb](notebooks/2_model_training.ipynb): shows how to perfrom a full training of the PlaNet model using PyTorch Lightning`.\n- [3_load_pretrained_and_prediction.ipynb](notebooks/3_load_pretrained_and_prediction.ipynb): shows how to load a pretrained model and how to use if to perform reconstruction of plasma equilibrium and to estimate the Grad-Shafranov operator.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n',
    'author': 'Matteo Bonotto',
    'author_email': 'm.bonotto@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
