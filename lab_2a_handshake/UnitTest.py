from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from playground.network.packet.fieldtypes.attributes import *
from HandShake import *
from ServerProtocol import ServerProtocol
from ClientProtocol import ClientProtocol
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

	



def basicUnitTestForProtocol():
	asyncio.set_event_loop(TestLoopEx())
	loop = asyncio.get_event_loop()

	server = ServerProtocol(loop)
	client = ClientProtocol(loop)
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)

	# test for general connection_made 
	client.connection_made(cTransport)
	server.connection_made(sTransport)
	print("- test for general connection_made SUCCESS")
	print ("")
	

	# negative test for messing up packet order 
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	client.connection_made(cTransport)
	server.connection_made(sTransport)

	MockHandShake_SYN = HandShake()
	MockHandShake_SYN.Type = 0
	MockHandShake_SYN.SequenceNumber = 1
	MockHandShake_SYN.Checksum = 1
	MockHandShake_SYN.Acknowledgement = 1
	MockHandShake_SYN.HLEN = 96
	packetBytes = MockHandShake_SYN.__serialize__()
	server.state = "SYN_State"
	client.state = "SYN_ACK_State"
	server.data_received(packetBytes)
	print(server.state)
	assert server.state == "error_state"
	print("- negative test for messing up packet order SUCCESS")
	print ("")

	# test for client vericifation result 
	cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	client.connection_made(cTransport)
	server.connection_made(sTransport)

	MockHandShake_ACK = HandShake()
	MockHandShake_ACK.Type = 2
	MockHandShake_ACK.SequenceNumber = 1
	MockHandShake_ACK.Checksum = 1
	MockHandShake_ACK.Acknowledgement = 1
	MockHandShake_ACK.HLEN = 96
	packetBytes = MockHandShake_ACK.__serialize__()
	server.state = "SYN_State"
	client.state = "Transmission_State"
	server.data_received(packetBytes)
	assert server.state == "Tramsmission_State"
	print("- test for client vericifation result SUCCESS")
	print ("")


if __name__ =="__main__":
	print ("=======================================")
	print ("### START BASIC UNIT TEST FOR HANDSHAKE PACKET###")
	print ("")
	basicUnitTestForHandShakePacket()
	print("")
	print("")
	print("### ALL HANDSHAKE PACKET UNIT TEST SUCCESS! ###")
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
	print()
	print()
	print()
	print("*******************************")
	print("*      All Unit Tests         *")
	print("*                             *")
	print("*   ****    *    ****  ****   *")
	print("*   *  *   * *   *     *      *")
	print("*   *  *  *   *  *     *      *")
	print("*   ****  *****  ****  ****   *")
	print("*   *     *   *     *     *   *")
	print("*   *     *   *     *     *   *")
	print("*   *     *   *  ****  ****   *")
	print("*                             *")
	print("*******************************")
	print()