from setuptools import setup, find_packages

setup(
    name="repospoofscanner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'typer',
        'rich',
        'httpx',
        'PyGithub',
        'rapidfuzz'
    ]
)