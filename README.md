# MODSDKSpring 示例

> 此分支内提供了使用 MODSDKSpring 框架的各种示例。

## TutorialMod

网易我的世界官方教程 [TutorialMod](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/60-Demo%E7%A4%BA%E4%BE%8B.html#TutorialMod) 的 MODSDKSpring 版本。

## TutorialComponentMod

使用 MODSDKSpring 组件机制改造的网易我的世界官方教程 [TutorialMod](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/60-Demo%E7%A4%BA%E4%BE%8B.html#TutorialMod)。

## ParticleMod

实现了生物受伤时播放火圈扩散粒子的效果。

包含定义组件、依赖注入、监听自定义事件。

## MultipleMod

演示了在 `modMain.py` 中注册多个客户端和服务端的情况。

包含定义组件、跨系统调用组件。

进入世界存档后，您将看到如下日志：

```log
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] BCopyServerComponent 组件创建成功
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] BCopyServerComponent 获取到的系统：<multipleModScripts.CopyServerSystem.CopyServerSystem object at 0x00000186D7503A58>
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] ACopyServerComponent 组件创建成功
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] ACopyServerComponent 获取到的系统：<multipleModScripts.CopyServerSystem.CopyServerSystem object at 0x00000186D7503A58>
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] CCopyServerComponent 组件创建成功
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] CCopyServerComponent 获取到的系统：<multipleModScripts.CopyServerSystem.CopyServerSystem object at 0x00000186D7503A58>
[2024-09-07 14:40:05,578] [INFO] [MODSDKSpring] CopyServerSystem 系统创建成功
[2024-09-07 14:40:05,585] [INFO] [MODSDKSpring] BMultipleServerComponent 组件创建成功
[2024-09-07 14:40:05,586] [INFO] [MODSDKSpring] BMultipleServerComponent 获取到的系统：<multipleModScripts.MultipleServerSystem.MultipleServerSystem object at 0x00000186D757CF98>
[2024-09-07 14:40:05,586] [INFO] [MODSDKSpring] AMultipleServerComponent 组件创建成功
[2024-09-07 14:40:05,586] [INFO] [MODSDKSpring] AMultipleServerComponent 获取到的系统：<multipleModScripts.MultipleServerSystem.MultipleServerSystem object at 0x00000186D757CF98>
[2024-09-07 14:40:05,586] [INFO] [MODSDKSpring] CMultipleServerComponent 组件创建成功
[2024-09-07 14:40:05,586] [INFO] [MODSDKSpring] CMultipleServerComponent 获取到的系统：<multipleModScripts.MultipleServerSystem.MultipleServerSystem object at 0x00000186D757CF98>
[2024-09-07 14:40:05,586] [INFO] [MODSDKSpring] MultipleServerSystem 系统创建成功
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] ACopyClientComponent 组件创建成功
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] ACopyClientComponent 获取到的系统：<multipleModScripts.CopyClientSystem.CopyClientSystem object at 0x00000186D0C3BF98>
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] CCopyClientComponent 组件创建成功
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] CCopyClientComponent 获取到的系统：<multipleModScripts.CopyClientSystem.CopyClientSystem object at 0x00000186D0C3BF98>
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] BCopyClientComponent 组件创建成功
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] BCopyClientComponent 获取到的系统：<multipleModScripts.CopyClientSystem.CopyClientSystem object at 0x00000186D0C3BF98>
[2024-09-07 14:40:06,345] [INFO] [MODSDKSpring] CopyClientSystem 系统创建成功
[2024-09-07 14:40:06,352] [INFO] [MODSDKSpring] BMultipleClientComponent 组件创建成功
[2024-09-07 14:40:06,352] [INFO] [MODSDKSpring] BMultipleClientComponent 获取到的系统：<multipleModScripts.MultipleClientSystem.MultipleClientSystem object at 0x00000186D0C474A8>
[2024-09-07 14:40:06,352] [WARNING] [MODSDKSpring] 没有找到带有 @InitComponentClient 或 @InitComponentServer 的类 ACopyClientComponent，将使用 None 进行注入。
[2024-09-07 14:40:06,354] [INFO] [MODSDKSpring] AMultipleClientComponent 组件创建成功
[2024-09-07 14:40:06,354] [INFO] [MODSDKSpring] AMultipleClientComponent 错误的获取到了：None
[2024-09-07 14:40:06,354] [INFO] [MODSDKSpring] AMultipleClientComponent 获取到的系统：<multipleModScripts.MultipleClientSystem.MultipleClientSystem object at 0x00000186D0C474A8>
[2024-09-07 14:40:06,354] [INFO] [MODSDKSpring] CMultipleClientComponent 组件创建成功
[2024-09-07 14:40:06,354] [INFO] [MODSDKSpring] CMultipleClientComponent 获取到的系统：<multipleModScripts.MultipleClientSystem.MultipleClientSystem object at 0x00000186D0C474A8>
[2024-09-07 14:40:06,354] [INFO] [MODSDKSpring] MultipleClientSystem 系统创建成功
[2024-09-07 14:40:10,845] [INFO] [MODSDKSpring] AMultipleClientComponent 正确的获取到了：<multipleModScripts.components.CopyMod.client.ACopyClientComponent.ACopyClientComponent object at 0x00000186D0C472B0>
```

## CirculateMod

演示了如何解决循环依赖。

包含定义组件、依赖注入、解决循环依赖。

进入世界存档后，您将看到如下日志：

```log
[2024-09-07 15:07:20,868] [INFO] [MODSDKSpring] CirculateServerSystem 系统创建成功
[2024-09-07 15:07:21,655] [INFO] [MODSDKSpring] A 组件创建成功
[2024-09-07 15:07:21,655] [INFO] [MODSDKSpring] B 组件创建成功
[2024-09-07 15:07:21,655] [INFO] [MODSDKSpring] C 组件创建成功
[2024-09-07 15:07:21,655] [INFO] [MODSDKSpring] CirculateClientSystem 系统创建成功
```

在游戏聊天框界面能看到下图所示的内容：

![游戏聊天框截图](https://github.com/user-attachments/assets/e28d90dd-7dcc-4414-86f5-5a5d1459c918)