import os
import subprocess
import requests
import m3u8
from datetime import datetime

def get_m3u8_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve M3U8 content from {url}")
        return None

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
    with open(file_path, 'r', encoding='utf-8') as f:
        m3u8_content = f.read()

    playlist = m3u8.loads(m3u8_content)
    results = []

    for segment in playlist.segments:
        url = segment.uri
        resolution = get_resolution(url)
        results.append(f"{url} - {resolution}")

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

