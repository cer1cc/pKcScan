## 使用方法

终端运行

```python
docker compose up# 启动数据库
python3 pKcScan.py # 就可以正常运行了
```

然后就可以使用该项目了

## 项目结构
```python
├── core
│   ├── bin
│   │   ├── app.py # 核心操作
│   │   ├── core.py # 核心方法
│   │   ├── forMogoDB.py # Mongodb 数据库 Poc json to PocData对象的操作 (操作的是连接成功后的对象)
│   │   ├── handlePoc.py # Poc json文件 文件相关方法
│   │   ├── __init__.py 
│   │   ├── OInitializeURL.py # URL对象 放置了一些简单操作
│   │   ├── Oreadjson.py # Poc Json 加载为对象 设置了一些方法
│   │   └── writeJsonToDB.py # 初始化数据库,删除数据库数据操作,读写Poc json至数据库 (调用mongoConnect中的方法)
│   ├── initialize
│   │   ├── color.py # 控制台彩色输出
│   │   ├── config.json # 脚本是否初始化的依据
│   │   ├── flag.py # 好看的输出
│   │   ├── globals.py # 全局参数设置
│   │   ├── __init__.py
│   │   ├── mongoConnect.py # 数据库连接 断开 写入操作 (直接操作数据库)
│   │   ├── printf.py # 打印方式统一控制
│   │   ├── shellArgparse.py # 脚本方法管理
│   │   └── system.py # 系统相关操作
│   └── library # 第三方库
│       ├── argparse_1_4_0
│       ├── colorama_0_4_6
│       ├── mongo_python_driver_4_7_2
│       ├── requests_2_32_2
│       └── __init__.py
├── docker-compose.yml # 数据库运行文件
├── module 
│   ├── fingerprint # 指纹放置在这里
│   │   └── allFingerprint
│   │       ├── indexpikachu.json
│   │       └── rcepikachu.json
│   ├── jsonC.py
│   ├── PentestDicts
│   │   ├── all-attacks # payload 放置在这里 全是字典,可以进行模糊测试 
│   │   │   ├── all-attacks-payloads.txt
│   │   │   ├── interesting-metacharacter.txt
│   │   │   ├── null-fuzz.txt
│   │   │   └── url-hex-fuzz.txt
│   │   ├── american-wordlist
│   │   │   ├── asteroids.txt
│   │   │   ├── bacteria.txt
│   │   │   ├── bible.txt
..............
│   ├── Poc # Poc 按分类放在这里
│   │   └── pikachu 
..............
│   ├── Report # 运行日志放在这里,生成的日志也在这里
│   │   └── report.md
│   ├── RW_Password.py # 密码查找的一个脚本
│   └── Template.json # Poc json 模板
├── pKcScan.py # 从这里开始
├── poetry.lock # 项目的依赖管理的锁文件
├── pyproject.toml # 项目的依赖控制文件
└── README.md
```
## 项目介绍

1. 项目从根目录文件 pKcScan.py 运行,调用 ./core/app.py 中为核心操作
2. 项目核心功能放在 core 模块,core.py 中(./core/core.py)
3. 使用mongo数据库管理poc和fingerprint, 第一次使用时将会将本地json格式的Poc加载至数据库

## fingerprint 相关规则

1. fingerprint 放在 module/fingerprint/allFingerprint 目录, 目录位置 ./module/fingerprint/allFingerprint
2. fingerprint 全部为 Json 文件(暂时只支持 Json 文件)
3. fingerprint 文件模板位于 ./module/fingerprint/Template.json (fingerprint 自行添加)
4. 请求包与响应包请按照http协议要求书写
5. 模板中可以有多次请求和响应
6. 如果只有一次请求就会分为两种情况, 一是请求方式为空的,就视为被动识别,不会发起请求检测;二是有请求方式的,就视为主动识别,会发起请求进行检测
7. 指纹识别优先执行被动识别, 如果识别成功,将不会执行主动识别

## Poc 相关规则

1. Poc 放在 module/poc 目录, 目录位置 ./module/Poc/
2. Poc 分类名称必须小写, 例如: ./module/Poc/pikachu
3. Poc 版本号位于 Poc 名称下一级, 例如: ./module/Poc/pikachu/1.1.1
4. Poc 全部为 Json 文件(暂时只支持 Json 文件)
5. Poc 文件模板位于 ./module/Poc/Template.json (Poc 自行添加)
6. 请求包与响应包请按照http协议要求书写
7. Poc类型 
>    类型1 为一次请求就能从响应中识别出漏洞特征 

>    类型2 为添加关键‘§’符号，将会对内容进行爆破，主要用于暴力检测

>    类型3 多次发包进行检测

