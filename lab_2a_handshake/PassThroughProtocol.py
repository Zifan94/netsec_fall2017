from playground.network.packet import PacketType
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
from MyPacket import *
from VerificationCodeServerProtocol import *
from VerificationCodeClientProtocol import *
import playground

class PassThroughProtocol1(StackingProtocol):
	def __init__(self):
		print("[Pass Through Protocol]: Init Compelete...")
		super().__init__
		self.transport = None

	def connection_made(self, transport):
		print("[Pass Through Protocol]: Connection Made...")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)

	def connection_lost(self, exc=None):
		self.higherProtocol().connection_lost()
		self.transport = None
		print("[Pass Through Protocol]: Connection Lost...")

	def data_received(self, data):
		print("[Pass Through Protocol]: data received...")
		self.higherProtocol().data_received(data)
		if self.higherProtocol().state == "close_state" or self.higherProtocol().state == "finish_state":
			self.transport.close()
