from setuptools import setup, find_namespace_packages

with open('readme.md', 'r') as f:
    description = f.read()

setup(name='cryptolab',
      version='1.0.1',
      description='Cryptolab library to replay historic data',
      url='https://www.crypto-lab.io',
      author='CryptoLab, Charles',
      author_email='contact@crypto-lab.io',
      license='MIT',
      long_description=description,
      long_description_content_type='text/markdown',
      packages=find_namespace_packages(),
      install_requires=['pandas', 'requests'],
      keywords='cryptolab backtest cryptocurrency cryptocurrencies api bitcoin binance gateio',
      project_urls={
        "Documentation": "https://www.crypto-lab.app/documentation",
        "Source Code": "https://github.com/crypto-lab-app/client-libraries",
        "Icon": "https://1.gravatar.com/avatar/5121577298f39a1661507198f8615319a7d7a14fad36f9ec52d20ae0d446bf69?size=512",
      },
)