import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bigquant_mcp_ricky",  # 请确保该名称在 PyPI 上尚未被使用
    version="0.0.1",
    author="Ricky Li",
    author_email="lingyuli513125@gmail.com",
    description="Test of bigquant mcp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "asyncio",         # 注意：标准库通常不需要列，但 async 使用 async-extra 时可能需指定
        "aiofiles>=23.1.0",
        "httpx>=0.24.0",
        "jieba>=0.42.1",
        "structlog>=23.1.0",
        "openai>=1.3.0",   # 请确认你所使用的 openai SDK 版本
        "PyMuPDF>=1.23.7",  # fitz 属于 PyMuPDF 包
    ],
)
