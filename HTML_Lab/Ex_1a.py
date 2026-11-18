import ssl
import urllib.request


URL = (
    "https://data.cityofchicago.org/Historic-Preservation/"
    "Landmark-Districts/zidz-sdfj/about_data"
)


ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen(URL) as response:
    print(response)
    for raw_line in response:
        line = raw_line.decode("utf-8")
        if "<title>" in line.lower():
            print(line)