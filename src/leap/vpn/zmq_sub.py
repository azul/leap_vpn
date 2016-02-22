import zmq

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt_string(zmq.SUBSCRIBE, u'')  # get everything

print "Getting updates from server..."
# get updates forever, quit with Ctrl+C
while True:
    data = socket.recv_string()
    print data
