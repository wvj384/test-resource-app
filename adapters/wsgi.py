from domain.resource_handler import ResourceHandler
import json

class HttpRequest:
    method: str = ''
    uri: str = ''
    qs_params: dict = {}
    body: dict = {}

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.uri = environ['REQUEST_URI']

    def __repr__(self):
        return f"<method:{self.method} uri:{self.uri}>"

class HttpResponse:
    body: dict = None
    status: str = ''

    def __repr__(self):
        return f"<body:{self.body} status:{self.status}>"

class WsgiApp:
    handler: ResourceHandler

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, environ, start_response):
        try:
            print(environ)
            request = HttpRequest(environ)
            response = self.handle_request(request)
            print(json.dumps(response.body).encode('utf8'))
            start_response(response.status, [('Content-Type','application/json')])
            if response.body is not None:
                return [json.dumps(response.body).encode('utf8')]
            else:
                return []
        except:
            start_response('500 Internal Server Error', [])
            return []

    def handle_request(self, request):
        response = HttpResponse()
        match request.method:
            case 'GET':
                return self.get_item(request, response)
            case 'POST':
                return self.update_item(request, response)
            case 'POST':
                return self.delete_item(request, response)
            case _:
                response.status='404 Not Found'
                return response

    def get_item(self, request, response):
        match request.uri:
            case '/resources':
                resource = self.handler.get_resource('idhere')
                response.status = '200 OK'
                response.body = resource
            case '/types':
                type = self.handler.get_type('idhere')
                response.status = '200 OK'
                response.body = type
            case _:
                response.status='404 Not Found'
        return response
        
    def update_item(self, request, response):
        match request.uri:
            case '/resources':
                self.handler.update_resource('idhere', {})
                response.status = '200 OK'
            case '/types':
                self.handler.update_type('idhere', {})
                response.status = '200 OK'
            case _:
                response.status='404 Not Found'
        return response
    
    def delete_item(self, request, response):
        match request.uri:
            case '/resources':
                self.handler.delete_resource('idhere', {})
                response.status = '200 OK'
            case '/types':
                self.handler.delete_type('idhere', {})
                response.status = '200 OK'
            case _:
                response.status='404 Not Found'
        return response
