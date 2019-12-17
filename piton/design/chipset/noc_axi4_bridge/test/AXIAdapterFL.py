'''
==========================================================================
 AXIAdapterFL.py
==========================================================================
Functional level model of AXI adapter with openpiton noc interface.

Author: Yanghui Ou
  Date: Dec 17, 2019

'''
from pymtl3 import *
from pymtl3.stdlib.fl import MemoryFL


class AXIAdapterFL( Component ):

  def construct( s ):
    ...

  def request( s, pkt ):
    ...

  def response( s ):
    ...
