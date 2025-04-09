from setuptools import setup, find_packages

setup(
    name="mcp-tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Remove mcp-server dependency since it's installed via mcp[cli]
    ],
) 