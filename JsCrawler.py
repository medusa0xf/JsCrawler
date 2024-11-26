import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def fetch_page(url, cookies=None):
    """Fetch the content of a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_js_files(html, base_url):
    """Extract JavaScript file URLs from the HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    js_files = []

    # Look for <script> tags with a 'src' attribute
    for script_tag in soup.find_all('script', src=True):
        js_url = urljoin(base_url, script_tag['src'])
        js_files.append(js_url)

    return js_files

def download_js_files(js_files, output_dir):
    """Download JavaScript files and store them locally."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for js_url in js_files:
        try:
            response = requests.get(js_url, timeout=10)
            response.raise_for_status()

            # Save the JavaScript file
            filename = os.path.join(output_dir, os.path.basename(js_url))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Downloaded: {js_url}")

        except requests.RequestException as e:
            print(f"Failed to download {js_url}: {e}")

def main():
    # Input the URL and optional cookies
    url = input("Enter the URL to crawl: ")
    cookie_str = input("Enter cookies (if any, in 'key=value; key2=value2' format, or press Enter to skip): ")

    # Parse cookies into a dictionary
    cookies = None
    if cookie_str:
        cookies = {key.strip(): value.strip() for key, value in (item.split('=') for item in cookie_str.split(';'))}

    print("\nFetching the webpage...")
    html = fetch_page(url, cookies=cookies)
    if not html:
        print("Failed to fetch the webpage.")
        return

    print("\nExtracting JavaScript files...")
    js_files = extract_js_files(html, url)
    print(f"Found {len(js_files)} JavaScript files.")

    if js_files:
        print("\nDownloading JavaScript files...")
        download_js_files(js_files, output_dir="downloaded_js")
        print(f"\nDownloaded {len(js_files)} JavaScript files. Check the 'downloaded_js' folder.")
    else:
        print("No JavaScript files found.")

if __name__ == "__main__":
    main()
