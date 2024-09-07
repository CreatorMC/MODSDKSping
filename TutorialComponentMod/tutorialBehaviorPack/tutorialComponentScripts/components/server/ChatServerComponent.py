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