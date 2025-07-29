from setuptools import setup, find_packages

setup(
    name="mseep-toast-mcp-server",
    author="mseep",
    author_email="support@skydeck.ai",
    maintainer="mseep",
    maintainer_email="support@skydeck.ai",
                    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "win10toast;platform_system=='Windows'",
    ],
    python_requires=">=3.8",
)
