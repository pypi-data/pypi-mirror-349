from setuptools import setup, find_packages
setup(
    name = "whlee",
    version = "0.0.4",
    description="toy tools update at 20250516",
    author = "whl",
    author_email = "2631@139.com",
    license="MIT",
    packages = find_packages(),
    python_requires=">=3.8",
    install_requires=['numpy', 'pandas', 'addict', 'openai==1.58.1']
)
