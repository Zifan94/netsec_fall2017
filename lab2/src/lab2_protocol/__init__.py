from PEEPPacket import *
from MyPacket import *
from PassThroughProtocol import *
from PEEPServerProtocol import *
from PEEPClientProtocol import *
from VerificationCodeClientProtocol import *
from VerificationCodeServerProtocol import *
from Util import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

	
cf = StackingProtocolFactory(lambda: PassThroughProtocol1(), lambda: PEEPClientProtocol())
sf = StackingProtocolFactory(lambda: PassThroughProtocol1(), lambda: PEEPServerProtocol())
lab2Connector = playground.Connector(protocolStack=(cf, sf))
playground.setConnector("lab2_protocol", lab2Connector)