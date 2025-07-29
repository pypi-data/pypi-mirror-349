from setuptools import find_packages, setup
from typing import List


def parse_requirements(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [
            require.strip() for require in f
            if require.strip() and not require.startswith('#')
        ]


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


version_file = 'mcp_studio/version.py'


def get_version():
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


setup(
    name='mcp-studio',
    version=get_version(),
    description=
    'MCP Studio',
    author='wangxingjun778',
    author_email='wangxingjun778@163.com',
    keywords='MCP,Agent',
    url='https://github.com/wangxingjun778/mcp-studio',
    license='Apache License 2.0',
    packages=find_packages(exclude=['*test*', 'demo']),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    long_description=readme(),
    long_description_content_type='text/markdown',
    package_data={},
)
