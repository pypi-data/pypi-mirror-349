from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='feds_shield',
    version='0.0.2',
    description='A simple cryptographic program',
    long_description=readme,
    author='Richard Pham',
    author_email='phamrichard45@gmail.com',
    url='https://github.com/Changissnz/feds_shield',
    #license=license,
    packages=find_packages(exclude=('tests','dat'))
)
