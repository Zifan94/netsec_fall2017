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
		#outBoundPacket.Checksum = Util.calculate_check_sum(outBoundPacket)

		return outBoundPacket

	""" *****************************************************************
	*** checksum function is a modified version of Jason Orendorff's  ***
	*** stackoverflow solution for TCP/UDP checksum found at          ***
	*** checksum-udp-calculation-python thread                        ***
	******************************************************************"""

	# add each 16 bit word to total and handle overflow
	@staticmethod
	def carry_around_add(a,b):
	    c = a + b
	    return (c & 0xffff) + (c >> 16)

	# take the one's complement of the sum of all 16 bit words in data.
	@staticmethod
	def checksum(msg):
	    total = 0
	    # if odd lengthed message, pad by two bytes for purposes of checksum
	    if ((len(msg) % 2) != 0):
	        msg += "\x00"
	    # convert each 16 bit word from string into type byte and add to total
	    for i in range(0, len(msg), 2):
	        word = ord(msg[i]) + (ord(msg[i+1]) << 8)
	        total = Util.carry_around_add(total, word)
	    return ~total & 0xffff

	# verify checksum
	@staticmethod
	def is_valid_checksum(msg, checksum):
	    total = 0
	    if ((len(msg) % 2) != 0):
	        msg += "\x00"
	    for i in range(0, len(msg), 2):
	        word = ord(msg[i]) + (ord(msg[i+1]) << 8)
	        total = Util.carry_around_add(total, word)
	    total = total & 0xffff
	    return (total + checksum) == 0xffff

	# Create string of bytes for calculating checksum
	@staticmethod
	def prepare_checksum_bytes(Type, seqNum=None, ackNum=None, data=None):
		strType = str(Type)
		byteString = " ".join("{:02x}".format(ord(c)) for c in strType)
		if (seqNum != None):
			strSeqNumBytes = str(seqNum)
			strSeqNumBytes = " ".join("{:02x}".format(ord(c)) for c in strSeqNumBytes)
			byteString = byteString + " " + strSeqNumBytes
		if (ackNum != None):
			strAckNumBytes = str(ackNum)
			strAckNumBytes = " ".join("{:02x}".format(ord(c)) for c in strAckNumBytes)
			byteString = byteString + " " + strAckNumBytes
		if (data != None):
			strDataBytes = str(data) # can we convert buffer type to string?
			strDataBytes = " ".join("{:02x}".format(ord(c)) for c in strDataBytes)
			byteString = byteString + " " + strDataBytes
		return byteString
