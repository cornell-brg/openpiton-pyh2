from pymtl3 import *

class axi4_read_req:
    def __init__(self, arid : Bits6,
                       araddr : Bits64,
                       arlen : Bits8,
                       arsize : Bits3,
                       arburst : Bits2,
                       arlock : Bits1,
                       arcache : Bits4,
                       arprot : Bits3,
                       arqos : Bits4,
                       arregion : Bits4,
                       aruser : Bits11    ):
        self.arid = arid
        self.araddr = araddr
        self.arlen = arlen
        self.arsize = arsize
        self.arburst = arburst
        self.arlock = arlock
        self.arcache = arcache
        self.arprot = arprot
        self.arqos = arqos
        self.arregion = arregion
        self.aruser = aruser

class axi4_read_resp:
    def __init__(self,
                 rid : Bits6,
                 rdata : Bits512,
                 rresp : Bits2,
                 rlast : Bits1,
                 ruser : Bits11 ):
        self.rid = rid
        self.rdata = rdata
        self.rresp = rresp
        self.rlast = rlast
        self.ruser = ruser

class axi4_write_req:
    def __init__(self,
                 awid : Bits6,
                 awaddr : Bits64,
                 awlen : Bits8,
                 awsize : Bits3,
                 awburst : Bits2,
                 awlock : Bits1,
                 awcache : Bits4,
                 awprot : Bits3,
                 awqos : Bits4,
                 awregion : Bits4,
                 awuser : Bits11,
                 wid : Bits6,
                 wdata : Bits512,
                 wstrb : Bits64,
                 wlast : Bits1,
                 wuser : Bits11):
        self.awid = awid
        self.awaddr = awaddr
        self.awlen = awlen
        self.awsize = awsize
        self.awburst = awburst
        self.awlock = awlock
        self.awcache = awcache
        self.awprot = awprot
        self.awqos = awqos
        self.awregion = awregion
        self.awuser = awuser
        self.wid = wid
        self.wdata = wdata
        self.wstrb = wstrb
        self.wlast = wlast
        self.wuser = wuser

class axi4_write_resp:
    def __init__(self,
                 bid : Bits6,
                 bresp : Bits2,
                 buser : Bits):
        self.bid = bid
        self.bresp = bresp
        self.buser = buser

class fake_axi4_mem:
    def __init__(self):
        self.mem = {}

    def read(self, req : axi4_read_req) -> axi4_read_resp:
        index = req.araddr >> 6
        return axi4_read_resp(req.arid, self.mem[index], Bits2(0), Bits1(1), req.aruser)

    def write(self, req: axi4_write_req) -> axi4_write_resp:
        index = req.awaddr >> 6
        write_data = self.mem[index]
        for i in range(64):
            if req.wstrb[i] == Bits1(1):
                write_data[i*8:i*8+63] = req.wdata[i*8:i*8+63]
        self.mem[index] = write_data
        return axi4_write_resp(req.awid, Bits2(0), req.buser)

