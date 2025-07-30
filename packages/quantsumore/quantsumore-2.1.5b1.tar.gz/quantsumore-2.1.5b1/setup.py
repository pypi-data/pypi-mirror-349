from setuptools import setup, find_packages
import sys
import os
import re

# Get the directory containing setup.py
current_dir = os.path.abspath(os.path.dirname(__file__))

version_file = os.path.join(current_dir, "quantsumore", "_version.py")

# Read version dynamically
version = {}
if os.path.exists(version_file):
    with open(version_file, encoding='utf-8') as f:
        exec(f.read(), version)  # Loads __version__ into dictionary


pep440_version = version.get("__version__", "0.0.0") 								# PEP 440 (Canonical Python version)
semver_version = re.sub(r'b(\d+)$', r'-beta.\1', pep440_version)    # SemVer-compatible pre-release

setup(
    name='quantsumore',
    version=pep440_version,  # Default to "0.0.0" if not found  
    author='Cedric Moore Jr.',
    author_email='cedricmoorejunior5@gmail.com',
    description='A comprehensive Python library for scraping and retrieving real-time data across multiple financial markets, including cryptocurrencies, equities, Forex, treasury yields, and consumer price index (CPI) data.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/cedricmoorejr/quantsumore/tree/v{pep440_version}',  # Dynamically inject version         
    project_urls={
        'Source Code': f'https://github.com/cedricmoorejr/quantsumore/releases/tag/v{semver_version}',        
    },
    packages=find_packages(exclude=["*.github", "*.__user_agents_config*", "*.__crypto_config*", "*.__os_config*", "*.__stock_config*"]),
    package_data={
        'quantsumore': [
            'gui/assets/*.ico',
            'gui/assets/*.png'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
    install_requires=[
        'openpyxl',
        'pandas',
        'requests',
        'matplotlib',
        'pillow',
        'numpy',
        'requests_cache',
        'bs4',
        'lxml',
        'importlib_resources; python_version < "3.9"',           
    ],
    license='Apache Software License',
    include_package_data=True,
)
