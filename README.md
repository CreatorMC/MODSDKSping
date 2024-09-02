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

    针对 MODSDKSpring，解释上一步骤中的代码。对于新增装饰器的详细说明，可以查看此文档中的 [装饰器文档](https://github.com/CreatorMC/MODSDKSping/tree/main?tab=readme-ov-file#) 部分。

    - @ListenEvent.InitServer 是什么？

      这是 MODSDKSpring 框架提供的一个装饰器，只能添加到**服务端类**的上方，标识此类是一个服务端。只有添加了这个装饰器，才能启用类内的其他 MODSDKSpring 中的装饰器。注意，使用时最后不要加括号。

      类似的还有 @ListenEvent.InitClient。

    - @ListenEvent.Server(eventName="ServerChatEvent") 是什么？

      这是 MODSDKSpring 框架提供的一个装饰器，只能添加到**服务端类或组件**的方法上。它代替了 self.ListenForEvent，表示此方法要监听的事件，事件的回调方法即是此方法。

      其中 `eventName` 表示要监听的事件的名称。除了监听 MODSDK 提供的事件，它还可以监听其他系统发送的自定义事件，详见装饰器文档部分。

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

5. 运行

    至此，我们已经完成了对快速入门示例的改造。把在 `TutorialServerSystem.py` 中的监听，移到了 `ChatServerComponent.py` 中。现在您可以导入改造后的行为包，在聊天窗口中输入 `钻石剑` 验证 Mod 是否生效。

6. 代码解释

    - @ListenEvent.InitComponentServer 是什么？

      这是 MODSDKSpring 框架提供的一个装饰器，只能添加到**服务端组件**的上方，标识此类是一个服务端组件。只有添加了这个装饰器，才能启用类内的其他 MODSDKSpring 中的装饰器。注意，使用时最后不要加括号。

      此装饰器还能具体指定该服务端组件属于哪个服务端，即组件的 `__init__` 方法中的参数 `server` 具体是哪个服务端系统。如果您在 `modMain.py` 中只注册了一个服务端，那么此处无需指定该组件属于哪个服务端。具体如何指定，详见装饰器文档部分。

      类似的还有 @ListenEvent.InitComponentClient。

# 装饰器文档

这一部分解释了 MODSDKSpring 中各个装饰器的用法。适合入门 MODSDKSpring 后快速查阅相关功能时使用。