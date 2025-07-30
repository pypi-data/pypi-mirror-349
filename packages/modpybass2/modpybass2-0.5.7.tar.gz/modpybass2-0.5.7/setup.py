import os


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
        content = file.read()
    return content


setup(
    name='modpybass',
    version='0.0.11',
    author='Taehong Kim',
    author_email='johannmkammiste@gmail.com',
    url='https://github.com/johannmkammiste/modpybassmacos',
    description=('modified pybass'),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='bass pybass audio',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    packages=['modpybass'],
    package_data={
        'modpybass': ['lib/x86/*', 'lib/x64/*', 'lib/aarch64/*', 'lib/armhf/*'],
    },
)
