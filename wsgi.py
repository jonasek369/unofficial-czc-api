from app import app as application
from Logger import *
import time
import cherrypy

LOG(INFO, "Starting test server")
time.sleep(0.5)

if __name__ == '__main__':
    cherrypy.tree.graft(application, "/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "localhost"
    server.socket_port = 5000
    server.thread_pool = 30
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()