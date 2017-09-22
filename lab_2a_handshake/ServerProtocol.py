from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from HandShake import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

import random

import asyncio

class ServerProtocol(asyncio.Protocol):
	state = "wait_for_HandShake_SYN"
	def __init__(self, loop):
		if __name__ =="__main__":
			print("Server Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		self.transport = None
		self.state = "wait_for_HandShake_SYN"

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
				# check checksum here, if checksum is incorrected, set "checksum_fail_state"
				if packet.Type == 1:	# incoming an SYN-ACK handshake packet
					if self.state != "wait_for_HandShake_SYN":
						if __name__ =="__main__":
							print("Server Side: Error: State Error! Expecting wait_for_HandShake_SYN but getting %s"%self.state)
						self.state = "error_state"
					else:
						outBoundPacket = HandShake()
						outBoundPacket.Type = 2
						outBoundPacket.SequenceNumber = random.randint(0, 2147483646/2)
						outBoundPacket.Checksum = 1
						outBoundPacket.Acknowledgement = packet.SequenceNumber+1
						outBoundPacket.HLEN = 96
						if __name__ =="__main__":
							print("Server Side: SYN reveived: Seq = %d, Ack = %d"%(packet.SequenceNumber,packet.Acknowledgement))
							print("Server Side: SYN-ACK sent: Seq = %d, Ack = %d"%(outBoundPacket.SequenceNumber, outBoundPacket.Acknowledgement))
						packetBytes = outBoundPacket.__serialize__()
						self.state = "wait_for_HandShake_ACK"
						self.transport.write(packetBytes)

				elif packet.Type == 3:	# incoming an ACK handshake packet
					if self.state != "wait_for_HandShake_ACK":
						if __name__ =="__main__":
							print("Server Side: Error: State Error! Expecting wait_for_HandShake_ACK but getting %s"%self.state)
						self.state = "error_state"
					else:
						if __name__ =="__main__":
							print("Server Side: ACK reveived")
							print("Server Side: CONNECTION ESTABLISHED!")
			
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