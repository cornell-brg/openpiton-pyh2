from pymtl3.passes.backends.sverilog import ImportPass

from .NOCAXI4Bridge import NOCAXI4Bridge

def test_import():
  m = NOCAXI4Bridge()
  m.elaborate()
  m = ImportPass()( m )
