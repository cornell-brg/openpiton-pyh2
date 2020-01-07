"""
========================================================================
packet_srcs.py
========================================================================
Test sources for multi-phit packet.

Author : Yanghui Ou
  Date : Jan 1, 2020
"""

from pymtl3 import *
from .packet_srcs import PacketSrcCL
from .packet_sinks import PacketSinkCL, PacketSinkUnorderedCL
from .piton_packet import *

#-------------------------------------------------------------------------
# TestHarnessSimple
#-------------------------------------------------------------------------

class TestHarnessSimple( Component ):

  def construct( s, SrcType, SinkType, PhitType, src_pkts, sink_pkts ):

    s.src  = SrcType( PhitType, src_pkts  )
    s.sink = SinkType( PhitType, sink_pkts )

    connect( s.src.send, s.sink.recv )

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return f'{s.src.line_trace()} >>> {s.sink.line_trace()}'

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
# test_simple
#-------------------------------------------------------------------------

def test_simple():

  pkts = [
    [ b32(1),  b32(2),  b32(3)           ],
    [ b32(11), b32(12), b32(13)          ],
    [ b32(21), b32(22), b32(23), b32(24) ],
  ]

  th = TestHarnessSimple( PacketSrcCL, PacketSinkCL, Bits64, pkts, pkts )
  th.elaborate()
  th.apply( SimulationPass() )
  run_sim( th )

#-------------------------------------------------------------------------
# test_simple
#-------------------------------------------------------------------------

def test_unorder():

  pkts = [
    mk_piton_rd_req( 0x2000, 64, True, 23 ),
    mk_piton_wr_req( 0x4000, 64, False, 23, b512(0xdeadbeefcafebabe) ),
    mk_piton_wr_resp( 23, False ),
  ]

  th = TestHarnessSimple( PacketSrcCL, PacketSinkUnorderedCL, Bits64, pkts, pkts[::-1] )
  th.elaborate()
  th.apply( SimulationPass() )
  run_sim( th )
