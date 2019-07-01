from setuptools import setup

version = {}
with open('spikely/version.py') as fp:
    exec(fp.read(), version)

with open('README.md', 'r') as fp:
    long_description = fp.read()


setup(
    name='spikely',
    version=version['__version__'],
    packages=['spikely'],
    install_requires=[
        'PyQt5>=5.12.3',
        'spikeextractors>=0.5.3',
        'spiketoolkit>=0.3.5'
    ],
    author='Roger Hurwitz',
    author_email='rogerhurwitz@gmail.com',
    description='A GUI around spikeextractors and spiketoolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
