from PEEPPacket import *
from MyPacket import *
from PassThroughProtocol import *
from ServerProtocol import *
from ClientProtocol import *
from VerificationCodeClientProtocol import *
from VerificationCodeServerProtocol import *
from Util import *
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

import playground

	
cf = StackingProtocolFactory(lambda: PassThroughProtocol1(), lambda: ClientProtocol())
sf = StackingProtocolFactory(lambda: PassThroughProtocol1(), lambda: ServerProtocol())
lab2Connector = playground.Connector(protocolStack=(cf, sf))
playground.setConnector("lab2_protocol", lab2Connector)