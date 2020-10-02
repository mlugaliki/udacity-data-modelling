##### Data modelling project

This project processes music streaming data from json into postgresql.
This data that is saved in postgresql is normalised, it can be used to generate business reports 

##### Installation
- install python3
- install postgresql
- create a python virtual environment
```python3
    python3 -m venv venv
```
- install panda and psycopg2 in your python virtual environment
```pip
    pip install panda
    pip install psycopg2
```
##### Database configuration
Open settings.py and update the following settings
```Postgresql
    host = '127.0.0.1'
    username = 'postgres'
    password = 'postgres'
    db_name = 'sparkifydb'
```
##### Description<br/>
|Item| Description|
|-----|-----------|
|host|database host IP|
|username|postgresql username|
|password|postgresql password|
|db_name|postgresql database name|

##### Running the application
```python
python main.py
```
NB running this from your python virtual environment