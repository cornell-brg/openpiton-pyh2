"""
========================================================================
packet_srcs.py
========================================================================
Test sources for multi-phit packet.

Author : Yanghui Ou
  Date : Jan 1, 2020
"""

from collections import deque

from pymtl3 import *
from pymtl3.stdlib.ifcs import RecvCL2SendRTL, SendIfcRTL

#-------------------------------------------------------------------------
# TestSrcCL
#-------------------------------------------------------------------------
# TODO: initial delay and interval delay

STATE_HEADER = 0
STATE_BODY   = 1

class PacketSrcCL( Component ):

  def construct( s, PhitType, pkts ):

    s.send    = NonBlockingCallerIfc( PhitType )
    s.pkts    = deque( pkts )
    s.state   = STATE_HEADER
    s.cur_pkt = []
    s.cur_idx = 0

    @s.update
    def up_src_send():
      if not s.reset:

        if s.state == STATE_HEADER:
          if s.send.rdy() and s.pkts:

            # Send the header phit
            s.cur_pkt = s.pkts.popleft()
            s.cur_idx = 0
            s.send( s.cur_pkt[ s.cur_idx ] )
            s.cur_idx += 1

            # If the packet is header only
            if s.cur_idx == len( s.cur_pkt ):
              s.state = STATE_HEADER
            else:
              s.state = STATE_BODY

        elif s.state == STATE_BODY:
          if s.send.rdy() and s.cur_pkt:

            # Send the body phit
            s.send( s.cur_pkt[ s.cur_idx ] )
            s.cur_idx += 1

            # When current packet is sent, Go to header state
            if s.cur_idx == len( s.cur_pkt ):
              s.state = STATE_HEADER

        else:
          assert False, "Undefined state!"

  def done( s ):
    return not s.pkts and s.state == STATE_HEADER

  # Line trace

  def line_trace( s ):
    return "{}".format( s.send )
