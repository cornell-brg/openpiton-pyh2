'''
==========================================================================
 piton_packet.py
==========================================================================
Util stuff for piton packet.

Author : Yanghui Ou
  Date : Dec 17, 2019
'''
import hypothesis
from hypothesis import strategies as st
from functools import reduce

from pymtl3.datatypes import strategies as pst
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
NBYTES = slice( 8,  11 )

# FLIT3

RESV3  = slice( 0, 30 )

#-------------------------------------------------------------------------
# openpiton message type
#-------------------------------------------------------------------------

LOAD_MEM         = b8(19)
NC_LOAD_REQ      = b8(14)
LOAD_MEM_ACK     = b8(24)
NC_LOAD_MEM_ACK  = b8(26)
STORE_MEM        = b8(20)
STORE_MEM_ACK    = b8(25)
NC_STORE_REQ     = b8(15)
NC_STORE_MEM_ACK = b8(27)

size_map = {
  b3( 0b000 ) : 0,
  b3( 0b001 ) : 1,
  b3( 0b010 ) : 2,
  b3( 0b011 ) : 4,
  b3( 0b100 ) : 8,
  b3( 0b101 ) : 16,
  b3( 0b110 ) : 32,
  b3( 0b111 ) : 64,
}

#-------------------------------------------------------------------------
# pitonpacket
#-------------------------------------------------------------------------

class PitonPacket:

  def __init__( s, nflits ):
    s.flits = [ b64( 0 ) for _ in range( nflits ) ]

#-------------------------------------------------------------------------
# mk_piton_rd_req
#-------------------------------------------------------------------------

def mk_piton_rd_req( addr, nbytes, cacheable, tag,
                     dst_chipid=0, dst_x=0, dst_y=0,
                     src_chipid=0, src_x=0, src_y=0 ):
  pkt = PitonPacket( nflits = 3 )
  pkt.flits[0][ CHIPID ] = b14(dst_chipid)
  pkt.flits[0][ XPOS   ] = b8(dst_x)
  pkt.flits[0][ YPOS   ] = b8(dst_y)
  pkt.flits[0][ TAG    ] = b8(tag)
  pkt.flits[0][ PLEN   ] = b8(2)
  pkt.flits[0][ CHIPID ] = b8(2)
  pkt.flits[0][ MTYPE  ] = b8(19) if cacheable else b8(14)

  pkt.flits[1][ ADDR   ] = b48(addr)
  pkt.flits[1][ NBYTES ] = b3(nbytes)

  pkt.flits[2][ CHIPID ] = b14(src_chipid)
  pkt.flits[2][ XPOS   ] = b8(src_x)
  pkt.flits[2][ YPOS   ] = b8(src_y)

  return list(pkt.flits)

#-------------------------------------------------------------------------
# mk_piton_wr_req
#-------------------------------------------------------------------------

def mk_piton_wr_req( addr, nbytes, cacheable, tag, data,
                     dst_chipid=0, dst_x=0, dst_y=0,
                     src_chipid=0, src_x=0, src_y=0 ):
  pkt = PitonPacket( nflits = 11 )
  pkt.flits[0][ CHIPID ] = b14(dst_chipid)
  pkt.flits[0][ XPOS   ] = b8(dst_x)
  pkt.flits[0][ YPOS   ] = b8(dst_y)
  pkt.flits[0][ TAG    ] = b8(tag)
  pkt.flits[0][ PLEN   ] = b8(10)
  pkt.flits[0][ CHIPID ] = b8(2)
  pkt.flits[0][ MTYPE  ] = b8( STORE_MEM ) if cacheable else b8( NC_STORE_MEM_ACK )

  pkt.flits[1][ ADDR   ] = b48(addr)
  pkt.flits[1][ NBYTES ] = b3(nbytes)

  pkt.flits[2][ CHIPID ] = b14(src_chipid)
  pkt.flits[2][ XPOS   ] = b8(src_x)
  pkt.flits[2][ YPOS   ] = b8(src_y)

  for i in range( 8 ):
    pkt.flits[i+3] = data[i*64:(i+1)*64]

  return list(pkt.flits)

#-------------------------------------------------------------------------
# mk_piton_rd_resp
#-------------------------------------------------------------------------

def mk_piton_rd_resp( data, tag, cacheable, chipid=0, dst_x=0, dst_y=0 ):
  pkt = PitonPacket( nflits=9 )

  pkt.flits[0][ MTYPE ]  = b8(LOAD_MEM_ACK) if cacheable else b8(NC_LOAD_MEM_ACK)
  pkt.flits[0][ PLEN  ]  = b8(8)
  pkt.flits[0][ TAG   ]  = b8(tag)
  pkt.flits[0][ CHIPID ] = b14(chipid)
  pkt.flits[0][ XPOS   ] = b8(dst_x)
  pkt.flits[0][ YPOS   ] = b8(dst_y)

  for i in range( 8 ):
    pkt.flits[i+1] = data[i*64:(i+1)*64]

  print( 'here', pkt.flits[1] )

  return list(pkt.flits)

#-------------------------------------------------------------------------
# mk_piton_wr_resp
#-------------------------------------------------------------------------

def mk_piton_wr_resp( tag, cacheable, chipid=0, dst_x=0, dst_y=0 ):
  pkt = PitonPacket( nflits=1 )

  pkt.flits[0][ MTYPE  ] = b8(STORE_MEM_ACK) if cacheable else b8(NC_STORE_MEM_ACK)
  pkt.flits[0][ PLEN   ] = b8(0)
  pkt.flits[0][ TAG    ] = b8(tag)
  pkt.flits[0][ CHIPID ] = b14(chipid)
  pkt.flits[0][ XPOS   ] = b8(dst_x)
  pkt.flits[0][ YPOS   ] = b8(dst_y)

  return list(pkt.flits)

#-------------------------------------------------------------------------
# piton_rd_reqs
#-------------------------------------------------------------------------
# TODO: for now only do 64 byte write

@st.composite
def piton_rd_reqs( draw, num_addr=4, base_addr=0x1000, max_x=8, max_y=8 ):
  idx   = draw( st.integers( 0, num_addr) )
  addr  = base_addr + idx * 0x40
  src_x = draw( st.integers( 0, max_x ) )
  src_y = draw( st.integers( 0, max_y ) )
  return mk_piton_rd_req( addr, 64, True, 0, src_x=src_x, src_y=src_y )

@st.composite
def piton_wr_reqs( draw, num_addr=4, base_addr=0x1000, max_x=8, max_y=8 ):
  idx     = draw( st.integers( 0, num_addr) )
  addr    = base_addr + idx * 0x40
  src_x   = draw( st.integers( 0, max_x ) )
  src_y   = draw( st.integers( 0, max_y ) )
  payload = draw( st.lists( pst.bits(64), min_size=8, max_size=8 ) )
  wr_data = reduce( lambda a, b: concat( b, a ), payload)
  return mk_piton_wr_req( addr, 64, True, 0, wr_data, src_x=src_x, src_y=src_y )

@st.composite
def piton_reqs( draw, num_addr=4, base_addr=0x1000, max_x=8, max_y=8 ):
  req_type = draw( st.sampled_from( [ 'rd', 'wr' ] ) )
  if req_type == 'rd':
    return draw( piton_rd_reqs( num_addr, base_addr, max_x, max_y ) )
  else:
    return draw( piton_wr_reqs( num_addr, base_addr, max_x, max_y ) )