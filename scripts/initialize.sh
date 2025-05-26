#! /usr/bin/bash

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

git submodule update --init --recursive

cd templates/APA

git sparse-checkout init --no-cone

git sparse-checkout set /versatile-apa/lib.typ /versatile-apa/utils/ /versatile-apa/assets/

cd ../../
