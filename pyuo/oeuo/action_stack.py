from collections import deque
#from pyuo.manager.props import FloatSetting
import gevent


class ActionStackError(Exception):
    pass


class _ActionStack(object):
    #stack_delay = FloatSetting('Action delay', default=.6)
    #todo: make this float setting
    stack_delay = .6

    def __init__(self, UO):
        self.UO = UO
        self.stack = deque()
        self.invoked = {}
        self.index = 0

    def push(self, action, args, kwargs):
        """Push an action into stack and return it's unique id

        :type action callable
        :type args tuple
        :type kwargs dict
        :rtype int
        """
        index = self.index
        self.stack.append((index, action, args, kwargs))
        self.index += 1
        return index

    def invoke_next(self):
        """Call action on the top of the stack, pop the action, and put the result into *invoked* dict
        Returns True if succeeded, or False if the stack is empty

        :rtype boolean
        """
        if not self.stack:
            return False
        action = self.stack.pop()
        index = action[0]
        result = action[1](*action[2], **action[3])
        print "POP %s" % str(action[1])
        assert index not in self.invoked
        self.invoked[index] = result
        return True

    def main_loop(self):
        while True:
            if self.invoke_next():
                gevent.sleep(self.stack_delay)
            else:
                gevent.sleep(0)

    def push_action(self, action, *args, **kwargs):
        """Push the action and wait for result. Return the result.
        :type action callable
        """
        print "PUSH %s" % str(action)
        index = self.push(action, args, kwargs)
        while not index in self.invoked:
            gevent.sleep(0)
        result = self.invoked[index]
        del self.invoked[index]
        return result


class ActionStack(_ActionStack):
    def Macro(self, param_1, param_2=0, string=''):
        return self.push_action(self.UO.Macro, param_1, param_2, string)

    def Drag(self, nid, namnt=None):
        return self.push_action(self.UO.Drag, nid, namnt)

    def DropC(self, contid, pos=None):
        return self.push_action(self.UO.DropC, contid, pos)

    def DropG(self, x, y, z=None):
        return self.push_action(self.UO.DropG, x, y, z)

    def DropPD(self):
        return self.push_action(self.UO.DropPD)

    def Equip(self, *nids):
        return self.push_action(self.UO.Equip, *nids)

    def CliDrag(self, nid):
        return self.push_action(self.UO.CliDrag, nid)