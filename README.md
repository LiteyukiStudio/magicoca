# Magicoca
![Logo](./logo.png)

## :art: 简介
Magicoca是一个基于MIT协议的简易Python进程通信库，提供了一种简单的方式来实现进程间通信。

## :rocket: 安装
使用pip安装：
```bash
pip install magicoca
```

或是使用源码安装(不推荐)：

1. 将仓库clone到本地
> 你需要首先安装[Git](https://git-scm.com/)

```bash
git clone https://github.com/LiteyukiStudio/magicoca
```

> 如果你的网络环境受到限制或影响, 也可以尝试使用Liteyuki Gitea镜像仓库:
> ```bash
> https://git.liteyuki.icu/bot/magicoca
> ```


2. 进入仓库目录(取决于你的文件夹路径)

```bash
cd magicoca
```

3. 使用pip本地安装
```bash
pip install -e .
```

## :hammer: 使用
```python
from magicoca.chan import Chan

# 创建一个通道
ch = Chan()

# 发送消息
ch << "hello"

# 接受消息
msg = str << ch

# 通道关闭
ch.close()
```

## :book: 文档

### 通道
通道是一个用于进程间通信的对象。
如:
```python
from magicoca.chan import Chan

ch = Chan()
```
这里的`ch`就是一个通道。

### 发送消息
使用`<<`操作符可以将消息发送到通道。
如:
```python
ch << "hello"
```
这里的`"hello"`就是一个消息。

当然你也可以发送其他类型的消息，比如数字、列表等。

### 接受消息
使用`>>`操作符可以从通道中接受消息。
如:
```python
msg = str << ch
```
这里的`msg`就是一个消息。

当然你也可以接受其他类型的消息，比如数字、列表等。

### 通道关闭
使用`close`方法可以关闭通道。
如:
```python
ch.close()
```
当通道关闭后，你就不能再向通道中发送消息了。

### 通道状态
你可以使用`is_closed`方法来判断通道是否关闭。
如:
```python
if ch.is_closed():
    print("通道已关闭")
else:
    print("通道未关闭")
```

或者基于该原理, 你可以使用`if not ch.is_closed():`来判断通道是否未关闭来间接性发送消息并随时关闭通道以避免出现可能的错误。

### 通道容量
实际上Magicoca的通道是没有容量限制的，你可以发送任意数量的消息。
当然, 前提是你的机器内存足够大。

### 通道类型
通道的类型是由你自己定义的。
如:
```python
from magicoca.chan import Chan

# 创建一个通道, 类型为str
ch = Chan(str)
```

如果不指定通道类型, 那么通道的类型将默认为`Any`。

### 通道超时
通道的超时是指在接受消息时, 如果没有消息, 那么就会等待一段时间, 直到有消息或者超时。
如:
```python
from magicoca.chan import Chan

# 创建一个通道, 类型为str, 超时时间为1秒
ch = Chan(str, timeout=1)
```

如果不指定超时时间, 那么通道的超时时间将默认为`None`。

即无限等待。

### 通道支持
支持线程间通信。
