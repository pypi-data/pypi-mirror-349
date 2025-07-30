from setuptools import setup, find_packages

setup(
    name="mbe_mcp_server",  # 项目名称
    version="0.1.0",  # 版本号
    description="韬略服务对外Mcp服务",  # 简要描述
    author="yanan.wya",  # 作者名字
    author_email="wya0556@qq.com",  # 作者邮箱
    url="",  # 项目
    packages=find_packages(),  # 自动发现所有包
    install_requires=[
        "mcp",  # 所依赖的第三方库，例如 mcp 库
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)