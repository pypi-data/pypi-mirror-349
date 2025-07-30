import os

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as readme:
    README = readme.read()

setup(
    name="bk-notice-sdk",  # 项目名称
    version="1.3.3",  # 项目版本
    description="A project for fetching and displaying announcement notifications.",  # 项目的简短描述
    packages=find_packages(),  # 包含项目中的所有包
    author="blueking",
    author_email="blueking@tencent.com",
    # url
    include_package_data=True,  # 包含非代码文件（如模板、静态文件等）
    long_description=README,  # 项目的详细描述，从 README.md 文件获取
    long_description_content_type="text/markdown",  # 详细描述的内容类型
    install_requires=requirements,  # 项目的依赖列表
)
