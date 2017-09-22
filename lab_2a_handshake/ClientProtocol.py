from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from HandShake import *
from Util import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

import random

import asyncio

class ClientProtocol(asyncio.Protocol):
	state = "initial_state"
	def __init__(self, loop):
		if __name__ =="__main__":
			print("Client Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		self.transport = None
		self.state = "initial_state"

	def connection_made(self, transport):
		if __name__ =="__main__":
			print("Client Side: Connection Made...")
		self.transport = transport

	def send_request_packet(self, callback=None):
		#print("Client: %s"%self.state)
		if self.state != "initial_state":
			if __name__ =="__main__":
				print("Client Side: Error: State Error! Expecting initial_state but getting %s"%self.state)
			self.state = "error_state"
			self.transport.close()
			self.loop.stop()
		else:
			self._callback = callback
			outBoundPacket = Util.create_outbound_handshake_packet(1, random.randint(0, 2147483646/2), 0)
			if __name__ =="__main__":
				print("Client Side: SYN sent: Seq = %d, Ack = %d"%(outBoundPacket.SequenceNumber,outBoundPacket.Acknowledgement))
			packetBytes = outBoundPacket.__serialize__()
			self.state = "wait_for_HandShake_SYNACK"
			self.transport.write(packetBytes)

	def connection_lost(self, exc=None):
		self.transport = None
		if __name__ =="__main__":
			print("Client Side: Connection Lost...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			if self.transport == None:
				continue
			if isinstance(packet, HandShake):
				# check checksum here, if checksum is incorrected, set "checksum_fail_state"
				if packet.Type == 2:	# incoming an SYN-ACK handshake packet
					if self.state != "wait_for_HandShake_SYNACK":
						if __name__ =="__main__":
							print("Client Side: Error: State Error! Expecting wait_for_HandShake_SYNACK but getting %s"%self.state)
						self.state = "error_state"
					else:
						outBoundPacket = Util.create_outbound_handshake_packet(3, packet.Acknowledgement+1, packet.SequenceNumber+1)
						if __name__ =="__main__":
							print("Client Side: SYN-ACK reveived: Seq = %d, Ack = %d"%(packet.SequenceNumber,packet.Acknowledgement))
							print("Client Side: ACK sent: Seq = %d, Ack = %d"%(outBoundPacket.SequenceNumber, outBoundPacket.Acknowledgement))
						packetBytes = outBoundPacket.__serialize__()
						self.state = "wait_for_data"
						self.transport.write(packetBytes)
				else: 
					if __name__ =="__main__":
						print("Client Side: Error: Unrecognize HandShake Type received!")
					self.state = "error_state"
			
			else:
				if __name__ =="__main__":
					print("Client Side: Error: Unexpected data received!")
				self.state = "error_state"
			if self.transport == None:
				continue




	

	def callbackForUserVCInput(self):
		answer = input("Client Side: Please input the verification code: ")
		return answer

if __name__ =="__main__":
	loop = asyncio.get_event_loop()
	#coro = loop.create_connection(lambda: VerificationCodeClientProtocol(1, loop), host="127.0.0.1", port=8000)
	coro = playground.getConnector().create_playground_connection(lambda: ClientProtocol(loop), "20174.1.1.1", 101)	
	transport, protocol = loop.run_until_complete(coro)
	#protocol.send_request_packet(protocol.callbackForUserVCInput)
	protocol.send_request_packet()
	loop.run_forever()
	loop.close()