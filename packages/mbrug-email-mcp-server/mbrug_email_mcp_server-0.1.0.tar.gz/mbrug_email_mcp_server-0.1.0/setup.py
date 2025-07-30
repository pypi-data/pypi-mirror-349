from setuptools import setup, find_namespace_packages

setup(
    name="mbrug-email-mcp-server",
    version="0.1.0",
    description="Email MCP Server for Amazon Q CLI",
    packages=find_namespace_packages(include=["mbrug", "mbrug.*"]),
    py_modules=["email_mcp_server"],
    entry_points={
        'console_scripts': [
            'email-mcp-server=email_mcp_server:run_server',
        ],
        'amazon_q_mcp.servers': [
            'mbrug.email-mcp-server=mbrug.email_mcp_server:run_server',
        ],
    },
    install_requires=[
        "google-auth-oauthlib",
        "google-auth",
        "google-api-python-client",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
