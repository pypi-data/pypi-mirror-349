hw-oa 
# 项目文档

## 本地运行项目
uvicorn app.main:app --reload
## 安装twine
uv pip install twine
## 发布项目
创建 ~/.pypirc，内容如下
```
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = ****
```
uv build # 构建，完成后会生成目录 dist，下面放着压缩包
twine upload dist/* # 配置 ～/.pypirc后不需要手动输入密码

[uvicorn参考文档](https://www.uvicorn.org/deployment/)

## 项目描述
- 由cicd工具生成模板
