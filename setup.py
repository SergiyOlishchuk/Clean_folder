from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='1.0.0',
    author='author',
    author_email='author@example.com',
    description='Python package for sorting folders',
    long_description='Python package for sorting folders',
    packages=find_packages(),
    classifiers= [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    requires=['zipp'],
    entry_points={
        'console_scripts' : [
            'clean-folder=clean_folder.clean:main'
        ]
    }
)

