#!/bin/bash

cd $(dirname $0)

python -m coverage run -m hfcommon_tests.runtests
