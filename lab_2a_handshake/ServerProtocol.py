from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from PEEPPacket import *
from Util import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

import random

import asyncio

class ServerProtocol(asyncio.Protocol):
	state = "SYN_ACK_State"
	def __init__(self, loop):
		if __name__ =="__main__":
			print("Server Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		self.transport = None
		self.state = "SYN_ACK_State"

	def connection_made(self, transport):
		if __name__ =="__main__":
			print("Server Side: Connection Made...")
		self.transport = transport

	def connection_lost(self, exc=None):
		self.transport = None
		if __name__ =="__main__":
			print("Server Side: Connection Lost...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			if self.transport == None:
				continue
			if isinstance(packet, HandShake):
				print (packet.Acknowledgement)
				if packet.Acknowledgement == 0:
					checksum_bytes = Util.prepare_checksum_bytes(packet.Type, packet.SequenceNumber)
				else:
					checksum_bytes = Util.prepare_checksum_bytes(packet.Type, packet.SequenceNumber, packet.Acknowledgement)
				valid = Util.is_valid_checksum(checksum_bytes, packet.Checksum)
				if (valid == 0):
					outBoundPacket = Util.create_outbound_handshake_packet(5, random.randint(0, 2147483646/2), packet.SequenceNumber+1) # maybe a different sequence number
					self.state = "error_state"
					print("Checksum error, resetting connection")
					packetBytes = outBoundPacket.__serialize__()
					self.transport.write(packetBytes)
				else: print("server checksum good")
				if packet.Type == 0:	# incoming an SYN-ACK handshake packet
					if self.state != "SYN_ACK_State":
						if __name__ =="__main__":
							print("Server Side: Error: State Error! Expecting SYN_ACK_State but getting %s"%self.state)
						self.state = "error_state"
					else:
						outBoundPacket = Util.create_outbound_handshake_packet(1, random.randint(0, 2147483646/2), packet.SequenceNumber+1)
						checksum_bytes = Util.prepare_checksum_bytes(outBoundPacket.Type, outBoundPacket.SequenceNumber, outBoundPacket.Acknowledgement)
						checksum = Util.checksum(checksum_bytes)
						outBoundPacket.Checksum = checksum
						if __name__ =="__main__":
							print("Server Side: SYN reveived: Seq = %d, Ack = %d"%(packet.SequenceNumber,packet.Acknowledgement))
							print("Server Side: SYN-ACK sent: Seq = %d, Ack = %d"%(outBoundPacket.SequenceNumber, outBoundPacket.Acknowledgement))
						packetBytes = outBoundPacket.__serialize__()
						self.state = "SYN_State"
						self.transport.write(packetBytes)

				elif packet.Type == 2:	# incoming an ACK handshake packet
					if self.state != "SYN_State":
						if __name__ =="__main__":
							print("Server Side: Error: State Error! Expecting SYN_State but getting %s"%self.state)
						self.state = "error_state"
					else:

						if __name__ =="__main__":
							print("Server Side: ACK reveived: Seq = %d, Ack = %d"%(packet.SequenceNumber,packet.Acknowledgement))
							print("Server Side: CONNECTION ESTABLISHED!")
						self.state = "Tramsmission_State"

			else:
				if __name__ =="__main__":
					print("Server Side: Error: Unexpected data received!")
				self.state = "error_state"
			if self.transport == None:
				continue




if __name__ =="__main__":
	loop = asyncio.get_event_loop()
	#coro = loop.create_server(lambda: VerificationCodeServerProtocol(loop), port=8000)
	coro = playground.getConnector().create_playground_server(lambda: ServerProtocol(loop), 101)
	server = loop.run_until_complete(coro)
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass

	#server.close()
	#loop.run_until_complete(server.wait_closed())
	loop.close()
