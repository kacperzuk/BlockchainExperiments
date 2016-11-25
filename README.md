First install rethinkdb: https://rethinkdb.com/docs/install/

Start in root directory of repository:

```
git submodule update --init
sudo apt-get install libyaml-dev gnupg libffi-dev build-essential python3 python3-pip # or equivalent for your distro
sudo pip3 install virtualenv # if you dont have it
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
cd bigchaindb/
python3 setup.py install
cd ../src/data
rethinkdb --join karand.kacperzuk.pl:29015 >/dev/null &
bigchaindb -y configure
bigchaindb start >/dev/null &
cd ..
env FLASK_APP=main.py flask initdb
python3 main.py
```
now visit http://localhost:5000/
