# -*- coding: utf-8 -*-
import constant.SystemType as SystemType
import constant.Target as Target
from log.Log import logger
from exception.BeanCurrentlyInCreationException import BeanCurrentlyInCreationException

class BeanFactory(object):
    """
    存储和操作 Bean 对象的类
    """

    # 组件类本身的字典 (依赖注入全部完成后清空)
    # 字典内数据格式如下:
    # componentClsDict = {
    #     SystemType.CLIENT: {
    #         'xxxClientComponent': [ cls, targetNamespace, targetSystemName ],
    #         ...
    #     },
    #     SystemType.SERVER: {
    #         'xxxServerComponent': [ cls, targetNamespace, targetSystemName ],
    #         ...
    #     }
    # }
    componentClsDict = {
        SystemType.CLIENT: {},
        SystemType.SERVER: {}
    }

    # 组件对象字典 (Bean 的容器)
    # 字典内数据格式如下:
    # componentObjectDict = {
    #     SystemType.CLIENT: {
    #         'xxxClientComponent': object,
    #         ...
    #     },
    #     SystemType.SERVER: {
    #         'xxxServerComponent': object,
    #         ...
    #     }
    # }
    componentObjectDict = {
        SystemType.CLIENT: {},
        SystemType.SERVER: {}
    }

    # 组件对象等待注入的字典 (二级缓存，用于解决循环依赖) (依赖注入全部完成后清空)
    # 字典内数据格式如下:
    # componentObjectWaitInjectDict = {
    #     SystemType.CLIENT: {
    #         'xxxClientComponent': object,
    #         ...
    #     },
    #     SystemType.SERVER: {
    #         'xxxServerComponent': object,
    #         ...
    #     }
    # }
    componentObjectWaitInjectDict = {
        SystemType.CLIENT: {},
        SystemType.SERVER: {}
    }

    # 为了清空不再使用的变量，引入的临时列表
    componentKeyTempList = []

    @staticmethod
    def getBean(systemType, beanName):
        """
        获取容器中的 Bean

        Args:
            systemType (str): Bean 绑定的系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
            beanName (str): Bean 的名称，即类名首字母小写，比如你有一个名为 "TestComponentClient" 的类，那么 Bean 的名称为 "testComponentClient"

        Returns:
            (object | None): 返回容器中的 Bean。如果 Bean 不存在，返回 None
        """
        tempDict =  BeanFactory.componentObjectDict.get(systemType)
        if not tempDict:
            return None
        return tempDict.get(beanName)

    @staticmethod
    def createBean(system, systemType, namespace, systemName):
        """
        创建 Bean 并进行依赖注入

        Args:
            system (ClientSystem | ServerSystem): 被注册的客户端或服务端对象
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
            namespace (str): system 的命名空间
            systemName (str): system 的系统名称
        """
        for clsName, componentList in BeanFactory.componentClsDict[systemType].items():
            # 判断此 cls 是不是要注入此 system
            if (componentList[1] == namespace or componentList[1] == Target.DEFAULT) and \
                (componentList[2] == systemName or componentList[2] == Target.DEFAULT):
                BeanFactory.createBeanDfs(componentList[0], system, [], systemType, namespace, systemName)

    @staticmethod
    def createBeanWithInit(cls, system, systemType, namespace, systemName):
        """
        为带有 @Init 的类进行依赖注入，获取所需要的对象并返回

        Args:
            cls (type): 类型本身
            system (ClientSystem | ServerSystem): 被注册的客户端或服务端对象
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
            namespace (str): system 的命名空间
            systemName (str): system 的系统名称

        Returns:
            list: 所需要的对象列表
        """
        dependenceList = []
        # 判断此方法有 @Autowired (只有构造方法会因为 @Autowired 而增加 args 变量)
        if 'args' in cls.__init__.__dict__:
            args = cls.__init__.args
            # 如果构造方法中的参数个数大于 3，说明有需要注入的对象
            if len(args) > 3:
                for i in xrange(3, len(args)):
                    # 如果此类没有加 @InitComponent，则注入 None
                    if not BeanFactory.componentClsDict[systemType].__contains__(args[i]):
                        logger.warning("没有找到带有 @InitComponentClient 或 @InitComponentServer 的类 %s，将使用 None 进行注入。", args[i][0].upper() + args[i][1:])
                        dependenceList.append(None)
                        continue
                    # 判断此 cls 是不是要注入此 system
                    componentList = BeanFactory.componentClsDict[systemType][args[i]]
                    if (componentList[1] == namespace or componentList[1] == Target.DEFAULT) and \
                        (componentList[2] == systemName or componentList[2] == Target.DEFAULT):
                        dependenceList.append(BeanFactory.createBeanDfs(componentList[0], system, [], systemType, namespace, systemName))
                    else:
                        logger.warning("在 %s 类的 __init__ 方法中，%s 指定的系统不是此类，将使用 None 进行注入。如果您想在此系统中调用其他系统的组件，请使用 BeanFactory.getBean() 方法。", cls.__name__, args[i][0].upper() + args[i][1:])
                        dependenceList.append(None)
        return dependenceList

    @staticmethod
    def createBeanDfs(cls, system, creatingClsList, systemType, namespace, systemName):
        """
        递归创建 Bean, 并将 Bean 放入容器中

        Args:
            cls (type): 类型本身
            system (ClientSystem | ServerSystem): 被注册的客户端或服务端对象
            creatingClsList (list): 正在创建的类列表，用于判断是否产生循环依赖
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER,
            namespace (str): system 的命名空间
            systemName (str): system 的系统名称

        Returns:
            object: 创建的对象
        """
        clsName = cls.__name__[0].lower() + cls.__name__[1:]
        # 先判断自己是不是已经被创建 (因为递归创建对象，当前要创建的对象可能已经被创建了，就没有必要再创建一次了)
        if BeanFactory.componentObjectDict[systemType].__contains__(clsName):
            return BeanFactory.componentObjectDict[systemType][clsName]
            
        # 此类的构造方法依赖的对象列表 (如果有 @Autowired 会动态向列表中添加依赖的对象)
        dependenceList = [system]
        method = cls.__init__
        # 标记当前类是否懒注入 (即构造方法中所需要的对象都用 None 注入)
        lazy = False
        if 'lazy' in method.__dict__:
            lazy = method.lazy
        # 判断此方法有 @Autowired (只有构造方法会因为 @Autowired 而增加 args 变量)
        if 'args' in method.__dict__:
            args = method.args
            # 如果构造方法中的参数个数大于 2，说明有需要注入的对象
            if len(args) > 2:
                nextCreatingClsList =  creatingClsList + [clsName]
                # 遍历需要注入的参数
                for i in xrange(2, len(args)):
                    # 如果使用了 @Lazy，使用 None 进行注入
                    if lazy:
                        dependenceList.append(None)
                        continue
                    # 如果发现需要注入的参数正在创建列表中，并且没有开启懒注入, 说明遇到循环依赖
                    if args[i] in creatingClsList:
                        raise BeanCurrentlyInCreationException("类 %s 和 %s 之间存在循环依赖，请使用 @Lazy 解决。" % (cls.__name__, args[i][0].upper() + args[i][1:]))
                    # 如果此类没有加 @InitComponent，则注入 None
                    if not BeanFactory.componentClsDict[systemType].__contains__(args[i]):
                        logger.warning("没有找到带有 @InitComponentClient 或 @InitComponentServer 的类 %s，将使用 None 进行注入。", args[i][0].upper() + args[i][1:])
                        dependenceList.append(None)
                        continue
                    # 判断当前 system 是不是 args[i] 要绑定的对象
                    componentList = BeanFactory.componentClsDict[systemType][args[i]]
                    if not ((componentList[1] == namespace or componentList[1] == Target.DEFAULT) and \
                        (componentList[2] == systemName or componentList[2] == Target.DEFAULT)):
                        logger.warning("在 %s 组件的 __init__ 方法中，%s 指定的系统和此组件指定的系统不一致，将使用 None 进行注入。如果您想在此组件中调用其他系统的组件，请使用 BeanFactory.getBean() 方法。", cls.__name__, args[i][0].upper() + args[i][1:])
                        dependenceList.append(None)
                        continue
                    # 递归创建对象
                    dependenceobj = BeanFactory.createBeanDfs(componentList[0], system, nextCreatingClsList, systemType, namespace, systemName)
                    dependenceList.append(dependenceobj)
        # 拿到了需要注入的所有对象，创建对象
        obj = cls(*dependenceList)
        # 将对象放入容器中
        BeanFactory.componentObjectDict[systemType][clsName] = obj

        # 如果使用了 @Lazy，将创建的对象放入二级缓存，在之后会有方法遍历二级缓存中的对象，进行二次依赖注入
        if lazy:
            BeanFactory.componentObjectWaitInjectDict[systemType][clsName] = obj
        
        # 在临时列表中记录这个对象被创建了
        BeanFactory.componentKeyTempList.append(clsName)

        return obj

    @staticmethod
    def dependenceInjectLast(systemType):
        """
        最后一次依赖注入，遍历二级缓存，进行循环依赖对象的注入

        Args:
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
        """
        for clsName, obj in BeanFactory.componentObjectWaitInjectDict[systemType].items():
            args = obj.__init__.args
            for i in xrange(2, len(args)):
                if not BeanFactory.componentObjectDict[systemType].__contains__(args[i]):
                    logger.warning("没有找到带有 @InitComponentClient 或 @InitComponentServer 的类 %s，将使用 None 进行注入。", args[i][0].upper() + args[i][1:])
                    setattr(obj, args[i], None)
                    continue
                setattr(obj, args[i], BeanFactory.componentObjectDict[systemType][args[i]])

    @staticmethod
    def clearNoNeedVariable(systemType):
        """
        清理不需要的变量

        Args:
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
        """
        for clsName in BeanFactory.componentKeyTempList:
            BeanFactory.componentClsDict[systemType].pop(clsName, None)
            BeanFactory.componentObjectWaitInjectDict[systemType].pop(clsName, None)
        BeanFactory.componentKeyTempList = []