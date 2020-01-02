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

  def request( s, pkt ):

    # Cacheable read

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
      aligned_addr = addr
      data = s.mem.read( aligned_addr, 64 )

      return mk_piton_rd_resp( data, tag, True, chipid, xpos, ypos )

    # Non-cacheable read

    elif pkt.flits[0][ MTYPE ] == NC_LOAD_REQ:
      addr   = pkt.flits[0][ ADDR   ]
      nbytes = size_map[ pkt.flits[0][ NBYTES ] ]
      chipid = pkt.flits[0][ CHIPD ]
      xpos   = pkt.flits[0][ XPOS  ]
      ypos   = pkt.flits[0][ YPOS  ]
      tag    = pkt.flits[0][ TAG   ]

      # TODO:
      # - support variable length
      # - 64B aligned      
      aligned_addr = addr
      data = s.mem.read( aligned_addr, 64 )

      return mk_piton_rd_resp( data, tag, False, chipid, xpos, ypos )

    # Cacheable store

    elif pkt.flits[0][ MTYPE ] == STORE_MEM:
      addr   = pkt.flits[0][ ADDR   ]
      nbytes = size_map[ pkt.flits[0][ NBYTES ] ]
      chipid = pkt.flits[0][ CHIPD ]
      xpos   = pkt.flits[0][ XPOS  ]
      ypos   = pkt.flits[0][ YPOS  ]
      tag    = pkt.flits[0][ TAG   ]

      aligned_addr = addr
      data = mk_bits( 512 )()
      for i in range( 8 ):
        data[i*64:(i+1)*64] = b64( pkt.flits[i] )
      
      s.mem.write( aligned_addr, 64 ) 

      return mk_piton_wr_resp( tag, True, chipid, xpos, ypos )
    

    # Non-cacheable store

    elif pkt.flits[0][ MTYPE ] == NC_STORE_REQ:
      addr   = pkt.flits[0][ ADDR   ]
      nbytes = size_map[ pkt.flits[0][ NBYTES ] ]
      chipid = pkt.flits[0][ CHIPD ]
      xpos   = pkt.flits[0][ XPOS  ]
      ypos   = pkt.flits[0][ YPOS  ]
      tag    = pkt.flits[0][ TAG   ]

      aligned_addr = addr
      data = mk_bits( 512 )()
      for i in range( 8 ):
        data[i*64:(i+1)*64] = b64( pkt.flits[i] )
      
      s.mem.write( aligned_addr, 64 ) 

      return mk_piton_wr_resp( tag, False, chipid, xpos, ypos )

