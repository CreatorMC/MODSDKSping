# -*- coding: utf-8 -*-
import sys
import os
import shutil
import constants

def main():
    """
    控制台命令入口
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            print("Start initializing your Mod...")
            initMOD()
            print("Created successfully!")
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
    modFullPath = os.path.join(os.getcwd(), modDirName)
    # 创建 mod 相关文件和文件夹
    shutil.copytree('template', modFullPath)
    modName = raw_input("Please enter the Mod name, which will serve as the namespace registered to the engine:\n").strip()
    clientSystemName = raw_input("Please enter the client system name, which will serve as the class name for the client system:\n").strip()
    serverSystemName = raw_input("Please enter the server system name, which will serve as the class name for the server system:\n").strip()
    
    # 修改 modConfig.py 文件
    configFilePath = os.path.join(modFullPath, constants.CONFIG_FILE_PATH)
    with open(configFilePath, 'r') as f:
        fstr = f.read()
    fstr = fstr.replace(constants.MOD_NAME, modName)
    fstr = fstr.replace(constants.MOD_DIR_NAME, modDirName)
    fstr = fstr.replace(constants.CLIENT_SYSTEM_NAME, clientSystemName)
    fstr = fstr.replace(constants.SERVER_SYSTEM_NAME, serverSystemName)
    with open(configFilePath, 'w') as f:
        f.write(fstr)
    
    # 修改 ClientSystem.py 文件
    clientSystemFilePath = os.path.join(modFullPath, constants.CLIENT_SYSTEM_FILE_PATH)
    with open(clientSystemFilePath, 'r') as f:
        fstr = f.read()
    fstr = fstr.replace(constants.CLIENT_SYSTEM_NAME, clientSystemName)
    with open(clientSystemFilePath, 'w') as f:
        f.write(fstr)
    os.rename(clientSystemFilePath,  os.path.join(modFullPath, clientSystemName + '.py'))
    
    # 修改 ServerSystem.py 文件
    serverSystemFilePath = os.path.join(modFullPath, constants.SERVER_SYSTEM_FILE_PATH)
    with open(serverSystemFilePath, 'r') as f:
        fstr = f.read()
    fstr = fstr.replace(constants.SERVER_SYSTEM_NAME, serverSystemName)
    with open(serverSystemFilePath, 'w') as f:
        f.write(fstr)
    os.rename(serverSystemFilePath,  os.path.join(modFullPath, serverSystemName + '.py'))
    
    # 修改 modMain.py 文件
    modMainFilePath = os.path.join(modFullPath, constants.MOD_MAIN_FILE_PATH)
    with open(modMainFilePath, 'r') as f:
        fstr = f.read()
    fstr = fstr.replace(constants.MOD_NAME, modName)
    with open(modMainFilePath, 'w') as f:
        f.write(fstr)
    
    # 创建其他文件夹
    componentClientFullPath = os.path.join(modFullPath, 'components' + os.sep + 'client')
    componentServerFullPath = os.path.join(modFullPath, 'components' + os.sep + 'server')
    os.makedirs(componentClientFullPath)
    os.makedirs(componentServerFullPath)
    initFilePaths = [modFullPath, componentClientFullPath, componentServerFullPath]
    for path in initFilePaths:
        open(os.path.join(path, '__init__.py'), 'w').close()
    shutil.copytree('plugins', modFullPath + os.sep + 'plugins')