import xml.dom.minidom
import sys
from enum import Enum


class AppConfig:
    def __init__(self):
        self.apkDir = './'
        self.apktool = self.apkDir + '/apktool.jar'
        self.outputDir = self.apkDir + '/apk/'


def analyze_parameters():
    if len(sys.argv) == 1:
        print("Too few arguments")
        exit()

    class CurrentArg(Enum):
        UNKNOWN = -1
        APK_DIR = 0
        APKTOOL_PATH = 1
        OUTPUT_DIR = 2

    current = CurrentArg.APK_DIR
    app_config = AppConfig()
    output_dir_set = False
    apktool_path_set = False
    apk_dir_set = False

    for i in range(1, len(sys.argv)):
        if sys.argv[i][0] == '-':
            current = {
                '-output': CurrentArg.OUTPUT_DIR,
                '-apktool': CurrentArg.APKTOOL_PATH
            }.get(sys.argv[i], CurrentArg.UNKNOWN)
        else:
            if current == CurrentArg.APK_DIR:
                app_config.apkDir = sys.argv[i]
                apk_dir_set = True
            elif current == CurrentArg.APKTOOL_PATH:
                app_config.apktool = sys.argv[i]
                apktool_path_set = True
            elif current == CurrentArg.OUTPUT_DIR:
                app_config.outputDir = sys.argv[i]
                output_dir_set = True

            current = CurrentArg.APK_DIR

    if not apk_dir_set:
        print("No apk directory provided")
        exit()
    if not output_dir_set:
        app_config.outputDir = app_config.apkDir + '/apk/'
    if not apktool_path_set:
        app_config.apktool = app_config.apkDir + '/apktool.jar'

    return app_config


def main():
    app_config = analyze_parameters()


main()
