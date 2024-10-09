# magicoca
A communication library for Python

## 支持的通信方式
- 进程通信

## 稀奇古怪的语法

```python
from magicoca.chan import Chan

ch = Chan()

# 发送消息

ch << "hello"

# 接受消息

msg = str << ch

# 通道关闭

ch.close()

# 可跨进程通信
```