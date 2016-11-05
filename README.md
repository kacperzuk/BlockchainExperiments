Start in root directory of repository:

```
sudo pip3 install virtualenv # if you dont have it
virtualenv env
source env/bin/activate
pip install rethinkdb flask bigchaindb python-gnupg
cd src/data
rethinkdb &>/dev/null &
bigchaindb -y configure
bigchaindb start &>/dev/null &
cd ..
env FLASK_APP=main.py flask initdb
python3 main.py
```
now visit http://localhost:5000/
