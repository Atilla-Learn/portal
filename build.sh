#! /bin/sh

pyenv venv
source venv/bin/activate
pip install -r requirements.txt
python generate.py
bower install
tar cvzf atilla-learn-portal-`git rev-parse --short HEAD`.tar.gz web
