from setuptools import setup, find_packages

setup(
    name='spikely',
    version='0.3.5',
    packages=find_packages(),
    install_requires=['PyQt5', 'spikeextractors', 'spiketoolkit'],
    author='Roger Hurwitz',
    author_email='rogerhurwitz@gmail.com',
    description='An app wrapper around spikeextractors and spiketoolkit',
    url='https://github.com/SpikeInterface/spikely',
    entry_points={
        'console_scripts': [
            'spikely=spikely.main:launch_spikely'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
