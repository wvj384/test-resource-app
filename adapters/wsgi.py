from domain.resource_handler import ResourceHandler
from urllib.parse import parse_qs
import json

FEDERAL_TAX_RATE = 0.10

class HttpRequest:
    method: str = ''
    req_type: str = ''
    params: dict = {}
    body: dict = {}

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.req_type = get_type(environ['PATH_INFO'])
        self.params = parse_qs(environ['QUERY_STRING'])
        if environ.get('CONTENT_TYPE', '') == 'application/json':
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
            except:
                content_length = 0
            body = environ['wsgi.input'].read(content_length)
            self.body = json.loads(body)
    def __repr__(self):
        return f"<method:{self.method} uri:{self.req_type} params:{self.params} body:{self.body}>"

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
            request = HttpRequest(environ)
            print(request)
            response = self.handle_request(request)
            start_response(response.status, [('Content-Type','application/json')])
            if response.body is not None:
                return [json.dumps(response.body).encode('utf8')]
            else:
                return []
        except Exception as e:
            print(e)
            start_response('500 Internal Server Error', [('Content-Type','application/json')])
            return []

    def handle_request(self, request):
        response = HttpResponse()
        if request.req_type == '':
            response.status='404 Not Found'
        else:
            match request.method:
                case 'GET':
                    return self.get_item(request, response)
                case 'POST':
                    return self.update_item(request, response)
                case 'DELETE':
                    return self.delete_item(request, response)
                case _:
                    response.status='404 Not Found'
        return response

    def get_item(self, request, response):
        method_name = 'get_' + request.req_type
        func = getattr(self.handler, method_name)
        resource = func(request.params)
        response.status = '200 OK'
        response.body = resource
        return response
    
    def update_item(self, request, response):
        method_name = 'update_' + request.req_type
        func = getattr(self.handler, method_name)
        func(request.params, request.body)
        response.status = '200 OK'
        return response
    
    def delete_item(self, request, response):
        method_name = 'delete_' + request.req_type
        func = getattr(self.handler, method_name)
        func(request.params)
        response.status = '200 OK'
        return response
    
def get_type(path):
    req_type = ''
    match path:
        case '/api/v1/resources':
            req_type = 'resource'
        case '/api/v1/types':
            req_type = 'type'
    return req_type