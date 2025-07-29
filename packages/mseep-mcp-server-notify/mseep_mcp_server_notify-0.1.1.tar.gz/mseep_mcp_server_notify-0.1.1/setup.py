
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-notify",
    version="0.1.0",
    description="MCP Server for system notifications with sound",
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
    install_requires=['mcp[cli]>=1.0.0', 'pydantic>=2.0', 'plyer>=2.0', "pygame>=2.1; platform_system != 'Windows' and platform_system != 'Darwin'", 'requests>=2.25.1', 'apprise>=1.9.2'],
    keywords=["mseep"] + [],
)
