
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-gsuite",
    version="0.4.1",
    description="MCP Server to connect to Google G-Suite",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['beautifulsoup4>=4.12.3', 'google-api-python-client>=2.154.0', 'httplib2>=0.22.0', 'mcp>=1.3.0', 'oauth2client==4.1.3', 'python-dotenv>=1.0.1', 'pytz>=2024.2', 'requests>=2.32.3'],
    keywords=["mseep"] + [],
)
