# hdruk-api-test

## Introduction

* This service (API endpoint) returns paginated results with options for:
   * `total` - the total number of results to show (default 25)
   * `page` - the page number of the results (default 1)
   * `omit` - comma seperated list of fields to exclude from the returned list (
* Tried and tested using Python3.8
* Main code is in `app/main.py`
* Code tests are in `app/tests.py`
* Github CI for checking pylint and running the code tests is in `.github/workflows/ci.yml`
   * Github action is generated to test these two stages in python 3.8 for each push
* Additional docker file is found in `Dockerfile`
* Additional in

## Installing 

Clone the repo:
```
git clone https://github.com/calmacx/hdruk-api-test.git
cd hdruk-api-test
```

Setup a virtual environment, personally I use `pyenv`:
```
pyenv local 3.8.0
python -m venv .
source bin/activate
```

Install requirements
```
python -m pip install pip --upgrade
python -m pip install -r requirements.txt
```

## Start the App 

```
uvicorn app.main:app --reload
```

## Examples

### Command Line 

```
curl -X 'GET' \
  'http://127.0.0.1:8000/pages/?page=2&total=25&omit=body' \
  -H 'accept: application/json'
```

### Python Requests
```
>> import requests
>> requests.get('http://127.0.0.1:8000/pages/?page=2&total=2&omit=body').json()
[{'postId': 1, 'id': 3, 'name': 'odio adipisci rerum aut animi', 'email': 'Nikita@garfield.biz'}, {'postId': 1, 'id': 4, 'name': 'alias odio sit', 'email': 'Lew@alysha.tv'}]
```

### Docs

Nativate to the automatically generated [docs](http://127.0.0.1:8000/docs)

You will be able to see how to manually test and play with the API via Swagger

![image](https://user-images.githubusercontent.com/69473770/226174312-29f62971-87df-4ae5-91ee-12d0daebaedf.png)


