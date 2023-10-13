from web.web_handler import handle_request

def application(environ, start_response):
    try:
        return handle_request(environ, start_response)
    except:
        # environ['wsgi.errors'].write(traceback.format_exc())
        status = '500 Internal Server Error'
        # data = uncaught_exception_data
        start_response('500 Internal Server Error', [('Content-Type','application/json')])
        return []
