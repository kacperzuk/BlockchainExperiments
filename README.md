Start in root directory of repository:

```
sudo pip3 install virtualenv # if you dont have it
virtualenv env
source env/bin/activate
pip install rethinkdb flask bigchaindb python-gnupg
cd src/data
rethinkdb &>/dev/null &
bigchaindb configure -y
bigchaindb &>/dev/null start &
cd ..
python3 main.py
```
now visit http://localhost:5000/
