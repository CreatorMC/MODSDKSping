![MODSDKSpring](https://github.com/user-attachments/assets/1963bf92-d5e0-41f7-b5b9-b049f0ab8cb8)

# 什么是 MODSDKSpring

MODSDKSpring 是一个非官方的，由创造者MC制作的，在网易我的世界 MODSDK 基础上开发的框架。目的是为了简化并规范网易我的世界 [MOD](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/1-Mod%E5%BC%80%E5%8F%91%E7%AE%80%E4%BB%8B/1-Mod%E7%AE%80%E4%BB%8B.html) 的开发。

# 为什么要用 MODSDKSpring

MODSDKSpring 定义了一系列的装饰器（就像您在 modMain.py 中看到的 @Mod.InitClient() 这种写法），避免了自己写 self.ListenForEvent 去监听事件。另外，MODSDKSpring 借鉴了 Java 语言中的知名框架 Spring 的相关概念，实现了针对 MODSDK 的控制反转和依赖注入。

具体而言，框架可以做到只注册一个客户端类和服务端类，就能像注册了多个客户端类和服务端类那样，每个模块（.py 文件）各司其职，自己监听需要监听的事件并在模块内处理。这样一来，我们可以设计出更合理的 MOD 结构，不必在单个 py 文件中把所有功能都耦合到一起。

上面的描述如果没看懂也没关系，在接下来的快速入门中，您将直观的感受到使用 MODSDKSpring 所带来的便捷。

# 下载

```shell
pip install mc-creatormc-sdkspring
```

如果您安装了 Python2 和 Python3，您可能需要使用下方的命令去下载。

```shell
pip2 install mc-creatormc-sdkspring
```

# 快速入门
