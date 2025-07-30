from setuptools import setup

with open('/home/hassan/Documents/codes/deusfinance/web3py-collections/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    install_requires=required
)
