'''
==========================================================================
 piton_packet.py
==========================================================================
Util stuff for piton packet.

Author : Yanghui Ou
  Date : Dec 17, 2019
'''
from pymtl3 import *

#-------------------------------------------------------------------------
# openpiton slices
#-------------------------------------------------------------------------

# FLIT1

CHIPID = slice( 50, 64 )
XPOS   = slice( 42, 50 )
YPOS   = slice( 34, 42 )
FBITS  = slice( 30, 34 )
PLEN   = slice( 22, 30 )
MTYPE  = slice( 14, 22 )
TAG    = slice( 6,  14 )
RESV   = slice( 0,  6  )

# FLIT2

ADDR   = slice( 16, 64 )
OPT2   = slice( 0,  16 )

# FLIT3

RESV3  = slice( 0, 30 )

#-------------------------------------------------------------------------
# PitonPacket
#-------------------------------------------------------------------------

class PitonPacket:

  def __init__( s, nflits ):
    s.flits = [ b64( 0 ) for _ in range( nflits ) ]

