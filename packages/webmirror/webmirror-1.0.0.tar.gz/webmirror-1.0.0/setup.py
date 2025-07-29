# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="webmirror",
    version="1.0.0",
    author="Your Name",
    author_email="nafisfuad340@gmail.com",
    description="A multi-threaded website mirroring tool that downloads and saves websites locally.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nfs-tech-bd/webmirror ",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Environment :: Console",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "beautifulsoup4",
        "urllib3"
    ],
    entry_points={
        "console_scripts": [
            "webmirror=webmirror.webmirror:main",
        ],
    },
)