from setuptools import find_packages, setup

setup(
    name="event_core",  # Replace with your package name
    version="1.1.0",  # Initial version
    author="axwhyzee",  # Author of the package
    url="https://github.com/axwhyzee/multi-modal-retrieval-event-core",
    packages=find_packages(),
    install_requires=[
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "click==8.1.8",
        "idna==3.10",
        "iniconfig==2.0.0",
        "packaging==24.2",
        "pathspec==0.12.1",
        "platformdirs==4.3.6",
        "pluggy==1.5.0",
        "python-dotenv==1.0.1",
        "redis==5.2.1",
        "requests==2.32.3",
        "urllib3==2.3.0",
    ],
    python_requires=">=3.11",
)
