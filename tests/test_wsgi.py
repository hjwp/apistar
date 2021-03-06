from apistar import App, Route
from apistar import http, wsgi
from apistar.test import TestClient


def get_wsgi_environ(environ: wsgi.WSGIEnviron) -> http.Response:
    return http.Response({
        'environ': environ
    })


def get_wsgi_response() -> wsgi.WSGIResponse:
    return wsgi.WSGIResponse(
        '200 OK',
        [('Content-Type', 'application/json')],
        [b'{"hello": "world"}']
    )


app = App(routes=[
    Route('/wsgi_environ/', 'get', get_wsgi_environ),
    Route('/wsgi_response/', 'get', get_wsgi_response),
])


client = TestClient(app)


def test_wsgi_environ():
    response = client.get('http://example.com/wsgi_environ/')
    assert response.json() == {'environ': {
        'HTTP_ACCEPT': '*/*',
        'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
        'HTTP_CONNECTION': 'keep-alive',
        'HTTP_HOST': 'example.com',
        'HTTP_USER_AGENT': 'requests_client',
        'PATH_INFO': '/wsgi_environ/',
        'QUERY_STRING': '',
        'REQUEST_METHOD': 'GET',
        'SCRIPT_NAME': '',
        'wsgi.url_scheme': 'http',
    }}


def test_wsgi_response():
    response = client.get('http://example.com/wsgi_response/')
    assert response.json() == {'hello': 'world'}
