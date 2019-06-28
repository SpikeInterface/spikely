from setuptools import setup, find_packages

setup(
    name='spikely',
    version='0.3.1',
    author='Roger Hurwitz',
    author_email='rogerhurwitz@gmail.com',
    description='An app for building spike processing pipelines',
    url='https://github.com/SpikeInterface/spikely',
    packages=find_packages(),
    classifers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
