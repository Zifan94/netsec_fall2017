from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from PEEPPacket import *
from Util import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

import random

import asyncio

class ServerProtocol(StackingProtocol):
	state = "SYN_ACK_State_0"
	def __init__(self, loop):
		print("PEEP Server Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		super().__init__
		self.transport = None
		self.state = "SYN_ACK_State_0"

	def connection_made(self, transport):
		print("PEEP Server Side: Connection Made...")
		self.transport = transport

	def connection_lost(self, exc=None):
		self.transport = None
		print("PEEP Server Side: Connection Lost...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			print()
			if self.transport == None:
				continue

			#Do checksum verification first!
			if (Util.hasValidChecksum(packet) == 0): 
				print("PEEP Server side: checksum is bad")
				self.state = "error_state"
			else: # checksum is good, now we look into the packet
				print("PEEP Server side: checksum is good")
				
				if packet.Type == 0:	# incoming an SYN handshake packet
					if self.state != "SYN_ACK_State_0":
						print("PEEP Server Side: Error: State Error! Expecting SYN_ACK_State but getting %s"%self.state)
						self.state = "error_state"
					else:
						outBoundPacket = Util.create_outbound_packet(1, random.randint(0, 2147483646/2), packet.SequenceNumber+1)

						print("PEEP Server Side: SYN reveived: Seq = %d"%(packet.SequenceNumber))
						print("PEEP Server Side: SYN-ACK sent: Seq = %d, Ack = %d"%(outBoundPacket.SequenceNumber, outBoundPacket.Acknowledgement))
						packetBytes = outBoundPacket.__serialize__()
						self.state = "SYN_State_1"
						self.transport.write(packetBytes)

				elif packet.Type == 2:	# incoming an ACK handshake packet
					if self.state != "SYN_State_1":
						print("PEEP Server Side: Error: State Error! Expecting SYN_State but getting %s"%self.state)
						self.state = "error_state"
					else:

						print("PEEP Server Side: ACK reveived: Seq = %d, Ack = %d"%(packet.SequenceNumber,packet.Acknowledgement))
						print("PEEP Server Side: CONNECTION ESTABLISHED!")
						self.state = "Transmission_State_2"
						
						print("PEEP Server Side: ### THREE-WAY HANDSHAKE established ###")
						print()
						higherTransport = StackingTransport(self.transport)
						self.higherProtocol().connection_made(higherTransport)

			if self.transport == None:
				continue
			if self.state == "error_state":
				self.transport.close()
				self.loop.stop()




# if __name__ =="__main__":
# 	loop = asyncio.get_event_loop()
# 	coro = playground.getConnector().create_playground_server(lambda: ServerProtocol(loop), 101)
# 	server = loop.run_until_complete(coro)
# 	try:
# 		loop.run_forever()
# 	except KeyboardInterrupt:
# 		pass

# 	loop.close()
