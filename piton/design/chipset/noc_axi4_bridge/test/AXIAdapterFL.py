'''
==========================================================================
 AXIAdapterFL.py
==========================================================================
Functional level model of AXI adapter with openpiton noc interface.

Author: Yanghui Ou
  Date: Dec 17, 2019

'''
from pymtl3 import *
from pymtl3.stdlib.fl import MemoryFL
from .piton_packet import *


class AXIAdapterFL( Component ):

  def construct( s ):

    s.mem = MemoryFL()
    ...

  def request( s, pkt ):
    if pkt.flits[0][ MTYPE ] == LOAD_MEM:

      addr   = pkt.flits[0][ ADDR   ]
      nbytes = size_map[ pkt.flits[0][ NBYTES ] ]
      chipid = pkt.flits[0][ CHIPD ]
      xpos   = pkt.flits[0][ XPOS  ]
      ypos   = pkt.flits[0][ YPOS  ]
      tag    = pkt.flits[0][ TAG   ]

      # TODO:
      # - support variable length
      # - 64B aligned      
      aligned_addr = 
      data = s.mem.read( aligned_addr, 512 )

      return mk_piton_rd_resp( data, tag, chipid, xpos, ypos )

    elif pkt.flits[0][ MTYPE ] == NC_LOAD_REQ:
      ...

    elif pkt.flits[0][ MTYPE ] == STORE_MEM:
      ...

    elif pkt.flits[0][ MTYPE ] == NC_STORE_REQ:
      ...
