from pathlib import Path

from setuptools import find_packages, setup

from b24pysdk import SDK_VERSION


def _readme():
    return Path("README.md").read_text(encoding="utf-8")


setup(
    name="b24pysdk",
    version=SDK_VERSION,
    author="Bitrix24",
    author_email="example@gmail.com",
    description="This is the simplest module for quick work with files.",
    long_description=_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/bitrix24/b24pysdk",
    packages=find_packages(),
    install_requires=[],
    classifiers=[],
    keywords="bitrix24 api",
    project_urls={},
    python_requires=">=3.9",
)
