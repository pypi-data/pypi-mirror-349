from setuptools import setup, find_packages

setup(
    name='wtfport-cli',
    version='1.0.4',
    description='Check what process is using a port (CLI)',
    author='Anil Raj Rimal',
    author_email='anilrajrimal@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wtfport = wtfport.cli:main',
        ],
    },
    install_requires=[
        'psutil',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.9',
)
