from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from playground.network.packet.fieldtypes.attributes import *
from HandShake import *
# from VerificationCodeServerProtocol import VerificationCodeServerProtocol
# from VerificationCodeClientProtocol import VerificationCodeClientProtocol
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream as MockTransport
from playground.network.testing import MockTransportToProtocol

import asyncio

def basicUnitTestForHandShakePacket():
	
	# test for HandShake Serialize Deserialize
	packet1 = HandShake()
	packet1.Type = 1
	packet1.SequenceNumber = 1
	packet1.Checksum = 1
	packet1.Acknowledgement = 1
	packet1.HLEN = 1
	packet1Bytes = packet1.__serialize__()
	packet1_serialized_deserialized = HandShake.Deserialize(packet1Bytes)
	assert packet1 == packet1_serialized_deserialized
	print ("- test for HandShake Serialize Deserialize SUCCESS")



	# negative test for HandShake Serialize Deserialize
	packet1 = HandShake()
	packet1.Type = 1
	packet1.SequenceNumber = 1
	packet1.Checksum = 1
	packet1.Acknowledgement = 1
	packet1.HLEN = 1
	packet1Bytes = packet1.__serialize__()
	packet1_serialized_deserialized = HandShake.Deserialize(packet1Bytes)

	packet2 = HandShake()
	packet2.Type = 1
	packet2.SequenceNumber = 1
	packet2.Checksum = 999
	packet2.Acknowledgement = 1
	packet2.HLEN = 1
	packet2Bytes = packet2.__serialize__()
	packet2_serialized_deserialized = HandShake.Deserialize(packet2Bytes)
	assert packet1_serialized_deserialized != packet2_serialized_deserialized
	print ("- negative test for HandShake Serialize Deserialize SUCCESS")



	# test for HandShake Optional fields
	packet1 = HandShake()
	packet1.Type = 1
	packet1.Checksum = 1
	packet1.HLEN = 1
	packet1Bytes = packet1.__serialize__()
	packet1_serialized_deserialized = HandShake.Deserialize(packet1Bytes)
	assert packet1 == packet1_serialized_deserialized
	print ("- test for  HandShake Optional fields SUCCESS")

	






# def basicUnitTestForProtocol():
# 	asyncio.set_event_loop(TestLoopEx())
# 	loop = asyncio.get_event_loop()

# 	server = VerificationCodeServerProtocol(loop)
# 	client = VerificationCodeClientProtocol(1, loop)
# 	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)

# 	# test for general connection_made 
# 	client.connection_made(cTransport)
# 	server.connection_made(sTransport)
# 	print("- test for general connection_made SUCCESS")
# 	print ("")
	
# 	# test for client verification code length 
# 	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
# 	client.connection_made(cTransport)
# 	server.connection_made(sTransport)

# 	MockRequestPacket = RequestPacket()
# 	MockRequestPacket.ID = 1
# 	packetBytes = MockRequestPacket.__serialize__()
# 	server.data_received(packetBytes)
# 	assert len(str(server._verificationCode)) == 6
# 	print("- test for client verification code length SUCCESS")
# 	print ("")

# 	# negative test for messing up packet order 
# 	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
# 	client.connection_made(cTransport)
# 	server.connection_made(sTransport)

# 	MockVerifyPacket = VerifyPacket()
# 	MockVerifyPacket.ID = 1
# 	MockVerifyPacket.answer = server._verificationCode
# 	packetBytes = MockVerifyPacket.__serialize__()
# 	server.state = "wait_for_verify_packet"
# 	client.state = "initial_state"
# 	server.data_received(packetBytes)
# 	assert client.state == "error_state"
# 	print("- negative test for messing up packet order SUCCESS")
# 	print ("")

# 	# test for client vericifation result 
# 	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
# 	client.connection_made(cTransport)
# 	server.connection_made(sTransport)

# 	MockVerifyPacket = VerifyPacket()
# 	MockVerifyPacket.ID = 1
# 	MockVerifyPacket.answer = server._verificationCode
# 	packetBytes = MockVerifyPacket.__serialize__()
# 	server.state = "wait_for_verify_packet"
# 	client.state = "wait_for_result_packet"
# 	server.data_received(packetBytes)
# 	assert server._result == "pass"
# 	print("- test for client vericifation result SUCCESS")
# 	print ("")

# 	# negative test for client vericifation result
# 	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
# 	client.connection_made(cTransport)
# 	server.connection_made(sTransport)

# 	MockVerifyPacket = VerifyPacket()
# 	MockVerifyPacket.ID = 1
# 	MockVerifyPacket.answer = 0
# 	packetBytes = MockVerifyPacket.__serialize__()
# 	server.state = "wait_for_verify_packet"
# 	client.state = "wait_for_result_packet"
# 	server.data_received(packetBytes)
# 	assert server._result == "fail"
# 	print("- negative test for client vericifation result SUCCESS")
# 	print ("")

if __name__ =="__main__":
	print ("=======================================")
	print ("### START BASIC UNIT TEST FOR HANDSHAKE PACKET###")
	print ("")
	basicUnitTestForHandShakePacket()
	print("")
	print("")
	print("### ALL HANDSHAKE PACKET UNIT TEST SUCCESS! ###")
	print("=====================================")

	# print ("==========================================")
	# print ("### START BASIC UNIT TEST FOR PROTOCOL ###")
	# print ("")
	# basicUnitTestForProtocol()
	# print("")
	# print("")
	# print("### ALL PROTOCOL UNIT TEST SUCCESS! ###")
	# print("=======================================")


	print()
	print("  **********************************")
	print("  ***** ALL UNIT TEST SUCCESS! *****")
	print("  **********************************")
	print()