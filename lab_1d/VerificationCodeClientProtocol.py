from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER
from MyPacket import *

import random

import asyncio

class VerificationCodeClientProtocol(asyncio.Protocol):
	state = "initial_state"
	def __init__(self, ID, loop):
		if __name__ =="__main__":
			print("Client Side Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		self.transport = None
		self.state = "initial_state"
		self.message = ID

	def connection_made(self, transport):
		if __name__ =="__main__":
			print("Client Side: Connection Made...")
		self.transport = transport
		#print("Client: %s"%self.state)
		if self.state != "initial_state":
			if __name__ =="__main__":
				print("Server Side: Error: State Error! Expecting initial_state but getting %s"%self.state)
			self.state = "error_state"
			self.transport.close()
			self.loop.stop()
	
		outBoundPacket = RequestPacket()
		outBoundPacket.ID = self.message
		packetBytes = outBoundPacket.__serialize__()
		self.state = "wait_for_verification_code_packet"
		self.transport.write(packetBytes)

	def connection_lost(self, exc=None):
		self.transport = None
		if __name__ =="__main__":
			print("Client Side: Event Loop Stop...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			if isinstance(packet, VerificationCodePacket):
				#print("Client: %s"%self.state)
				if self.state != "wait_for_verification_code_packet":
					if __name__ =="__main__":
						print("Client Side: Error: State Error! Expecting wait_for_verification_code_packet but getting %s"%self.state)
					self.state = "error_state"
					self.loop.stop()
				outBoundPacket = VerifyPacket()
				outBoundPacket.ID = packet.ID
				# if __name__ =="__main__":
				# 	print("Client Side: The Verification Code received from Server is: %d..."%packet.originalVerificationCode)
				# outBoundPacket.answer = input("Client Side: Please input the verification code: ")
				outBoundPacket.answer = packet.originalVerificationCode
				packetBytes = outBoundPacket.__serialize__()
				self.state = "wait_for_result_packet"
				self.transport.write(packetBytes)
			elif isinstance(packet, ResultPacket):
				#print("Client: %s"%self.state)
				if self.state != "wait_for_result_packet":
					if __name__ =="__main__":
						print("Client Side: Error: State Error! Expecting wait_for_result_packet but getting %s"%self.state)
					self.state = "error_state"
					self.loop.stop()
				if __name__ =="__main__":
					print("Client Side: Verification %s..."%packet.passfail)
				self.state = "finish_state"
			else:
				#print("Client: %s"%self.state)
				if __name__ =="__main__":
					print("Client Side: Error: Unexpected data received!")
				self.loop.stop()
				self.state = "finish_state"
			if self.state == "finish_state" or self.state == "error_state":
				self.loop.stop()
				#self.transport.close()

if __name__ =="__main__":
	loop = asyncio.get_event_loop()
	coro = loop.create_connection(lambda: VerificationCodeClientProtocol(1, loop), host="127.0.0.1", port=8000)
	client = loop.run_until_complete(coro)
	loop.run_forever()
	print("ready to close")
	loop.close()