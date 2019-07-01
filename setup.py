from setuptools import setup

version = {}
with open('spikely/version.py') as fp:
    exec(fp.read(), version)


setup(
    name='spikely',
    version=version['__version__'],
    packages=['spikely'],
    install_requires=[
        'PyQt5>=5.12.3',
        'spikeextractors',
        'spiketoolkit'
    ],
    author='Roger Hurwitz',
    author_email='rogerhurwitz@gmail.com',
    description='An app wrapper around spikeextractors and spiketoolkit',
    url='https://github.com/SpikeInterface/spikely',
    entry_points={
        'console_scripts': [
            'spikely=spikely.spikely_main:launch_spikely'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
