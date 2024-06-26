# -*- coding:utf-8 -*-

from setuptools import setup

lint_deps = ["black==20.8b1", "mypy==0.790"]

extra_require = {
    "lint": lint_deps,
}

setup(
    name="mystery_o_matic",
    version="0.1",
    description="",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=[
        "mystery_o_matic",
        "mystery_o_matic.output",
        "mystery_o_matic.output.html",
        "mystery_o_matic.output.text",
    ],
    license="AGPL3",
    entry_points="""
    [console_scripts]
    mystery-o-matic = mystery_o_matic.__main__:main
    """,
    install_requires=[
        "solidity_parser",
        "slither_analyzer",
        "pygraphviz",
        "networkx",
        "yattag",
        "python-telegram-bot",
        "spacy",
    ],
    extras_require=extra_require,
    url="https://github.com/mystery-o-matic/mystery-o-matic.github.io",
)
