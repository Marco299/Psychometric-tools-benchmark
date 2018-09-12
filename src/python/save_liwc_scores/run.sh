#!/bin/bash
export PYTHONPATH=$PYTHONPATH:../:../
# first mandatory param: liwc scores file name
# second mandatory param: liwc dictionary, either 2007 or 2015
python liwc_scores.py $@