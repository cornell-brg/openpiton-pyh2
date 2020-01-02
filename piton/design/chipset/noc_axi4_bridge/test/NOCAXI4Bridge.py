#=========================================================================
# NOCAXI4Bridge.py
#=========================================================================
# PyMTL3 wrapper of noc_axi4_bridge

from pymtl3 import *
from pymtl3.passes.backends.sverilog import ImportConfigs
from pymtl3.passes.backends.sverilog.util.utility import get_dir
from pymtl3.stdlib.ifcs import SendIfcRTL, RecvIfcRTL, InValRdyIfc, OutValRdyIfc

from .axi_msgs import *

# BitsNOCDataWidth = Bits64
# BitsAXI4IDWidth  = Bits6
# BitsAXI4AddrWidth = Bits64
# BitsAXI4LenWidth = Bits8
# BitsAXI4SizeWidth = Bits3
# BitsAXI4BurstWidth = Bits2
# BitsAXI4CacheWidth = Bits4
# BitsAXI4PortWidth = Bits3
# BitsAXI4QoSWidth = Bits4
# BitsAXI4RegionWidth = Bits4
# BitsAXI4UserWidth = Bits11
# BitsAXI4DataWidth = Bits512
# BitsAXI4RespWidth = Bits2
# BitsAXI4StrbWidth = Bits64

#-------------------------------------------------------------------------
# NOCAXI4Bridge
#-------------------------------------------------------------------------
# Imported module

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

#-------------------------------------------------------------------------
# ValRdy2Send
#-------------------------------------------------------------------------

class ValRdy2Send( Component ):

  def construct( s, MsgType ):

    s.in_ = InValRdyIfc( MsgType )
    s.out = SendIfcRTL( MsgType ) 

    @s.update
    def comb_logic0():
      s.in_.rdy = s.out.rdy

    @s.update
    def comb_logic1():
      s.out.en  = s.out.rdy & s.in_.val
    
    @s.update
    def comb_logic2(): 
      s.out.msg = s.in_.msg
  
  def line_trace( s ):
    return "{} | {}".format( s.in_, s.out )

#-------------------------------------------------------------------------
# EnRdy2ValRdy
#-------------------------------------------------------------------------

class Recv2ValRdy( Component ):

  def construct( s, MsgType ):

    s.in_ = RecvIfcRTL( MsgType )
    s.out = OutValRdyIfc( MsgType ) 

    @s.update
    def comb_logic0():
      s.in_.rdy = s.out.rdy
    
    @s.update
    def comb_logic1():
      s.out.val = s.in_.en
    
    @s.update
    def comb_logic2(): 
      s.out.msg = s.in_.msg
  
  def line_trace( s ):
    return "{} | {}".format( s.in_, s.out )

#-------------------------------------------------------------------------
# AXI4Adapter
#-------------------------------------------------------------------------
# Wrap the imported module with send/recv interface

