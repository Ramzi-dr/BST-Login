from app import app
from gevent.pywsgi import WSGIServer
if __name__ == '__main__':
    #app.run(debug=True, port=80, host='0.0.0.0')
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
