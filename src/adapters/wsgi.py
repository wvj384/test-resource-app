from domain.resource_handler import ResourceHandler
from urllib.parse import parse_qs
import json

HTTP_STATUS_OK = '200 OK'
HTTP_STATUS_BAD_REQUEST = '400 Bad Request'
HTTP_STATUS_NOT_FOUND = '404 Not Found'
HTTP_STATUS_INTERNAL_ERROR = '500 Internal Server Error'

class HttpRequest:
    method: str = None
    req_type: str = None
    params: dict = {}
    body: dict = {}

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.req_type = get_type(environ['PATH_INFO'])
        self.params = parse_qs(environ['QUERY_STRING'])
        if environ.get('CONTENT_TYPE', None) == 'application/json':
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
            except:
                content_length = 0
            body = environ['wsgi.input'].read(content_length)
            self.body = json.loads(body)
    def __repr__(self):
        return f"<method:{self.method} uri:{self.req_type} params:{self.params} body:{self.body}>"

class HttpResponse:
    body: list[dict] | dict = None
    status: str = None

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
            print(response.body)
            if response.body is not None:
                return [json.dumps(response.body).encode('utf8')]
            else:
                return []
        except Exception as e:
            print(e)
            start_response(HTTP_STATUS_INTERNAL_ERROR, [('Content-Type','application/json')])
            return []

    def handle_request(self, request):
        response = HttpResponse()
        if request.req_type is None:
            response.status=HTTP_STATUS_NOT_FOUND
        else:
            match request.method:
                case 'GET':
                    return self.get_items(request, response)
                case 'POST':
                    return self.create_item(request, response)
                case 'DELETE':
                    return self.delete_item(request, response)
                case _:
                    response.status=HTTP_STATUS_NOT_FOUND
        return response

    def get_items(self, request, response):
        try:
            ids = [int(id) for id in request.params.get('id', [])]
            method_name = 'get_' + request.req_type
            func = getattr(self.handler, method_name)
            items = func({'ids': ids})
            response.status = HTTP_STATUS_OK
            response.body = items
            return response
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            return response
    
    def create_item(self, request, response):
        method_name = 'create_' + request.req_type
        func = getattr(self.handler, method_name)
        item = func(request.body)
        response.status = HTTP_STATUS_OK
        response.body = item
        return response
    
    def delete_item(self, request, response):
        method_name = 'delete_' + request.req_type
        func = getattr(self.handler, method_name)
        func(request.params)
        response.status = HTTP_STATUS_OK
        return response
    
def get_type(path):
    req_type = None
    match path:
        case '/api/v1/resources':
            req_type = 'resource'
        case '/api/v1/types':
            req_type = 'type'
    return req_type