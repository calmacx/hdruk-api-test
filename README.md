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
* Additional docker file is found in `Dockerfile` or can use a `docker-compose` wrapper
* Additional simple instructions for deploying to GCP app engine 

I chose to write this mini-api using [FastAPI](https://fastapi.tiangolo.com/) because I've used it once before and found it to be the most straight forward and __fast__ (in the sense of getting started) approach for a simple API. I'm more comfortable with Flask and a bit of Django for python based backends/APIs, though in the future I'd probably be more inclined to use FastAPI again and learn more about it.

On top of the fact that the automatically generated documentation (`<api_url>/docs`) is super useful, I used FastAPI to demonstrate how I would code a simple API up with the expectation that it'd likely have to be extended much further. It's a big open-source project that is maintained by lots of other people with a tonne of documentation, so it'd be easy for someone else working on the code to pick it up and extend it.

## Installing 

Clone the repo:
```
git clone https://github.com/calmacx/hdruk-api-test.git
cd hdruk-api-test
```

Setup a virtual environment (personally I use `pyenv`):
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

To start for development (and debateable might be production ready to use uvicorn - though I'm not 100% sure on best practices here)..
```
$ uvicorn app.main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/calummacdonald/HDRUK/hdruk-api-test']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [70939] using WatchFiles
INFO:     Started server process [70956]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Examples

Once running you can test the API end point at `http://127.0.0.1:8000/pages`

The acceptance criteria should work via queries, e.g. `<url>/pages/?page=2&total=25&omit=body,email`

### Command Line 

Use bash curl to get a response...
```
curl -X 'GET' \
  'http://127.0.0.1:8000/pages/?page=2&total=25&omit=body' \
  -H 'accept: application/json'
```

### Python Requests

Using python to get a response...
```
>> import requests
>> requests.get('http://127.0.0.1:8000/pages/?page=2&total=2&omit=body').json()
[{'postId': 1, 'id': 3, 'name': 'odio adipisci rerum aut animi', 'email': 'Nikita@garfield.biz'}, {'postId': 1, 'id': 4, 'name': 'alias odio sit', 'email': 'Lew@alysha.tv'}]
```

The API by default will be able to handle errors/bad inputs:
```
>>> requests.get('http://127.0.0.1:8000/pages/?page=2&total=2&omit=body,blah').json()  
{'detail': "{'blah'} not valid field(s) to omit"}

>>> requests.get('http://127.0.0.1:8000/pages/?page=-100&total=2&omit=body').json()  
{'detail': [{'loc': ['query', 'page'], 'msg': 'ensure this value is greater than 0', 'type': 'value_error.number.not_gt', 'ctx': {'limit_value': 0}}]}
```


### Docs

FastAPI automatically generated some documentation on how to use the API. Nativate to the automatically generated [docs at http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You will be able to see how to manually test and play with the API via Swagger

![image](https://user-images.githubusercontent.com/69473770/226174312-29f62971-87df-4ae5-91ee-12d0daebaedf.png)



## Deployment

If I was to be deploying this as a production ready service, it would have my GitHub actions/CI either build a docker image and deploy a container or use something like GCP app-engine (which I'm relatively famililar with). The later I find really straight forward for a simple project, but I've never used it for a big project or anything complex.

The project currently runs via:
```
uvicorn app.main:app --reload
```
which is probably not the best for production, more for development.

For production - using gunicorn could be better, or using uvicorn inside a docker container could be ok - I'm not 100% sure.

### Docker

A `Dockerfile` exists with a `docker-compose` yaml wrapper. I like using the latter more - just find it easier to manage images/containers, even if it's just a wrapper for one docker service. It's also good practice for when you might add extra services and build as a stack (e.g. add-in some frontend or proper db).
```
docker-compose up --build
```

### GCP App Engine

A basic configuration file for GCP can be found here: `gcp-api.yaml`, containing:
```yaml
runtime: python38
service: api
instance_class: F4
entrypoint: gunicorn --worker-class uvicorn.workers.UvicornWorker -b :$PORT --workers=1 app.main:app
```
I was able to practice a very very simple deployment to GCP app-engine by doing:
```
gcloud projects create --name hdruk
gcloud config set project hdruk-XXXXXX
gcloud app create
gcloud app deploy gcp-api.yaml
```
