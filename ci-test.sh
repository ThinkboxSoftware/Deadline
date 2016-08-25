#!/bin/sh
pep8 --filename=*.py --count --ignore=W293,E201,E202,E501 .
python -m compileall -f -q .

