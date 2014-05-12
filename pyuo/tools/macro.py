from pyuo.oeuo import UO

def use_item(id_):
    UO.LObjectID = id_
    UO.Macro(17, 0)

