from setuptools import setup, find_packages

setup(
name="mcp_calpower_server", 
version="0.2.0",
author="MJ",
author_email="sufer76980@163.com",
description="A Model Context Protocol server for power calculating. This server enables LLMs to use calculator for precise numerical power calculations.",
long_description=open("README.md", "r", encoding="utf-8").read(),
long_description_content_type="text/markdown",
packages=find_packages(),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires='>=3.6',
)