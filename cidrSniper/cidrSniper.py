import argparse
import ipaddress

BANNER=f"""
   ______________  ____     _____       _                
  / ____/  _/ __ \/ __ \   / ___/____  (_)___  ___  _____
 / /    / // / / / /_/ /   \__ \/ __ \/ / __ \/ _ \/ ___/
/ /____/ // /_/ / _, _/   ___/ / / / / / /_/ /  __/ /    
\____/___/_____/_/ |_|   /____/_/ /_/_/ .___/\___/_/     
                                     /_/                 
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
       
    def deduplicateLines(hosts:list) -> list:
        return list(set(hosts))
    
    def sortLines(hosts:list) -> list:
        return sorted(hosts, key=ipaddress.ip_address)



def parse_args():
    parser = argparse.ArgumentParser(description='Parse a list of CIDR ranges and output all hosts within ignoring the network and broadcast addresses')
    
    parser.add_argument("-s", "--single", type=str, help="Provide a single CIDR range on the command line")
    parser.add_argument("-f", "--file", type=str, help="Provide path to a file of newline separated CIDR ranges")
    parser.add_argument("-o", "--outfile", type=str, help="Will output to a file instead of stdout. No formatting, just dumps all hosts into a file")
    parser.add_argument("-d", "--deduplicate", action="store_true" ,help="De-duplicate the output hosts when outputting to file")
    parser.add_argument("-x", "--sort", action="store_true" ,help="Sort the output hosts when outputting to file")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(BANNER)
    
    
    if args.single:
        print(f"Generating hosts for {args.single}...\n")
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
            total_lines = []
            for line in lines:
                line = line.strip()
                single_cidr = Parser.parseSingleCDIR(line)
                for host in single_cidr:
                    total_lines.append(host)
            with open(output_file,"w") as writer:
                if args.deduplicate:
                    total_lines = Parser.deduplicateLines(total_lines)
                if args.sort:
                    total_lines = Parser.sortLines(total_lines)
                writer.writelines(line + "\n" for line in total_lines)
        else:
            # Print to stdout with a bit of janky formatting
            for line in lines:
                line = line.strip()
                single_cidr = Parser.parseSingleCDIR(line)
                number_of_hosts = Parser.countTotalHostsWithinCDIR(line)
                print(f"\n{line} has {number_of_hosts} total hosts:")
                for host in single_cidr:
                    print(f"    [*] {host}")



