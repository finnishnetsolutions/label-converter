#!/usr/bin/env bash

rm -rf ./.tox ./.pytest_cache ./build ./dist ./label_converter.egg-info

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
