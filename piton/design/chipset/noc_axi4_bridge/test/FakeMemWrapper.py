'''
==========================================================================
 FakeMemWrapper.py
==========================================================================
'''
from pytml3 import *

from .fake_axi4_mem.py import fake_axi4_mem

class FakeMemWrapper( Component ):

  def construct( s ):
    s.m_axis_awid   = InPort( BitsN )
    s.m_axis_awaddr = InPort( BitsN )
    ...


    s.fake_mem = fake_axi4_mem() 

    @s.update
    def xtick():
      fake_axi4_mem.read()


