
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-sqlalchemy-server",
    version="0.3.1",
    description="A simple MCP ODBC server using FastAPI and ODBC",
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
    install_requires=['mcp[cli]>=1.4.1', 'pyodbc>=5.2.0', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
