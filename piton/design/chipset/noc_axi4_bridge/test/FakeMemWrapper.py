'''
==========================================================================
 FakeMemWrapper.py
==========================================================================
'''
from pytml3 import *

from .fake_axi4_mem.py import fake_axi4_mem

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

class FakeMemWrapper( Component ):

  def construct( s ):

    # Interface 

    # Addr write
    s.m_axi_awid     = InPort( BitsAXI4IDWidth )
    s.m_axi_awaddr   = InPort( BitsAXI4AddrWidth )
    s.m_axi_awlen    = InPort( BitsAXI4LenWidth )
    s.m_axi_awsize   = InPort( BitsAXI4SizeWidth )
    s.m_axi_awburst  = InPort( BitsAXI4BurstWidth )
    s.m_axi_awlock   = InPort( Bits1 )
    s.m_axi_awcache  = InPort( BitsAXI4CacheWidth )
    s.m_axi_awprot   = InPort( BitsAXI4PortWidth )
    s.m_axi_awqos    = InPort( BitsAXI4QoSWidth )
    s.m_axi_awregion = InPort( BitsAXI4RegionWidth )
    s.m_axi_awuser   = InPort( BitsAXI4UserWidth )
    s.m_axi_awvalid  = InPort( Bits1 )
    s.m_axi_awready  = OutPort( Bits1 )

    # Data write
    s.m_axi_wid    = InPort( BitsAXI4IDWidth )
    s.m_axi_wdata  = InPort( BitsAXI4DataWidth )
    s.m_axi_wstrb  = InPort( BitsAXI4StrbWidth )
    s.m_axi_wlast  = InPort( Bits1 )
    s.m_axi_wuser  = InPort( BitsAXI4UserWidth )
    s.m_axi_wvalid = InPort( Bits1 )
    s.m_axi_wready = OutPort( Bits1 )

    # Addr read
    s.m_axi_arid     = InPort( BitsAXI4IDWidth )
    s.m_axi_araddr   = InPort( BitsAXI4AddrWidth )
    s.m_axi_arlen    = InPort( BitsAXI4LenWidth )
    s.m_axi_arsize   = InPort( BitsAXI4SizeWidth )
    s.m_axi_arburst  = InPort( BitsAXI4BurstWidth )
    s.m_axi_arlock   = InPort( Bits1 )
    s.m_axi_arcache  = InPort( BitsAXI4CacheWidth )
    s.m_axi_arprot   = InPort( BitsAXI4PortWidth )
    s.m_axi_arqos    = InPort( BitsAXI4QoSWidth )
    s.m_axi_arregion = InPort( BitsAXI4RegionWidth )
    s.m_axi_aruser   = InPort( BitsAXI4UserWidth )
    s.m_axi_arvalid  = InPort( Bits1 )
    s.m_axi_arready  = OutPort( Bits1 )

    # Data read
    s.m_axi_rid    = OutPort( BitsAXI4IDWidth )
    s.m_axi_rdata  = OutPort( BitsAXI4DataWidth )
    s.m_axi_rresp  = OutPort( BitsAXI4RespWidth )
    s.m_axi_rlast  = OutPort( Bits1 )
    s.m_axi_ruser  = OutPort( BitsAXI4UserWidth )
    s.m_axi_rvalid = OutPort( Bits1 )
    s.m_axi_rready = InPort( Bits1 )

    s.m_axi_bid    = OutPort( BitsAXI4IDWidth )
    s.m_axi_bresp  = OutPort( BitsAXI4RespWidth )
    s.m_axi_buser  = OutPort( BitsAXI4UserWidth )
    s.m_axi_bvalid = OutPort( Bits1 )
    s.m_axi_bready = InPort( Bits1 )

    # Component

    s.fake_mem = fake_axi4_mem() 

    # Update block

    @s.update
    def xtick_read_addr():

      fake_axi4_mem.read()


