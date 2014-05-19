
__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"


from .stack import Stack
import traceback

RVARS = ['AR',
         'BackpackID',
         'CharDir',
         'CharID',
         'CharName',
         'CharPosX',
         'CharPosY',
         'CharPosZ',
         'CharStatus',
         'CharType',
         'CliCnt',
         'CliLang',
         'CliLeft',
         'CliLogged',
         'CliNr',
         'CliTop',
         'CliVer',
         'CliXRes',
         'CliYRes',
         'ContID',
         'ContKind',
         'ContName',
         'ContPosX',
         'ContPosY',
         'ContSizeX',
         'ContSizeY',
         'ContType',
         'CR',
         'CursKind',
         'CursorX',
         'CursorY',
         'Dex',
         'EnemyHits',
         'EnemyID',
         'ER',
         'Followers',
         'FR',
         'Gold',
         'Hits',
         'Int',
         'ItemCnt',
         'LHandID',
         'LLiftedID',
         'LLiftedKind',
         'LLiftedType',
         'LObjectID',
         'LObjectType',
         'LShard',
         'LSkill',
         'LSpell',
         'LTargetID',
         'LTargetKind',
         'LTargetTile',
         'LTargetX',
         'LTargetY',
         'LTargetZ',
         'Luck',
         'Mana',
         'MaxDmg',
         'MaxFol',
         'MaxHits',
         'MaxMana',
         'MaxStam',
         'MaxStats',
         'MaxWeight',
         'MinDmg',
         'NextCPosX',
         'NextCPosY',
         'PR',
         'RHandID',
         'Sex',
         'Shard',
         'Stamina',
         'Str',
         'SysMsg',
         'TargCurs',
         'TP',
         'Weight']


