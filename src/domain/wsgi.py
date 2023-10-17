import json
from domain.errors import ResourceHandlerError, INVALID_ID_ERROR
from domain.resource_handler import ResourceHandler
from urllib.parse import parse_qs


HTTP_STATUS_OK = "200 OK"
HTTP_STATUS_BAD_REQUEST = "400 Bad Request"
HTTP_STATUS_NOT_FOUND = "404 Not Found"
HTTP_STATUS_INTERNAL_ERROR = "500 Internal Server Error"

USER_ERROR_INVALID_ID = "invalid id in qs"


class HttpRequest:
    method: str
    path: str
    params: dict = {}
    body: dict = {}

    def __init__(self, environ):
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.params = parse_qs(environ["QUERY_STRING"])
        if environ.get("CONTENT_TYPE", None) == "application/json":
            try:
                content_length = int(environ.get("CONTENT_LENGTH", 0))
            except:
                content_length = 0
            body = environ["wsgi.input"].read(content_length)
            self.body = json.loads(body)

    def __repr__(self):
        return f"<method:{self.method} path:{self.path} params:{self.params} body:{self.body}>"


class HttpResponse:
    body: list[dict] | dict | None = None
    status: str | None = None

    def __repr__(self):
        return f"<body:{self.body} status:{self.status}>"


class WsgiApp:
    handler: ResourceHandler

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, environ, start_response):
        try:
            request = HttpRequest(environ)
            print(f"request {request}")
            response = self.handle_request(request)
            start_response(response.status, [("Content-Type", "application/json")])
            print(f"response {response}")
            if response.body is not None:
                return [json.dumps(response.body).encode("utf8")]
            else:
                return []
        except Exception as e:
            print(e)
            start_response(
                HTTP_STATUS_INTERNAL_ERROR, [("Content-Type", "application/json")]
            )
            return []

    def handle_request(self, request):
        response = HttpResponse()
        match request.method, request.path:
            # Types
            case "POST", "/api/v1/types":
                return self.create_type(request, response)
            case "PUT", "/api/v1/types":
                return self.update_type(request, response)
            case "GET", "/api/v1/types":
                return self.get_types(request, response)
            case "DELETE", "/api/v1/types":
                return self.delete_types(request, response)
            # Resources
            case "POST", "/api/v1/resources":
                return self.create_resource(request, response)
            case "PUT", "/api/v1/resources":
                return self.update_resource(request, response)
            case "GET", "/api/v1/resources":
                return self.get_resources(request, response)
            case "DELETE", "/api/v1/resources":
                return self.delete_resources(request, response)
            case _:
                response.status = HTTP_STATUS_NOT_FOUND
        return response

    # Types

    def create_type(self, request, response):
        try:
            item = self.handler.create_type(request.body)
            response.status = HTTP_STATUS_OK
            response.body = item
            return response
        except ResourceHandlerError as e:
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    def update_type(self, request, response):
        try:
            id = request.params.get("id", None)
            if request.params.get("id", None) is None:
                response.status = HTTP_STATUS_BAD_REQUEST
                response.body = get_user_error(USER_ERROR_INVALID_ID)
                return response
            item = self.handler.update_type(id[0], request.body)
            response.status = HTTP_STATUS_OK
            response.body = item
            return response
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            response.body = get_user_error(USER_ERROR_INVALID_ID)
        except ResourceHandlerError as e:
            print(e)
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    def get_types(self, request, response):
        try:
            ids = [int(id) for id in request.params.get("id", [])]
            items = self.handler.get_types(ids)
            response.status = HTTP_STATUS_OK
            response.body = items
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            response.body = get_user_error(USER_ERROR_INVALID_ID)
        except ResourceHandlerError as e:
            print(e)
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    def delete_types(self, request, response):
        try:
            ids = [int(id) for id in request.params.get("id", [])]
            if len(ids) == 0:
                response.status = HTTP_STATUS_BAD_REQUEST
                response.body = get_user_error(USER_ERROR_INVALID_ID)
                return response
            items = self.handler.delete_types(ids)
            response.status = HTTP_STATUS_OK
            response.body = items
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            response.body = get_user_error(USER_ERROR_INVALID_ID)
        except ResourceHandlerError as e:
            print(e)
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    # Resources

    def create_resource(self, request, response):
        try:
            item = self.handler.create_resource(request.body)
            response.status = HTTP_STATUS_OK
            response.body = item
            return response
        except ResourceHandlerError as e:
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    def update_resource(self, request, response):
        try:
            id = request.params.get("id", None)
            if request.params.get("id", None) is None:
                response.status = HTTP_STATUS_BAD_REQUEST
                response.body = get_user_error(USER_ERROR_INVALID_ID)
                return response
            item = self.handler.update_resource(id[0], request.body)
            response.status = HTTP_STATUS_OK
            response.body = item
            return response
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            response.body = get_user_error(USER_ERROR_INVALID_ID)
        except ResourceHandlerError as e:
            print(e)
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    def get_resources(self, request, response):
        try:
            type_ids = [int(id) for id in request.params.get("type_id", [])]
            ids = [int(id) for id in request.params.get("id", [])]
            items = self.handler.get_resources(ids, type_ids)
            response.status = HTTP_STATUS_OK
            response.body = items
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            response.body = get_user_error(USER_ERROR_INVALID_ID)
        except ResourceHandlerError as e:
            print(e)
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    def delete_resources(self, request, response):
        try:
            ids = [int(id) for id in request.params.get("id", [])]
            if len(ids) == 0:
                response.status = HTTP_STATUS_BAD_REQUEST
                response.body = get_user_error(USER_ERROR_INVALID_ID)
                return response
            items = self.handler.delete_resources(ids)
            response.status = HTTP_STATUS_OK
            response.body = items
        except ValueError as e:
            print(e)
            response.status = HTTP_STATUS_BAD_REQUEST
            response.body = get_user_error(USER_ERROR_INVALID_ID)
        except ResourceHandlerError as e:
            print(e)
            response.status = HTTP_STATUS_INTERNAL_ERROR
            response.body = get_user_error(e)
        return response

    # Utils


def get_user_error(e):
    return {"error": str(e)}
