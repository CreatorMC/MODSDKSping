# -*- coding: utf-8 -*-
import re
import sys
import os
import shutil
import constants

# 获取当前包的根目录
packagePath = os.path.dirname(__file__)

def main():
    """
    控制台命令入口
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            print("Start initializing your Mod...")
            initMOD()
            print("Created successfully!")
        elif sys.argv[1] == 'import':
            print("Starting to create the __init__.py file.")
            initPy(sys.argv)
        else:
            print("Incorrect sub command.")
    else:
        print("Only modsdkspring was entered, please enter the sub command.")

def initMOD():
    """
    初始化 MOD 相关文件和文件夹
    """
    # 提醒用户，输入要创建的 mod 文件夹的名称
    modDirName = raw_input("Please enter the name of the Mod folder:\n").strip()
    # 输入 Mod 名称（命名空间）
    modName = raw_input("Please enter the Mod name, which will serve as the namespace registered to the engine:\n").strip()
    # 输入客户端系统名称
    clientSystemName = raw_input("Please enter the client system name, which will serve as the class name for the client system:\n").strip()
    # 输入服务端系统名称
    serverSystemName = raw_input("Please enter the server system name, which will serve as the class name for the server system:\n").strip()
    # 得到 Mod 的绝对路径
    modFullPath = os.path.join(os.getcwd(), modDirName)

    # 复制模板文件
    shutil.copytree(os.path.join(packagePath, constants.TEMPLATE_DIR_NAME), modFullPath)

    # 复制 MODSDKSpring 框架
    shutil.copytree(os.path.join(packagePath, constants.PLUGINS_DIR_NAME), modFullPath + os.sep + constants.PLUGINS_DIR_NAME)

    # 修改 ClientSystem.txt 文件名
    clientSystemFilePath = os.path.join(modFullPath, constants.CLIENT_SYSTEM_FILE_PATH)
    os.rename(clientSystemFilePath,  os.path.join(modFullPath, clientSystemName + '.txt'))
    
    # 修改 ServerSystem.txt 文件名
    serverSystemFilePath = os.path.join(modFullPath, constants.SERVER_SYSTEM_FILE_PATH)
    os.rename(serverSystemFilePath,  os.path.join(modFullPath, serverSystemName + '.txt'))
    
    # 替换模板文件中定义的占位符，并把所有 .txt 文件改为 .py
    for root, dirs, files in os.walk(modFullPath):
        for file in files:
            if not file.endswith('.txt'):
                continue
            filePath = os.path.join(root, file)
            
            # 如果此文件不在 plugins 文件夹中，则进行文本替换
            if constants.PLUGINS_DIR_NAME not in root:
                with open(filePath, 'r') as f:
                    fstr = f.read()
                fstr = fstr.replace(constants.MOD_NAME, modName)
                fstr = fstr.replace(constants.MOD_DIR_NAME, modDirName)
                fstr = fstr.replace(constants.CLIENT_SYSTEM_NAME, clientSystemName)
                fstr = fstr.replace(constants.SERVER_SYSTEM_NAME, serverSystemName)
                with open(filePath, 'w') as f:
                    f.write(fstr)
            
            # 修改文件扩展名
            os.rename(filePath, os.path.join(root, file[:file.rfind('.')] + '.py'))

def initPy(args):
    """
    自动生成 __init__.py 文件，其中会自动 import 当前文件夹及其子文件夹中所有的类

    Args:
        args (list): 命令参数列表
    """
    # 要生成 __init__.py 文件的位置
    path = ""
    if len(args) == 2:
        # 取当前路径
        path = os.getcwd()
    elif len(args) == 4 and args[2] == '--path':
        # 取 --path 后的路径
        path = args[3]
    else:
        print("Usage: modsdkspring import --path \"path_to_directory\"")
        return
    
    pattern = r'class\s+([a-zA-Z][a-zA-Z0-9_]*)(\(.*\))?\s*:'
    pathRootDir = path[path.rfind(os.sep) + 1:]
    content = ""
    for root, dirs, files in os.walk(path):
        for file in files:
            # 过滤掉不是以 .py 结尾的文件，或者以 '_' 开头的文件
            if not file.endswith('.py') or file.startswith('_'):
                continue
            filePath = os.path.join(root, file)
            with open(filePath, 'r') as f:
                fstr = f.read()
            matches = re.findall(pattern, fstr)
            # 去掉扩展名 '.py'
            tempModulePath = filePath[:-3]
            # 去掉盘符
            tempModulePath = tempModulePath.split(":" + os.sep, 1)[1] if (":" + os.sep) in tempModulePath else tempModulePath
            # 去掉多余路径
            tempModulePath = tempModulePath[tempModulePath.find(pathRootDir + os.sep) + len(pathRootDir + os.sep):]
            # 将路径分隔符替换为 '.'
            tempModulePath = tempModulePath.replace(os.sep, '.')
            for className, superClassName in matches:
                content += ('from {} import {}\n'.format(tempModulePath, className))
    
    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write(content)
    print("Successfully created the __init__.py file!")