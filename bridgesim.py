from bridge import Bridge, ExtendedLAN

def input_bridge_LAN(inp):
    data = inp.split()
    return data[0], data[1:]

def STP(bridge, lan, flag):
    Run = True
    t=1
    
    while Run:
        for i in range(len(bridge)):
            bridge[i].sendMsg(t)

        t = t+1
        Run = False

    

    for i in range(len(bridge)):
        if bridge[i].change:
            Run = True
            break
    
    if flag == 1:
        msg = []
        print("flag")
        for i in len(bridge):
            msg.append(bridge[i].msg)
        print('\n'.sorted(msg))

    for i in range(len(bridge)):
        bridge_curr = bridge[i]
        output = []
       
        for lan in bridge_curr.ports:
            if bridge_curr.rp is lan:
                output.append(f'{lan}-RP')
            elif lan in bridge_curr.dp:
                output.append(f'{lan}-DP')
            else:
                output.append(f'{lan}-NP')
        print(f'{bridge_curr} ' + ' '.join(sorted(output)))
       




if __name__ == '__main__':

    flag = input()
    bridge_num = int(input())
    bridge = []
    LANs = {}
    lan_num = 0
    for i in range(bridge_num):
        bridges, ports = input_bridge_LAN(input())
        bridge.append(Bridge(bridges, i, flag))
        #print(ports)

        for p in ports:
            LANs[p] = ExtendedLAN(p)     
            bridge[i].connections(LANs[p])
            LANs[p].connect(bridge[i])
        
        #lan_num = lan_num + len(ports)
    STP(bridge, LANs, flag)