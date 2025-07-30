# -*- coding:utf-8 -*-
import os
from setuptools import find_packages
from setuptools import setup

install_requires = []

exclude_file_patterns = ["*.gif"]
version = {}
with open(os.path.join("yeying/version.py")) as fp:
    exec(fp.read(), version)

setup(
    name="yeying-client-python",
    version=version["__version__"],
    description="yeying python client",
    url="https://github.com/yeying-community/yeying-client-python",
    author="yeying-community",
    author_email="your@email.com",
    install_requires=install_requires,
    packages=find_packages(where=".", exclude=exclude_file_patterns),
    # package_data={"": ["*.so", "*.jar", "templates/**/*", "static/**/*"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [

        ]
    },
)
