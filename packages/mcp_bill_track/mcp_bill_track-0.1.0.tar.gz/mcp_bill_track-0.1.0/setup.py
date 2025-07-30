from setuptools import setup, find_packages

setup(
    name="mcp_bill_track",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp"
    ],
    description="个人记账 MCP 服务",
    keywords="bill, track, mcp",
    python_requires=">=3.10",
)
