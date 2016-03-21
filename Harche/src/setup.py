from setuptools import setup, find_packages

setup(
    name='sports',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = sports.settings']},
)
