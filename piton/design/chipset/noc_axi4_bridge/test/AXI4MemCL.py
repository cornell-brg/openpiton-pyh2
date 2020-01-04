'''
==========================================================================
AXI4MemCL.py
==========================================================================
A CL memory with AXI4 interface.

Author : Yanghui Ou
  Date : Jan 1, 2020
'''

from pymtl3 import *
from pymtl3.stdlib.fl import MemoryFL
from pymtl3.stdlib.cl.DelayPipeCL import DelayPipeSendCL, DelayPipeDeqCL
from pymtl3.stdlib.ifcs import SendIfcRTL, RecvIfcRTL, RecvCL2SendRTL, RecvRTL2SendCL

from .axi_msgs import *

class AXI4MemCL( Component ):

  def construct( s, delay_ar=1, delay_dr=1,
                 delay_aw=1, delay_dw=1, delay_resp=1 ):

    # Interface

    s.addr_read = NonBlockingCalleeIfc( AXI4AddrRead )
    s.data_read = NonBlockingCallerIfc( AXI4DataRead )

    s.addr_write = NonBlockingCalleeIfc( AXI4AddrWrite )
    s.data_write = NonBlockingCalleeIfc( AXI4DataWrite )
    s.write_resp = NonBlockingCallerIfc( AXI4WriteResp )

    # Delay pipes

    s.pipe_ar = DelayPipeDeqCL ( delay = delay_ar )( enq = s.addr_read )
    s.pipe_dr = DelayPipeSendCL( delay = delay_dr )( send = s.data_read )

    s.pipe_aw   = DelayPipeDeqCL ( delay = delay_aw   )( enq = s.addr_write )
    s.pipe_dw   = DelayPipeDeqCL ( delay = delay_dr   )( enq = s.data_write )
    s.pipe_resp = DelayPipeSendCL( delay = delay_resp )( send = s.write_resp )

    # Internal memory
    # TODO: parametrize

    s.mem = MemoryFL()

    # State variables

    s.aw_msg   = None
    s.dw_msg   = None
    s.ar_msg = None

    # Update blocks
    # TODO: support streaming

    @s.update
    def xtick():

      # Assemble write request

      if s.pipe_aw.deq.rdy():
        s.aw_msg = s.pipe_aw.deq()

      if s.pipe_dw.deq.rdy():
        s.dw_msg = s.pipe_dw.deq()

      # Write memory if write request if ready

      if s.aw_msg and s.dw_msg:
        # Write memory
        # TODO: calculate aligned address
        wr_addr = s.aw_msg.awaddr
        wr_data = s.mem.read( wr_addr, 64 )

        for i in range( 64 ):
          wr_data[i*8:(i+1)*8] = s.dw_msg.wdata[i*8:(i+1)*8]

        s.mem.write( wr_addr, 64, wr_data )

        # Send response and clear message
        resp = AXI4WriteResp( s.aw_msg.awid, b2(0), s.aw_msg.awuser )
        s.pipe_resp.enq( resp )

        s.aw_msg = None
        s.dw_msg = None

      # Assemble read request

      if s.pipe_ar.deq.rdy():
        s.ar_msg = s.pipe_ar.deq()

      # Read memory if read request is ready

      if s.ar_msg:
        # Read memory
        # TODO: calculate aligned address
        rd_addr = s.ar_msg.araddr
        rd_data = s.mem.read( rd_addr, 64 )

        # Send read response and clear message
        resp = AXI4DataRead( s.ar_msg.arid, rd_data, b2(0), b1(1), s.ar_msg.aruser )
        s.pipe_dr.enq( resp )
        s.ar_msg = None

  # TODO
  def line_trace( s ):
    return ''

#-------------------------------------------------------------------------
# AXI4MemRTL
#-------------------------------------------------------------------------
# Wrap the CL memory with RTL interface

class AXI4MemRTL( Component ):

  def construct( s, delay_ar=1, delay_dr=1,
                 delay_aw=1, delay_dw=1, delay_resp=1 ):

    # Interface

    s.addr_read = RecvIfcRTL( AXI4AddrRead )
    s.data_read = SendIfcRTL( AXI4DataRead )

    s.addr_write = RecvIfcRTL( AXI4AddrWrite )
    s.data_write = RecvIfcRTL( AXI4DataWrite )
    s.write_resp = SendIfcRTL( AXI4WriteResp )

    # Internal memory

    s.mem_cl = AXI4MemCL( delay_ar, delay_dr, delay_aw, delay_dw, delay_resp )

    # Adapters

    s.adapter_ar = RecvRTL2SendCL( AXI4AddrRead )(
      recv = s.addr_read,
      send = s.mem_cl.addr_read,
    )

    s.adapter_dr = RecvCL2SendRTL( AXI4DataRead )(
      recv = s.mem_cl.data_read,
      send = s.data_read,
    )

    s.adapter_aw = RecvRTL2SendCL( AXI4AddrWrite )(
      recv = s.addr_write,
      send = s.mem_cl.addr_write,
    )

    s.adapter_dw = RecvRTL2SendCL( AXI4DataWrite )(
      recv = s.data_write,
      send = s.mem_cl.data_write,
    )

    s.adapter_resp = RecvCL2SendRTL( AXI4WriteResp )(
      recv = s.mem_cl.write_resp,
      send = s.write_resp,
    )

  # TODO
  def line_trace( s ):
    return ''

