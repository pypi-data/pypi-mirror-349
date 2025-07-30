# Copyright (c) 2025 StasX (Kozosvyst Stas). All rights reserved.

from setuptools import setup, find_packages
import os
from io import open

# Read long description from README
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="xnet-toolkit",
    version="1.1.0",
    packages=find_packages(),
    package_data={
        'xnet_system': ['config.json'],
        '': ['latest_version.txt', 'bash_completion.sh']
    },
    install_requires=[
        'asyncio>=3.4.3',
        'ipaddress>=1.0.23',
        'cryptography>=3.4.0',
        'requests>=2.25.0',
        'scapy>=2.4.0',
        'netifaces>=0.11.0',
        'prettytable>=2.0.0',
        'pyOpenSSL>=20.0.0',
        'argon2-cffi>=20.1.0',
        'psutil>=5.8.0',
        'dnspython>=2.1.0',
        'graphviz>=0.16',
        'python-iptables>=1.0.0; platform_system != "Windows"',
        'weasyprint>=52.5',
    ],
    entry_points={
        'console_scripts': [
            'xnet=xnet_system.cli:main',
        ],
    },
    author="StasX (Kozosvyst Stas)",
    author_email="xnet@sxservisecli.tech",
    description="Professional Network Administration and Security Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="network, security, administration, scanner, monitoring, tools",
    url="https://github.com/StasX-Official/xnet",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/StasX-Official/xnet/issues",
        "Source": "https://github.com/StasX-Official/xnet",
    },
)
