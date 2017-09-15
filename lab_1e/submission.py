from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from MyPacket import *
from VerificationCodeServerProtocol import VerificationCodeServerProtocol
from VerificationCodeClientProtocol import VerificationCodeClientProtocol
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream as MockTransport
from playground.network.testing import MockTransportToProtocol

import asyncio

def basicUnitTestForPacket():
	
	# test for RequestPacket
	packet1 = RequestPacket()
	packet1.ID = 1
	packet1Bytes = packet1.__serialize__()
	packet1a = RequestPacket.Deserialize(packet1Bytes)
	assert packet1 == packet1a
	print ("- test for RequestPacket SUCCESS")

	# negative test for RequestPacket
	packet1 = RequestPacket()
	packet1.ID = 1
	packet1Bytes = packet1.__serialize__()
	assert packet1 != packet1Bytes
	print ("- negative test for RequestPacket SUCCESS")
	print ("")




	# test for VerificationCodePacket
	packet2 = VerificationCodePacket()
	packet2.ID = 1
	packet2.originalVerificationCode = 447755
	packet2Bytes = packet2.__serialize__()
	packet2a = VerificationCodePacket.Deserialize(packet2Bytes)
	assert packet2 == packet2a
	print ("- test for VerificationCodePacket SUCCESS")

	# negative test for VerificationCodePacket
	packet2 = VerificationCodePacket()
	packet2.ID = 1
	packet2.originalVerificationCode = 447755
	packet2Bytes = packet2.__serialize__()
	packet2a = VerificationCodePacket.Deserialize(packet2Bytes)
	packet2.originalVerificationCode = 447756
	assert packet2 != packet2a
	print ("- negative test for VerificationCodePacket SUCCESS")
	print ("")




	# test for VerifyPacket
	packet3 = VerifyPacket()
	packet3.ID = 1
	packet3.answer = 447755
	packet3Bytes = packet3.__serialize__()
	packet3a = VerifyPacket.Deserialize(packet3Bytes)
	assert packet3 == packet3a
	print ("- test for VerifyPacket SUCCESS")

	# negative test for VerifyPacket
	packet3 = VerifyPacket()
	packet3.ID = 1
	packet3.answer = 447755
	packet3Bytes = packet3.__serialize__()
	packet3a = VerifyPacket.Deserialize(packet3Bytes)
	packet3.answer = 447754
	assert packet3 != packet3a
	print ("- negative test for VerifyPacket SUCCESS")
	print ("")




	# test for ResultPacket
	packet4 = ResultPacket()
	packet4.ID = 1
	packet4.passfail = "pass"
	packet4Bytes = packet4.__serialize__()
	packet4a = ResultPacket.Deserialize(packet4Bytes)
	assert packet4 == packet4a
	print ("- test for ResultPacket SUCCESS")

	# negative test for ResultPacket
	packet4 = ResultPacket()
	packet4.ID = 1
	packet4.passfail = "pass"
	packet4Bytes = packet4.__serialize__()
	packet4a = ResultPacket.Deserialize(packet4Bytes)
	packet4.passfail = "fail"
	assert packet4 != packet4a
	print ("- negative test for ResultPacket SUCCESS")
	print ("")


	# test for HangUpPacket
	packet5 = HangUpPacket()
	packet5.ID = 1
	packet5.hangup = True
	packet5Bytes = packet5.__serialize__()
	packet5a = HangUpPacket.Deserialize(packet5Bytes)
	assert packet5 == packet5a
	print ("- test for HangUpPacket SUCCESS")

	# negative test for HangUpPacket
	packet5 = HangUpPacket()
	packet5.ID = 1
	packet5.hangup = True
	packet5Bytes = packet5.__serialize__()
	assert packet5 != packet1Bytes
	print ("- negative test for HangUpPacket SUCCESS")
	print ("")






	# test for Deserializer
	pktBytes = packet1.__serialize__() + packet2.__serialize__() + packet3.__serialize__() + packet4.__serialize__()
	deserializer = PacketType.Deserializer()
	deserializer.update(pktBytes)
	print("- Start deserializer process!")
	for packet in deserializer.nextPackets():
		print("  got a packet! ",end='')
		if packet == packet1: print("  It's RequestPacket!")
		elif packet == packet2: print("  It's VerificationCodePacket!")
		elif packet == packet3: print("  It's VerifyPacket!")
		elif packet == packet4: print("  It's ResultPacket!")
		else: assert 1 == 0
	print("- test for deserializer SUCCESS")



def basicUnitTestForProtocol():
	asyncio.set_event_loop(TestLoopEx())
	loop = asyncio.get_event_loop()

	server = VerificationCodeServerProtocol(loop)
	client = VerificationCodeClientProtocol(1, loop)
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)

	# test for general connection_made 
	client.connection_made(cTransport)
	server.connection_made(sTransport)
	print("- test for general connection_made SUCCESS")
	print ("")
	
	# test for client verification code length 
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	client.connection_made(cTransport)
	server.connection_made(sTransport)

	MockRequestPacket = RequestPacket()
	MockRequestPacket.ID = 1
	packetBytes = MockRequestPacket.__serialize__()
	server.data_received(packetBytes)
	assert len(str(server._verificationCode)) == 6
	print("- test for client verification code length SUCCESS")
	print ("")

	# negative test for messing up packet order 
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	client.connection_made(cTransport)
	server.connection_made(sTransport)

	MockVerifyPacket = VerifyPacket()
	MockVerifyPacket.ID = 1
	MockVerifyPacket.answer = server._verificationCode
	packetBytes = MockVerifyPacket.__serialize__()
	server.state = "wait_for_verify_packet"
	client.state = "initial_state"
	server.data_received(packetBytes)
	assert client.state == "error_state"
	print("- negative test for messing up packet order SUCCESS")
	print ("")

	# test for client vericifation result 
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	client.connection_made(cTransport)
	server.connection_made(sTransport)

	MockVerifyPacket = VerifyPacket()
	MockVerifyPacket.ID = 1
	MockVerifyPacket.answer = server._verificationCode
	packetBytes = MockVerifyPacket.__serialize__()
	server.state = "wait_for_verify_packet"
	client.state = "wait_for_result_packet"
	server.data_received(packetBytes)
	assert server._result == "pass"
	print("- test for client vericifation result SUCCESS")
	print ("")

	# negative test for client vericifation result
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	client.connection_made(cTransport)
	server.connection_made(sTransport)

	MockVerifyPacket = VerifyPacket()
	MockVerifyPacket.ID = 1
	MockVerifyPacket.answer = 0
	packetBytes = MockVerifyPacket.__serialize__()
	server.state = "wait_for_verify_packet"
	client.state = "wait_for_result_packet"
	server.data_received(packetBytes)
	assert server._result == "fail"
	print("- negative test for client vericifation result SUCCESS")
	print ("")

if __name__ =="__main__":
	print ("=======================================")
	print ("### START BASIC UNIT TEST FOR PACKET###")
	print ("")
	basicUnitTestForPacket()
	print("")
	print("")
	print("### ALL PACKET UNIT TEST SUCCESS! ###")
	print("=====================================")

	print ("==========================================")
	print ("### START BASIC UNIT TEST FOR PROTOCOL ###")
	print ("")
	basicUnitTestForProtocol()
	print("")
	print("")
	print("### ALL PROTOCOL UNIT TEST SUCCESS! ###")
	print("=======================================")


	print()
	print("  **********************************")
	print("  ***** ALL UNIT TEST SUCCESS! *****")
	print("  **********************************")
	print()
