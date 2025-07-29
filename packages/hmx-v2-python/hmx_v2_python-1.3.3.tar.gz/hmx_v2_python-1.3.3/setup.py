from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md').read()

REQUIREMENTS = [
    'eth_keys==0.5.0',
    'eth-account==0.10.0',
    'eth-abi>=4.0.0,<5.0.0',
    'uniswap-universal-router-decoder',
    'web3>=6.0.0,<7.0.0',
    'simple-multicall-v6',
    'responses',
    'python-dotenv>=1.0.0',
]

setup(
    name='hmx-v2-python',
    version='1.3.3',
    packages=find_packages(),
    package_data={
      'hmx2': ['abis/*.json'],
    },
    description='HMXv2 Python SDK',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/HMXOrg/v2-sdk-python',
    author='HMXOrg',
    license='MIT',
    author_email='contact@hmx.org',
    install_requires=REQUIREMENTS,
    keywords='hmx exchange perp dex defi ethereum eth arbitrum blast',
    classifiers=[
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.11',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
