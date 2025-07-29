# A minimal setup.py file for supporting editable installs

from setuptools import setup, find_packages

setup(
    name="mseep-llm-os",
    author="mseep",
    author_email="support@skydeck.ai",
    maintainer="mseep",
    maintainer_email="support@skydeck.ai",
                    packages=find_packages(),
    version="0.1.1",
)
