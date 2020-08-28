virtualenv env --python=/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
source env/bin/activate
pip install -U pip==20.2.2
pip install -r requirements.txt
deactivate