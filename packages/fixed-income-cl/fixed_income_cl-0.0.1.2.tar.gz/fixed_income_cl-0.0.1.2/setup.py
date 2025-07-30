from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    description = fh.read()

setup(
    name='fixed_income_cl',
    version='0.0.1.2',
    author='Manuel Progaska',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'requests'
        ],
    long_description=description,
    long_description_content_type='text/markdown',
    )