python -m venv penv
source penv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
chmod +x pre-commit
cp pre-commit ../.git/hooks
