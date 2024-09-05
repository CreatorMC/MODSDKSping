![MODSDKSpring](https://github.com/user-attachments/assets/1963bf92-d5e0-41f7-b5b9-b049f0ab8cb8)

# 什么是 MODSDKSpring

MODSDKSpring 是一个非官方的，由魔灵工作室-创造者MC制作的，在网易我的世界 MODSDK 基础上开发的框架。目的是为了简化并规范网易我的世界 [MOD](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/1-Mod%E5%BC%80%E5%8F%91%E7%AE%80%E4%BB%8B/1-Mod%E7%AE%80%E4%BB%8B.html) 的开发。

# 为什么要用 MODSDKSpring

MODSDKSpring 定义了一系列的装饰器（就像您在 modMain.py 中看到的 @Mod.InitClient() 这种写法），避免了自己写 self.ListenForEvent 去监听事件。另外，MODSDKSpring 借鉴了 Java 语言中的知名框架 Spring 的相关概念，实现了针对 MODSDK 的控制反转和依赖注入。

具体而言，框架可以做到只注册一个客户端类和服务端类，就能像注册了多个客户端类和服务端类那样，每个模块（.py 文件）各司其职，自己监听需要监听的事件并在模块内处理。这样一来，我们可以设计出更合理的 Mod 结构，不必在单个 `.py` 文件中把所有功能都耦合到一起。

上面的描述如果没看懂也没关系，在接下来的快速入门中，您将直观的感受到使用 MODSDKSpring 所带来的便捷。

# Python 版本

因为网易我的世界 MODSDK 使用的是 [python 2.7.18](https://www.python.org/downloads/release/python-2718/)，所以此框架也使用相同的版本。

# 框架下载

```shell
pip install mc-creatormc-sdkspring
```

如果您安装了 Python2 和 Python3，您可能需要使用下方的命令去下载。

```shell
pip2 install mc-creatormc-sdkspring
```

# 示例代码

本文档中的教程源码，均可在仓库中的 [example](https://github.com/CreatorMC/MODSDKSping/tree/example) 分支中查看。

# 快速入门

> 快速入门教程改造自网易我的世界开发者官网 DemoMod 中的 [TutorialMod](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/60-Demo%E7%A4%BA%E4%BE%8B.html#TutorialMod)。您在阅读本篇教程时，可与官方代码进行对照，感受 MODSDKSpring 的便捷。

> 教程开始前，请确保您已经下载并安装了 [python 2.7.18](https://www.python.org/downloads/release/python-2718/)、[MODSDKSpring](https://github.com/CreatorMC/MODSDKSping/tree/main?tab=readme-ov-file#%E6%A1%86%E6%9E%B6%E4%B8%8B%E8%BD%BD) 以及 [ModSDK 补全库](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.html?catalog=1#%E5%AE%89%E8%A3%85mod-sdk%E8%A1%A5%E5%85%A8%E5%BA%93)。

> 虽然 [ModSDK 补全库](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.html?catalog=1#%E5%AE%89%E8%A3%85mod-sdk%E8%A1%A5%E5%85%A8%E5%BA%93) 理论上不是必须的，但安装后可以帮助您的代码编辑器使用语法补全等功能。

> 本教程假设您对 MODSDK 已经有了基本的了解，理解基础的事件监听与回调机制。如果您还不了解，请参考 [官方教程](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.html?catalog=1) 自行学习。

1. 创建文件夹

    首先，创建一个如下所示的行为包结构。

    ```txt
    TutorialMod
    └── tutorialBehaviorPack
        ├── entities
        └── manifest.json
    ```

    其中，manifest.json 文件内的内容如下。

    ```json
    {
      "format_version": 2,
      "header": {
        "name": "MODSDKSpring教程行为包",
        "description": "作者:创造者MC",
        "uuid": "a44ca707-044d-47c4-ab75-d0568eef5d00",
        "version": [1 ,0 ,0],
        "min_engine_version": [1 ,18 ,0]
      },
      "modules": [
        {
          "description": "作者:创造者MC",
          "uuid": "627b21f9-f6e5-44f1-82d3-4f3249606e20",
          "version": [1,0,0],
          "type": "data"
        }
      ]
    }
    ```

2. 自动生成 Mod 结构
    
    MODSDKSpring 提供了命令行形式的自动生成工具，能够自动生成包含 MODSDKSpring 的初始的 Mod 结构。

    如果您的电脑是 Windows 系统，在 `TutorialMod/tutorialBehaviorPack` 文件夹内的地址栏上输入 `cmd` 并按下 `Enter` 键，即可在当前位置打开一个命令行窗口。

    ![打开命令行窗口截图](https://github.com/user-attachments/assets/e109fa00-b301-47ed-a575-74043327ed54)

    接着输入以下命令：

    ```shell
    modsdkspring init
    ```

    您会在命令行窗口看到如下输出：

    ```shell
    Start initializing your Mod...
    Please enter the name of the Mod folder:
    ```

    请注意，如果您看到的是：

    ```shell
    'modsdkspring' 不是内部或外部命令，也不是可运行的程序或批处理文件。
    ```

    说明您还没有下载并安装 MODSDKSpring。请查看本文档上方的 [框架下载](https://github.com/CreatorMC/MODSDKSping/tree/main?tab=readme-ov-file#%E6%A1%86%E6%9E%B6%E4%B8%8B%E8%BD%BD) 部分，然后重复此步骤。

    接下来按照提示 Please enter the name of the Mod folder（请输入 Mod 文件夹的名称），输入以下名称后按 `Enter` 键。

    ```shell
    tutorialScripts
    ```

    接着出现提示 Please enter the Mod name, which will serve as the namespace registered to the engine（请输入Mod名称，该名称将作为注册到引擎的命名空间），继续输入以下内容后按 `Enter` 键。

    ```shell
    TutorialMod
    ```

    接着出现提示 Please enter the client system name, which will serve as the class name for the client system（请输入客户端系统名称，该名称将作为客户端系统的类名），继续输入以下内容后按 `Enter` 键。

    ```shell
    TutorialClientSystem
    ```

    接着出现提示 Please enter the server system name, which will serve as the class name for the server system（请输入服务端系统名称，该名称将作为服务端系统的类名），继续输入以下内容后按 `Enter` 键。

    ```shell
    TutorialServerSystem
    ```

    最后出现提示 Created successfully!

    ![命令行窗口](https://github.com/user-attachments/assets/253378a0-4468-466b-965c-be7961f600a1)

    此时查看文件夹结构，您应该得到了如下所示的结构：

    ```txt
    TutorialMod
    └── tutorialBehaviorPack
        ├── entities
        ├── tutorialScripts
        │   ├── components
        │   │   ├── client
        │   │   │   └── __init__.py
        │   │   ├── server
        │   │   │   └── __init__.py
        │   │   └── __init__.py
        │   ├── modCommon
        │   │   ├── __init__.py
        │   │   └── modConfig.py
        │   ├── plugins
        │   │   ├── MODSDKSpring
        │   │   │   └── ...
        │   │   └── __init__.py
        │   ├── __init__.py
        │   ├── modMain.py
        │   ├── TutorialClientSystem.py
        │   └── TutorialServerSystem.py
        └── manifest.json
    ```

    现在，这个 Mod 已经可以直接放入游戏中运行了。

3. Mod 结构介绍

    > 如果您已经会使用 MODSDK 了，那么这一部分快速浏览一遍即可。

    - \_\_init\_\_.py

      python2 中，每个包含 `.py` 文件的文件夹内都需要一个 `__init__.py` 文件。

    - modMain.py

      此文件是 Python 逻辑的入口文件，需要在这里定义哪个类是客户端，哪个类是服务端，以及 Mod 的名称和版本。

      实际上，您可以在 `modMain.py` 中，创建多个 `class`，以此创建多个 Mod。但在 MODSDKSpring 中，我们不推荐这样做。因为 MODSDKSpring 的架构，已经解决了这样做所带来的“好处”。尽管如此，为了框架的灵活性和对现有项目的改造，MODSDKSpring 仍然兼容在同一个 `modMain.py` 中定义多个 Mod 的写法。在后面的部分中，您可以看到相关的写法。

      更多关于此文件的详细说明，请参考 [官方文档](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.html?catalog=1#modmain-py%E6%98%AF%E4%BB%80%E4%B9%88)。
    
    - TutorialClientSystem.py

      此文件是 Mod 的客户端。每个玩家都拥有一个独立的客户端，但服务端是当前联机房间内所有玩家共享的。

      更多关于此文件的详细说明，请参考 [官方文档](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.html?catalog=1#%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8E%E5%AE%A2%E6%88%B7%E7%AB%AF)。

    - TutorialServerSystem.py

      此文件是 Mod 的服务端。每个玩家都拥有一个独立的客户端，但服务端是当前联机房间内所有玩家共享的。

      更多关于此文件的详细说明，请参考 [官方文档](https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.html?catalog=1#%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8E%E5%AE%A2%E6%88%B7%E7%AB%AF)。

    - components

      存放“组件”的文件夹，此处的“组件”，是 MODSDKSpring 的一个概念。在后续的文档中会详细介绍。

      其中，`client` 文件夹，存放能调用**客户端**相关 API 的组件。`server` 文件夹，存放能调用**服务端**相关 API 的组件。

    - modCommon

      存放 Mod 中一些通用的模块。其中，`modConfig.py` 文件中，默认存放了有关 Mod 本身信息的一些常量。
    
    - plugins

      插件文件夹，可存放一些额外的第三方模块（通常不是你自己编写的模块）。MODSDKSpring 框架本身被放置在此文件夹中。

4. 监听事件

    打开 TutorialServerSystem.py 文件，添加以下代码：

    ```python
    @ListenEvent.Server(eventName="ServerChatEvent")
    def OnServerChat(self, args):
        print "==== OnServerChat ==== ", args
        # 生成掉落物品
        # 当我们输入的信息等于右边这个值时，创建相应的物品
        # 创建Component，用来完成特定的功能，这里是为了创建Item物品
        playerId = args["playerId"]
        comp = compFactory.CreateItem(playerId)
        if args["message"] == "钻石剑":                      
            # 调用SpawnItemToPlayerInv接口生成物品到玩家背包，参数参考《MODSDK文档》
            comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_sword", "count":1, 'auxValue': 0}, playerId)
        elif args["message"] == "钻石镐":
            comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_pickaxe", "count":1, 'auxValue': 0}, playerId)
        elif args["message"] == "钻石头盔":
            comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_helmet", "count":1, 'auxValue': 0}, playerId)
        elif args["message"] == "钻石胸甲":
            comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_chestplate", "count":1, 'auxValue': 0}, playerId)
        elif args["message"] == "钻石护腿":
            comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_leggings", "count":1, 'auxValue': 0}, playerId)
        elif args["message"] == "钻石靴子":
            comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_boots", "count":1, 'auxValue': 0}, playerId)
        else:
            print "==== Sorry man ===="
    ```

    最终，整个文件的代码如下：

    ```python
    # -*- coding: utf-8 -*-

    import mod.server.extraServerApi as serverApi
    from tutorialScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
    ServerSystem = serverApi.GetServerSystemCls()
    compFactory = serverApi.GetEngineCompFactory()

    @ListenEvent.InitServer
    class TutorialServerSystem(ServerSystem):

        def __init__(self, namespace, systemName):
            pass

        @ListenEvent.Server(eventName="ServerChatEvent")
        def OnServerChat(self, args):
            print "==== OnServerChat ==== ", args
            # 生成掉落物品
            # 当我们输入的信息等于右边这个值时，创建相应的物品
            # 创建Component，用来完成特定的功能，这里是为了创建Item物品
            playerId = args["playerId"]
            comp = compFactory.CreateItem(playerId)
            if args["message"] == "钻石剑":                      
                # 调用SpawnItemToPlayerInv接口生成物品到玩家背包，参数参考《MODSDK文档》
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_sword", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石镐":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_pickaxe", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石头盔":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_helmet", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石胸甲":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_chestplate", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石护腿":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_leggings", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石靴子":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_boots", "count":1, 'auxValue': 0}, playerId)
            else:
                print "==== Sorry man ===="

    ```

    上面的代码监听了 [ServerChatEvent](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html#serverchatevent) 事件，和官方教程一样，当玩家在聊天框中输入指定的文字，就会给予玩家指定的物品。

    看到这里，您可能会有几个疑问。不用担心，继续往下看，我马上会向您解释这一切。

5. 代码解释

    针对 MODSDKSpring，解释上一步骤中的代码。对于新增装饰器的详细说明，可以查看此文档中的 [装饰器文档](#%E8%A3%85%E9%A5%B0%E5%99%A8%E6%96%87%E6%A1%A3) 部分。

    - @ListenEvent.InitServer 是什么？

      这是 MODSDKSpring 框架提供的一个装饰器，只能添加到**服务端类**的上方，标识此类是一个服务端。只有添加了这个装饰器，才能启用类内的其他 MODSDKSpring 中的装饰器。注意，使用时最后不要加括号。

      类似的还有 @ListenEvent.InitClient。

    - @ListenEvent.Server(eventName="ServerChatEvent") 是什么？

      这是 MODSDKSpring 框架提供的一个装饰器，只能添加到**服务端类或组件**的方法上。它代替了 self.ListenForEvent，表示此方法要监听的事件，事件的回调方法即是此方法。

      其中 `eventName` 表示要监听的事件的名称。除了监听 MODSDK 提供的事件，它还可以监听其他系统发送的自定义事件，详见 [监听自定义事件](#%E7%9B%91%E5%90%AC%E8%87%AA%E5%AE%9A%E4%B9%89%E4%BA%8B%E4%BB%B6) 部分。

      类似的还有 @ListenEvent.Client。
    
    - \_\_init\_\_ 方法内的 super(XXX, self).\_\_init\_\_(namespace, systemName) 去哪了？

      对父类构造方法的调用，已经被封装进了 MODSDKSpring 内部。您不再需要，也不应该手动调用父类构造方法。
    
    - Destroy 方法去哪了？

      Destroy 方法已经被封装进了 MODSDKSpring 内部，并且会在系统销毁时自动取消系统中所有的监听。您不需要重写 Destroy 方法了，但是，如果您需要在 Destroy 方法中做除了取消监听以外的事情，您仍然可以重写 Destroy 方法，并且不会影响自动取消监听的功能。

6. 运行

    恭喜你！现在可以把上面的行为包放入游戏了。如果您使用网易的我的世界开发者启动器，您应该会在进入游戏时看到如下内容。

    ![启动日志截图](https://github.com/user-attachments/assets/cb77899b-1f92-45df-b524-2afdbf25bfd8)

    在游戏的聊天窗口中输入 `钻石剑`，验证 Mod 是否生效。如果您遇到了问题，可以再仔细看看上面的步骤，或下载 example 分支内的示例。

# 定义组件

这里的“组件”，是一个 MODSDKSpring 中的概念。通常情况下，我们会在一个客户端系统或服务端系统中监听很多事件，写很多的回调函数，这就导致我们的代码都耦合在一个文件内，添加和修改都很麻烦。这点在大项目中尤其明显。

针对上述情况，MODSDKSpring 提出了“组件”的概念。所谓“组件”，在功能上可以看作是一个独立的客户端/服务端，组件可以像独立的客户端/服务端那样，自己监听事件并进行处理。这样一来，您可以将一些具有共同特点的功能，单独写成一个 `.py` 文件，再也不用迷失在成百上千行的代码中了。

组件分为两种，一种是客户端组件，一种是服务端组件。无论是客户端组件还是服务端组件，它们都可以有多个。一个组件只属于一个系统。

上面说的这些暂时理解不了没关系，接下来我会带您改造快速入门中的示例，用组件的方式去实现相同的功能。

1. 复制文件夹

    复制我们在快速入门中创建的文件夹 `TutorialMod`，并重命名为 `TutorialComponentMod`。
    
    如果您没有跟着快速入门去做也没关系，在仓库的 example 分支中，可以下载快速入门中的代码。

    将 `tutorialBehaviorPack` 中的 `tutorialScripts` 文件夹重命名为 `tutorialComponentScripts`。

2. 修改配置

    打开 `manifest.json` 修改其中的 `uuid`。UUID 可以使用一些在线网站生成，具体请自行搜索。

    打开 `modCommon` 文件夹下的 `modConfig.py` 文件，修改为如下内容：

    ```python
    # -*- coding: utf-8 -*-

    # Mod Version
    MOD_NAMESPACE = "TutorialComponentMod"
    MOD_VERSION = "0.0.1"

    # Client System
    CLIENT_SYSTEM_NAME = "TutorialClientSystem"
    CLIENT_SYSTEM_CLS_PATH = "tutorialComponentScripts.TutorialClientSystem.TutorialClientSystem"

    # Server System
    SERVER_SYSTEM_NAME = "TutorialServerSystem"
    SERVER_SYSTEM_CLS_PATH = "tutorialComponentScripts.TutorialServerSystem.TutorialServerSystem"
    ```

3. 创建服务端组件

    回想一下，我们需要监听 `ServerChatEvent` 事件，此事件是一个服务端事件，所以只能用服务端去监听。因此，我们需要创建一个服务端组件，用来专门做这一件事情。

    在 `components` 文件夹内的 `server` 文件夹内，创建一个叫做 `ChatServerComponent.py` 的文件。

    文件内代码如下：

    ```python
    # -*- coding: utf-8 -*-
    import mod.server.extraServerApi as serverApi
    from tutorialComponentScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
    ServerSystem = serverApi.GetServerSystemCls()
    compFactory = serverApi.GetEngineCompFactory()

    @ListenEvent.InitComponentServer
    class ChatServerComponent(object):
        
        def __init__(self, server):
            # 获取服务端系统对象，即 TutorialServerSystem 的对象
            self.server = server

        # 监听ServerChatEvent的回调函数
        @ListenEvent.Server(eventName="ServerChatEvent")
        def OnServerChat(self, args):
            print "==== OnServerChat ==== ", args
            # 生成掉落物品
            # 当我们输入的信息等于右边这个值时，创建相应的物品
            # 创建Component，用来完成特定的功能，这里是为了创建Item物品
            playerId = args["playerId"]
            comp = compFactory.CreateItem(playerId)
            if args["message"] == "钻石剑":                      
                # 调用SpawnItemToPlayerInv接口生成物品到玩家背包，参数参考《MODSDK文档》
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_sword", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石镐":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_pickaxe", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石头盔":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_helmet", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石胸甲":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_chestplate", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石护腿":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_leggings", "count":1, 'auxValue': 0}, playerId)
            elif args["message"] == "钻石靴子":
                comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_boots", "count":1, 'auxValue': 0}, playerId)
            else:
                print "==== Sorry man ===="
    ```

    创建组件时，无论是客户端组件还是服务端组件，都需要继承自 `object` 类，即上方代码中的 `class ChatServerComponent(object):`。

    组件的 `__init__` 方法中的参数，必须有第二个变量（即上方代码中的 `__init__(self, server)` 中的 `server` 变量）。

    如果是客户端组件，`__init__` 方法一般写为 `__init__(self, client)`。

    如果创建的是**服务端组件**，需要在类的上方添加 `@ListenEvent.InitComponentServer` 装饰器。

    如果创建的是**客户端组件**，需要在类的上方添加 `@ListenEvent.InitComponentClient` 装饰器。

4. 修改客户端和服务端文件

    打开 `TutorialClientSystem.py` 文件，修改为以下内容：

    ```python
    # -*- coding: utf-8 -*-

    import mod.client.extraClientApi as clientApi
    # 因为文件夹名称改变，所以导入路径也改变了
    from tutorialComponentScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
    ClientSystem = clientApi.GetClientSystemCls()
    compFactory = clientApi.GetEngineCompFactory()

    @ListenEvent.InitClient
    class TutorialClientSystem(ClientSystem):

        def __init__(self, namespace, systemName):
            pass

    ```

    打开 `TutorialServerSystem.py` 文件，修改为以下内容：

    ```python
    # -*- coding: utf-8 -*-

    import mod.server.extraServerApi as serverApi
    # 因为文件夹名称改变，所以导入路径也改变了
    from tutorialComponentScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
    # 导入组件，尽管这里你没有显式使用它，也必须导入！
    from tutorialComponentScripts.components.server.ChatServerComponent import ChatServerComponent
    ServerSystem = serverApi.GetServerSystemCls()
    compFactory = serverApi.GetEngineCompFactory()

    @ListenEvent.InitServer
    class TutorialServerSystem(ServerSystem):

        def __init__(self, namespace, systemName):
            pass

    ```

    需要特别注意的是，因为网易我的世界限制了 python 的 `os` 模块，MODSDKSpring 框架无法通过路径扫描自动导入所需要的组件，所以您必须在 `TutorialServerSystem.py` 文件中手动导入需要的服务端组件，即 `from tutorialComponentScripts.components.server.ChatServerComponent import ChatServerComponent`。

    同理，如果您创建客户端组件，也需要在客户端系统文件中手动导入需要的客户端组件。

    **通常情况下，这是您的组件不生效的首要原因，请务必牢记！**

    > 有一种更加方便的导入组件的方式，并且 MODSDKSpring 框架提供了类似于 `modsdkspring init` 一样的控制台命令。强烈建议您阅读高级内容中的 [快速导入组件](#%E5%BF%AB%E9%80%9F%E5%AF%BC%E5%85%A5%E7%BB%84%E4%BB%B6) 部分。

5. 运行

    至此，我们已经完成了对快速入门示例的改造。把在 `TutorialServerSystem.py` 中的监听，移到了 `ChatServerComponent.py` 中。现在您可以导入改造后的行为包，在聊天窗口中输入 `钻石剑` 验证 Mod 是否生效。

6. 代码解释

    - @ListenEvent.InitComponentServer 是什么？

      这是 MODSDKSpring 框架提供的一个装饰器，只能添加到**服务端组件**的上方，标识此类是一个服务端组件。只有添加了这个装饰器，才能启用类内的其他 MODSDKSpring 中的装饰器。注意，使用时最后不要加括号。

      此装饰器还能具体指定该服务端组件属于哪个服务端，即组件的 `__init__` 方法中的参数 `server` 具体是哪个服务端系统。如果您在 `modMain.py` 中只注册了一个服务端，那么此处无需指定该组件属于哪个服务端。具体如何指定，详见装饰器文档部分。

      类似的还有 @ListenEvent.InitComponentClient。

# 监听自定义事件

在实际开发中，我们经常会自定义事件，以此来进行客户端与服务端之间的相互通信。MODSDKSpring 也提供了监听自定义事件的方法。

- @ListenEvent.Client

    用于**客户端系统/组件**监听事件，只能添加到**客户端系统/组件**的方法上方。

    其拥有四个参数，参数名及含义如下：

    - eventName (str): 监听的事件名称。
    - namespace (str, 可选): 所监听事件的来源系统的 namespace。默认值为 clientApi.GetEngineNamespace()。
    - systemName (str, 可选): 所监听事件的来源系统的 systemName。默认值为 clientApi.GetEngineSystemName()。
    - priority (int, 可选): 回调函数的优先级。默认值为 0，这个数值越大表示被执行的优先级越高，最高为10。

- @ListenEvent.Server

    用于**服务端系统/组件**监听事件，只能添加到**服务端系统/组件**的方法上方。

    其拥有四个参数，参数名及含义如下：

    - eventName (str): 监听的事件名称。
    - namespace (str, 可选): 所监听事件的来源系统的 namespace。默认值为 clientApi.GetEngineNamespace()。
    - systemName (str, 可选): 所监听事件的来源系统的 systemName。默认值为 clientApi.GetEngineSystemName()。
    - priority (int, 可选): 回调函数的优先级。默认值为 0，这个数值越大表示被执行的优先级越高，最高为10。

客户端系统/组件监听自定义事件的方式如下：

```python
@ListenEvent.Client(namespace=modConfig.MOD_NAMESPACE, systemName=modConfig.SERVER_SYSTEM_NAME, eventName="DamageEventToClient")
def damageEvent(self, event):
    pass
```

服务端系统/组件同理，只是替换为 `@ListenEvent.Server`。

在 [ParticleMod]() 示例中，客户端组件 `HurtEntityClientComponent.py` 监听了服务端组件 `HurtEntityServerComponent.py` 发出的自定义事件 `DamageEventToClient`。您可以下载此示例，查看具体代码。

# 跨组件调用（依赖注入）

设想这样一个场景，您定义了一个专门用于播放粒子的客户端组件 `P`。您有另一个客户端组件 `A`。您想实现在客户端组件 `A` 中调用客户端组件 `P` 中的方法。这时候应该怎么办呢？

要想实现在 `A` 中调用 `P` 的方法，`A` 必须获取到 `P` 的对象，然后执行 `P.xxx()` 这样的语句。`A` 和 `P` 的这种关系，我们可以称为 `A` 依赖于 `P`。即，`P` 是 `A` 的依赖。

MODSDKSpring 框架可以管理上述的依赖关系。具体做法是，框架会在组件被创建时，将组件的对象放入“容器”（实际上就是一个字典）当中。当组件 `A` 需要另一个组件 `P` 时，框架可以从容器中拿到 `P`，并把 `P` 通过**某种方式**传递给 `A`。

这样，`A` 便可以调用 `P` 的方法，并且不会产生 `P` 这个类的新对象。实现了组件的单例模式，节约内存。

那么，**某种方式**具体是什么？MODSDKSpring 框架目前提供了两种从容器中获取组件对象的方法。这两种方法有它们各自的使用场景，具体细节请继续阅读。

## 组件类的对象在容器中的存储形式

所谓的容器，实际上就是一个 `dict` 类型的变量！千万不要想的太复杂，我不喜欢玩文字游戏，希望您也一样。

假设，有一个客户端组件类，类名是 `HurtEntityClientComponent`。当此类在框架中创建对象后，框架会给它起一个“名字”，叫做 `hurtEntityClientComponent`（类名首字母小写）。这个“名字”是容器中的 `key`，而这个 `key` 对应的 `value` 就是类 `HurtEntityClientComponent` 的对象！形式如下。

```python
{
    'hurtEntityClientComponent': HurtEntityClientComponent()
    # ...
}
```

了解了这些，您可以更好的理解下方的从容器中获取组件对象的方法。

## 构造方法注入

假设，有一个客户端组件 `HurtEntityClientComponent`，需要使用另一个客户端组件 `ParticleClientComponent`。

首先，在 `HurtEntityClientComponent` 的 `__init__` 方法的参数上，添加一个变量，名字为 `particleClientComponent`（对应组件类名的首字母小写，**名字不能变！**）。如果您有更多需要调用的组件，在 `__init__` 方法的参数中，可以继续添加更多类似形式的变量。

然后，在 `__init__` 方法的上方添加一个装饰器 `@Autowired`，开启依赖注入。

最后，框架会自动在 `HurtEntityClientComponent` 类的对象被创建时，通过 `__init__` 方法的参数，传入对应的 `ParticleClientComponent` 类的对象。

示例代码如下：

```python
# -*- coding: utf-8 -*-
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from particleModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from particleModScripts.modCommon import modConfig
from particleModScripts.modCommon import eventConfig

@ListenEvent.InitComponentClient
class HurtEntityClientComponent(object):

    @Autowired
    def __init__(self, client, particleClientComponent):
        self.client = client
        self.particleClientComponent = particleClientComponent
```

上述代码来源于 example 分支中的 [ParticleMod]() 示例，您可以自行下载查看。

注意，在 `__init__` 方法中，变量 `particleClientComponent` 不总是有值。如果有循环依赖的情况，可能变量 `particleClientComponent` 在执行完 `__init__` 方法后，才被赋值，所以变量 `particleClientComponent` 在 `__init__` 方法中可能为 `None`。

因此，我建议您永远不要在 `__init__` 方法中调用其他组件的方法！`__init__` 方法应该只做赋值操作！

至于循环依赖是什么情况，请查看 [解决循环依赖](#%E8%A7%A3%E5%86%B3%E5%BE%AA%E7%8E%AF%E4%BE%9D%E8%B5%96) 部分。

> `@Autowired` 也可以被添加到**客户端/服务端系统**的 `__init__` 方法上方，但通常情况下，您不应该这么做。

## getBean() 方法

方法在 `xxx.plugins.MODSDKSpring.core.BeanFactory` 中，`xxx` 应替换为您的行为包中的 Mod 文件夹名称，如 `tutorialScripts`。

- 描述

    该方法能够直接从容器中获取组件对象。

- 参数

    |参数名|数据类型|说明|
    |-----|--------|----|
    |systemType|str|想要获取的组件的类型<br>值为 `SystemType.CLIENT` 或 `SystemType.SERVER`<br>`SystemType` 在 `xxx.plugins.MODSDKSpring.core.constant.SystemType` 中|
    |beanName|str|存放组件的容器的 `key`<br>即类名首字母小写，比如你有一个类名为 `TestComponentClient` 的组件，那么它的 `key` 为 `testComponentClient`|

- 返回值

    |数据类型|说明|
    |-------|----|
    |object \| None|返回容器中的组件对象<br>如果组件不存在，则返回 None|

- 示例

    ```python
    from tutorialScripts.plugins.MODSDKSpring.core.BeanFactory import BeanFactory
    import tutorialScripts.plugins.MODSDKSpring.core.constant.SystemType as SystemType

    testComponentClient = BeanFactory.getBean(SystemType.CLIENT, 'testComponentClient')
    ```

> 该方法适用于在注册了多个客户端系统或服务端系统的情况下，某个系统的组件要调用另外一个系统的组件时使用。一般情况下，请使用 `@Autowired`。

> 该方法不会产生循环依赖问题。

> 永远不要在 `__init__` 方法中使用 `getBean()`，因为此时您需要的组件可能尚未创建。

# 解决循环依赖

设想这样一个场景，您有一个组件 `A`，还有一个组件 `B`。您想在组件 `A` 中调用组件 `B` 的方法，同时，您也想在组件 `B` 中调用组件 `A` 中的方法。这两个组件都想调用对方，就形成了所谓的循环依赖。

从代码逻辑上讲，当组件 `A` 被创建时，框架发现组件 `A` 需要一个组件 `B`，于是就先去创建组件 `B` 的对象。但是在创建组件 `B` 时，框架又发现组件 `B` 需要组件 `A`，于是又去创建组件 `A` 的对象，这就形成了一个循环。如果不做任何处理，最终会因为递归层数过多，抛出异常。

MODSDKSpring 框架目前提供了两种解决循环依赖的方法。一种是在需要调用另一个组件的地方，手动调用 `getBean()` 方法。需要注意的是，不要在 `__init__` 方法中使用 `getBean()`。

另外一种方法，是使用装饰器 `@Lazy`。这种方法应该是您的首选。

## 使用 @Lazy

假设组件 `A` 和 `B` 之间存在循环依赖，那么您只需要在 `A` 或者 `B` 中的 `__init__` 方法上的 `@Autowired` 上面添加 `@Lazy` 即可。注意，是 `A` 或者 `B`，在其中一个类的 `@Autowired` 上面加就行！

添加了 `@Lazy` 的 `__init__` 方法，会在创建对象时先用 `None` 填充方法内的组件的变量。在 `__init__` 方法执行完成，所有组件被创建之后，会再次执行依赖注入，给对象中的组件的变量赋值（如下方代码中的 `self.b`）。示例代码如下。

```python
# -*- coding: utf-8 -*-
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from particleModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from particleModScripts.plugins.MODSDKSpring.core.Lazy import Lazy
from particleModScripts.modCommon import modConfig
from particleModScripts.modCommon import eventConfig

@ListenEvent.InitComponentClient
class A(object):

    @Lazy
    @Autowired
    def __init__(self, client, b):
        self.client = client
        self.b = b # self.b 的值此时为 None，所有组件创建完成后，框架会自动为 self.b 赋值。
```

如果遇到了问题，您可以下载 example 分支中的 [CirculateMod]() 示例，此示例专门演示了如何解决循环依赖。

> `@Lazy` 只能写在 `@Autowired` 的上方！如果写在 `@Autowired` 下方，您会在网易我的世界开发者启动器的日志窗口中看到 `@Lazy 必须添加在 @Autowired 的上方。` 的异常提示。

> `@Lazy` 不能用于**客户端/服务端系统**的 `__init__` 方法上（这里指的是客户端或服务端系统，不是组件）。因为这完全没有必要，使用 `@Autowired` 已足够将组件注入到客户端/服务端系统中，并且不会与系统之间产生循环依赖。如果您对此仍有疑惑，请查看 [CirculateMod]() 示例。

# 高级内容

> 对您来说，这部分的内容不是使用框架所必须看的。但如果您了解了这些高级内容，可能在某些场景下会帮助您更方便的使用框架。

## 快速导入组件

假设您的 Addon 文件结构如下：

```txt
TutorialMod
└── tutorialBehaviorPack
    ├── entities
    ├── tutorialScripts
    │   ├── components
    │   │   ├── client
    │   │   │   ├── __init__.py
    │   │   │   ├── AClientComponent.py
    │   │   │   ├── BClientComponent.py
    │   │   │   └── CClientComponent.py
    │   │   ├── server
    │   │   │   ├── __init__.py
    │   │   │   ├── AServerComponent.py
    │   │   │   ├── BServerComponent.py
    │   │   │   └── CServerComponent.py
    │   │   └── __init__.py
    │   ├── modCommon
    │   │   ├── __init__.py
    │   │   └── modConfig.py
    │   ├── plugins
    │   │   ├── MODSDKSpring
    │   │   │   └── ...
    │   │   └── __init__.py
    │   ├── __init__.py
    │   ├── modMain.py
    │   ├── TutorialClientSystem.py
    │   └── TutorialServerSystem.py
    └── manifest.json
```

在 `TutorialMod/tutorialBehaviorPack/tutorialScripts/components/client/__init__.py` 文件中编写如下代码：

```python
# -*- coding: utf-8 -*-
# 此处假设模块名和模块中定义的类名相同，请根据您的实际情况进行导入
from AClientComponent import AClientComponent
from BClientComponent import BClientComponent
from CClientComponent import CClientComponent
```

在 `TutorialMod/tutorialBehaviorPack/tutorialScripts/components/server/__init__.py` 文件中编写如下代码：

```python
# -*- coding: utf-8 -*-
# 此处假设模块名和模块中定义的类名相同，请根据您的实际情况进行导入
from AServerComponent import AServerComponent
from BServerComponent import BServerComponent
from CServerComponent import CServerComponent
```

在 `TutorialMod/tutorialBehaviorPack/tutorialScripts/TutorialClientSystem.py` 文件顶部添加如下代码：

```python
from tutorialScripts.components.client import *
```

在 `TutorialMod/tutorialBehaviorPack/tutorialScripts/TutorialServerSystem.py` 文件顶部添加如下代码：

```python
from tutorialScripts.components.server import *
```

这样，每当您增加或删除组件时，不需要改动 `TutorialClientSystem.py` 和 `TutorialServerSystem.py` 文件，只需要改动 `client` 和 `server` 文件夹内的 `__init__.py` 文件即可。

您可能还是觉得很麻烦，还是要手动修改文件，称不上“快速”。针对这点，MODSDKSpring 提供了一个控制台命令，能够自动生成上述的 `__init__.py` 文件。

### 自动生成所需的 \_\_init\_\_.py 文件

打开您的命令行窗口，或者在您的代码编辑器中打开一个终端。然后将当前位置切换到 `.../components/client` 或 `.../components/server` 文件夹下。输入下方命令：

```shell
modsdkspring import
```

正常的话，您应该会看到以下输出：

```shell
Starting to create the __init__.py file.
Successfully created the __init__.py file!
```

然后在 `.../components/client` 或 `.../components/server` 文件夹内，就会自动生成一个 `__init__.py` 文件（如果此文件已存在，会自动覆盖文件中的内容）。其中导入了此文件夹及其子文件夹内所有的类。

很多时候，您在代码编辑器中打开一个终端，可能终端所在的默认位置并不是 `.../components/client` 或 `.../components/server`，并且您也不想手动切换位置。这时候，您可以使用 `modsdkspring import` 命令提供的参数 `--path`，指定路径。具体示例如下：

```shell
modsdkspring import --path "tutorialBehaviorPack/tutorialScripts/components/client"
```

上面的命令假设终端的当前位置在 `TutorialMod` 中。命令执行后，会在您指定的路径中生成一个 `__init__.py` 文件。

### 将命令配置为 Visual Studio Code 任务

尽管框架提供了相关命令，但每次添加或删除组件，您都要手动执行一次命令，这仍然比较麻烦，不够自动化。

如果您使用 Visual Studio Code 作为您的代码编辑器，您可以阅读此部分，按照步骤配置自动化任务。

最终实现的效果是，当您在 Visual Studio Code 中保存组件目录下的 `.py` 文件时，Visual Studio Code 将自动执行命令 `modsdkspring import --path "xxx"`。

> 此教程环境说明如下。<br>如果您的设备环境不符合下方的说明，您也可以按此教程尝试配置，如果您遇到了问题，可自行搜索解决。<br><br>操作系统：Windows 10<br>Visual Studio Code 版本：1.72.1

1. 安装扩展

    在 Visual Studio Code 中的扩展中搜索 [Save and Run](https://marketplace.visualstudio.com/items?itemName=wk-j.save-and-run) 或直接点击链接，安装此扩展。本教程的 Save and Run 版本为 0.0.22。

2. 配置扩展

    假设您有一个如下图所示的工作区：

    ![工作区截图](https://github.com/user-attachments/assets/b672f48a-c5b2-4824-b00a-381d1a02f7b3)

    您需要在 `settings` 中增加如下文本：

    ```json
    "saveAndRun": {
        "commands": [
            {
                "match": ".*\\\\components\\\\(client|server).*\\.py",
                "cmd": "modsdkspring import --path \"${fileDirname}\"",
                "useShortcut": false,
                "silent": false
            }
        ]
    }
    ```

    > 如果您有工作区文件 `XXX.code-workspace`，请按上方截图中的方式进行配置。如果您没有工作区文件，请在 `.vscode` 文件夹中的 `settings.json` 文件中添加配置。

    > 您可以修改 `match` 中的正则表达式，以符合您的实际情况。

3. 测试效果

    现在，请尝试修改 `.../components/client` 或 `.../components/server` 文件夹下的 `.py` 文件，在您按 `ctrl + s` 保存文件时，您可以看到 Visual Studio Code 将自动打开一个终端，并执行命令。

    ![测试效果截图](https://github.com/user-attachments/assets/54938356-2c2f-4498-aae0-2c9befcd1882)

## 在 modMain.py 中创建多个客户端和服务端的情况

> 在 MODSDKSpring 框架中，我不推荐您这么做。但是，如果您仍要这么做，MODSDKSpring 也提供了方法。

## 自定义 Mod 生成模板（未来可能的功能）

实际上，现在已经能自定义生成模板了，只是模板被内置在框架当中，没有提供对外的标准方法。感兴趣的开发者，可以阅读相关源码，自行探索自定义生成模板的方法。或者，欢迎您对本框架的代码做出贡献！

# 可能遇到的问题及解决方案

# 装饰器文档

> 这一部分解释了 MODSDKSpring 中各个装饰器的参数和含义。适合入门 MODSDKSpring 后快速查阅相关功能时使用。