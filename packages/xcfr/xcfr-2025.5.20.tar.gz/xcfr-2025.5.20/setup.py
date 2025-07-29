from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='xcfr',
    version='2025.5.20',
    description='xcfr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feng Zhu',
    author_email='fengzhu@ucar.edu',
    url='https://github.com/fzhu2e/xcfr',
    packages=find_packages(),
    include_package_data=True,
    license='BSD-3',
    zip_safe=False,
    keywords=['Climate Field Reconstruction'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'netCDF4',
        'xarray',
        'dask',
        'nc-time-axis',
        'colorama',
        'tqdm',
        'x4c-exp',
    ],
)
