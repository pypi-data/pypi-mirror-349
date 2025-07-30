from setuptools import setup, find_packages

setup(
    name="findacat-py",
    version="1.0.0",
    description="A Python wrapper for the finda.cat API.",
    author="Never",
    url="https://github.com/raz461/findacat-py",
    project_urls={
        "Source": "https://github.com/raz461/findacat-py",
        "Bug Tracker": "https://github.com/raz461/findacat-py/issues",
    },
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.10"
)