#!/bin/bash
rm -rf build dist yt_sdk.egg-info
python3 setup.py sdist bdist_wheel
twine upload dist/*
