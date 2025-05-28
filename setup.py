from setuptools import setup, find_packages

setup(
    name="gantt_app",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.22.0",
        "pandas>=1.4.0",
        "PyQt5>=5.15.0",
    ],
    author="开发者",
    author_email="dev@example.com",
    description="甘特图生成和管理应用",
    keywords="gantt,项目管理,图表",
    python_requires=">=3.8",
)