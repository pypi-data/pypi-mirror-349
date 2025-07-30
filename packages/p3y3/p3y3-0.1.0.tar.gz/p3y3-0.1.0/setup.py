from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name='p3y3',
    version='0.1.0',
    packages=['p3y3'],
    url='https://github.com/FAReTek1/p3y3',
    license='MIT',
    author='faretek1',
    author_email='',
    description='3y3 encoding in python',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
