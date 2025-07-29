
from setuptools import setup, find_packages

setup(
    name="mseep-jvm-mcp-server",
    version="0.1.1",
    description="基于Arthas的JVM监控MCP服务器实现",
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
    install_requires=['mcp[cli]>=1.3.0', 'paramiko>=3.5.1'],
    keywords=["mseep"] + ['java', 'jvm', 'monitoring', 'arthas', 'mcp'],
)
