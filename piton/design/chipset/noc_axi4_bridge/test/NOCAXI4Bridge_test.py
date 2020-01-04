'''
==========================================================================
NOCAXI4Bridge_test.py
==========================================================================
Tests for the NoC-AXI4 adapter.

Author : Yanghui Ou
  Date : Jan 1, 2020
'''

from pymtl3 import *
from pymtl3.passes.backends.sverilog import ImportPass

from .NOCAXI4Bridge import NOCAXI4Bridge, AXI4Adapter
from .AXIAdapterFL import AXIAdapterFL
from .AXI4MemCL import AXI4MemRTL
from .packet_srcs import PacketSrcCL
from .packet_sinks import PacketSinkCL
from .piton_packet import mk_piton_wr_req, mk_piton_wr_resp

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, src_pkts, sink_pkts ):

    s.src  = PacketSrcCL ( Bits64, src_pkts  )
    s.sink = PacketSinkCL( Bits64, sink_pkts )
    s.dut  = AXI4Adapter()
    s.mem  = AXI4MemRTL()

    s.src.send  //= s.dut.noc_recv
    s.sink.recv //= s.dut.noc_send

    s.dut.addr_read //= s.mem.addr_read
    s.dut.data_read //= s.mem.data_read

    s.dut.addr_write //= s.mem.addr_write
    s.dut.data_write //= s.mem.data_write
    s.dut.write_resp //= s.mem.write_resp

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.dut.line_trace()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( th, max_cycles=100 ):
  ncycles = 0
  print("")
  print("{:3}:{}".format( ncycles, th.line_trace() ))
  while not th.done() and ncycles < max_cycles:
    th.tick()
    ncycles += 1
    print("{:3}:{}".format( ncycles, th.line_trace() ))

  # Check timeout
  assert ncycles < max_cycles

#-------------------------------------------------------------------------
# Sanity check
#-------------------------------------------------------------------------

def test_import():
  m = NOCAXI4Bridge()
  m.elaborate()
  m = ImportPass()( m )
  m.elaborate()
  m.apply( SimulationPass() )
  m.sim_reset()
  m.tick()
  print()
  print( 'Imported!' )

def test_import_wrapped():
  m = AXI4Adapter()
  m.elaborate()
  m = ImportPass()( m )
  m.elaborate()
  m.apply( SimulationPass() )
  m.sim_reset()
  m.tick()
  print()
  print( 'Imported!' )

def test_import_th():
  m = TestHarness( [], [] )
  m.elaborate()
  m = ImportPass()( m )
  m.elaborate()
  m.apply( SimulationPass() )
  m.sim_reset()
  m.tick()
  print()
  print( 'Imported!' )

#-------------------------------------------------------------------------
# directed test
#-------------------------------------------------------------------------

def test_simple_wr():

  ref  = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  req  = [ mk_piton_wr_req( 0x1000, 64, True, 1, Bits512(0xdeadbeef), dst_x=1, dst_y=1 ) ]
  # resp = [ mk_piton_wr_resp( 1, True ) ]
  resp = [ ref.request( r ) for r in req ]

  th = TestHarness( req, resp )
  th.elaborate()
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th )
