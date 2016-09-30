from __future__ import print_function

import grpc

import hello_pb2

import tornado.ioloop
import tornado.web
from tornado import gen
import json


def run(name):
  channel = grpc.insecure_channel('localhost:8000')
  stub = hello_pb2.GreeterStub(channel)
  response = stub.SayHello(hello_pb2.HelloRequest(name=name))
  return "Greeter client received: " + response.message

class AsynGrpcHnalder(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        json_args = json.loads(self.request.body)
        resp = run(name=json_args['name'])
        self.write(resp)

app = tornado.web.Application([
    (r"/", AsynGrpcHnalder),
    ])

if __name__ == '__main__':
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
