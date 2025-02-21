from setuptools import find_packages, setup

setup(
    name="event_core",  # Replace with your package name
    version="1.0.0",  # Initial version
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
        "pytest==8.3.4",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.0.1",
        "requests==2.32.3",
        "s3transfer==0.11.2",
        "six==1.17.0",
        "types-colorama==0.4.15.20240311",
        "types-docutils==0.21.0.20241128",
        "types-pexpect==4.9.0.20241208",
        "types-Pygments==2.19.0.20250219",
        "types-requests==2.32.0.20241016",
        "types-setuptools==75.8.0.20250210",
        "typing_extensions==4.12.2",
        "urllib3==2.3.0",
    ],
    python_requires=">=3.11",
)
