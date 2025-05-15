# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT


from setuptools import setup, find_packages
import aibolit

setup(
    name='aibolit',
    version=aibolit.__version__,
    description=aibolit.__doc__.strip(),
    long_description='DevTool recommending how to improve the maintenance quality of '
                     'your Java classes',
    url='https://github.com/yegor256/aibolit',
    download_url='https://github.com/yegor256/aibolit',
    author=aibolit.__author__,
    author_email='yegor256@gmail.com',
    license=aibolit.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aibolit = aibolit.__main__:main'
        ],
    },
    extras_require={},
    install_requires=open('requirements.txt', 'r', encoding='utf-8').readlines(),
    tests_require=open('requirements.txt', 'r', encoding='utf-8').readlines(),
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    include_package_data=True,
    package_data={
        'aibolit': [
            'binary_files/halstead.jar',
            'binary_files/model.dat']
    },
)
