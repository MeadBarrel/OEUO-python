import os
from .oeuo import UO, AS

app_folder = os.path.split(os.path.split(__file__)[0])[0]

#Ok that dirty trick is to help IDE's know what's serpent
if False:
    from .serpent.manager import Manager_
    manager = Manager_(None, None)


