from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='kognie-api',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'setuptools>=65.5.0',
        'requests>=2.32.3'
    ],
    author='Kognie',
    long_description=long_description,
    long_description_content_type='text/markdown',
)