from setuptools import setup, find_packages

version = {}
with open('spikely/version.py') as fp:
    exec(fp.read(), version)

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(
    name='spikely',
    version=version['__version__'],
    description='Spike sorting made simple',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Roger Hurwitz',
    author_email='rogerhurwitz@gmail.com',
    url='https://github.com/SpikeInterface/spikely',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=[
        'pyqt5>=5.14.2',
        'spikeextractors>=0.8.4',
        'spikesorters>=0.3.3',
        'spiketoolkit>=0.6.3'
    ],
    entry_points={
        'console_scripts': [
            'spikely=spikely.spikely_main:launch_spikely'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
