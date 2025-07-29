from setuptools import setup, find_packages
setup(
    name='ptinnls',
    version='0.1.0',
    description='Implements Sparse NNLS',
    author='Nathan Wamsley',
    author_email='nwamsley@parallelsq.org',
    packages=['ptinnls'],
    install_requires=[
        'numpy',
        'cvxopt',
        'scipy'
    ],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)