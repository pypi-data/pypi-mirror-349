# proxyrotator

A simple Python utility to rotate proxies by validating them against ipinfo.io.

## Installation

```bash
pip install proxyrotator

from proxyrotator import getproxy

proxies = [
    "http://1.2.3.4:8080",
    "http://5.6.7.8:3128",
]

proxy = getproxy(proxies)
print(proxy)

