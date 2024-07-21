python -m venv pyenv
source pyenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
chmod +x pre-commit
cp pre-commit ../.git/hooks
