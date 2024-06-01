import os
import subprocess
import requests
import re

def get_resolution(url):
    try:
        command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', url]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Failed to get resolution for {url}")
            return "Resolution not found"
    except Exception as e:
        print(f"Exception occurred while getting resolution for {url}: {e}")
        return "Resolution not found"

def check_channels(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF'):
            url = lines[i + 1].strip()
            resolution = get_resolution(url)
            channel_info = lines[i].strip()
            results.append(f"{channel_info}\n{url} - {resolution}")

    return results

def save_results(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')

if __name__ == "__main__":
    input_file = 'myiptv.m3u'
    output_file = 'fenbianlv.txt'
    results = check_channels(input_file)
    save_results(results, output_file)
    print(f"Results saved to {output_file}")
