from setuptools import setup, find_packages

setup(
    name='ksfeatureselector',
    version='0.1.0',
    description='A simple Kolmogorov–Smirnov test-based feature selector for binary classification.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='V Subrahmanya Raghu Ram Kishore Parupudi',
    author_email='pvsrrkishore@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
