from setuptools import setup, find_packages
 
setup(
    name="hzzzwl-agriculture-mcp",  # 包名，pip install 时用这个
    version="0.1.1",
    description="A tool for search agriculture information",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            # 定义命令行工具，用户运行 uvx your-mcp-server 时会执行 your_mcp_server.main:main
            'hzzzwl-agriculture-mcp=hzzzwl_agriculture_mcp.server:main',
        ],
    },
    author="hzzzwl",
    author_email="1085501772@qq.com",
    url="",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
)