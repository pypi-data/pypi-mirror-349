from setuptools import setup, find_packages

setup(
    name="my_alibaba_cloud_ops_mcp_server",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # 必要的元数据
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/repository",

    # 项目依赖
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
    ],

    # 可选的分类信息
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
