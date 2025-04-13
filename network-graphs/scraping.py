from waybackpy import WaybackMachineCDXServerAPI
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import time
import random
import os

# Define websites to analyze
target_domains = ["epa.gov", "sustainability.gov", "noaa.gov"]

# Define timepoints for analysis (YYYYMMDD format)
timepoints = ["20250401"]

# User agent (required for waybackpy)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Create output directory if it doesn't exist
os.makedirs("network-data", exist_ok=True)

def get_archived_urls(domain, timepoint, max_urls=100):
    """Retrieve archived URLs for a domain near a specific timepoint."""
    print(f"Retrieving URLs for {domain} at timepoint {timepoint}...")
    try:
        cdx = WaybackMachineCDXServerAPI(
            domain, 
            user_agent,
            start_timestamp=timepoint,
            end_timestamp=str(int(timepoint) + 10000)
        )
        
        # Get snapshots
        snapshots = list(cdx.snapshots())[:max_urls]
        if not snapshots:
            print(f"No snapshots found for {domain} at {timepoint}")
            return []
            
        # Debug snapshot structure
        if snapshots:
            print(f"First snapshot attributes: {dir(snapshots[0])}")
        
        # Extract URLs using the correct attribute 
        urls = []
        for snapshot in snapshots:
            # Try different possible attribute names
            if hasattr(snapshot, 'original_url'):
                urls.append(snapshot.original_url)
            elif hasattr(snapshot, 'url'):
                urls.append(snapshot.url)
            elif hasattr(snapshot, 'original'):
                urls.append(snapshot.original)
            else:
                # Extract from string representation as fallback
                snapshot_str = str(snapshot)
                if 'http' in snapshot_str:
                    parts = snapshot_str.split()
                    for part in parts:
                        if part.startswith(('http://', 'https://')):
                            urls.append(part)
                            break
        
        # Remove duplicates
        unique_urls = []
        for url in urls:
            if url and url not in unique_urls:
                unique_urls.append(url)
        
        return unique_urls[:max_urls]
    
    except Exception as e:
        print(f"Error retrieving URLs for {domain} at {timepoint}: {e}")
        return []


def extract_links_from_archived_page(url, timepoint, target_domains):
    """Extract links from an archived page that point to any target domain."""
    try:
        # Construct the Wayback Machine URL
        timestamp = timepoint
        wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
        
        # Add delay to respect robots.txt and prevent rate limiting
        time.sleep(random.uniform(2, 5))
        
        # Fetch the archived page
        response = requests.get(wayback_url, timeout=30)
        if response.status_code != 200:
            return []
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all links
        extracted_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Check if this link points to any of our target domains
            if any(domain in href for domain in target_domains):
                extracted_links.append((url, href, timepoint))
                
        return extracted_links
    
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return []

