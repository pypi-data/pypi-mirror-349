from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="react-native-debugger-client",
    version="0.0.1.dev1",
    author="Erick Torres-Moreno",
    description="A Python client for interacting with React Native applications via the Hermes debugger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erickjtorres/react-native-debugger-client",  # Replace with your repo URL
    packages=find_packages(),
    package_data={
        "react_native_debugger_client": ["js_snippets/*.py"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Debuggers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "websocket-client>=1.3.0",
    ],
    keywords="react-native, hermes, debugger, testing, automation",
) 