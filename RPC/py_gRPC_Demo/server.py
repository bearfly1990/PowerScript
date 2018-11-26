import grpc
import time
import data_pb2, data_pb2_grpc
from concurrent import futures
# from demo import data_pb2, data_pb2_grpc

ONE_DAY_IN_SECONDS = 3600 * 24
HOST = 'localhost'
PORT = '8888'

class AddNumber(data_pb2_grpc.AddNumberServicer):
    def do_add(self, request, context):
        txt = request.text
        txt = str(int(txt) + 1)
        return data_pb2.data(text = txt)

def start_server():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    data_pb2_grpc.add_AddNumberServicer_to_server(AddNumber(), grpcServer)
    grpcServer.add_insecure_port(HOST + ':' + PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    start_server()




