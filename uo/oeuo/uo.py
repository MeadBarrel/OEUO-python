
__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"


from .stack import Stack
import os
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


class UOVarProperty(object):
    """Get/set uo.dll variable"""
    def __init__(self, method):
        self.method = method
        self.__doc__ = method.__doc__

    def __set__(self, instance, value):
        instance.Set(self.method.__name__, value)

    def __get__(self, instance, owner):
        return instance.Get(self.method.__name__)


if 'sphinx' in os.environ:
    class UOVarProperty(object):
        """Get/set uo.dll variable"""
        def __init__(self, method):
            self.method = method
            self.__doc__ = method.__doc__

        def __set__(self, instance, value):
            instance.Set(self.method.__name__, value)


    #def UOVarProperty(method):
    #    return method


class llUOVar(object):
    @UOVarProperty
    def AR(self):
        """System variable determines the Armor Rating (Physical Resistance with AoS system) of the character. This variable
        will not work unless the character status bar is open.

        .. seealso::
           :py:attr:`CR` :py:attr:`ER` :py:attr:`FR` :py:attr:`PR`
           """

    @UOVarProperty
    def BackpackID(self):
        """Contains the id of the current character's main backpack.

        .. seealso::
           :py:attr:`CharID`"""

    @UOVarProperty
    def CharDir(self):
        """Determines the direction the character is facing.

        Directions:
           * 0 -    North
           * 1 -    North East
           * 2 -    East
           * 3 -    South East
           * 4 -    South
           * 5 -    South West
           * 6 -    West
           * 7 -    North West

        .. seealso::
           :py:attr:`CharPosX`
           :py:attr:`CharPosY`
           :py:attr:`CharPosZ`
           :py:attr:`CursKind`
           :py:attr:`Shard`
        """

    @UOVarProperty
    def CharID(self):
        """Determines the id of your character. This is a unique identifier, so it can be used to identify different
        characters and make specific actions depending on what character it is.

        This variable can also be used as a container.

        .. seealso::
           :py:attr:`BackpackID` :py:attr:`CharName` :py:attr:`CharStatus` :py:attr:`Sex` :py:attr:`CharType`
        """

    @UOVarProperty
    def CharName(self):
        """Contains the name of the logged in character. Status bar must be open to function.

        .. seealso::
           :py:attr:`CharID`, :py:attr:`CharStatus`, :py:attr:`Sex`, :py:attr:`CharType`
        """

    @UOVarProperty
    def CharPosX(self):
        """This is be used to get the X Position of your character in game world coordinates."""

    @UOVarProperty
    def CharPosY(self):
        """This is be used to get the Y Position of your character in game world coordinates."""

    @UOVarProperty
    def CharPosZ(self):
        """This is be used to get the Z Position of your character in game world coordinates."""

    @UOVarProperty
    def CharStatus(self):
        """Determines different states that the character can be in.

        * C: poisioned
        * H: hidden
        * B: is female
        * C: is in war mode
        * D: affected with lethal strike
        * A: frozen
        """

    @UOVarProperty
    def CliCnt(self):
        """Contains the number of clients currently running.

        .. seealso::
           :py:attr:`CliNr`
        """

    @UOVarProperty
    def CliLang(self):
        """Returns the language of the current client.

        .. seealso::
           :py:attr:`CliVer`
        """

    @UOVarProperty
    def CliLeft(self):
        """Set or return the X coordinate of the left edge of the game-play window.

        .. seealso::
           :py:attr:`CliTop`
           :py:attr:`CliXRes`
           :py:attr:`CliYRes`
        """

    @UOVarProperty
    def CliLogged(self):
        """Returns True if a character is logged into the game, or False otherwise.

        .. seealso::
           :py:attr:`Shard`
        """

    @UOVarProperty
    def CliNr(self):
        """Set or return the game client to which the script is currently attached.

        .. seealso::
           :py:attr:`CliCnt`
        """


    @UOVarProperty
    def CliTitle(self):
        """Set or return the title of the UO window to which the script is currently attached.

        *Only available in OpenEUO build 0.91.0011 or higher (and UO client 7.0.10.3 or higher).*
        """

    @UOVarProperty
    def CliTop(self):
        """Set or return the Y value of the top edge of the game-play window.

        .. seealso::
           :py:attr:`CliLeft`
           :py:attr:`CliXRes`
           :py:attr:`CliYRes`
        """

    @UOVarProperty
    def CliVer(self):
        """Returns the version of the current client.

        .. seealso::
           :py:attr:`CliLang`
        """

    @UOVarProperty
    def CliXRes(self):
        """Set or return the width of the game-play window.

        .. seealso::
           :py:attr:`CliTop`
           :py:attr:`CliLeft`
           :py:attr:`CliYRes`
        """

    @UOVarProperty
    def CliYRes(self):
        """Set or return the height of the game-play window.

        .. seealso::
           :py:attr:`CliTop`
           :py:attr:`CliLeft`
           :py:attr:`CliXRes`
        """

    @UOVarProperty
    def ContID(self):
        """Returns the id of the "top most" gump/container. This means that the last gump that was opened or moved in
        any way.

        .. seealso::
           :py:attr:`ContKind`
           :py:attr:`ContName`
           :py:attr:`ContType`
           :py:attr:`ContTop`
           :py:attr:`GetCont`
        """

    @UOVarProperty
    def ContKind(self):
        """Returns the kind of the "top most" gump. This means that the last gump that was opened or moved in any way.
        Most menus have a kind attached to them. The can be utilized to find out if a crafting menu is open, if
        something is being dragged, if a runebook is open and many other things. This value is not static and can change
        every time a new patch is released for the client.

        .. seealso::
           :py:attr:`ContID`
           :py:attr:`ContName`
           :py:attr:`ContType`
        """

    @UOVarProperty
    def ContName(self):
        """Returns the object type of the "top most" gump. This means that the last gump that was opened or moved in any
        way.

        .. seealso::
           :py:attr:`ContID`
           :py:attr:`ContName`
           :py:attr:`ContType`
        """

    @UOVarProperty
    def ContPosX(self):
        """Set or return the screen x-coordinate of the "top most" gump. This means that the last gump that was opened
        or moved in any way.

        .. seealso::
           :py:attr:`ContPosY`
           :py:attr:`ContSizeX`
           :py:attr:`ContSizeY`
           :py:attr:`NextCPosX`
           :py:attr:`NextCPosY`
        """

    @UOVarProperty
    def ContPosY(self):
        """Set or return the screen y-coordinate of the "top most" gump. This means that the last gump that was opened
        or moved in any way.

        .. seealso::
           :py:attr:`ContPosX`
           :py:attr:`ContSizeX`
           :py:attr:`ContSizeY`
           :py:attr:`NextCPosX`
           :py:attr:`NextCPosY`
        """

    @UOVarProperty
    def ContSizeX(self):
        """Returns the width of the "top most" gump. This means that the last gump that was opened or moved in any way.

        .. seealso::
           :py:attr:`ContPosX`
           :py:attr:`ContPosY`
           :py:attr:`ContSizeY`
        """

    @UOVarProperty
    def ContSizeX(self):
        """Returns the height of the "top most" gump. This means that the last gump that was opened or moved in any way.

        .. seealso::
           :py:attr:`ContPosX`
           :py:attr:`ContPosY`
           :py:attr:`ContSizeX`
        """

    @UOVarProperty
    def ContType(self):
        """Returns the object type of the "top most" gump. This means that the last gump that was opened or moved in any
        way.

           :py:attr:`ContID`
           :py:attr:`ContKind`
           :py:attr:`ContName`
        """

    @UOVarProperty
    def CR(self):
        """Returns the Cold Resist of the character. The character status bar must be open to read this variable properly.

        :py:attr:`AR`
        :py:attr:`ER`
        :py:attr:`FR`
        :py:attr:`PR`
        """

    @UOVarProperty
    def CursKind(self):
        """Returns the facet where the character is.

        * 0: Felucca
        * 1: Trammel
        * 2: Ilshenar
        * 3: Malas
        * 4: Tokuno
        * 5: SA

        .. seealso::
           :py:attr:`CharPosX`
           :py:attr:`CharPosY`
           :py:attr:`CharPosZ`
           :py:attr:`Shard`
        """

    @UOVarProperty
    def CursorX(self):
        """Holds the current x-coordinate screen position of the mouse cursor.

        The cursor coordinates (CursorX and CursorY) are given relative to the upper left corner of the clients
        game play window. above and to the left of the game play window, these coordinates will be negative.
        Undefined if the client is minimized.

        .. seealso::
           :py:attr:`uo.serpent.manager.get_mouse` (Todo: implement)
           :py:meth:`llUO.Click`
           :py:attr:`CursorY`
        """

    @UOVarProperty
    def CursorY(self):
        """Holds the current y-coordinate screen position of the mouse cursor.

        The cursor coordinates (CursorX and CursorY) are given relative to the upper left corner of the clients
        game play window. above and to the left of the game play window, these coordinates will be negative.
        Undefined if the client is minimized.

        .. seealso::
           :py:attr:`uo.serpent.manager.get_mouse` (Todo: implement)
           :py:meth:`llUO.Click`
           :py:attr:`CursorX`
        """

    @UOVarProperty
    def Dex(self):
        """Returns the current Dexterity of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`Int`
           :py:attr:`Str`
           :py:attr:`MaxStats`
           :py:attr:`MaxStam`
           :py:attr:`Stamina`
           * :meth:`llUO.StatLock`
        """

    @UOVarProperty
    def EnemyHits(self):
        """Returns the percentage of hit points left on the current enemy as given by :py:attr:`UO.EnemyID.
         It is only possible to see one enemy at a time using this variable. If you have more than one enemy, the
         variable will switch values randomly.

         .. seealso::
           :py:attr:`EnemyID`
        """

    @UOVarProperty
    def EnemyID(self):
        """Returns the ID of a current enemy mobile.

        .. note::
           It is only possible to see one enemy at a time using this variable. If you have more than one enemy, the
           variable will switch ID's randomly. Under current version and earlier (0.9s), if you utilize a pet, UO.EnemyID
           may actually reflect the pet's ID in lieu of that of an enemy so always double check the returned value.

        .. seealso::
           :py:attr:`EnemyHits`
        """

    @UOVarProperty
    def ER(self):
        """ Returns the Energy Resist of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`AR`
           :py:attr:`CR`
           :py:attr:`FR`
           :py:attr:`PR`
        """

    @UOVarProperty
    def Followers(self):
        """Returns the current number of followers for the character. The character status bar must be open to read this
        variable properly.

        .. seealso::
           :py:attr:`MaxFol`
        """

    @UOVarProperty
    def FR(self):
        """Returns the Fire Resist of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`AR`
           :py:attr:`CR`
           :py:attr:`ER`
           :py:attr:`PR`
        """

    @UOVarProperty
    def GetHP(self):
        """Returns the hit points of the targetted id as a percentage.

        .. seealso::
           :py:attr:`EnemyHits`
        """

    @UOVarProperty
    def Gold(self):
        """Returns the total amount of gold carried by the character. The character status bar must be open to read this
        variable properly."""

    @UOVarProperty
    def Hits(self):
        """Returns the current Hit Points of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`MaxHits`
        """

    @UOVarProperty
    def Int(self):
        """Returns the Intelligence of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`Dex`
           :py:attr:`Str`
           :py:attr:`MaxStats`
           :py:attr:`MaxStam`
           :py:attr:`Stamina`
           :py:meth:`llUO.StatLock`
        """

    @UOVarProperty
    def LHandID(self):
        """Return the item held in the character's left hand, or set the item to be held upon employing UO.Macro(24,1).

        .. note::
           This variable is used with an event macro in order to place an item in your character's left hand. It
           must be set to a valid items ID, and the item must be able to be held in the character's left hand in order to
           work.

        .. seealso::
           :py:attr:`RHandID`
           :py:meth:`llUO.Macro`
        """

    @UOVarProperty
    def LLiftedID(self):
        """Returns the id of the object last dragged/lifted (either manually or with the UO.CliDrag event, or via
        UO.Click).

        .. note::
           The UO.Drag function, being packet based, does not affect this variable.*

        .. seealso::
           :py:meth:`llUO.Click`
           :py:meth:`llUO.CliDrag`
           :py:attr:`LLiftedKind`
           :py:attr:`LLiftedType`
        """

    @UOVarProperty
    def LLiftedKind(self):
        """Returns whether or not an object is being dragged/lifted(either manually or with the UO.CliDrag event, or via
        UO.Click). The possible values are: 0 - an object is not on the cursor, and 1 - an object is on the cursor.

        .. note::
           The UO.Drag function, being packet based, does not affect this variable.*

        .. seealso::
           :py:meth:`llUO.Click`
           :py:meth:`llUO.CliDrag`
           :py:attr:`LLiftedType`
           :py:attr:`TargCurs`
        """

    @UOVarProperty
    def LLiftedType(self):
        """Returns the type of the object last dragged/lifted (either manually or with the UO.CliDrag event, or via
        UO.Click).

        .. note::
           The UO.Drag function, being packet based, does not affect this variable.

        .. seealso::
           :py:meth:`llUO.Click`
           :py:meth:`llUO.CliDrag`
           :py:attr:`LLiftedID`
           :py:attr:`LLiftedKind`
        """

    @UOVarProperty
    def LObjectID(self):
        """Returns the ID of the last used object. You can also write to this variable and use it in conjunction with
        UO.Macro(17) (LastObject), which will use the object as if it was double-clicked with the mouse.

        .. note::
           This variable is UO client dependent. Setting UO.LObjectID in one script will affect the variable as it
           is seen by all other scripts bound to that client. It is recommended to sanitize the variable by saving the
           existing value before overwriting it, then restoring the original value when the function is complete so as not
           to interfere with other potentially running scripts.

        .. seealso::
            :py:attr:`LObjectType`
        """

    @UOVarProperty
    def LObjectType(self):
        """Returns the object type of the last used object.

        .. seealso::
            :py:attr:`LObjectID`
        """

    @UOVarProperty
    def LShard(self):
        """Return or set the last shard of your choice.

        .LShard is where the unique shard number for the last shard picked is stored. This is the shard that is shown
        next to the globe on the shard selection page. Setting #LShard before logging in an account will make the client
        show the desired shard as the last shard logged in. Only exception will be when that specific shard isn't
        available.

        .. seealso::
           :py:attr:`CliLogged`
           :py:attr:`Shard`
           * http://www.easyuo.com/openeuo/wiki/index.php/UO.LShard
        """

    @UOVarProperty
    def LSkill(self):
        """Returns the skill last used. You can also write to this variable and use it in conjunction with UO.Macro(14)
        (LastSkill), which will perform the skill as if you clicked the blue diamond in the skill list.

        For the list of skills, see: http://www.easyuo.com/openeuo/wiki/index.php/UO.LSkill

        .. seealso::
           :py:attr:`LSpell`
        """

    @UOVarProperty
    def LSpell(self):
        """Returns the last spell cast. You can also write to this variable and use it in conjunction with UO.Macro(16)
        (LastSpell), which will cast the spell.

        For the list of spells, see: http://www.easyuo.com/openeuo/wiki/index.php/UO.LSpell

        .. seealso::
           :py:attr:`LSkill`
        """

    @UOVarProperty
    def LTargetID(self):
        """Return the id of the last target used. You can also write to this variable and use it in conjunction with
        UO.Macro(22) (LastTarget), which will target the object as if it was clicked with the mouse.

        .. seealso::
           :py:attr:`LTargetKind`
           :py:meth:`llUO.Macro`
        """

    @UOVarProperty
    def LTargetKind(self):
        """Returns the class of object that was last targeted. This variable should also be properly set before using
        UO.Macro(22) (Last Target macro).

        Values:
           * 1 - Object
           * 2 - Ground,Mountains,Caves
           * 3 - Resource: Tree,Water

        .. seealso::
           :py:attr:`LTargetID`
           :py:attr:`LTargetTile`
           :py:attr:`LTargetX`
           :py:attr:`LTargetY`
           :py:attr:`LTargetZ`
           :py:meth:`llUO.Macro`
        """

    @UOVarProperty
    def LTargetTile(self):
        """Returns the tile last targeted. The number in this variable is determined by the graphic of the tile. You can
        also write to this variable and use it in conjunction with UO.Macro(22) (LastTarget), which will target this
        tile as if it was clicked with the mouse.

        .. note::
           UO.LTargetKind must be set to 3 for UO.Macro(22) to utilize UO.LTargetTile.*

        .. seealso::
           :py:attr:`LTargetX`
           :py:attr:`LTargetY`
           :py:attr:`LTargetZ`
        """

    @UOVarProperty
    def LTargetX(self):
        """Returns the world x-coordinate of the last target used. You can also write to this variable and use it in
        conjunction with UO.Macro(22) (LastTarget), which will target this position as if it was clicked with the mouse.

        .. note::
           :py:attr:`LTargetKind` must be set to 2 or 3 for UO.Macro(22) to utilize UO.LTargetX.

        .. seealso::
           :py:attr:`LTargetY`
           :py:attr:`LTargetZ`
        """

    @UOVarProperty
    def LTargetY(self):
        """Returns the world y-coordinate of the last target used. You can also write to this variable and use it in
        conjunction with UO.Macro(22) (LastTarget), which will target this position as if it was clicked with the mouse.

        .. note::
           :py:attr:`LTargetKind` must be set to 2 or 3 for UO.Macro(22) to utilize LTargetY.

        .. seealso::
           :py:attr:`LTargetX`
           :py:attr:`LTargetZ`
        """

    @UOVarProperty
    def LTargetZ(self):
        """Returns the world z-coordinate of the last target used. You can also write to this variable and use it in
        conjunction with UO.Macro(22) (LastTarget), which will target this position as if it was clicked with the mouse.

        .. note::
           UO.LTargetKind must be set to 2 or 3 for UO.Macro(22) to utilize UO.LTargetZ.

        .. seealso::
           :py:attr:`LTargetX`
           :py:attr:`LTargetY`
        """

    @UOVarProperty
    def Luck(self):
        """Returns the current Luck of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`TP`
        """

    @UOVarProperty
    def Mana(self):
        """Returns the current Mana of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`MaxMana`
        """

    @UOVarProperty
    def MaxDmg(self):
        """Returns the current maximum damage yield of the weapon wielded by the character. The character status bar
        must be open to read this variable properly.

        .. seealso::
           :py:attr:`MinDmg`
        """

    @UOVarProperty
    def MaxFol(self):
        """Returns the maximum number of followers allowed for the character. The character status bar must be open to
        read this variable properly.

        .. seealso::
           :py:attr:`Followers`
        """

    @UOVarProperty
    def MaxHits(self):
        """Returns the maximum Hit Points of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`Hits`
        """

    @UOVarProperty
    def MaxMana(self):
        """Returns the maximum Mana of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`Mana`
        """

    @UOVarProperty
    def MaxStam(self):
        """ Returns the maximum Stamina of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`Stamina`
        """

    @UOVarProperty
    def MaxStats(self):
        """Returns the maximum combined Stats of the character. The character status bar must be open to read this
        variable properly.

        .. seealso::
           :py:attr:`Dex`
           :py:attr:`Int`
           :py:attr:`Str`
        """

    @UOVarProperty
    def MaxWeight(self):
        """Returns the maximum allowable Weight bearable by the character. The character status bar must be open to read
        this variable properly.

        .. seealso::
           :py:attr:`Weight
        """

    @UOVarProperty
    def MinDmg(self):
        """Returns the current minimum damage yield of the weapon wielded by the character. The character status bar
        must be open to read this variable properly.

        .. seealso::
           :py:attr:`MaxDmg`
        """

    @UOVarProperty
    def NextCPosX(self):
        """ Return or set the x-coordinate of where the next container/gump will open.

        .. note::
           The "Offset interface windows rather than perfectly stacking them" client option, in Interface options,
           must be turned on for this variable to work.

        .. seealso::
           :py:attr:`ContPosX`
           :py:attr:`ContPosY`
           :py:attr:`NextCPosY`
        """

    @UOVarProperty
    def NextCPosY(self):
        """ Return or set the y-coordinate of where the next container/gump will open.

        .. note::
           The "Offset interface windows rather than perfectly stacking them" client option, in Interface options,
           must be turned on for this variable to work.*

        .. seealso::
           :py:attr:`ContPosX`
           :py:attr:`ContPosY`
           :py:attr:`NextCPosX`
        """

    @UOVarProperty
    def PR(self):
        """Returns the Poison Resist of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`CR`
           :py:attr:`ER`
           :py:attr:`FR`
           :py:attr:`AR`
        """

    @UOVarProperty
    def RHandID(self):
        """Return the item held in the character's right hand, or set the item to be held upon employing UO.Macro(24,2).

        .. note::
           This variable is used with an event macro in order to place an item in your character's right hand. It
           must be set to a valid items ID, and the item must be able to be held in the character's right hand in order to
           work.*

        .. seealso::
           :py:attr:`LHandID`
        """

    @UOVarProperty
    def Sex(self):
        """Returns the sex of the character. The character status bar must be open to read this variable properly.

        *Yes please*

        .. seealso::
           :py:attr:`CharID`
           :py:attr:`CharName`
           :py:attr:`CharStatus`
           :py:attr:`CharType`
        """

    @UOVarProperty
    def Shard(self):
        """Returns the name of the shard that the client is logged in to.

        .. seealso::
           :py:attr:`CliLogged`
        """

    @UOVarProperty
    def Stamina(self):
        """Returns the current Stamina of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           :py:attr:`MaxStam`
        """

    @UOVarProperty
    def StatBar(self):
        """Pulls up the status bar for the given object id. Exclusive to OpenEUO."""

    @UOVarProperty
    def Str(self):
        """Returns the Strength of the character. The character status bar must be open to read this variable properly.

        .. seealso::
           :py:attr:`Int`
           :py:attr:`Dex`
        """

    @UOVarProperty
    def SysMsg(self):
        """Returns the latest system message.
        .. note::
           There appears to be no equivalent to the EUO #sysmsgcol variable for reading the system message color.

        .. seealso::
           :py:meth:`llUO.ScanJournal`
           :py:meth:`llUO.GetJournal`
        """

    @UOVarProperty
    def TargCurs(self):
        """Returns whether the game cursor is a targeting cursor, or may be set to obtain a targeting cursor."""

    @UOVarProperty
    def TP(self):
        """Returns the Tithing Points available to character. The character status bar must be open to read this
        variable properly."""

    @UOVarProperty
    def Weight(self):
        """Returns the current Weight of the character. The character status bar must be open to read this variable
        properly.

        .. seealso::
           * py:attr:`MaxWeight`
        """

