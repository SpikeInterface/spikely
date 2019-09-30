pip uninstall -y spikely
rd /s /q build
rd /s /q dist
rd /s /q spikely.egg-info
python setup.py install