class AXI4Adapter( Component ):

  def construct( s ):

    # NoC interface

    s.noc_recv = RecvIfcRTL( Bits64 )
    s.noc_send = SendIfcRTL( Bits64 )

    # AXI4 interface

    s.addr_read = SendIfcRTL( AXI4AddrRead )
    s.data_read = RecvIfcRTL( AXI4DataRead )

    s.addr_write = SendIfcRTL( AXI4AddrWrite )
    s.data_write = SendIfcRTL( AXI4DataWrite )
    s.write_resp = RecvIfcRTL( AXI4WriteResp )

    # Imported module

    s.adapter = NOCAXI4Bridge()

    # val/rdy to en/rdy adapters
    s.noc_recv_2_vr = Recv2ValRdy( Bits64 )( in_ = s.noc_recv )
    connect( s.noc_recv_2_vr.out.val, s.adapter.src_bridge_vr_noc2_val )
    connect( s.noc_recv_2_vr.out.rdy, s.adapter.src_bridge_vr_noc2_rdy )
    connect( s.noc_recv_2_vr.out.msg, s.adapter.src_bridge_vr_noc2_dat )

    s.noc_vr_2_send = ValRdy2Send( Bits64 )( out = s.noc_send )
    s.noc_vr_2_send.in_.val //= s.adapter.bridge_dst_vr_noc3_val
    s.noc_vr_2_send.in_.rdy //= s.adapter.bridge_dst_vr_noc3_rdy
    s.noc_vr_2_send.in_.msg //= s.adapter.bridge_dst_vr_noc3_dat
    
    s.ar_2_send = ValRdy2Send( AXI4AddrRead )( out = s.addr_read )
    s.ar_2_send.in_.val          //= s.adapter.m_axi_arvalid
    s.ar_2_send.in_.rdy          //= s.adapter.m_axi_arready
    s.ar_2_send.in_.msg.arid     //= s.adapter.m_axi_arid
    s.ar_2_send.in_.msg.araddr   //= s.adapter.m_axi_araddr
    s.ar_2_send.in_.msg.arlen    //= s.adapter.m_axi_arlen
    s.ar_2_send.in_.msg.arsize   //= s.adapter.m_axi_arsize
    s.ar_2_send.in_.msg.arburst  //= s.adapter.m_axi_arburst
    s.ar_2_send.in_.msg.arlock   //= s.adapter.m_axi_arlock
    s.ar_2_send.in_.msg.arcache  //= s.adapter.m_axi_arcache
    s.ar_2_send.in_.msg.arprot   //= s.adapter.m_axi_arprot
    s.ar_2_send.in_.msg.arqos    //= s.adapter.m_axi_arqos
    s.ar_2_send.in_.msg.arregion //= s.adapter.m_axi_arregion
    s.ar_2_send.in_.msg.aruser   //= s.adapter.m_axi_aruser

    s.recv_2_dr = Recv2ValRdy( AXI4DataRead )( in_ = s.data_read )
    s.recv_2_dr.out.val       //= s.adapter.m_axi_rvalid
    s.recv_2_dr.out.rdy       //= s.adapter.m_axi_rready
    s.recv_2_dr.out.msg.rid   //= s.adapter.m_axi_rid
    s.recv_2_dr.out.msg.rdata //= s.adapter.m_axi_rdata
    s.recv_2_dr.out.msg.rresp //= s.adapter.m_axi_rresp
    s.recv_2_dr.out.msg.rlast //= s.adapter.m_axi_rlast
    s.recv_2_dr.out.msg.ruser //= s.adapter.m_axi_ruser

    s.aw_2_send = ValRdy2Send( AXI4AddrWrite )( out = s.addr_write )
    s.aw_2_send.in_.val          //= s.adapter.m_axi_awvalid
    s.aw_2_send.in_.rdy          //= s.adapter.m_axi_awready
    s.aw_2_send.in_.msg.awid     //= s.adapter.m_axi_awid
    s.aw_2_send.in_.msg.awaddr   //= s.adapter.m_axi_awaddr
    s.aw_2_send.in_.msg.awlen    //= s.adapter.m_axi_awlen
    s.aw_2_send.in_.msg.awsize   //= s.adapter.m_axi_awsize
    s.aw_2_send.in_.msg.awburst  //= s.adapter.m_axi_awburst
    s.aw_2_send.in_.msg.awlock   //= s.adapter.m_axi_awlock
    s.aw_2_send.in_.msg.awcache  //= s.adapter.m_axi_awcache
    s.aw_2_send.in_.msg.awprot   //= s.adapter.m_axi_awprot
    s.aw_2_send.in_.msg.awqos    //= s.adapter.m_axi_awqos
    s.aw_2_send.in_.msg.awregion //= s.adapter.m_axi_awregion
    s.aw_2_send.in_.msg.awuser   //= s.adapter.m_axi_awuser

    s.dw_2_send = ValRdy2Send( AXI4DataWrite )( out = s.data_write )
    s.dw_2_send.in_.val       //= s.adapter.m_axi_wvalid
    s.dw_2_send.in_.rdy       //= s.adapter.m_axi_wready
    s.dw_2_send.in_.msg.wid   //= s.adapter.m_axi_wid
    s.dw_2_send.in_.msg.wdata //= s.adapter.m_axi_wdata
    s.dw_2_send.in_.msg.wstrb //= s.adapter.m_axi_wstrb
    s.dw_2_send.in_.msg.wlast //= s.adapter.m_axi_wlast
    s.dw_2_send.in_.msg.wuser //= s.adapter.m_axi_wuser

    s.recv_2_resp = Recv2ValRdy( AXI4WriteResp )( in_ = s.write_resp )
    s.recv_2_resp.out.val       //= s.adapter.m_axi_bvalid
    s.recv_2_resp.out.rdy       //= s.adapter.m_axi_bready
    s.recv_2_resp.out.msg.bid   //= s.adapter.m_axi_bid
    s.recv_2_resp.out.msg.bresp //= s.adapter.m_axi_bresp
    s.recv_2_resp.out.msg.buser //= s.adapter.m_axi_buser

  # Line trace

  def line_trace( s ):
    return f'{s.noc_recv}(){s.noc_send}'
