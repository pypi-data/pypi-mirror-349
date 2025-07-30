from setuptools import find_packages, setup

setup(
    name='cnutils',
    version='0.1.41',
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src",exclude=[]),
    package_data={
        '': ['*.py']
    },
    description='cnutils for free.',
    url='https://pypi.org/project/cnutils/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        # 依赖列表
    ],
    # 其他元数据
)