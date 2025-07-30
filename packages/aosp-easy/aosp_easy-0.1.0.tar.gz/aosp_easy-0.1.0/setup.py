#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='aosp_easy',  # 包的名字
    author='min',  # 作者
    version='0.1.0',  # 版本号
    license='MIT',

    description='create android app or service',  # 描述
    long_description='''quick create app or service in aosp source code 在Android源码中快速创建APP或者服务''',
    author_email='testmin@outlook.com',  # 你的邮箱**
    url='',
    packages=['aosp_easy'],  # 包名
    entry_points={
        'console_scripts': [
            'aosp_easy=aosp_easy.aosp_easy:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)