from uo.oeuo import UO, AS

def use_item(id_):
    UO.LObjectID = id_
    AS.Macro(17, 0)

