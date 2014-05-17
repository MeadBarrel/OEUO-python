from pyuo.oeuo import UO, AS
from .extensions import use_item, use_on
from .itertools import imap, ifilter
import itertools
import re
import gevent


class ItemProperty(object):
    def __init__(self, name, value=1.0, min_=None, max_=None):
        self.name = name
        self.value = value
        self.min_ = min_
        self.max_ = max_


class ItemProperties(object):
    #re_plaintext = '((?:\w| )+?)'
    re_name = re.compile('([a-zA-Z-_ ]+)')
    re_numerics = re.compile('(\d(?:\d|\.)+)')
    def __init__(self, property_strings):
        self._properties = {}
        for property_string in property_strings.split('\n'):
            self.parse_property(property_string.strip())

    def __getitem__(self, item):
        if item in self._properties:
            return self._properties[item]
        else:
            return ItemProperty(item, 0, 0, 0)

    def __contains__(self, item):
        return item in self._properties

    def full_string(self):
        result = ''
        for name, property in self._properties.iteritems():
            result += '%s: %s' % (name, str(property.value))

    def parse_property(self, property_string):
        match_name = self.re_name.match(property_string)
        if not match_name:
            return ItemProperty(property_string)
        name = match_name.groups()[0]
        name = name.strip()
        nums = self.re_numerics.findall(property_string)
        if not nums:
            self._properties[name] = ItemProperty(name)
        elif len(nums) == 1:
            self._properties[name] = ItemProperty(name, float(nums[0]))
        else:
            min_ = float(nums[0])
            max_ = float(nums[1])
            value = min_ + (max_ - min_)/2
            self._properties[name] = ItemProperty(name, value, min_, max_)

class Item(object):
    """Represents UO item."""

    def __init__(self, index=None):
        """Initialize the item.

        The item will be 'empty' if no index provided. When index is provided, it willl call UO.GetItem to create the
        item instance.
        """
        self.id_ = None
        self.type_ = None
        self.kind = None
        self.cont_id = None
        self.x = None
        self.y = None
        self.z = None
        self.stack = None
        self.rep = None
        self.col = None
        self._properties = None
        if index is not None:
            self._from_index(index)

    def __hash__(self):
        return hash(self.id_)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id_ == other
        elif isinstance(other, Item):
            return self.id_ == other.id_
        else:
            raise TypeError

    @property
    def properties(self):
        if self._properties is None:
            self._properties = ItemProperties(self.info[1])
        return self._properties

    def full_string(self):
        prop = self.info
        result = 'ITEM: %s\n' % prop[0]
        result += 'id: %i\n' % self.id_
        result += 'kind: %i\n' % self.kind
        result += 'col: %s\n' % str(self.col)
        result += 'Properties %s\n' % prop[1]
        return result

    @property
    def distance_to_player(self):
        x, y = UO.CharPosX, UO.CharPosY
        return max(abs(x - self.x), abs(y - self.y))

    @property
    def on_ground(self):
        return self.cont_id == 0

    @property
    def info(self):
        return UO.Property(self.id_)

    @property
    def name(self):
        return self.info[0]

    def _from_index(self, index):
        """Internal method to initialize the item with UO.GetItem."""
        self.id_, self.type_, self.kind, self.cont_id, self.x, self.y, self.z, self.stack, self.rep, self.col = UO.GetItem(index)

    def is_in_backpack(self):
        """Check if the item is in player's backpack and return a boolean."""
        return self.cont_id == UO.BackpackID

    def containers(self, depth=3):
        """Return a recursive list of containers this item is located in.

         .. method:: containers()
                     containers(depths)
        """
        result = []
        current = ItemFilter().with_id(self.cont_id).first()
        if current is None:
            return result
        result.append(current)
        for i in xrange(depth):
            if current.cont_id is None:
                break
            current = ItemFilter().with_id(current.cont_id).first()
            if not current:
                break
            result.append(current)
        return result

    def use(self):
        return use_item(self.id_)

    def use_on(self, target, timeout=None):
        if isinstance(target, Item):
            target = target.id_
        return use_on(self.id_, target, timeout)

class ItemFilter(object):
    def __init__(self, visible_only=False):
        self.visible_only = visible_only
        self.filters = []

    def search(self):
        count = None
        count =  UO.ScanItems()
        return ifilter(lambda item: all(filt(item) for filt in self.filters), imap(Item, xrange(count)))

    def first(self):
        srch = self.search()
        return next(srch, None)

    def all(self):
        srch = self.search()
        return list(srch)

    def with_id(self, id_):
        self.filters.append(lambda item: item.id_ == id_)
        return self

    def with_name(self, regexp):
        self.filters.append(lambda item: re.match(regexp, item.property[0]))

    def with_type(self, type_):
        self.filters.append(lambda item: item.type_ == type_)
        return self

    def in_container(self, cont_id):
        self.filters.append(lambda item: item.cont_id == cont_id)
        return self

    def in_backpack(self):
        self.filters.append(lambda item: item.is_in_backpack())
        return self

    def in_container_rec(self, cont_id, depth=3):
        self.filters.append(lambda item: cont_id in (cont.id_ for cont in item.containers(depth)))
        return self

    def in_backpack_rec(self, depth=3):
        return self.in_container_rec(UO.BackpackID, depth)

def get_by_id(id_):
    for item in iter_items():
        if item.id_ == id_:
            return item
    return None

def get_items(visible_only=False):
    count = UO.ScanItems(visible_only)
    return map(Item, xrange(count))

def iter_items(visible_only=False):
    count = UO.ScanItems(visible_only)
    return itertools.imap(Item, xrange(count))

def iter_items_async(visible_only=False):
    count = UO.ScanItems(visible_only)
    return imap(Item, xrange(count))


