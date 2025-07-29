
from setuptools import setup, find_packages

setup(
    name="mseep-odoo-mcp",
    version="0.0.3",
    description="MCP Server for Odoo Integration",
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
    install_requires=['mcp>=0.1.1', 'requests>=2.31.0', 'pypi-xmlrpc==2020.12.3'],
    keywords=["mseep"] + ['odoo', 'mcp', 'server'],
)
