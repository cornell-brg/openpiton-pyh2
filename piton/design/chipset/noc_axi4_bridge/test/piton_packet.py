'''
==========================================================================
 piton_packet.py
==========================================================================
Util stuff for piton packet.

Author : Yanghui Ou
  Date : Dec 17, 2019
'''
from pymtl3 import *

class PitonPacket:

  def __init__( s, nflits ):
    s.flits = [ b64( 0 ) for _ in range( nflits ) ]
