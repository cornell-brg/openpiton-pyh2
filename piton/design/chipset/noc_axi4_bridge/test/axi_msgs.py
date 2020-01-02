'''
==========================================================================
axi_msgs.py
==========================================================================
Bitstructs for axi interface.

Author : Yanghui Ou
  Date : Jan 1, 2020
'''

from pymtl3 import *

BitsNOCDataWidth = Bits64
BitsAXI4IDWidth  = Bits6
BitsAXI4AddrWidth = Bits64
BitsAXI4LenWidth = Bits8
BitsAXI4SizeWidth = Bits3
BitsAXI4BurstWidth = Bits2
BitsAXI4CacheWidth = Bits4
BitsAXI4PortWidth = Bits3
BitsAXI4QoSWidth = Bits4
BitsAXI4RegionWidth = Bits4
BitsAXI4UserWidth = Bits11
BitsAXI4DataWidth = Bits512
BitsAXI4RespWidth = Bits2
BitsAXI4StrbWidth = Bits64

@bitstruct
class AXI4AddrRead:
  arid     : Bits6
  araddr   : Bits64
  arlen    : Bits8
  arsize   : Bits3
  arburst  : Bits2
  arlock   : Bits1
  arcache  : Bits4
  arprot   : Bits3
  arqos    : Bits4
  arregion : Bits4
  aruser   : Bits11

@bitstruct
class AXI4DataRead:
  rid   : Bits6
  rdata : Bits512
  rresp : Bits2
  rlast : Bits1
  ruser : Bits11

@bitstruct
class AXI4AddrWrite:
  awid     : Bits6
  awaddr   : Bits64
  awlen    : Bits8
  awsize   : Bits3
  awburst  : Bits2
  awlock   : Bits1
  awcache  : Bits4
  awprot   : Bits3
  awqos    : Bits4
  awregion : Bits4
  awuser   : Bits11

@bitstruct
class AXI4DataWrite:
  wid      : Bits6
  wdata    : Bits512
  wstrb    : Bits64
  wlast    : Bits1
  wuser    : Bits11

@bitstruct
class AXI4WriteResp:
  bid   : Bits6
  bresp : Bits2
  buser : Bits11
