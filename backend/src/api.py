from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")

# http://localhost:8000/api/hello
def hello(request):
	return "Hello world!"