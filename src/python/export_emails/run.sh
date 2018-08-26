#!/bin/bash
export PYTHONPATH=$PYTHONPATH:../:../
# optional param: reset, to empty the db tables containing personality data
python export.py