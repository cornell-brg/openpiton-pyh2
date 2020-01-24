'''
==========================================================================
NOCAXI4Bridge_test.py
==========================================================================
Tests for the NoC-AXI4 adapter.

Author : Yanghui Ou
  Date : Jan 1, 2020
'''

import hypothesis
from hypothesis import strategies as st
from hypothesis import Phase
from pymtl3 import *
from pymtl3.passes.backends.sverilog import ImportPass, ImportConfigs

from .NOCAXI4Bridge import NOCAXI4Bridge, AXI4Adapter
from .AXIAdapterFL import AXIAdapterFL
from .AXI4MemCL import AXI4MemRTL
from .packet_srcs import PacketSrcCL
from .packet_sinks import PacketSinkUnorderedCL as PacketSinkCL
from .piton_packet import *

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, src_pkts, sink_pkts ):

    s.src  = PacketSrcCL ( Bits64, src_pkts  )
    s.sink = PacketSinkCL( Bits64, sink_pkts )
    s.dut  = AXI4Adapter()
    s.mem  = AXI4MemRTL( delay_ar=1, delay_dr=4, delay_aw=1, delay_dw=4, delay_resp=2 )

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
    # return s.mem.line_trace()

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

  if th.done():
    print( )

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

def test_simple_wr_rd():

  ref  = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  req  = [
    mk_piton_wr_req( 0x1000, 2, False, 1, Bits512(0xdeadbeef), dst_x=1, dst_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 1 ),
  ]
  # resp = [ mk_piton_wr_resp( 1, True ) ]
  resp = [ ref.request( r ) for r in req ]

  th = TestHarness( req, resp )
  th.elaborate()
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th )

def test_wr_rd_hi():

  ref  = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  req  = [
    mk_piton_wr_req( 0x1000, 64, False, 1, Bits512(1 << 64*1), dst_x=1, dst_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 1 ),
  ]
  # resp = [ mk_piton_wr_resp( 1, True ) ]
  resp = [ ref.request( r ) for r in req ]

  th = TestHarness( req, resp )
  th.elaborate()
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th )

# This counter example was found by pyh2
def test_stress():
  ref = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  req = [
    mk_piton_wr_req( 0x1000, 64, False, 0, Bits512(0), src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_wr_req( 0x1000, 64, False, 0, Bits512(0), src_x=1, src_y=1 ),
    mk_piton_wr_req( 0x1000, 64, False, 0, Bits512(0), src_x=1, src_y=1 ),
    mk_piton_wr_req( 0x1000, 64, False, 0, Bits512(0), src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
  ]
  resp = [ ref.request( r ) for r in req ]
  print( len(resp) )
  assert len(req)==len(resp)

  th = TestHarness( req, resp )
  th.elaborate()
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th, max_cycles=500 )

def test_stress2():
  ref = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  req = [
    mk_piton_wr_req( 0x1000, 64, False, 0, Bits512(0xfaceb00c), src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_rd_req( 0x1000, 64, False, 0, src_x=1, src_y=1 ),
    mk_piton_wr_req( 0x1000, 64, False, 0, Bits512(0x8badf00d), src_x=1, src_y=1 ),
  ]
  resp = [ ref.request( r ) for r in req ]
  print( len(resp) )
  assert len(req)==len(resp)

  th = TestHarness( req, resp )
  th.elaborate()
  # th.dut.adapter.config_sverilog_import = ImportConfigs( vl_trace=True )
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th, max_cycles=500 )

#-------------------------------------------------------------------------
# has_wr_req
#-------------------------------------------------------------------------
# Helper function that checks if there is at least one wr request in the
# list

def is_wr_req( req ):
  return req[0][ MTYPE ] == STORE_MEM or req[0][ MTYPE ] == NC_STORE_REQ

def has_wr_req( reqs ):
  if not is_wr_req( reqs[0] ):
    return False

  for r in reqs:
    if is_wr_req(r):
      return True

  return False

#-------------------------------------------------------------------------
# pyh2 test
#-------------------------------------------------------------------------

@hypothesis.settings(
  deadline     = None,
  max_examples = 1000,
  phases = [ Phase.generate ]
)
@hypothesis.given(
  reqs = st.lists( piton_reqs(), min_size=2, max_size=100 )
)
def test_hypothesis_gen_only( reqs ):
  hypothesis.assume( has_wr_req( reqs ) )
  # hypothesis.assume( len( reqs ) >= 2 )
  ref  = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  resps = [ ref.request( r ) for r in reqs ]
  th = TestHarness( reqs, resps )
  th.elaborate()
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th, max_cycles = 500 )

#-------------------------------------------------------------------------
# pyh2 test
#-------------------------------------------------------------------------

@hypothesis.settings(
  deadline     = None,
  max_examples = 1000,
)
@hypothesis.given(
  reqs = st.lists( piton_reqs(), min_size=2, max_size=20 )
)
def test_hypothesis_shrink( reqs ):
  hypothesis.assume( has_wr_req( reqs ) )
  # hypothesis.assume( len( reqs ) >= 2 )
  ref  = AXIAdapterFL()
  ref.elaborate()
  ref.apply( SimulationPass() )

  resps = [ ref.request( r ) for r in reqs ]
  th = TestHarness( reqs, resps )
  th.elaborate()
  th = ImportPass()( th )
  th.elaborate()
  th.apply( SimulationPass() )
  th.sim_reset()
  run_sim( th, max_cycles = 500 )
