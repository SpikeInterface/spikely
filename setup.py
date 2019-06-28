from setuptools import setup

setup(
    name='spikely',
    version='0.3.5',
    packages=['spikely'],
    install_requires=['PyQt5'],
    author='Roger Hurwitz',
    author_email='rogerhurwitz@gmail.com',
    description='An app for building spike processing pipelines',
    url='https://github.com/SpikeInterface/spikely',
    entry_points={
        'console_scripts': [
            'spikely=spikely.spikely:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
