from setuptools import setup

setup(
    name='pycorebaz',
    version='0.0.12',
    packages=['pycorebaz','pycorebaz.mx', 'pycorebaz.mx.com', 'pycorebaz.mx.com.bancoazteca', 'pycorebaz.mx.com.bancoazteca.cloud', 'pycorebaz.mx.com.bancoazteca.cloud.core',
              'pycorebaz.mx.com.bancoazteca.cloud.core.utilerias', 'pycorebaz.mx.com.bancoazteca.cloud.core.seguridad',
              'pycorebaz.mx.com.bancoazteca.cloud.core.models','pycorebaz.mx.com.bancoazteca.cloud.core.handlers',
              'pycorebaz.mx.com.bancoazteca.cloud.core.db',
              'pycorebaz.mx.com.bancoazteca.cloud.core.log', 'pycorebaz.mx.com.bancoazteca.cloud.configuracion'],
    url='http://devops:9001',
    license='License :: OSI Approved :: MIT License',
    author='Chapter Cloud and DevOps',
    author_email='clouddevops@elektra.com.mx',
    description='',
    install_requires = [ # Optional
      "requests","pycryptodome","paprika","json-encoder","pyctuator","python-dotenv","starlette","pytest-cov","pytest","pytz","oracledb",
        "httpx","PyJWT","python-dotenv","json-encoder","boto3","psycopg2-binary"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords = ["BAZ", "Cobranza", "Cloud","Python","Template","Rest","Core","pycorebaz"]  # Optional
)
