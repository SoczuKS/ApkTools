import os
import xml.etree.ElementTree
import sys
from enum import Enum
from pathlib import Path
from urllib import request
import shutil


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
        self.forceApktools = False
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
            if sys.argv[i] == '--force-apktool' or sys.argv[i] == '-f':
                app_config.forceApktools = True
                continue
            elif sys.argv[i] == '-s' or sys.argv[i] == '--skip-sources':
                app_config.skipSources = True
                continue

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
    # Things to do:
    # 1. Take the lib folder of the config.arch APK and add it to the decompiled base APK.
    # 2. Open AndroidManifest.xml in the decompiled base APK and remove this setup: android:isSplitRequired="true".


def do_stuff_split_in_4(app_config):
    print('Processing files...')
    output_dir_path = Path(app_config.outputDir)

    # Step 1
    # Put all files of the split APKs to the base APK but do not override files
    print("Copying...")
    dst = app_config.outputDir + "/base"
    dst_path = Path(dst)
    for d in output_dir_path.iterdir():
        if d.is_dir():
            if not d.name == 'base':
                src_path = Path(d)
                copydir(src_path, dst_path)

    # Step 2
    # Open the AndroidManifest.xml in the decompiled base APK and remove this setup: android:isSplitRequired="true"
    et = xml.etree.ElementTree.parse(dst + "/AndroidManifest.xml")
    root = et.getroot()
    application_tag = root.find('application')

    for attr in application_tag.attrib:
        if not attr.find('isSplitRequired') == -1:
            application_tag.attrib.pop(attr)
            break

    et.write(dst + "/AndroidManifest.xml", xml_declaration=True, encoding='utf-8')

    # Step 3
    # Open the apktool.yml and add in the doNotCompress tag of the base.apk everything you have in the other split APKs

    # Step 4
    # Check the .xml files in the res/value folder in all the split APKs and add whats missing inside that files from the other split APKs to the base APK .xml files


def copydir(src_path, dst_path):
    # Recursive copy of dir tree without overwriting
    for item in src_path.iterdir():
        dst = Path(dst_path.__str__() + "/" + item.name)
        if item.is_dir():
            if dst.exists():
                copydir(item, dst)
            else:
                shutil.copytree(item, dst)
        elif item.is_file():
            if not dst.exists():
                shutil.copy2(item, dst)


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