def collect_network_data(timepoint, target_domains, max_urls_per_domain=50):
    """Collect network data for the specified domains at a timepoint."""
    print(f"\n{'='*50}")
    print(f"Collecting data for timepoint: {timepoint}")
    print(f"{'='*50}\n")
    
    # Dictionary to store domain URLs
    domain_urls = {}
    all_links = []
    
    # Get URLs for each domain
    for domain in target_domains:
        domain_urls[domain] = get_archived_urls(domain, timepoint, max_urls_per_domain)
        print(f"Retrieved {len(domain_urls[domain])} URLs for {domain}")
    
    # Process each URL to extract links
    total_urls = sum(len(urls) for urls in domain_urls.values())
    print(f"Processing {total_urls} URLs to extract links...")
    
    start_time = time.time()
    processed_count = 0
    
    with tqdm(total=total_urls) as pbar:
        for source_domain, urls in domain_urls.items():
            for url in urls:
                # Extract links from this page
                links = extract_links_from_archived_page(url, timepoint, target_domains)
                all_links.extend(links)
                
                processed_count += 1
                pbar.update(1)
                
                # Provide time estimate after processing some URLs
                if processed_count == 5:
                    time_elapsed = time.time() - start_time
                    time_per_url = time_elapsed / 5
                    estimated_total_time = time_per_url * total_urls
                    print(f"\nEstimated time to process all {total_urls} URLs: {estimated_total_time/60:.1f} minutes")
    
    # Create nodes dataframe
    all_nodes = set()
    for source, target, _ in all_links:
        all_nodes.add(source)
        all_nodes.add(target)
    
    nodes_data = []
    for node in all_nodes:
        domain = None
        for target_domain in target_domains:
            if target_domain in node:
                domain = target_domain
                break
        nodes_data.append({
            'url': node,
            'domain': domain
        })
    
    # Create edges dataframe
    edges_data = []
    for source, target, timestamp in all_links:
        source_domain = None
        target_domain = None
        
        for domain in target_domains:
            if domain in source:
                source_domain = domain
            if domain in target:
                target_domain = domain
        
        edges_data.append({
            'source': source,
            'source_domain': source_domain,
            'target': target,
            'target_domain': target_domain,
            'timestamp': timestamp
        })
    
    # Save data to CSV files
    nodes_df = pd.DataFrame(nodes_data)
    edges_df = pd.DataFrame(edges_data)
    
    nodes_df.to_csv(f"network-data/nodes_{timepoint}.csv", index=False)
    edges_df.to_csv(f"network-data/edges_{timepoint}.csv", index=False)
    
    print(f"\nData collection complete for {timepoint}:")
    print(f"- Collected {len(nodes_data)} nodes")
    print(f"- Collected {len(edges_data)} edges")
    print(f"- Data saved to network-data/nodes_{timepoint}.csv and network-data/edges_{timepoint}.csv")
    
    return len(nodes_data), len(edges_data)

def main():
    """Run the data collection for all timepoints."""
    
    # Track total data collection statistics
    collection_stats = {}
    total_start_time = time.time()
    
    for timepoint in timepoints:
        timepoint_start = time.time()
        nodes_count, edges_count = collect_network_data(timepoint, target_domains, max_urls_per_domain=30)
        timepoint_end = time.time()
        
        collection_stats[timepoint] = {
            'nodes': nodes_count,
            'edges': edges_count,
            'time_minutes': (timepoint_end - timepoint_start) / 60
        }
    
    total_time = (time.time() - total_start_time) / 60
    
    # Create a combined dataset across all timepoints
    print("\nMerging all timepoints into a single dataset...")
    
    # Combine nodes from all timepoints
    all_nodes_dfs = []
    for timepoint in timepoints:
        try:
            df = pd.read_csv(f"network-data/nodes_{timepoint}.csv")
            df['timepoint'] = timepoint
            all_nodes_dfs.append(df)
        except Exception as e:
            print(f"Error reading nodes for {timepoint}: {e}")
    
    if all_nodes_dfs:
        combined_nodes = pd.concat(all_nodes_dfs, ignore_index=True)
        combined_nodes.drop_duplicates(subset=['url'], inplace=True)
        combined_nodes.to_csv("network-data/all_nodes.csv", index=False)
    
    # Combine edges from all timepoints
    all_edges_dfs = []
    for timepoint in timepoints:
        try:
            df = pd.read_csv(f"network-data/edges_{timepoint}.csv")
            all_edges_dfs.append(df)
        except Exception as e:
            print(f"Error reading edges for {timepoint}: {e}")
    
    if all_edges_dfs:
        combined_edges = pd.concat(all_edges_dfs, ignore_index=True)
        combined_edges.to_csv("network-data/all_edges.csv", index=False)
    
    # Print summary statistics
    print("\nData Collection Summary:")
    print(f"{'='*50}")
    print(f"Total time: {total_time:.1f} minutes")
    print("\nTimepoint Statistics:")
    
    for timepoint, stats in collection_stats.items():
        print(f"Timepoint {timepoint}:")
        print(f"  - Nodes: {stats['nodes']}")
        print(f"  - Edges: {stats['edges']}")
        print(f"  - Time: {stats['time_minutes']:.1f} minutes")
    
    print("\nCombined dataset created:")
    print("  - all_nodes.csv: All unique nodes across timepoints")
    print("  - all_edges.csv: All edges across timepoints")

if __name__ == "__main__":
    main()
