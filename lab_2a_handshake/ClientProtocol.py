from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from PEEPPacket import *
from Util import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

import random

import asyncio

class ClientProtocol(StackingProtocol):
	state = "Initial_SYN_State_0"
	def __init__(self, loop):
		print("PEEP Client Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		super().__init__
		self.transport = None
		self.state = "Initial_SYN_State_0"

	def connection_made(self, transport):
		print("PEEP Client Side: Connection Made...")
		self.transport = transport
		self.send_request_packet()

	def send_request_packet(self, callback=None):
		#print("Client: %s"%self.state)
		if self.state != "Initial_SYN_State_0":
			print("PEEP Client Side: Error: State Error! Expecting Initial_SYN_State but getting %s"%self.state)
			self.state = "error_state"
			self.transport.close()
			self.loop.stop()
		else:
			self._callback = callback
			outBoundPacket = Util.create_outbound_packet(0, random.randint(0, 2147483646/2))
			print("PEEP Client Side: SYN sent: Seq = %d"%(outBoundPacket.SequenceNumber))
			packetBytes = outBoundPacket.__serialize__()
			self.state = "SYN_ACK_State_1"
			self.transport.write(packetBytes)

	def connection_lost(self, exc=None):
		self.transport = None
		print("PEEP Client Side: Connection Lost...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			print()
			if self.transport == None:
				continue

			 #Do checksum verification first!
			if (Util.hasValidChecksum(packet) == 0):
				print("PEEP Client side: checksum is bad")
				self.state = "error_state"
			else:  # checksum is good, now we look into the packet
				print("PEEP Client side: checksum is good")
				
				if packet.Type == 1:	# incoming an SYN-ACK handshake packet
					if self.state != "SYN_ACK_State_1":
						if __name__ =="__main__":
							print("PEEP Client Side: Error: State Error! Expecting SYN_ACK_State but getting %s"%self.state)
						self.state = "error_state"
					else:
						outBoundPacket = Util.create_outbound_packet(2, packet.Acknowledgement+1, packet.SequenceNumber+1)

						if __name__ =="__main__":
							print("PEEP Client Side: SYN-ACK reveived: Seq = %d, Ack = %d"%(packet.SequenceNumber,packet.Acknowledgement))
							print("PEEP Client Side: ACK sent: Seq = %d, Ack = %d"%(outBoundPacket.SequenceNumber, outBoundPacket.Acknowledgement))
						packetBytes = outBoundPacket.__serialize__()
						self.state = "Transmission_State_2"
						self.transport.write(packetBytes)

						print("PEEP Client Side: ### THREE-WAY HANDSHAKE established ###")
						print()
						higherTransport = StackingTransport(self.transport)
						self.higherProtocol().connection_made(higherTransport)
				else:
					print("PEEP Client Side: Error: Unrecognize HandShake Type received!")
					self.state = "error_state"

			if self.transport == None:
				continue
			if self.state == "error_state":
				self.transport.close()
				self.loop.stop()






	def callbackForUserVCInput(self):
		answer = input("Client Side: Please input the verification code: ")
		return answer

# if __name__ =="__main__":
# 	loop = asyncio.get_event_loop()
# 	coro = playground.getConnector().create_playground_connection(lambda: ClientProtocol(loop), "20174.1.1.1", 101)
# 	transport, protocol = loop.run_until_complete(coro)
# 	protocol.send_request_packet()
# 	loop.run_forever()
# 	loop.close()
