from setuptools import setup, find_packages

setup(
    name="osintcat",
    version="0.3",
    packages=find_packages(),
    install_requires=["requests"],
    author="flux",
    description="python package for osintcat.ru",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stormylol/osintcat",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)
