# -*- coding:utf-8 -*-

from setuptools import setup

lint_deps = ["black==20.8b1", "mypy==0.790"]

extra_require = {
    "lint": lint_deps,
}

setup(
    name="DetectiveMysteryOMatic",
    version="0.1",
    description="",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=[
        "DetectiveMysteryOMatic",
        "DetectiveMysteryOMatic.output",
        "DetectiveMysteryOMatic.output.html",
        "DetectiveMysteryOMatic.output.text",
    ],
    license="AGPL3",
    entry_points="""
    [console_scripts]
    MysteryOMatic = DetectiveMysteryOMatic.__main__:main
    """,
    install_requires=["solidity_parser", "slither_analyzer", "pygraphviz", "networkx", "yattag", "telegram"],
    extras_require=extra_require,
    url="https://github.com/neuromancer/DetectiveMysteryOMatic",
)
