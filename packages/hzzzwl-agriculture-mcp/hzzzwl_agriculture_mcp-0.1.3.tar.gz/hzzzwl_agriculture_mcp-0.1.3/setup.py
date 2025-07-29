from setuptools import setup, find_packages
 
setup(
    name="hzzzwl-agriculture-mcp",  # 包名，pip install 时用这个
    version="0.1.3",
    description="A tool for search agriculture information",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
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