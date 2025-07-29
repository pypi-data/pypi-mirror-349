
from setuptools import setup, find_packages

setup(
    name="mseep-firstcycling",
    version="0.1.0",
    description="FirstCycling MCP server for accessing professional cycling data",
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.5.0', 'beautifulsoup4', 'lxml', 'numpy', 'pandas', 'python-dateutil', 'pytz', 'requests', 'slumber', 'soupsieve'],
    keywords=["mseep"] + [],
)
