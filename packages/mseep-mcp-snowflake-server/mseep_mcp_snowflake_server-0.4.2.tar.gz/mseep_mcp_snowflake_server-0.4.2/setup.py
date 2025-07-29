
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_snowflake_server",
    version="0.4.0",
    description="A simple Snowflake MCP server",
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
    install_requires=['mcp>=1.0.0', 'snowflake-connector-python[pandas]>=3.12.0,<3.14.0', 'pandas>=2.2.3', 'python-dotenv>=1.0.1', 'sqlparse>=0.5.3', 'snowflake-snowpark-python>=1.26.0'],
    keywords=["mseep"] + [],
)
