First install rethinkdb: https://rethinkdb.com/docs/install/

Start in root directory of repository:

```
sudo apt-get install gnupg libffi-dev build-essential python3 python3-pip # or equivalent for your distro
sudo pip3 install virtualenv # if you dont have it
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd src/data
rethinkdb --join karand.kacperzuk.pl:29015 >/dev/null &
bigchaindb -y configure
bigchaindb start >/dev/null &
cd ..
env FLASK_APP=main.py flask initdb
python3 main.py
```
now visit http://localhost:5000/
