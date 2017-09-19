from playground.network.packet import PacketType
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
from MyPacket import *
from VerificationCodeServerProtocol import *
from VerificationCodeClientProtocol import *
import playground

# Pass Through Server
class PassThroughProtocol1(StackingProtocol):
	def __init__(self):
		print("[Pass Through 1]: Init Compelete...")
		super().__init__
		self.transport = None

	def connection_made(self, transport):
		print("[Pass Through 1]: Connection Made...")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)

	def connection_lost(self, exc=None):
		# print("[Pass Through 1]: Connection Losting...")
		self.higherProtocol().connection_lost()
		self.transport = None
		print("[Pass Through 1]: Connection Lost...")

	def data_received(self, data):
		#print("[Pass Through 1]: data received...%s"%data)
		print("[Pass Through 1]: data received...")
		self.higherProtocol().data_received(data)
		if self.higherProtocol().state == "close_state" or self.higherProtocol().state == "finish_state":
			self.transport.close()

# Pass Through Client
class PassThroughProtocol2(StackingProtocol):
	def __init__(self):
		print("[Pass Through 2]: Init Compelete...")
		super().__init__
		self.transport = None

	def connection_made(self, transport):
		print("[Pass Through 2]: Connection Made...")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)

	def connection_lost(self, exc=None):
		# print("[Pass Through 2]: Connection Losting...")
		self.higherProtocol().connection_lost()
		self.transport = None
		print("[Pass Through 2]: Connection Lost...")

	def data_received(self, data):
		# print("[Pass Through 2]: data received...%s"%data)
		print("[Pass Through 2]: data received...")
		self.higherProtocol().data_received(data)
		if self.higherProtocol().state == "close_state" or self.higherProtocol().state == "finish_state":
			self.transport.close()




f = StackingProtocolFactory(lambda: PassThroughProtocol1(), lambda: PassThroughProtocol2())
ptConnector = playground.Connector(protocolStack=f)
playground.setConnector("passthrough", ptConnector)
print("----- NEW CONNECTOR passthrough SETUP -----")