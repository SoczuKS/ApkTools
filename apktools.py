import os
import xml.dom.minidom
import sys
from enum import Enum
from pathlib import Path
from urllib import request


class AppConfig:
    class AppType(Enum):
        UNKNOWN = 0
        SINGLE = 1
        SPLIT_IN_2 = 2
        SPLIT_IN_4 = 4

    def __init__(self):
        self.apkDir = './'
        self.apktool = self.apkDir + '/apktool.jar'
        self.outputDir = self.apkDir + '/apk/'
        self.skipSources = True
        self.appType = AppConfig.AppType.UNKNOWN


def parameters_validation(app_config):
    apk_dir_path = Path(app_config.apkDir)
    apktool_path = Path(app_config.apktool)
    output_path = Path(app_config.outputDir)

    if not apktool_path.is_file():
        print('No apktool in given location. Downloading...')
        request.urlretrieve('https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.5.0.jar', apktool_path)

    if not apk_dir_path.is_dir():
        print("Given apks directory doesn't exists")
        exit(3)

    if not output_path.exists():
        output_path.mkdir(parents=True)
    elif not output_path.is_dir():
        print("Given output location isn't a directory")
        exit(4)


def analyze_parameters():
    if len(sys.argv) == 1:
        print("Too few arguments")
        exit(1)

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
        exit(2)
    if not output_dir_set:
        app_config.outputDir = app_config.apkDir + '/apk/'
    if not apktool_path_set:
        app_config.apktool = app_config.apkDir + '/apktool.jar'

    return app_config


def decompile_apks(app_config):
    apk_dir_path = Path(app_config.apkDir)

    for file in apk_dir_path.iterdir():
        if file.suffix == '.apk':
            file_output_dir_name = app_config.outputDir + file.stem
            file_full_name = app_config.apkDir + file.name

            cmd = 'java -jar ' + app_config.apktool + ' -q'
            cmd += ' d ' + file_full_name
            if app_config.skipSources:
                cmd += ' -s '
            cmd += ' -o ' + file_output_dir_name

            os.system(cmd)


def detect_app_type(app_config):
    apk_files_counter = 0
    apk_dir_path = Path(app_config.apkDir)

    for file in apk_dir_path.iterdir():
        if file.suffix == '.apk':
            apk_files_counter += 1

    if apk_files_counter == 1:
        app_config.appType = AppConfig.AppType.SINGLE
    elif apk_files_counter == 2:
        app_config.appType = AppConfig.AppType.SPLIT_IN_2
    elif apk_files_counter == 4:
        app_config.appType = AppConfig.AppType.SPLIT_IN_4


def do_stuff_single(app_config):
    print('Processing files...')


def do_stuff_split_in_2(app_config):
    print('Processing files...')


def do_stuff_split_in_4(app_config):
    print('Processing files...')


def do_apk_stuff(app_config):
    print('Detecting app type...')
    detect_app_type(app_config)

    print('Decompiling apk...')
    decompile_apks(app_config)

    if app_config.appType == AppConfig.AppType.SINGLE:
        do_stuff_single(app_config)

    elif app_config.appType == AppConfig.AppType.SPLIT_IN_2:
        do_stuff_split_in_2(app_config)

    elif app_config.appType == AppConfig.AppType.SPLIT_IN_4:
        do_stuff_split_in_4(app_config)


def main():
    app_config = analyze_parameters()
    parameters_validation(app_config)
    do_apk_stuff(app_config)


main()
