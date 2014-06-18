#JavaMonkey

A python package for chimpchat protocol

##Usage
```
from JavaMonkey import Utils
from JavaMonkey.JavaMonkey import JavaMonkey
JavaMonkey_jarfiles = Utils.list_jarfile()
Utils.startJVM(JavaMonkey_jarfiles)
monkey = JavaMonkey(device_id = <id>)
monkey.device_wake()
print monkey.get_view_id_list()
Utils.shutdownJVM()
```
