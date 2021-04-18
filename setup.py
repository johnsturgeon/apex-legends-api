""" setup script for apex_legends_api """
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='apex-legends-api',
    version='1.3.2',
    packages=['apex_legends_api'],
    python_requires='>=3.6.*',
    url='https://github.com/johnsturgeon/apex-legends-api',
    license='MIT',
    author='John Sturgeon',
    author_email='john.sturgeon@me.com',
    install_requires=requirements,
    description='Python wrapper for https://apexlegendsapi.com',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