class llUO(llUOVar):
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

        * :meth:`DropC`
        * :meth:`DropG`
        * :meth:`DropPD`

        .. warning::
           Using this method while character is moving will probably cause UO client to crash.
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

        Args:
           index (int): Determines what line of the journal to get. 0 is the most recent line nIndex is what line of the
              journal you wish to get, 1 is the next most recent and so on.

        Returns:
           line (str), col (int): line will hold the line of text, col will be the color of the text.
        """
        return self.Call("GetJournal", index)

    def GetPix(self, x, y):
        """Saves the color value of the pixel given by the screen coordinate parameters"""
        return self.Call("GetPix", x, y)

    def GetShop(self):
        """bRes,nPos,nCnt,nID,nType,nMax,nPrice,sName = UO.GetShop()

        This command retrieves information about the currently shown top entry on an open shopping gump.

        .. note:: Every time you scroll to a new entry, you have to call UO.GetShop.
        """
        return self.Call("GetShop")

    def GetSkill(self, skill):
        """Returns the folowing variables on the choosen skill.

        :synopsis: sNorm, nReal, nCap, nLock = UO.GetSkill(skill)
        """
        return self.Call("GetSkill", skill)

    def HideItem(self, nid):
        """This command removes a specific item id's graphic from the client.

        It can be used to unclutter the visual appearance of the client however,
        it does nothing on the server. Only non-static items that are on the ground can be hidden.
        Items will reappear if the client is resynchronized with the server

        .. warning::
           Make sure the item exists in client's memory before invoking the method, otherwise a crash might occur.
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

    def Get(self, varname):
        """Internal method to get variable value from uo.dll"""
        return self.stack.execute('Get', varname)

    def Set(self, varname, value):
        """Internal method to set variable vailue in uo.dll"""
        self.stack.execute('Set', varname, value)

    def Call(self, func, *args):
        """Internal method to call a function from uo.dll"""
        return self.stack.execute('Call', func, *args)

