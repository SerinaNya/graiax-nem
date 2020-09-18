@echo off
del dist\* /Q
python setup.py sdist bdist_wheel
twine upload dist/*