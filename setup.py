from setuptools import find_packages, setup

setup(
    name="event_core",
    version="1.3.4",
    author="axwhyzee",
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
        "typing_extensions==4.12.2",
        "urllib3==2.3.0",
    ],
    python_requires=">=3.11",
)
