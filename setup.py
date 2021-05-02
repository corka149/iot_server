from setuptools import setup

setup(
    name="iot_server",
    version="1.0.0",
    packages=[
        "iot_server",
        "iot_server.api",
        "iot_server.model",
        "iot_server.core",
        "iot_server.infrastructure",
    ],
    package_dir={"": "src"},
    include_package_data=True,  # IMPORTANT for configs in combination with MANIFEST.in
    url="https://github.com/corka149",
    license="",
    author="corka149",
    author_email="corka149@mailbox.org",
    description="A small web server that manages io-things. ",
    install_requires=[
        "fastapi",
        "mongoengine",
        "uvicorn[standard]",
        "gunicorn",
        "pydantic",
    ],
)
