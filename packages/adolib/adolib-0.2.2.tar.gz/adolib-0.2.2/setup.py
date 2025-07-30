from setuptools import setup, find_packages

setup(
    name="adolib",
    version="0.2.2",
    description="A beginner-friendly Python utilities library",
    author="Karl Santiago Bernaldez",
    author_email="bernaldezkarlsantiago@gmail.com",
    packages=find_packages(include=["adolib", "adolib.*"]),
    python_requires=">=3.6",
    license="MIT",
)
