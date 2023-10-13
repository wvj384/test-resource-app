import json

def application(environ, start_response):
    try:
        return handle_request(environ, start_response)
    except:
        # environ['wsgi.errors'].write(traceback.format_exc())
        status = '500 Internal Server Error'
        # data = uncaught_exception_data
        start_response('500 Internal Server Error', [('Content-Type','application/json')])
        return []

def handle_request(environ, start_response):
    print(environ)
    request_method = environ['REQUEST_METHOD']
    match request_method:
        case 'GET':
            return get_item(environ, start_response)
        case 'POST':
            return update_item(environ, start_response)
        case _:
            start_response('404 Not Found', [('Content-Type','application/json')])
            return []

def get_item(environ, start_response):
    request_uri = environ['REQUEST_URI']
    match request_uri:
        case '/resources':
            return get_resources(environ, start_response)
        case '/types':
            return get_types(environ, start_response)
        case _:
            start_response('404 Not Found', [('Content-Type','application/json')])
            return []
    
def update_item(environ, start_response):
    request_uri = environ['REQUEST_URI']
    match request_uri:
        case '/resources':
            return update_resources(environ, start_response)
        case '/types':
            return update_types(environ, start_response)
        case _:
            start_response('404 Not Found', [('Content-Type','application/json')])
            return []

def get_resources(environ, start_response):
    start_response('200 OK', [('Content-Type','application/json')])
    return [json.dumps(['foo', {'bar': ('get_resources', None, 1.0, 2)}]).encode('utf8')]

def get_types(environ, start_response):
    start_response('200 OK', [('Content-Type','application/json')])
    return [json.dumps(['foo', {'bar': ('get_types', None, 1.0, 2)}]).encode('utf8')]

def update_resources(environ, start_response):
    start_response('200 OK', [('Content-Type','application/json')])
    return [json.dumps(['foo', {'bar': ('update_resources', None, 1.0, 2)}]).encode('utf8')]

def update_types(environ, start_response):
    start_response('200 OK', [('Content-Type','application/json')])
    return [json.dumps(['foo', {'bar': ('update_types', None, 1.0, 2)}]).encode('utf8')]


# {'REQUEST_METHOD': 'GET', 'REQUEST_URI': '/resources', 'PATH_INFO': '/resources', 'QUERY_STRING': '', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SCRIPT_NAME': '', 
# 'SERVER_NAME': 'spb-nb-veselov', 'SERVER_PORT': '3031', 'REMOTE_ADDR': '127.0.0.1', 'HTTP_HOST': '127.0.0.1:3031', 'HTTP_USER_AGENT': 'curl/7.81.0', 
# 'HTTP_ACCEPT': 'application/json', 'wsgi.input': <uwsgi._Input object at 0x7f968e3ffe90>, 'wsgi.file_wrapper': <built-in function uwsgi_sendfile>, 
# 'wsgi.version': (1, 0), 'wsgi.errors': <_io.TextIOWrapper name=2 mode='w' encoding='UTF-8'>, 'wsgi.run_once': False, 'wsgi.multithread': False, 
# 'wsgi.multiprocess': False, 'wsgi.url_scheme': 'http', 'uwsgi.version': b'2.0.22', 'uwsgi.node': b'spb-nb-veselov'}

# {'REQUEST_METHOD': 'GET', 'REQUEST_URI': '/types', 'PATH_INFO': '/types', 'QUERY_STRING': '', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SCRIPT_NAME': '', 
# 'SERVER_NAME': 'spb-nb-veselov', 'SERVER_PORT': '3031', 'REMOTE_ADDR': '127.0.0.1', 'HTTP_HOST': '127.0.0.1:3031', 'HTTP_USER_AGENT': 'curl/7.81.0', 
# 'HTTP_ACCEPT': 'application/json', 'wsgi.input': <uwsgi._Input object at 0x7f968e3ffe90>, 'wsgi.file_wrapper': <built-in function uwsgi_sendfile>, 
# 'wsgi.version': (1, 0), 'wsgi.errors': <_io.TextIOWrapper name=2 mode='w' encoding='UTF-8'>, 'wsgi.run_once': False, 'wsgi.multithread': False, 
# 'wsgi.multiprocess': False, 'wsgi.url_scheme': 'http', 'uwsgi.version': b'2.0.22', 'uwsgi.node': b'spb-nb-veselov'}