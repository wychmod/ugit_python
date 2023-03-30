# ugit_python
用python语言实现git。

## 本地安装ugit
```shell
pip install -e .  
```

## 本地保存单个对象
```shell
ugit init
Initialized empty ugit repository in .ugit
echo some file > bla
ugit hash-object bla
0e08b5e8c10abc3e455b75286ba4a1fbd56e18a5
ugit cat-file 0e08b5e8c10abc3e455b75286ba4a1fbd56e18a5
some file
```