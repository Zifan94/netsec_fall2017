from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from playground.network.packet.fieldtypes.attributes import *
from PEEPPacket import *
from Util import *
from ServerProtocol import ServerProtocol
from ClientProtocol import ClientProtocol
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream as MockTransport
from playground.network.testing import MockTransportToProtocol

import asyncio
def basicUnitTestForUtil():

	# test for create_outbound_packet()
	packet1 = Util.create_outbound_packet(1, 2, 3, b"data")
	assert packet1.Type == 1
	assert packet1.SequenceNumber == 2
	assert packet1.Acknowledgement == 3
	assert packet1.Data == b"data"
	print ("- test for Util.create_outbound_packet() SUCCESS")	




def basicUnitTestForPEEPPacketPacket():

	# test for PEEPPacket Serialize Deserialize
	packet1 = Util.create_outbound_packet(1, 1, 1, b"data")
	packet1Bytes = packet1.__serialize__()
	packet1_serialized_deserialized = PEEPPacket.Deserialize(packet1Bytes)
	assert packet1 == packet1_serialized_deserialized
	print ("- test for PEEPPacket Serialize Deserialize SUCCESS")


	# negative test for PEEPPacket Serialize Deserialize
	packet1 = Util.create_outbound_packet(1, 1, 1, b"data")
	packet1Bytes = packet1.__serialize__()
	packet1_serialized_deserialized = PEEPPacket.Deserialize(packet1Bytes)

	packet2 = Util.create_outbound_packet(1, 2, 1, b"datadata")
	packet2Bytes = packet2.__serialize__()
	packet2_serialized_deserialized = PEEPPacket.Deserialize(packet2Bytes)
	assert packet1_serialized_deserialized != packet2_serialized_deserialized
	print ("- negative test for PEEPPacket Serialize Deserialize SUCCESS")



	# test for PEEPPacket Optional fields
	packet1 = Util.create_outbound_packet(1, 2, 3)
	packet1Bytes = packet1.__serialize__()
	packet1_serialized_deserialized = PEEPPacket.Deserialize(packet1Bytes)
	assert packet1 == packet1_serialized_deserialized
	print ("- test for  PEEPPacket Optional fields SUCCESS")





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

	MockPEEPPacket_SYN = Util.create_outbound_packet(0, 1, 1, b"data")
	packetBytes = MockPEEPPacket_SYN.__serialize__()
	server.state = "SYN_State_1"
	client.state = "SYN_ACK_State_1"
	server.data_received(packetBytes)
	assert server.state == "error_state"
	print("- negative test for messing up packet order SUCCESS")
	print ("")

	# # test for client vericifation result (disabled for now because of stacking protocol)
	# cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
	# client.connection_made(cTransport)
	# server.connection_made(sTransport)

	# MockPEEPPacket_ACK = Util.create_outbound_packet(2, 1, 1, b"data")
	# packetBytes = MockPEEPPacket_ACK.__serialize__()
	# server.state = "SYN_State_1"
	# client.state = "Transmission_State_2"
	# server.data_received(packetBytes)
	# assert server.state == "Transmission_State_2"
	# assert client.state == "Transmission_State_2"
	# print("- test for client vericifation result SUCCESS")
	# print ("")


if __name__ =="__main__":
	print ("=======================================")
	print ("### START BASIC UNIT TEST FOR Util###")
	print ("")
	basicUnitTestForUtil()
	print("")
	print("")
	print("### ALL UTIL UNIT TEST SUCCESS! ###")
	print("=====================================")

	print ("=======================================")
	print ("### START BASIC UNIT TEST FOR PEEPPacket PACKET###")
	print ("")
	basicUnitTestForPEEPPacketPacket()
	print("")
	print("")
	print("### ALL PEEPPacket PACKET UNIT TEST SUCCESS! ###")
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
