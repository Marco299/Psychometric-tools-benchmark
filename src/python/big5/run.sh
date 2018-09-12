#!/bin/bash
export PYTHONPATH=$PYTHONPATH:../:../
# mandatory param: liwc dictionary, either 2007 or 2015
python big5.py $@