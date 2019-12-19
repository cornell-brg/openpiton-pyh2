#=========================================================================
# NOCAXI4Bridge.py
#=========================================================================
# PyMTL3 wrapper of noc_axi4_bridge

from pymtl3 import *
from pymtl3.passes.backends.sverilog import ImportConfigs
from pymtl3.passes.backends.sverilog.util.utility import get_dir

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

class NOCAXI4Bridge( Component ):
  def construct( s ):

    s.uart_boot_en = InPort( Bits1 )
    s.phy_init_done = InPort( Bits1 )

    s.src_bridge_vr_noc2_val = InPort( Bits1 )
    s.src_bridge_vr_noc2_dat = InPort( BitsNOCDataWidth )
    s.src_bridge_vr_noc2_rdy = OutPort( Bits1 )
    s.bridge_dst_vr_noc3_val = OutPort( Bits1 )
    s.bridge_dst_vr_noc3_dat = OutPort( BitsNOCDataWidth )
    s.bridge_dst_vr_noc3_rdy = InPort( Bits1 )

    s.m_axi_awid = OutPort( BitsAXI4IDWidth )
    s.m_axi_awaddr = OutPort( BitsAXI4AddrWidth )
    s.m_axi_awlen = OutPort( BitsAXI4LenWidth )
    s.m_axi_awsize = OutPort( BitsAXI4SizeWidth )
    s.m_axi_awburst = OutPort( BitsAXI4BurstWidth )
    s.m_axi_awlock = OutPort( Bits1 )
    s.m_axi_awcache = OutPort( BitsAXI4CacheWidth )
    s.m_axi_awprot = OutPort( BitsAXI4PortWidth )
    s.m_axi_awqos = OutPort( BitsAXI4QoSWidth )
    s.m_axi_awregion = OutPort( BitsAXI4RegionWidth )
    s.m_axi_awuser = OutPort( BitsAXI4UserWidth )
    s.m_axi_awvalid = OutPort( Bits1 )
    s.m_axi_awready = InPort( Bits1 )

    s.m_axi_wid =  OutPort( BitsAXI4IDWidth )
    s.m_axi_wdata = OutPort( BitsAXI4DataWidth )
    s.m_axi_wstrb = OutPort( BitsAXI4StrbWidth )
    s.m_axi_wlast = OutPort( Bits1 )
    s.m_axi_wuser = OutPort( BitsAXI4UserWidth )
    s.m_axi_wvalid = OutPort( Bits1 )
    s.m_axi_wready = InPort( Bits1 )

    s.m_axi_arid =  OutPort( BitsAXI4IDWidth )
    s.m_axi_araddr = OutPort( BitsAXI4AddrWidth )
    s.m_axi_arlen = OutPort( BitsAXI4LenWidth )
    s.m_axi_arsize = OutPort( BitsAXI4SizeWidth )
    s.m_axi_arburst = OutPort( BitsAXI4BurstWidth )
    s.m_axi_arlock = OutPort( Bits1 )
    s.m_axi_arcache = OutPort( BitsAXI4CacheWidth )
    s.m_axi_arprot = OutPort( BitsAXI4PortWidth )
    s.m_axi_arqos = OutPort( BitsAXI4QoSWidth )
    s.m_axi_arregion = OutPort( BitsAXI4RegionWidth )
    s.m_axi_aruser = OutPort( BitsAXI4UserWidth )
    s.m_axi_arvalid = OutPort( Bits1 )
    s.m_axi_arready = InPort( Bits1 )

    s.m_axi_rid =  InPort( BitsAXI4IDWidth )
    s.m_axi_rdata = InPort( BitsAXI4DataWidth )
    s.m_axi_rresp = InPort( BitsAXI4RespWidth )
    s.m_axi_rlast = InPort( Bits1 )
    s.m_axi_ruser = InPort( BitsAXI4UserWidth )
    s.m_axi_rvalid = InPort( Bits1 )
    s.m_axi_rready = OutPort( Bits1 )

    s.m_axi_bid =  InPort( BitsAXI4IDWidth )
    s.m_axi_bresp = InPort( BitsAXI4RespWidth )
    s.m_axi_buser = InPort( BitsAXI4UserWidth )
    s.m_axi_bvalid = InPort( Bits1 )
    s.m_axi_bready = OutPort( Bits1 )
 
    s.config_sverilog_import = ImportConfigs(
      # Name of the top Verilog module
      top_module = 'noc_axi4_bridge', # File containing the top module
      # vl_src = "$PITON_ROOT/piton/design/chipset/noc_axi4_bridge/rtl/noc_axi4_bridge.v",
      vl_Wno_list = ['WIDTH', 'UNSIGNED', 'CASEINCOMPLETE', 'INITIALDLY',
                     'COMBDLY', 'UNOPTFLAT', 'STMTDLY', 'PINMISSING'
      ],
      # vl_flist = '$PITON_ROOT/build/manycore/rel-0.1/flist',
      vl_flist = '$PITON_ROOT/piton/design/chipset/noc_axi4_bridge/rtl/Flist.noc_axi4_bridge.import',
      vl_include = [
        # mc_define.h
        '$PITON_ROOT/piton/design/chipset/include/',
        # module lookup
        '$PITON_ROOT/piton/design/chipset/noc_axi4_bridge/rtl/',
        '$PITON_ROOT/piton/design/include/',
        '$PITON_ROOT/piton/design/chipset/rtl/',
        '$PITON_ROOT/piton/design/common/rtl/',
      ],

      # Map python names to Verilog names
      port_map = {
        "clk" : "clk",
        "reset" : "rst_n",
        "uart_boot_en" : "uart_boot_en",
        "phy_init_done" : "phy_init_done" ,
        "src_bridge_vr_noc2_val" : "src_bridge_vr_noc2_val",
        "src_bridge_vr_noc2_dat" : "src_bridge_vr_noc2_dat",
        "src_bridge_vr_noc2_rdy" : "src_bridge_vr_noc2_rdy",
        "bridge_dst_vr_noc3_val" : "bridge_dst_vr_noc3_val",
        "bridge_dst_vr_noc3_dat" : "bridge_dst_vr_noc3_dat",
        "bridge_dst_vr_noc3_rdy" : "bridge_dst_vr_noc3_rdy",

        "m_axi_awid" : "m_axi_awid",
        "m_axi_awaddr" : "m_axi_awaddr",
        "m_axi_awlen" : "m_axi_awlen",
        "m_axi_awsize" : "m_axi_awsize",
        "m_axi_awburst" : "m_axi_awburst",
        "m_axi_awlock" : "m_axi_awlock",
        "m_axi_awcache" : "m_axi_awcache",
        "m_axi_awprot" : "m_axi_awprot",
        "m_axi_awqos" : "m_axi_awqos",
        "m_axi_awregion" : "m_axi_awregion",
        "m_axi_awuser" : "m_axi_awuser",
        "m_axi_awvalid" : "m_axi_awvalid",
        "m_axi_awready" : "m_axi_awready",

        "m_axi_wid" : "m_axi_wid",
        "m_axi_wdata" : "m_axi_wdata",
        "m_axi_wstrb" : "m_axi_wstrb",
        "m_axi_wlast" : "m_axi_wlast",
        "m_axi_wuser" : "m_axi_wuser",
        "m_axi_wvalid" : "m_axi_wvalid",
        "m_axi_wready" : "m_axi_wready",

        "m_axi_arid" : "m_axi_arid",
        "m_axi_araddr" : "m_axi_araddr",
        "m_axi_arlen" : "m_axi_arlen",
        "m_axi_arsize" : "m_axi_arsize",
        "m_axi_arburst" : "m_axi_arburst",
        "m_axi_arlock" : "m_axi_arlock",
        "m_axi_arcache" : "m_axi_arcache",
        "m_axi_arprot" : "m_axi_arprot",
        "m_axi_arqos" : "m_axi_arqos",
        "m_axi_arregion" : "m_axi_arregion",
        "m_axi_aruser" : "m_axi_aruser",
        "m_axi_arvalid" : "m_axi_arvalid",
        "m_axi_arready" : "m_axi_arready",

        "m_axi_rid" : "m_axi_rid",
        "m_axi_rdata" : "m_axi_rdata",
        "m_axi_rresp" : "m_axi_rresp",
        "m_axi_rlast" : "m_axi_rlast",
        "m_axi_ruser" : "m_axi_ruser",
        "m_axi_rvalid" : "m_axi_rvalid",
        "m_axi_rready" : "m_axi_rready",

        "m_axi_bid" : "m_axi_bid",
        "m_axi_bresp" : "m_axi_bresp",
        "m_axi_buser" : "m_axi_buser",
        "m_axi_bvalid" : "m_axi_bvalid",
        "m_axi_bready" : "m_axi_bready",
      }
    )
