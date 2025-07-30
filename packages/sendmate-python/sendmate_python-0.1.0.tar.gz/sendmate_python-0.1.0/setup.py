from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sendmate-python",
    version="0.1.0",
    author="Nextune Solutions",
    author_email="info@nextunesolutions.com",
    description="SendMate Python SDK for payment processing and wallet management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nextunesolutions/sendmate-python",
    packages=find_packages(),
    keywords=['payments', 'mpesa', 'mpesa api', 'card payments', 'visa',
              'mastercard', 'payments kenya', 'mpesa stk-push', 'stk push', 'sendmate', 'airtime',],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
    ],
) 