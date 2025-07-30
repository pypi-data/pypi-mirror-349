# 用于计算阿里云的签名

## 打包
```shell
python setup.py sdist bdist_wheel
```

## 上传
### 安装依赖工具
```shell
pip install twine
```
### 上传到pypi（需要提前准备好账号）
```shell
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```