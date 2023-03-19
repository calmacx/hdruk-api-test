from fastapi import FastAPI,Query,HTTPException
from typing import List,Union
from pydantic import BaseModel
import requests

# Use pydantic for data classes as FastAPI is built on this
# - useful for return types and validation etc.
# - also using it because in a real world scenario
#   you could replace this with a proper database connection
#   such as SQLAlchemy or MongoEngine (im most famililar with this)
class Item(BaseModel):
    postId:int
    id:int
    name:str
    email:str
    body:str

# Setup our API client
# - using FastAPI because it's very simple to setup
# - I was going to use Flask/Django but I just want a basic API that comes with
#   automatic documentation and other nice features
app = FastAPI()

# Retrieve data: assuming the data is uniform (all have the same fields and data types)
# - I decided to cache this data into memory as its not that big
# - in a proper scenario this would be a connection to a DB
# - or could be a connection to an external API that could be refreshed
#   on each query or some sort of better caching
base_url = 'https://jsonplaceholder.typicode.com/comments'
data = [
	Item.parse_obj(x)
	for x in requests.get(base_url).json()
]

# Create an API endpoint
# - Fast API will handle a lot of the validation
# - e.g. if you try and pass a non-int to the total, it'll return a bad response
# Example:
#  - <url>/pages/?omit=name&total=25&page=5
@app.get("/pages/",response_model=Union[List[Item],List[dict]])
def get_(page: int = Query(gt=0,default=1,description='Page number to retrieve'),
		 total: int = Query(gt=0,default=25,description='Number of items to return for pagination'),
		 omit: str = Query(None,description='Comma seperated list of fields to omit in the return')):
	#filter the cached data on the page and number of enteries per page to return

	#note: we start indexing 'page' from 1
	retval = data[(page-1)*total:page*total]
	#check if there's any fields to omit
	if omit:
		# FastAPI seems setup to handle this stuff better if multiple parameters are passed individually
		# - e.g. omit=name&omit=blah
		# You can then setup with omit: List[str] = Query()
		# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
		# Perhaps there's a better way to do this without having to pass as comma seperated and manually validate
		# I couldn't see a good way quickly, so doing it this way...
		omit = set(omit.split(","))
		#compare omit values against allowed fields in the schema
		check = omit - set(Item.schema()['properties'])
		#if there are field(s) passed that are not in the schema, return a 404
		if check:
			raise HTTPException(status_code=404, detail=f"{check} not valid field(s) to omit")
		#otherwise exclude this set of fields for the return value
		retval = [x.dict(exclude=omit) for x in retval]
	#return the data
	return retval

@app.get("/")
def home():
	return "Hello HDRUK"
