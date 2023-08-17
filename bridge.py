class Bridge:
    def __init__(self, bridgeName, id, flag):
        self.name = bridgeName
        self.id = id
        self.root = self
        self.rootDist = 0

        self.ports = []
        self.portStatus = [1]*len(self.ports)

        self.rp = None
        self.dp = []
        self.np = None
        
        self.msg = []
        self.flag = flag

        self.change = False

    def connections(self, LAN):
        self.ports.append(LAN)
        self.dp.append(LAN)


    def sendMsg (self, t):
        if (self.flag == 1):
            self.msg.append(f'{t} s {self} ({self.root} {self.rootDist} {self})')

        for LAN in self.ports:
            LAN.forward((self.root, self.rootDist, self), t)


    def receiveMsg(self, t, message, LAN):
        root, rootDist, bridge = message

        
        if self.flag == 1:
            self.msg.append(f"{t+1} r {self} ({self.root} {self.rootDist} {self})")
            
            
        if self.rootDist > rootDist or (self.rootDist == rootDist and self.id > bridge.id):
            if LAN in self.dp:
                self.dp.remove(LAN)
                self.change = True

        rootDist = rootDist + 1

        if root.id > self.root.id or (root.id == self.root.id and rootDist > self.rootDist):
            return

        
        self.root = root
        self.rootDist = rootDist
        self.rp = LAN
        self.change = True


    def __repr__(self):
      return self.name


class ExtendedLAN:
    def __init__(self, name_LAN):
        self.name = name_LAN
        self.connections = []

    def connect(self, bridgeName):
        self.connections.append(bridgeName)

    def forward(self, message, t):
        sender = message[2]

        for bridge in self.connections:
            if bridge is not sender:
                bridge.receiveMsg(t, message, self)

    def __repr__(self):
      return self.name