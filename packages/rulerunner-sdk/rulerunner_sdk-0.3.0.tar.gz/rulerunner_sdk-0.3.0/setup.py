from setuptools import setup

setup(
    name="rulerunner-sdk",
    version="0.3.0",
    packages=['rulerunner_sdk'],
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.0.0",
    ],
    author="RuleRunner",
    author_email="support@rulerunner.com",
    description="Official Python SDK for RuleRunner API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RuleRunner",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 