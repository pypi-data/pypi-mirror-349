# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jwtee",
    version="1.0.0",
    author="0xNafisSec",
    author_email="nafisfuad340@gmail.com",
    description="A stylish JWT decoder for hackers and developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nfs-tech-bd/jwtee",
    packages=find_packages(),
    license='MIT',  # Modern way to specify license
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Environment :: Console",
    ],
    python_requires='>=3.6',
    install_requires=[
        "colorama",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "jwtee=jwtee.jwtee:main",
        ],
    },
)