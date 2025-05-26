python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

git submodule update --init --recursive

cd templates/APA

git sparse-checkout init --no-cone

git sparse-checkout set /versatile-apa/lib.typ /versatile-apa/utils/ /versatile-apa/assets/

cd ../../
