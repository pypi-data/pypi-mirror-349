
from setuptools import setup, find_packages

setup(
    name="mseep-crewai-adapters",
    version="0.1.2",
    description="Native adapter support for CrewAI with Model Context Protocol (MCP) integration",
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
    install_requires=['crewai>=0.1.0', 'pydantic>=2.0.0', 'mcp>=1.3.0', 'pydantic-core>=2.0.0', 'build>=1.2.2.post1', 'twine>=6.1.0'],
    keywords=["mseep"] + ['crewai', 'mcp', 'adapters', 'ai', 'agents'],
)
