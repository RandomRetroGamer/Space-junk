echo " >> starting build.sh << "
echo
echo 

python3 -m venv .venv

echo "--------------------"

echo
echo
echo

source .venv/bin/activate
pip install -r requirements.txt

echo
echo
echo

python3 main.py

echo
echo
echo "--------------------"

