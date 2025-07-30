from setuptools import setup, find_packages

# 使用 UTF-8 编码读取 README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# 读取 LICENSE 文件
with open("LICENSE", encoding="utf-8") as f:
    license_text = f.read()

setup(
    name="calculate-power-mcp-76980",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
    ],
    author="MCP Developer",
    author_email="mcp@example.com",
    description="A Model Context Protocol Server implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcp-developer/mcp-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    package_data={
        "mcp_server": ["examples/*.py"],
    },
    include_package_data=True,
    license=license_text,
) 