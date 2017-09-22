from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from HandShake import *

class Util():
	@staticmethod
	def create_outbound_handshake_packet(Type, seqNum=None, ackNum=None):
		outBoundPacket = HandShake()
		outBoundPacket.Type = Type
		if seqNum != None: outBoundPacket.SequenceNumber = seqNum
		if ackNum != None: outBoundPacket.Acknowledgement = ackNum
		outBoundPacket.HLEN = 96
		outBoundPacket.Checksum = 0; # initialization
		outBoundPacket.Checksum = Util.calculate_check_sum(outBoundPacket)

		return outBoundPacket

	@staticmethod
	def calculate_check_sum(packet):
		if isinstance(packet, HandShake):
			return 1;  # TODO: implement checksum here
		else:
			print("CheckSum calculate failed!")
			return 9999999;

