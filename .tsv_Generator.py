#!/usr/bin/env python3

from scapy.all import rdpcap, IP, TCP, UDP
from collections import defaultdict
from tqdm import tqdm
import os

class FlowExtractor:
    def __init__(self):
        self.flows = defaultdict(lambda: {
            'packets': [],
            'total_bytes': 0
        })
    
    def get_flow_key(self, pkt):
        if IP not in pkt:
            return None
        
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        
        if TCP in pkt:
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
            protocol = "TCP"
        elif UDP in pkt:
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport
            protocol = "UDP"
        else:
            return None
        
        forward_key = (src_ip, src_port, dst_ip, dst_port, protocol)
        backward_key = (dst_ip, dst_port, src_ip, src_port, protocol)
        
        return min(forward_key, backward_key)
    
    def parse_pcap(self, pcap_file):
        try:
            packets = rdpcap(pcap_file)
        except Exception:
            return
        
        for pkt in tqdm(packets, desc="Extracting flows"):
            flow_key = self.get_flow_key(pkt)
            
            if flow_key is None:
                continue
            
            self.flows[flow_key]['packets'].append({
                'timestamp': float(pkt.time),
                'length': len(pkt)
            })
            self.flows[flow_key]['total_bytes'] += len(pkt)
    
    def export_to_tsv(self, output_file, label):
        flow_count = 0
        with open(output_file, 'w') as f:
            for flow_key, flow_data in tqdm(self.flows.items(), desc="Writing flows"):
                packets = flow_data['packets']
                
                if len(packets) < 2:
                    continue
                
                packets = sorted(packets, key=lambda x: x['timestamp'])
                
                src_ip, src_port, dst_ip, dst_port, protocol = flow_key
                base_timestamp = int(packets[0]['timestamp'])
                total_bytes = flow_data['total_bytes']
                
                relative_times = []
                for pkt in packets:
                    rel_time = pkt['timestamp'] - base_timestamp
                    relative_times.append(f"{rel_time:.6f}")
                
                row = [
                    label,
                    src_ip,
                    str(src_port),
                    dst_ip,
                    str(dst_port),
                    protocol,
                    str(base_timestamp),
                    str(total_bytes),
                    '0'
                ]
                row.extend(relative_times)
                
                f.write('\t'.join(row) + '\n')
                flow_count += 1
        
        return flow_count


def process_all_pcaps(pcap_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    all_files = [f for f in os.listdir(pcap_dir) if not f.endswith('.lnk')]
    
    botnet_files = [f for f in all_files if f.startswith('capEC2AMAZ-')]
    benign_files = [f for f in all_files if f.startswith(('capDESKTOP-', 'capPC1-', 'capWIN-'))]
    
    for i, pcap_file in enumerate(botnet_files, 1):
        extractor = FlowExtractor()
        file_path = os.path.join(pcap_dir, pcap_file)
        extractor.parse_pcap(rf"{file_path}")
        
        output_file = os.path.join(output_dir, f"Botnet-{i:03d}.tsv")
        extractor.export_to_tsv(rf"{output_file}", "Botnet")
    
    for i, pcap_file in enumerate(benign_files, 1):
        extractor = FlowExtractor()
        file_path = os.path.join(pcap_dir, pcap_file)
        extractor.parse_pcap(rf"{file_path}")
        
        output_file = os.path.join(output_dir, f"Benign-{i:03d}.tsv")
        extractor.export_to_tsv(rf"{output_file}", "Benign")


if __name__ == "__main__":
    pcap_dir = r"..."
    output_dir = r"..."
    
    process_all_pcaps(pcap_dir, output_dir)
