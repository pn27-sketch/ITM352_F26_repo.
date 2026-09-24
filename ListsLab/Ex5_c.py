from urllib.parse import urlparse

url = input("Enter a URL: ")
domain = urlparse(url).hostname
tld = domain.rsplit(".", 1)[-1]

print("Domain:", domain)
print("TLD:", tld)