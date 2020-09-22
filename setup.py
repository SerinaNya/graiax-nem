import setuptools

with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='graiax-nem',
    version='0.0.3.dev2',
    author='Xiao_Jin',
    keywords='graia graiax nem graiax-nem graia-message',
    description='适用于 Graia Framework 的消息解析过滤器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jinzhijie/graiax-nem',
    packages=['graiax/nem'],
    install_requires=['graia-application-mirai'],
    python_requires='>=3.7',
)
