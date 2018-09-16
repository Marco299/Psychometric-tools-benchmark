#!/bin/bash
export PYTHONPATH=$PYTHONPATH:../:../
# mandatory param: tool, either liwc07, liwc15 or twitPers
python big5.py $@