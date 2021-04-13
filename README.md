# ApkTools

## Prerquisities
1. You need to install PyYAML
```
pip install pyyaml
```

## Usage
```
python apktools.py [-<option> value] /path/to/directory/with/apks
```

### Command line arguments
| Argument | Possible values | Description |
|----------|-----------------|-------------|
| &#x2011;apktool&#160;value | Every valid path | Path to apktool jar file which will be used (if file doesn't exist apktool will be downloaded there) |
| &#x2011;output&#160;value | Every valid path | Directory in which all files will be extracted |
| &#x2011;s <br> &#x2011;&#x2011;skip&#x2011;sources | | Add &#x2011;&#x2011;skip&#x2011;sources to apktool |
| &#x2011;f <br> &#x2011;&#x2011;force | | Add &#x2011;&#x2011;force to apktool |
