from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from MyPacket import *

import random

import asyncio

class VerificationCodeServerProtocol(asyncio.Protocol):
	state = "wait_for_request_packet"
	def __init__(self, loop):
		if __name__ =="__main__":
			print("Server Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		self.transport = None
		self.state = "wait_for_request_packet"
		self._result = "null"
		self._verificationCode = 1

	def connection_made(self, transport):
		if __name__ =="__main__":
			print("Server Side: Connection Made...")
		self.transport = transport

	def connection_lost(self, exc):
		self.transport = None
		if __name__ =="__main__":
			print("Server Side: Event Loop Stop...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			if self.transport == None:
				#self.loop.stop()
				continue
			if self.state == "error_state":
				self.transport.close()
			if isinstance(packet, RequestPacket):
				#print("Server: %s"%self.state)
				if self.state != "wait_for_request_packet":
					if __name__ =="__main__":
						print("Server Side: Error: State Error! Expecting wait_for_request_packet but getting %s"%self.state)
					self.state = "error_state"
					#self.loop.stop()
				else:
					outBoundPacket = VerificationCodePacket()
					outBoundPacket.ID = packet.ID
					self._verificationCode = random.randint(100000, 999999)
					outBoundPacket.originalVerificationCode = self._verificationCode
					if __name__ =="__main__":
						print("Server Side: Sending Verification Code is: %d..."%outBoundPacket.originalVerificationCode)
					packetBytes = outBoundPacket.__serialize__()
					self.state = "wait_for_verify_packet"
					self.transport.write(packetBytes)
			elif isinstance(packet, VerifyPacket):
				#print("Server: %s"%self.state)
				if self.state != "wait_for_verify_packet":
					if __name__ =="__main__":
						print("Server Side: Error: State Error! Expecting wait_for_verify_packet but getting %s"%self.state)
					self.state = "error_state"
					#self.loop.stop()
				else:
					outBoundPacket = ResultPacket()
					outBoundPacket.ID = packet.ID
					if packet.answer == self._verificationCode:	
						outBoundPacket.passfail = "pass"
						self._result = "pass"
					else:	
						outBoundPacket.passfail = "fail"
						self._result = "fail"
					packetBytes = outBoundPacket.__serialize__()
					self.state = "wait_for_hangup_packet"
					self.transport.write(packetBytes)
					if __name__ =="__main__":
						print("Server Side: Verification Result is: %s..."%outBoundPacket.passfail)
			elif isinstance(packet, HangUpPacket):
				#print("Server: %s"%self.state)
				if self.state != "wait_for_hangup_packet":
					if __name__ =="__main__":
						print("Server Side: Error: State Error! Expecting wait_for_hangup_packet but getting %s"%self.state)
					self.state = "error_state"
					#self.loop.stop()
				else:
					self.state = "close_state"
			else:
				#print("Server: %s"%self.state)
				if __name__ =="__main__":
					print("Client Side: Error: Unexpected data received!")
				self.state = "error_state"
			if self.transport == None:
				#self.loop.stop()
				continue
			if self.state == "error_state" or self.state == "close_state":
				self.transport.close()

		
			

if __name__ =="__main__":
	loop = asyncio.get_event_loop()
	coro = loop.create_server(lambda: VerificationCodeServerProtocol(loop), port=8000)
	server = loop.run_until_complete(coro)
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()