from setuptools import setup

setup(
    name='wtfport-cli',
    version='1.0.2',
    packages=['wtfport'],
    entry_points={
        'console_scripts': [
            'wtfport = wtfport.cli:main',
        ],
    },
    install_requires=[
        'psutil',
    ],
)
