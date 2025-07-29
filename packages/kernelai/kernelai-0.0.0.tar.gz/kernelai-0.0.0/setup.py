from setuptools import setup, find_packages

setup(
    name='kernelai',
    version='0.0.0',
    author='Patryk Zdunowski',
    author_email='zdunekere@gmail.com',
    description='AI Kernel',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)