from setuptools import setup, find_packages

setup(
    name="proxyrotator",
    version="0.0.2",
    author="M Vashishta Varma",
    author_email="levovarma@gmail.com",
    description="A simple proxy rotation utility",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)
