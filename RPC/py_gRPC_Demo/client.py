
import grpc
import data_pb2, data_pb2_grpc

HOST = 'localhost'
PORT = '8888'

def run():
    conn = grpc.insecure_channel(HOST + ':' + PORT)
    client = data_pb2_grpc.AddNumberStub(channel=conn)
    response = client.do_add(data_pb2.data(text='3'))
    print("received: " + response.text)

if __name__ == '__main__':
    run()