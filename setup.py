import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import aibolit

setup(
    name='aibolit',
    version=aibolit.__version__,
    description=aibolit.__doc__.strip(),
    long_description='Defect Detection Static Analyzer with Machine Learning in Mind',
    url='https://github.com/yegor256/aibolit',
    download_url='https://github.com/yegor256/aibolit',
    author=aibolit.__author__,
    author_email='yegor256@gmail.com',
    license=aibolit.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'http = aibolit.__main__:main'
        ],
    },
    extras_require={},
    install_requires=[],
    tests_require=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
)
