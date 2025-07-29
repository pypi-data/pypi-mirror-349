
from setuptools import setup, find_packages

setup(
    name="mseep-android-mcp",
    version="0.1.0",
    description="An MCP server for android automation",
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.3.0', 'pillow>=11.1.0', 'pure-python-adb>=0.3.0.dev0', 'pyyaml>=6.0.2'],
    keywords=["mseep"] + [],
)
