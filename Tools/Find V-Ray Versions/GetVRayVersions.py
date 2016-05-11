import winreg
import pprint

SOFTWARE = 'V-Ray'

try:
    i = 0
    explorer = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
    )

    while True:
        key = winreg.EnumKey(explorer, i)
        if SOFTWARE in key:
            item = winreg.OpenKey(explorer, key)
            version, type = winreg.QueryValueEx(item, "DisplayVersion")
            winreg.CloseKey(item)
            
            print('{0}:\n\t{1}'.format(key, version))
        
        i += 1

except WindowsError as e:
    print(e)

winreg.CloseKey(explorer)
