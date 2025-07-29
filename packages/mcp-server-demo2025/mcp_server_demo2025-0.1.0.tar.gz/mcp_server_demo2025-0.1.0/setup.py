from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "MCP Demo Server 2025"

setup(
    name="mcp-server-demo2025",
    version="0.1.0",
    packages=find_packages(),
    author="Your Name",
    author_email="your@email.com",
    description="一个演示用的MCP服务器2025版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-server-demo2025",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp>=1.6.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-demo2025=mcp_server_demo2025.__main__:main",
        ],
    },
) 