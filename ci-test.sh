#!/bin/sh
pep8 --filename=*.py --count --ignore=W293,E501 .
python -m compileall -f -q .

