
from setuptools import setup, find_packages

setup(
    name="mseep-daraja",
    version="0.1.0",
    description="Add your description here",
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
    install_requires=['boto3>=1.37.22', 'httpx>=0.28.1', 'ipykernel>=6.29.5', 'langchain-mongodb>=0.6.0', 'langchain-openai>=0.3.11', 'mcp[cli]>=1.5.0', 'pymongo>=4.11.3', 'python-dotenv>=1.1.0', 'unstructured-client>=0.30.6'],
    keywords=["mseep"] + [],
)
