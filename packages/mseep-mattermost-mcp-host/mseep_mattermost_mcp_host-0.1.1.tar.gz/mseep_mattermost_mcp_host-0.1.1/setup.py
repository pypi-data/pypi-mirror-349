
from setuptools import setup, find_packages

setup(
    name="mseep-mattermost-mcp-host",
    version="0.1.0",
    description="Mattermost MCP Host with MCP Client",
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
    install_requires=['aiohttp>=3.11.13', 'langchain[openai]>=0.3.21', 'langchain-openai>=0.3.9', 'langgraph>=0.3.18', 'mattermost>=6.5.0', 'mattermostdriver>=7.3.2', 'mcp[cli]>=1.3.0', 'nest-asyncio>=1.6.0', 'openai>=1.65.5', 'pytest>=8.3.5', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
