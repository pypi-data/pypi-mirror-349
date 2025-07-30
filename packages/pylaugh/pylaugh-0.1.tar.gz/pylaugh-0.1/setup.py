from setuptools import setup, find_packages

setup(
    name="pylaugh",
    version="0.1",
    packages=find_packages(),
    description="A Python module that delivers programming jokes and puns!",
    author="Vibhor Kedia",
    author_email="vibhorkedia21@gmail.com",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[],  # Dependencies (leave empty if none)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)