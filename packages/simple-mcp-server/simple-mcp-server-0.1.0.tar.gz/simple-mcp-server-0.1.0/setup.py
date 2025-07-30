from setuptools import setup, find_packages

setup(
    name="simple-mcp-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'mcp-server>=0.1.0',
    ],
    entry_points={
        'console_scripts': [
            'simple-mcp-server=simple_mcp_server.server:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple MCP server with hello and dice rolling tools",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple-mcp-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
