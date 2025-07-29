from setuptools import setup, find_packages

setup(
    name="mseep-optimized-memory-mcp-server",
    author="mseep",
    author_email="support@skydeck.ai",
    maintainer="mseep",
    maintainer_email="support@skydeck.ai",
                    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "aiofiles>=23.2.1",
        "mcp>=1.1.2",
        "aiosqlite>=0.20.0",
    ],
    python_requires=">=3.12",
)
