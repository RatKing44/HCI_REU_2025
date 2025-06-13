import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urlparse
import re
from urllib.parse import urlparse
import sys

def extract_company_name(text):
    # Look for common EULA phrasing
    lines = text.strip().splitlines()
    print(lines[3])
    return lines[3]


def extract_clean_text(url):
    # Use newspaper3k to extract the main content
    article = Article(url)
    article.download()
    article.parse()
    
    # Use BeautifulSoup for additional cleanup
    soup = BeautifulSoup(article.html, 'html.parser')

    # Remove nav, footer, header, scripts, and styles
    for tag in soup(['nav', 'footer', 'header', 'script', 'style', 'aside']):
        tag.decompose()

    # Get the remaining text
    text = soup.get_text(separator='\n')
    
    # Clean up extra blank lines and whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)

def get_clean_filename(url, text):
    company_name = None
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or "output"

    # Remove 'www.' prefix
    hostname = re.sub(r'^www\.', '', hostname)

    # Get the root domain (before first dot)
    match = re.match(r'^([^.]+)', hostname)
    base_name = match.group(1) if match else "output"

    # Determine document type from URL
    doc_type = ""
    lower_url = url.lower()
    if "privacy" in lower_url:
        doc_type = "_Priv"
    elif "term" or "tos" in lower_url:
        doc_type = "_ToS"
    elif "license" in lower_url or "eula" in lower_url:
        doc_type = "_EULA"

    if "store" in base_name:
        company_name = extract_company_name(text)
    if company_name:
        base_name = f"{base_name}_{company_name}"
    
    return f"{base_name}{doc_type}.txt"


def save_to_file(text, filename):
    try:
        with open('EULAS/' + filename, 'x', encoding='utf-8') as f:
            f.write(text)
    except IOError as e:
        print(f"[!] Error saving file '{filename}' : {e}")
        save_to_file(text, filename.replace('.txt', '_dupe.txt'))
        return -1
    

def main():
    if len(sys.argv) == 1:
        print("Processing all URLs in 'EULA_URLs.txt'...")
        with open("EULA_URLs.txt") as f:
            for line in f:
                if not line.strip():
                    continue
                if line.startswith('#'):
                    print(f"{line.strip()}")
                    continue
                url = line.strip()
                try:
                    clean_text = extract_clean_text(url)
                    filename = get_clean_filename(url, clean_text)
                    if save_to_file(clean_text, filename) == -1:
                        continue
                    print(f"[✓] Cleaned policy text saved to '{filename}'")
                except Exception as e:
                    print(f"[!] Failed to extract content: {e}")
        sys.exit(1)
    if len(sys.argv) != 2:
        print("Usage: python extract_policy_text.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    try:
        clean_text = extract_clean_text(url)
        filename = get_clean_filename(url, clean_text)
        save_to_file(clean_text, filename)
        print(f"[✓] Cleaned policy text saved to '{filename}'")
    except Exception as e:
        print(f"[!] Failed to extract content: {e}")

if __name__ == "__main__":
    main()
