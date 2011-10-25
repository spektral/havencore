
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Helloer(DatagramProtocol):

    def startProtocol(self):
        host = "192.168.255.247"
        port = 60000

        self.transport.connect(host, port)
        print "Connected"
        self.transport.write("helo")

    def datagramReceived(self, data, (host,port)):
        print "Received %r from %s:%d" % (data, host, port)

    def connectionRefused(self):
        print "No connection!"


reactor.listenUDP(0, Helloer())
reactor.run()
