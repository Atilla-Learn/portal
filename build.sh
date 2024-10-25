#! /bin/bash

virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
python3 generate.py
bower install
tar cvzf atilla-learn-portal-`git rev-parse --short HEAD`.tar.gz web