import _winreg
import pprint

SOFTWARE = 'V-Ray'

try:
    i = 0
    explorer = _winreg.OpenKey(
        _winreg.HKEY_LOCAL_MACHINE,
        'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
    )

    while True:
        key = _winreg.EnumKey(explorer, i)
        if SOFTWARE in key:
            item = _winreg.OpenKey(explorer, key)
            version, type = _winreg.QueryValueEx(item, "DisplayVersion")
            _winreg.CloseKey(item)
            
            print('{0}:\n\t{1}'.format(key, version))
        
        i += 1

except WindowsError as e:
    print e

_winreg.CloseKey(explorer)