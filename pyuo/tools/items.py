from pyuo.oeuo import UO
from .extensions import use_item, use_on
from itertools import imap, ifilter

class Item(object):
    def __init__(self, index=None):
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
        if index is not None:
            self.from_index(index)

    def from_index(self, index):
        self.id_, self.type_, self.kind, self.cont_id, self.x, self.y, self.z, self.stack, self.rep, self.col = UO.GetItem(index)

    def is_in_backpack(self):
        return self.cont_id == UO.BackpackID

    def containers(self, depth=3):
        result = []
        current = ItemFilter().with_id(self.cont_id).first()
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

    def use_on(self, target, callback=None, timeout=None, failure=None):
        if isinstance(target, Item):
            target = target.id_
        use_on(self.id_, target, callback, timeout, failure)

class ItemFilter(object):
    def __init__(self, visible_only=False):
        self.visible_only = visible_only
        self.filters = []

    def search(self):
        count =  UO.ScanItems()
        return ifilter(lambda item: all(filter(item) for filter in self.filters), imap(Item, xrange(count)))

    def first(self):
        srch = self.search()
        return next(srch, None)

    def all(self):
        srch = self.search()
        return list(srch)

    def with_id(self, id_):
        self.filters.append(lambda item: item.id_ == id_)
        return self

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







