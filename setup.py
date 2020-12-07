# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

packages = find_packages(exclude=('test', 'tests.*', "test*"))


def get_dis():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


def main():
    dis = get_dis()
    setup(
        name="nonebot-plugin-picsearcher",
        version="0.1.0",
        url="https://github.com/synodriver/nonebot_plugin_picsearcher",
        packages=packages,
        keywords=["nonebot"],
        description="A picsearch plugin for nonebot2",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="synodriver",
        author_email="diguohuangjiajinweijun@gmail.com",
        python_requires=">=3.6",
        install_requires=["aiohttp", "lxml"],
        license='GPLv3',
        classifiers=[
            "Framework :: asyncio",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython"
        ],
        include_package_data=True
    )


if __name__ == "__main__":
    main()
