from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='apex-legends-api',
    version='0.1.10',
    packages=['apex_legends_api'],
    python_requires='>=3.6.*',
    url='https://github.com/johnsturgeon/apex-legends-api',
    license='MIT',
    author='John Sturgeon',
    author_email='john.sturgeon@me.com',
    install_requires=['requests >= 2.5.4.1'],
    description='Python wrapper for https://apexlegendsapi.com',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
