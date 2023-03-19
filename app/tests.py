from fastapi.testclient import TestClient
#import our app
from .main import app

#create the test client
client = TestClient(app)

#test the dummy main response
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello HDRUK"

#test all
def test_pages_default():
    response = client.get("/pages")
    assert response.status_code == 200

#test omitting a single field
def test_pages_omit_single():
    response = client.get("/pages?omit=name")
    assert response.status_code == 200

#test omitting multiple fields
def test_pages_omit_multiple():
    response = client.get("/pages?omit=name,body,id")
    assert response.status_code == 200

#test that it failed with a 404 if the field is unknown
def test_pages_omit_fail():
    response = client.get("/pages?omit=blah")
    assert response.status_code == 404

#test changing the total per page
def test_pages_omit_total():
    response = client.get("/pages?total=2")
    assert response.status_code == 200

#test some bad total inputs (needs to be >=1 total)
def test_pages_total_fail():
    response = client.get("/pages?total=0")
    assert response.status_code == 422

#also needs to be an integer
def test_pages_total_fail_2():
    response = client.get("/pages?total=blah")
    assert response.status_code == 422

#test total and page number change together
def test_pages_total_and_page():
    response = client.get("/pages?total=2&page=2")
    assert response.status_code == 200

#test changing the total, page number and omitting fields at the same time
def test_pages_all():
    response = client.get("/pages?total=2&page=2&omit=email,id")
    assert response.status_code == 200

	
