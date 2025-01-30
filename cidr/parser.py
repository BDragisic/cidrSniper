import argparse
import ipaddress

BANNER=f"""
"""


class Parser():
    
    def countTotalHostsWithinCDIR(cdir_range:str) -> int:
        try:
            network = ipaddress.ip_network(cdir_range, strict=False)
            return network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
        except ValueError:
            print(f"{cdir_range} does not appear to be a valid CIDR range! Ignoring...")
            return ""

    def parseSingleCDIR(cdir_range:str) -> list:
        try:
            network = ipaddress.ip_network(cdir_range, strict=False)
            full_hosts = [str(ip) for ip in network.hosts()] 
            return full_hosts
        except ValueError:
           print(f"{cdir_range} does not appear to be a valid CIDR range! Ignoring...")
           return ""



def parse_args():
    parser = argparse.ArgumentParser(description='Parse a list of CIDR ranges and output all hosts within ignoring the network and broadcast addresses')
    
    parser.add_argument("-s", "--single", type=str, help="Provide a single CIDR range on the command line")
    parser.add_argument("-f", "--file", type=str, help="Provide path to a file of newline separated CIDR ranges")
    parser.add_argument("-o", "--outfile", type=str, help="Will output to a file instead of stdout. No formatting, just dumps all hosts into a file")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(BANNER)
    
    
    if args.single:
       single_cidr = Parser.parseSingleCDIR(args.single)
       number_of_hosts = Parser.countTotalHostsWithinCDIR(args.single)
       print(f"Total Hosts: {number_of_hosts}\n")
       print("\n".join(single_cidr))
       
    elif args.file:
        file_path = args.file
        try:
            with open(file_path,"r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            exit(1)
        
        if args.outfile:
            output_file = args.outfile
            with open(output_file,"w") as writer:
                for line in lines:
                    line = line.strip()
                    single_cidr = Parser.parseSingleCDIR(line)
                    for host in single_cidr:
                        writer.write(host + "\n")
        else:
            # Printpytho to stdout with a bit of janky formatting
            for line in lines:
                line = line.strip()
                single_cidr = Parser.parseSingleCDIR(line)
                number_of_hosts = Parser.countTotalHostsWithinCDIR(line)
                print(f"\n{line} has {number_of_hosts} total hosts:")
                for host in single_cidr:
                    print(f"    [*] {host}")



