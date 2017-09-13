from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER

class RequestPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.zifan.RequestPacket"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
		("ID", UINT32),
		]


class VerificationCodePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.zifan.VerificationCodePacket"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
		("ID", UINT32),
		("originalVerificationCode", UINT32)
		]


class VerifyPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.zifan.VerifyPacket"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
		("ID", UINT32),
		("answer", UINT32)
		]


class ResultPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.zifan.ResultPacket"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
		("ID", UINT32),
		("passfail", STRING)
		]
