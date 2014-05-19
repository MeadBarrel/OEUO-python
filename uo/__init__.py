import os
from .oeuo import UO, AS

app_folder = os.path.split(os.path.split(__file__)[0])[0]

#Ok that dirty trick is to help IDE's know what's manager
if False:
    from .manager.manager import _Manager
    manager = _Manager(None, None)


