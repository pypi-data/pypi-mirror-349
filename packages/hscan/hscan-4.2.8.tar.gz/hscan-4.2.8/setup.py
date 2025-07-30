import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hscan",
    version="4.2.8",
    author="jyanghe",
    author_email="jyanghe1023@gmail.com",
    description="A python framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jyangHe/hscan",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'scan': ['**/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.0",
    install_requires=[
        "httpx[http2]==0.27.2",
        "requests==2.32.3",
        "aiofiles==24.1.0",
        "aio-pika==9.5.4",
        "beautifulsoup4==4.12.3",
        "redis==5.2.1",
        "motor==3.6.0",
        "Brotli==1.1.0",
        "pymongo==4.9.2",
        "chardet==5.2.0",
        "asyncpg==0.30.0",
        "aioboto3==13.2.0",
        "aiomysql==0.2.0",
        "curl-cffi==0.7.4",
        "aiohttp==3.11.10",
        "loguru==0.7.3",
        "oss2==2.15.0",
        "aiokafka==0.12.0",
        "DrissionPage==4.1.0.14",
        "tenacity==9.0.0",
        "html5lib==1.1",
    ],
    setup_requires=["wheel"],
)
