from socket import socket,AF_PACKET,SOCK_RAW,ntohs
from iptc import Rule,Target,Chain,Table
from struct import *




class GET_sock(socket):
    def __init__(self, family = 17, type = 3, proto =768, fileno = None):
        super().__init__(family, type, proto, fileno)

class MainServerSNIFF(GET_sock):

    def read(self,file):
        reading = open(file,'r')
        returnas = list()
        lns = reading.readlines()
        for ii in lns:
            if ii.find('servermacaddr:') != -1:
                result = ii.split('servermacaddr:')[1]
                if ' ' in result:
                    result = result.replace(' ','')
                fresult = result
                returnas.append(fresult)
            if ii.find('whitelist') != -1:
                result = ii.split('whitelist:')[1]
                if ' ' in result:
                    result = result.replace(' ','')
                fresult = result.split(',')[:]
                for ii in fresult:
                    returnas.append(ii)
            if ii.find('interface') != -1:
                result = ii.split('interface:')[1]
                if ' ' in result:
                    result = result.replace(' ','')
                returnas.append(result)
        return returnas


    def eth_addr(self,mac_hex) :
        return ':'.join(f'{byte:02x}' for byte in mac_hex)

    def block_mac_address(self,own_interface=str(),mac_address=str()):
        try:
            # Create a new rule
            rule = Rule()
            rule.in_interface = own_interface 
            
            # Match the MAC address
            mac_match = rule.create_match("mac")
            mac_match.mac_source = mac_address
            
            # Set the target to DROP
            rule.target = Target(rule, "DROP")
            
            # Add the rule to the INPUT chain
            chain = Chain(Table(Table.FILTER), "INPUT")
            chain.insert_rule(rule)
            
            print(f"Successfully blocked MAC address: {mac_address}")
        except Exception as e:
            print(f"Failed to block MAC address: {mac_address}. Error: {e}")




    def main(self):
        print('OK')
        try:
            file_config = input('Choose file config server\n\n\n#')
            print(file_config)
            config = self.read(file=file_config)
            self.server_w  = config[0]
            self.interface = config[-1]
            self.clients_w =config[1:-1]
        except Exception as i:
            print(i)

            print(self.server_w,self.interface,self.clients_w)
            exit()
        while True:
            packet = self.recvfrom(65565)
            
            packet = packet[0]
            

            eth_length = 14
            
            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH' , eth_header)
            eth_protocol = ntohs(eth[2])

            proto   = eth_protocol

            src_mac = self.eth_addr(packet[6:12])
            dst_mac = self.eth_addr(packet[0:6])
            print('Destination MAC : ' + self.eth_addr(packet[0:6]) + ' Source MAC : ' + self.eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol))
            #exit()
            if src_mac not in self.server_w and dst_mac not in self.server_w:
                if src_mac not in self.clients_w and dst_mac not in self.clients_w:
                    pass
                    self.block_mac_address(own_interface=self.interface,mac_address=src_mac)
                    self.block_mac_address(own_interface=self.interface,mac_address=dst_mac)

#MainServerSNIFF().main()

