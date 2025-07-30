from setuptools import setup, find_packages

setup(
    name='Data_Structure_Hub',
    version='0.1.0',
    author='Yashashvi bhardwaj',
    author_email='yashashvibhardwaj@gmail.com',
    description='A Python package with basic data structures',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
