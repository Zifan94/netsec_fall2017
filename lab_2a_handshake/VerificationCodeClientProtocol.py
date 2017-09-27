from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from MyPacket import *
from PassThroughProtocol import *
from ClientProtocol import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

import random

import asyncio

class VerificationCodeClientProtocol(asyncio.Protocol):
	state = "initial_state"
	def __init__(self, ID, loop):
		if __name__ =="__main__":
			print("App_Layer Client Side: Init Compelete...")
		self.loop = loop
		self._deserializer = PacketType.Deserializer()
		self.transport = None
		self.state = "initial_state"
		self.message = ID

	def connection_made(self, transport):
		if __name__ =="__main__":
			print("App_Layer Client Side: Connection Made...")
		self.transport = transport

	def send_request_packet(self, callback=None):
		#print("Client: %s"%self.state)
		if self.state != "initial_state":
			if __name__ =="__main__":
				print("App_Layer Client Side: Error: State Error! Expecting initial_state but getting %s"%self.state)
			self.state = "error_state"
			self.transport.close()
			self.loop.stop()
		else:
			if __name__ =="__main__":
				print("App_Layer Client Side: Sending first packet...")
			self._callback = callback
			outBoundPacket = RequestPacket()
			outBoundPacket.ID = self.message
			packetBytes = outBoundPacket.__serialize__()
			self.state = "wait_for_verification_code_packet"
			self.transport.write(packetBytes)

	def connection_lost(self, exc=None):
		self.transport = None
		if __name__ =="__main__":
			print("App_Layer Client Side: Connection Lost...")
		self.loop.stop()

	def data_received(self, data):
		self._deserializer.update(data)
		for packet in self._deserializer.nextPackets():
			if self.transport == None:
				# self.loop.stop()
				continue
			# if self.state == "error_state":
			# 	# self.transport.close() #using pass through ptl to close 
			# 	self.transport = None
			if isinstance(packet, VerificationCodePacket):
				#print("Client: %s"%self.state)
				if self.state != "wait_for_verification_code_packet":
					if __name__ =="__main__":
						print("App_Layer Client Side: Error: State Error! Expecting wait_for_verification_code_packet but getting %s"%self.state)
					self.state = "error_state"
					#self.loop.stop()
				else:
					outBoundPacket = VerifyPacket()
					outBoundPacket.ID = packet.ID
					if __name__ =="__main__":
						print("App_Layer Client Side: The Verification Code received from Server is: %d..."%packet.originalVerificationCode)
					# outBoundPacket.answer = input("Client Side: Please input the verification code: ")
					if self._callback == None:
						outBoundPacket.answer = packet.originalVerificationCode
					else:
						answer = self._callback()
						outBoundPacket.answer = answer
					packetBytes = outBoundPacket.__serialize__()
					self.state = "wait_for_result_packet"
					self.transport.write(packetBytes)
			elif isinstance(packet, ResultPacket):
				#print("Client: %s"%self.state)
				if self.state != "wait_for_result_packet":
					if __name__ =="__main__":
						print("App_Layer Client Side: Error: State Error! Expecting wait_for_result_packet but getting %s"%self.state)
					self.state = "error_state"
					#self.loop.stop()
				else:
					if __name__ =="__main__":
						print("App_Layer Client Side: The Result of Verification is:")
						if packet.passfail == 'pass':
							print("")
							print(" ****    *    ****  ****   ")
							print(" *  *   * *   *     *      ")
							print(" *  *  *   *  *     *      ")
							print(" ****  *****  ****  ****   ")
							print(" *     *   *     *     *   ")
							print(" *     *   *     *     *   ")
							print(" *     *   *  ****  ****   ")
							print("")
						elif packet.passfail == 'fail':
							print("")
							print(" ****    *    ****  *      ")
							print(" *      * *    *    *      ")
							print(" *     *   *   *    *      ")
							print(" ****  *****   *    *      ")
							print(" *     *   *   *    *      ")
							print(" *     *   *   *    *      ")
							print(" *     *   *  ****  ****   ")
							print("")
						else:
							print("Undefine!")
					outBoundPacket = HangUpPacket()
					outBoundPacket.ID = packet.ID
					outBoundPacket.hangup = True
					packetBytes = outBoundPacket.__serialize__()
					self.state = "finish_state"
					if __name__ =="__main__":
						print("App_Layer Client Side: Sent Hang up signal!")
					self.transport.write(packetBytes)
			else:
				#print("Client: %s"%self.state)
				if __name__ =="__main__":
					print("App_Layer Client Side: Error: Unexpected data received!")
				self.state = "error_state"
			if self.transport == None:
				#self.loop.stop()
				continue
			# if self.state == "error_state":
			# 	# self.transport.close() #using pass through ptl to close 
			# 	self.transport = None




	

	def callbackForUserVCInput(self):
		answer = input("App_Layer Client Side: Please input the verification code: ")
		return answer

if __name__ =="__main__":

	loop = asyncio.get_event_loop()
	loop.set_debug(enabled = True)

	f = StackingProtocolFactory(lambda: PassThroughProtocol1(), lambda: ClientProtocol(loop))
	# f = StackingProtocolFactory(lambda: ClientProtocol(loop), lambda: PassThroughProtocol1())
	ptConnector = playground.Connector(protocolStack=f)
	playground.setConnector("passthroughClient", ptConnector)
	print("----- NEW CONNECTOR SETUP on Client Side-----")

	#coro = loop.create_connection(lambda: VerificationCodeClientProtocol(1, loop), host="127.0.0.1", port=8000)
	coro = playground.getConnector('passthroughClient').create_playground_connection(lambda: VerificationCodeClientProtocol(1, loop), "20174.1.1.1", 101)	
	transport, protocol = loop.run_until_complete(coro)
	protocol.send_request_packet(protocol.callbackForUserVCInput)
	# protocol.send_request_packet()
	loop.run_forever()
	loop.close()