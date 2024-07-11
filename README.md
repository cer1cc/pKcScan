# 正经的声明

pKcScan 是由 cer1cc 开发的一个漏洞扫描工具。该项目使用 CC BY-NC-SA 4.0 许可证进行许可。要查看此许可证的副本，请访问 CC BY-NC-SA 4.0。

## 你可以自由地：

分享 —— 在任何媒介或格式中复制和再分发本作品
演绎 —— 混合、转换、和基于本作品创作
只要遵守许可条款，许可人不能收回这些自由。

## 根据以下条款：

署名 —— 你必须给出适当的署名，提供指向许可证的链接，并表明是否对作品进行了修改。你可以以任何合理的方式进行，但不得以任何方式暗示许可人认可你或你的使用。
非商业性使用 —— 你不得将本作品用于商业目的。
相同方式共享 —— 如果你再混合、转换或者基于本作品进行创作，你必须基于与原作品相同的许可协议分发你的贡献。
没有附加限制 —— 你不得适用法律条款或技术措施从而限制其他人做许可证允许的事情。
声明：
你不必遵守许可协议中的条款，对于那些处于公共领域的部分，或者你的使用被适用的例外或限制允许的部分。

许可证不提供任何担保。该许可证可能无法为你的使用提供所需的所有权限。例如，其他权利如公开权、隐私权或道德权利可能会限制你对素材的使用。

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
3. 使用 mongo 数据库管理 poc 和 fingerprint, 第一次使用时将会将本地 json 格式的 Poc 加载至数据库

## fingerprint 相关规则

1. fingerprint 放在 module/fingerprint/allFingerprint 目录, 目录位置 ./module/fingerprint/allFingerprint
2. fingerprint 全部为 Json 文件(暂时只支持 Json 文件)
3. fingerprint 文件模板位于 ./module/fingerprint/Template.json (fingerprint 自行添加)
4. 请求包与响应包请按照 http 协议要求书写
5. 模板中可以有多次请求和响应
6. 如果只有一次请求就会分为两种情况, 一是请求方式为空的,就视为被动识别,不会发起请求检测;二是有请求方式的,就视为主动识别,会发起请求进行检测
7. 指纹识别优先执行被动识别, 如果识别成功,将不会执行主动识别

## Poc 相关规则

1. Poc 放在 module/poc 目录, 目录位置 ./module/Poc/
2. Poc 分类名称必须小写, 例如: ./module/Poc/pikachu
3. Poc 版本号位于 Poc 名称下一级, 例如: ./module/Poc/pikachu/1.1.1
4. Poc 全部为 Json 文件(暂时只支持 Json 文件)
5. Poc 文件模板位于 ./module/Poc/Template.json (Poc 自行添加)
6. 请求包与响应包请按照 http 协议要求书写
7. Poc 类型
   > 类型 1 为一次请求就能从响应中识别出漏洞特征

> 类型 2 为添加关键‘§’符号，将会对内容进行爆破，主要用于暴力检测

> 类型 3 多次发包进行检测