class _UO(object):
    """Object representing the game environment. All UO.dll functions and vars are exported as members of this object.
    """
    rvars = RVARS
    def __init__(self):
        self.stack = Stack()

    def set_client(self, client):
        self.CliNr = client

    def CliDrag(self, nid):
        """Drags the object specified by id nid.

        This drag is performed by the client and affects the UO.LLifted* variables.
        Corresponding drop should be completed with a UO.Click() command.
        """
        return self.Call('CliDrag', nid)

    def Click(self, x, y, bLeft, bDown, bUp, bMC):
        """Mimics a click of the mouse in a specific position on the screen.

        So if you want to click something, the mouse button should go down and up. If you want to drag something,
        the mouse button should only go down but not up. Dropping means only up.
        """
        return self.Call("Click", x, y, bLeft, bDown, bUp, bMC)

    def ContTop(self, index):
        """Moves the gump enumerated as index to the top of the gump heap, i.e. make it the top level gump/container
        (index = 0)."""
        return self.Call("ContTop", index)

    def Drag(self, nid, namnt=None):
        """Drag the object specified by id nid via packets.

        This will not affect the UO.LLifted* variables. Alternatively, specify the amount namnt to drag if the object is
        a stack. namnt defaults to 1. A drag initiated in this manner should be terminated with a drop via one of the
        following commands:

        * UO.DropC,
        * UO.DropG,
        * or UO.DropPD.
        """
        if namnt is None:
            return self.Call("Drag", nid)
        else:
            return self.Call("Drag", nid, namnt)

    def DropC(self, contid, pos=None):
        """The UO.DropC command drops obects you drag using the UO.Drag command to any container you want.
        If you specify nx/ny then the item will be dropped in the container at the coordinates relative to the
        container's location, otherwise it will be dropped on the container.

        If you want to combine the stack being dragged with another stack of the same item type, just pass the ID of the
        destination stack as contid.

        Do not use this command to terminate a drag initiated by the UO.CliDrag function
        """
        if pos is None:
            return self.Call("DropC", contid)
        else:
            return self.Call("DropC", contid, pos[0], pos[1])

    def DropG(self, x, y, z=None):
        """The UO.DropG command drops objects you drag using the UO.Drag command to the given ground (world) coordinate.

        If no z coordinate is specified, the default will be UO.CharPosZ.
        Do not use this command to terminate a drag initiated via the UO.CliDrag function.
        """
        if z is None:
            return self.Call("DropG", x, y)
        else:
            return self.Call("DropG", x, y, z)

    def DropPD(self):
        """Drops an item you drag using UO.Drag onto the paperdoll.

        Do not use this to terminate a drag initiated via the UO.CliDrag function.
        """
        return self.Call("DropPD")

    def Equip(self, *nids):
        """Instantly equips all of the given object id's. Only available on EA/Mythic shards. Exclusive to OpenEUO.

        Note that this does not work with strings.
        If you want to send multiple IDs to this you may call with a table instead of a string: ...
        """
        return self.Call("Equip", *nids)

    def ExMsg(self, nid, string, nfont=None, ncolor=None):
        """Shows the string str over the object given by the object id nid.

        The optional font and color arguments change the appearance of the message that is displayed.
        """
        if nfont is not None:
            if ncolor is not None:
                return self.Call("ExMsg", nid, nfont, ncolor, string)
            else:
                return self.Call("ExMsg", nid, nfont, string)
        elif ncolor is not None:
            return self.Call("ExMsg", nid, ncolor, string)
        else:
            return self.Call("ExMsg", nid, string)

    def GetCont(self, nIndex):
        """Returns values associated with the gump at location nIndex on the 'gump heap'.

        nIndex 0 is the topmost gump.
        Returned values are the name,x screen coordinate, y screen coordinate,
        width, height, gumpkind, charid, chartype and char hp value.

        If nIndex >= number of gumps, UO.GetCont returns nil.
        """
        return self.Call("GetCont", nIndex)

    def GetItem(self, nIndex):
        """Returns values associated with a item denoted by nIndex after a UO.ScanItems command.

        Returned values are the id,type,kind,containing item id (if any),x,y,z,
        stack amount,reputation, and color. x,y, and z may be gump-relative or global coordinates depending upon
        whether the item is in a container or not.
        """
        return self.Call("GetItem", nIndex)

    def GetJournal(self, index):
        """Used to read the content fetched by UO.ScanJournal.

        nIndex is what line of the journal you wish to get,
        0 is the most recent line with 1 being the next most recent and so on. sLine will hold the line of text.
        nCol will be the color of the text.
        """
        return self.Call("GetJournal", index)

    def GetPix(self, x, y):
        """Saves the color value of the pixel given by the screen coordinate parameters"""
        return self.Call("GetPix", x, y)

    def GetShop(self):
        """bRes,nPos,nCnt,nID,nType,nMax,nPrice,sName = UO.GetShop()

        This command retrieves information about the currently shown top entry on an open shopping gump.

        Note: Every time you scroll to a new entry, you have to call UO.GetShop.
        """
        return self.Call("GetShop")

    def GetSkill(self, skill):
        """Returns the folowing variables on the choosen skill.

        Synopsis: nNorm, nReal, nCap, nLock = UO.GetSkill(sSkill)
        """
        return self.Call("GetSkill", skill)

    def HideItem(self, nid):
        """This command removes a specific item id's graphic from the client.

        It can be used to unclutter the visual appearance of the client however,
        it does nothing on the server. Only non-static items that are on the ground can be hidden.
        Items will reappear if the client is resynchronized with the server
        """
        return self.Call("HideItem", nid)

    def Key(self, key, bcntrl=None, balt=None, bshift=None):
        """Sends a keystroke to the client. Key can be modified by CTRL, ALT, and or SHIFT by providing the optional
        boolean parameters.

        The key-specifier string key can be A-Z, 0-9, F1-F12 and ESC, BACK, TAB, ENTER, PAUSE, CAPSLOCK, SPACE, PGDN,
        PGUP, END, HOME, LEFT, RIGHT, UP, DOWN, PRNSCR, INSERT, DELETE, NUMLOCK or SCROLLLOCK.
        """
        bargs = [k for k in (bcntrl, balt, bshift) if k is not None]
        return self.Call("Key", key, *bargs)

    def Macro(self, param1, param2, string = None):
        """Causes the client to use one of the pre-defined, internal UO client macros."""
        if string is None:
            return self.Call("Macro", param1, param2)
        else:
            return self.Call("Macro", param1, param2, string)

    def Move(self, x, y, tolerance=None, timeout=None):
        """Moves the character to a specified position.

        No pathfinding is done, so you should probably use event PathFind instead.
        If unspecified, tolerance defaults to 2. If unspecified, timeout defaults to 52s.
        Note: Please note that if you are using UOAssist, you need to make sure these keys
        are not assigned to anything:
        Cursor Up, Cursor Down, Cursor Left, Cursor Right, Home, End, Page Up and Page Down.

        OpenEUO uses these keys to move your character.
        """
        return self.Call("Move", x, y, tolerance, timeout)

    def Msg(self, string):
        """This command sends a series of key-strokes to the client as specified by string str.
        IN EUO a '$' sign denoted a carriage return. In OpenEUO you must pass the carridge return character
        (ascii code 13).
        """
        return self.Call("Msg", string)

    def PathFind(self, x, y, z):
        """Moves you to the game world position given by the coordinates.
        In Easyuo, the Z coordinate could be omitted, and was assumed to be -1.
        Currently OpenEUO requires all three coordinates.
        """
        return self.Call("PathFind", x, y, z)

    def Popup(self, nid, x=0, y=0):
        """UO.Popup command opens the context menu of an item/npc with id nid at location x/y."""
        return self.Call("Popup", nid, x, y)

    def Property(self, id_):
        """This command returns name and info strings for the given item id.

        Newlines in the returned info are replaced with '$' symbols."""
        return self.Call("Property", id_)

    def RenamePet(self, id_, name):
        """Changes the name of the pet id nid to the name specified by the string name."""
        return self.Call("RenamePet", id_, name)

    def ScanItems(self, visible_only=False):
        """Scans all objects in client memory and returns the number of items found.

        Invisible objects may be excluded using the sole parameter.
        Once objects are scanned, their parameters are discovered by iterating over the UO.GetItem command,
        increasing the index from 0 to nCnt - 1.

        .. method:: ScanItems()
                    ScanItems(visible_only)
        """
        return self.Call("ScanItems", visible_only)

    def ScanJournal(self, old_ref):
        """Used to scan content of journal for use by UO.GetJournal.

         nNewRef,nCnt = UO.ScanJournal(nOldRef)

        nNewRef gives a unique numeric code every time the journal changes.
        nCnt Gives the number of lines in the journal.
        OldRef need to be set to a number.
        """
        return self.Call("ScanJournal", old_ref)

    def SetShop(self, id_, num):
        """Changes the amount to purchase in a shopping gump given by an item's id.

        Before calling UO.SetShop you have to add at least one item to the buy list.
        This means you first have to double click the item so it gets added to the buy list with amount equal to 1,
        then you may call UO.SetShop to change that amount.
        Despite the fact that using UO.SetShop will not update the graphics in the buy gump,
        the amount to sell is set in the client's memory.
        """
        return self.Call("SetShop", id_, num)

    def SkillLock(self, skill, lock):
        """Changes the skill lock on the skill specified by the string sSkill to either: up, down or locked (0,1,2)."""
        return self.Call("SkillLock", skill, lock)

    def StatBar(self, id_):
        """Pulls up the status bar for the given object id. Exclusive to OpenEUO."""
        return self.Call("StatBar", id_)

    def StatLock(self, stat, lock):
        """Changes the stat lock on the stat specified by string sStat ("int","dex", or "str") to either:
        up, down or locked (0,1,2)."""
        return self.Call("StatLock", stat, lock)

    def SysMessage(self, msg, col=None):
        """Outputs a message as a system message inside the client.
        The string sMsg specifies the message, the optional numeric parameter specifies the system message color.
        """
        return self.Call("SysMessage", msg, col)

    def TileCnt(self, x, y, facet=None):
        """Retrieves the number of tiles for a specific game world position.

        The default value for facet is the current facet. Otherwise follows the values for UO.CursKind.
        """
        return self.Call("TileCnt", x, y, facet)

    def TileGet(self, x, y, index, facet=None):
        """Retrieves the tile type, z value, name, and flags for the indexed tile at the given location.

        Use UO.TileCnt to determine how many tiles are indexed at a particular location.
        The default value for facet is the current facet. Otherwise follows the values for UO.CursKind. UO.
        TileInit must be called prior to using UO.TileGet
        """
        return self.Call("TileGet", x, y, index, facet)

    def TileInit(self, no_overrides):
        """Initializes the tile information for retrieval in OpenEUO.

        Setting bnooverrides to true forces OpenEUO to disregard the statics override file (VerData.mul),
        which could be useful for freeshards that do not use the overrides.
        If you don't know what VerData.mul is, you probably don't need to use the noOverrides option.
        This function only needs to be called once in a script, and only if tile data is to be accessible.
        """
        return self.Call("TileInit", no_overrides)

    def __getattr__(self, item):
        if item in self.rvars:
            return self.Get(item)
        return lambda *args: self.stack.execute(item, *args)

    def __setattr__(self, key, value):
#        if key == 'rvars':
#            self.__dict__['rvars'] = value
        if key in self.rvars:
            self.Set(key, value)
        else:
            self.__dict__[key] = value


