# drinklist-api
The new backend for the FIUS drinklist

## Setup dev env

```shell
# setup virtualenv
virtualenv venv # or python -m venv venv
. venv/bin/activate


# install requirements
pip install -r requirements_developement.txt
pip install -r requirements.txt

pip install -e . 
```

## Start server
```shell
./start.sh
```