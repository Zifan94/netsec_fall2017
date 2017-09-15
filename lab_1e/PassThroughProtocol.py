from playground.network.packet import PacketType
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
from MyPacket import *
from VerificationCodeServerProtocol import *
from VerificationCodeClientProtocol import *
import playground

# Pass Through Server
class PassThroughServerProtocol(StackingProtocol):
	def __init__(self):
		print("[Server Pass Through]: Init Compelete...")
		super().__init__
		self.transport = None

	def connection_made(self, transport):
		print("[Server Pass Through]: Connection Made...")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)

	def connection_lost(self, exc=None):
		# print("[Server Pass Throught]: Connection Losting...")
		self.higherProtocol().connection_lost()
		self.transport = None
		print("[Server Pass Throught]: Connection Lost...")

	def data_received(self, data):
		#print("[Server Pass Through]: data received...%s"%data)
		print("[Server Pass Through]: data received...")
		self.higherProtocol().data_received(data)
		if self.higherProtocol().state == "close_state":
			self.transport.close()

# Pass Through Client
class PassThroughClientProtocol(StackingProtocol):
	def __init__(self):
		print("[Client Pass Through]: Init Compelete...")
		super().__init__
		self.transport = None

	def connection_made(self, transport):
		print("[Client Pass Through]: Connection Made...")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)

	def connection_lost(self, exc=None):
		# print("[Client Pass Through]: Connection Losting...")
		self.higherProtocol().connection_lost()
		self.transport = None
		print("[Client Pass Through]: Connection Lost...")

	def data_received(self, data):
		# print("[Client Pass Through]: data received...%s"%data)
		print("[Client Pass Through]: data received...")
		self.higherProtocol().data_received(data)
		if self.higherProtocol().state == "finish_state":
			self.transport.close()




f = StackingProtocolFactory(lambda: PassThroughServerProtocol(), lambda: PassThroughClientProtocol())
ptConnector = playground.Connector(protocolStack=f)
playground.setConnector("passthrough", ptConnector)
print("----- NEW CONNECTOR passthrough SETUP -----")