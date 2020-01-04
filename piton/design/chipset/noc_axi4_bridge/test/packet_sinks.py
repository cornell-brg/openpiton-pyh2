"""
========================================================================
packet_sinks.py
========================================================================
Test sinks with CL and RTL interfaces.

Author : Yanghui Ou
  Date : Jan 1, 2019
"""

from pymtl3 import *
from pymtl3.stdlib.ifcs import RecvIfcRTL, RecvRTL2SendCL

#-------------------------------------------------------------------------
# TestSinkCL
#-------------------------------------------------------------------------
# TODO: initial delay and interval delay

STATE_HEADER = 0
STATE_BODY   = 1

class PacketSinkCL( Component ):

  def construct( s, PhitType, pkts, cmp_fn=lambda a, b : a == b ):

    print( pkts )

    s.recv.Type = PhitType

    s.idx          = 0
    s.pkts         = list( pkts )
    s.cmp_fn       = cmp_fn
    s.error_msg    = ''

    s.all_msg_recved = False
    s.done_flag      = False

    s.state   = STATE_HEADER
    s.cur_pkt = []

    s.buf_pkt = []
    s.buf_idx = 0

    s.recv_called = False

    @s.update
    def up_sink_count():
      # Raise exception at the start of next cycle so that the errored
      # line trace gets printed out
      if s.error_msg:
        raise Exception( s.error_msg )

      # Tick one more cycle after all message is received so that the
      # exception gets thrown
      if s.all_msg_recved:
        s.done_flag = True

      if s.idx >= len( s.pkts ):
        s.all_msg_recved = True

    # Constraints

    s.add_constraints(
      U( up_sink_count ) < M( s.recv ),
      U( up_sink_count ) < M( s.recv.rdy )
    )

  @non_blocking( lambda s: True )
  def recv( s, phit ):

    # Sanity check

    if s.idx >= len( s.pkts ):
      s.error_msg = ( 'Test Sink received more pkts than expected!\n'
                      f'Received : {msg}' )
      return

    # State transition

    if s.state == STATE_HEADER:
      assert not s.buf_pkt
      assert s.buf_idx == 0
      s.cur_pkt = s.pkts[ s.idx ]
      s.buf_pkt.append( phit )
      s.buf_idx += 1

      if s.buf_idx != len( s.cur_pkt ):
        s.state = STATE_BODY

    elif s.state == STATE_BODY:
      s.buf_pkt.append( phit )
      s.buf_idx += 1

      if s.buf_idx == len( s.cur_pkt ):
        s.state = STATE_HEADER

    else:
      assert False, "Undefined state!"

    # Correctness check

    if s.cur_pkt and s.buf_idx == len( s.cur_pkt ):

      for i in range( len( s.cur_pkt ) ):
        if not s.cmp_fn( s.buf_pkt[i], s.cur_pkt[i] ):
          s.error_msg = (
            f'Test sink {s} received WRONG message!\n'
            f'Expected : { s.pkts[ s.idx ] }\n'
            f'Received : { s.buf_pkt }\n'
            f'Phit {i} does not match'
          )
          return

      s.buf_pkt = []
      s.buf_idx = 0
      s.idx += 1

  def done( s ):
    return s.done_flag

  # Line trace
  def line_trace( s ):
    return f'{s.recv}({s.state})'
