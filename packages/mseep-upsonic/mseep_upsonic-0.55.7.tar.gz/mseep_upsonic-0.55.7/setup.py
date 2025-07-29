
from setuptools import setup, find_packages

setup(
    name="mseep-upsonic",
    version="0.55.6",
    description="Task oriented AI agent framework for digital workers and vertical AI agents",
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
    install_requires=['cloudpickle>=3.1.0', 'dill>=0.3.9', 'httpx>=0.27.2', 'psutil==6.1.1', 'rich>=13.9.4', 'sentry-sdk[opentelemetry]>=2.19.2', 'toml>=0.10.2', 'uv>=0.5.20', 'fastapi>=0.115.6', 'mcp[cli]==1.5.0', 'pydantic-ai==0.1.3', 'python-dotenv>=1.0.1', 'uvicorn>=0.34.0', 'beautifulsoup4>=4.12.3', 'boto3>=1.35.99', 'botocore>=1.35.99', 'google>=3.0.0', 'markitdown==0.0.1', 'matplotlib>=3.10.0', 'pyautogui>=0.9.54', 'python-multipart>=0.0.20', 'requests>=2.32.3', 'duckduckgo-search>=7.3.1', 'nest-asyncio>=1.6.0', 'pydantic-ai-slim[anthropic,bedrock,openai]>=0.0.45', 'pydantic==2.10.5'],
    keywords=["mseep"] + [],
)
