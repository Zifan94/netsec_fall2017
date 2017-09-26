from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, UINT16, UINT8, STRING, BUFFER, BOOL
from playground.network.packet.fieldtypes.attributes import *

class PEEPPacket(PacketType):
	DEFINITION_IDENTIFIER = "PEEP.Packet"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
		("Type", UINT8),
		("SequenceNumber", UINT32({Optional: True})),
		("Checksum", UINT16),
		("Acknowledgement", UINT32({Optional: True})),
		("Data", BUFFER({Optional: True}))
	]

	# SYN -		TYPE 0
	# SYN-ACK -  TYPE 1
	# ACK - 		TYPE 2
	# RIP -		TYPE 3
	# RIP-ACK -	TYPE 4
	# RST -		TYPE 5
