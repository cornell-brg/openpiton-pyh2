
from pymtl3 import *
from pymtl3.passes.backends.sverilog import ImportPass

from .NOCAXI4Bridge import NOCAXI4Bridge, AXI4Adapter

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
