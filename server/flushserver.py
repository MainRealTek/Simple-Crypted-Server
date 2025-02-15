from iptc import Table


class mac_FLUSH(object):
    def GO(self):
        table = Table(Table.FILTER)
        table.autocommit = False 

        for chain in table.chains:
            for rule in chain.rules:
                for match in rule.matches:
                    if match.name == "mac" and rule.target.name == "DROP":
                        chain.delete_rule(rule)
                        print(f"Deleted rule dropping MAC address: {match.mac_source}")

        table.commit()  
        table.refresh()  

mac_FLUSH().GO()

