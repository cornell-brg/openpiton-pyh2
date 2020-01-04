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

    if pkt[0][ MTYPE ] == LOAD_MEM:

      tag    = pkt[0][ TAG   ]
      addr   = pkt[1][ ADDR   ]
      nbytes = size_map[ pkt[1][ NBYTES ] ]
      chipid = pkt[2][ CHIPID ]
      xpos   = pkt[2][ XPOS   ]
      ypos   = pkt[2][ YPOS   ]

      # TODO:
      # - support variable length
      # - 64B aligned
      aligned_addr = addr
      assert addr % 64 == 0
      data = s.mem.read( aligned_addr, 64 )
      print( 'rd:', aligned_addr, data )

      return mk_piton_rd_resp( data, tag, True, chipid, xpos, ypos )

    # Non-cacheable read

    elif pkt[0][ MTYPE ] == NC_LOAD_REQ:
      tag    = pkt[0][ TAG   ]
      addr   = pkt[1][ ADDR   ]
      nbytes = size_map[ pkt[1][ NBYTES ] ]
      chipid = pkt[2][ CHIPID ]
      xpos   = pkt[2][ XPOS   ]
      ypos   = pkt[2][ YPOS   ]

      # TODO:
      # - support variable length
      # - 64B aligned
      aligned_addr = addr
      assert addr % 64 == 0
      data = s.mem.read( aligned_addr, 64 )

      return mk_piton_rd_resp( data, tag, False, chipid, xpos, ypos )

    # Cacheable store

    elif pkt[0][ MTYPE ] == STORE_MEM:
      tag    = pkt[0][ TAG    ]
      addr   = pkt[1][ ADDR   ]
      nbytes = size_map[ pkt[1][ NBYTES ] ]
      chipid = pkt[2][ CHIPID ]
      xpos   = pkt[2][ XPOS   ]
      ypos   = pkt[2][ YPOS   ]

      aligned_addr = addr
      assert addr % 64 == 0
      data = s.mem.read( aligned_addr, 64 )
      for i in range( 8 ):
        data[i*64:(i+1)*64] = b64( pkt[i+3] )

      s.mem.write( aligned_addr, 64, data )
      # print( tag, chipid, xpos, ypos )
      # print( 'wr', aligned_addr, data )
      return mk_piton_wr_resp( tag, True, chipid, xpos, ypos )


    # Non-cacheable store

    elif pkt[0][ MTYPE ] == NC_STORE_REQ:
      tag    = pkt[0][ TAG    ]
      addr   = pkt[1][ ADDR   ]
      nbytes = size_map[ pkt[1][ NBYTES ] ]
      chipid = pkt[2][ CHIPID ]
      xpos   = pkt[2][ XPOS   ]
      ypos   = pkt[2][ YPOS   ]

      aligned_addr = addr
      assert addr % 64 == 0
      data = s.mem.read( aligned_addr, 64 )
      for i in range( 8 ):
        data[i*64:(i+1)*64] = b64( pkt[i] )

      s.mem.write( aligned_addr, 64 )

      return mk_piton_wr_resp( tag, False, chipid, xpos, ypos )

