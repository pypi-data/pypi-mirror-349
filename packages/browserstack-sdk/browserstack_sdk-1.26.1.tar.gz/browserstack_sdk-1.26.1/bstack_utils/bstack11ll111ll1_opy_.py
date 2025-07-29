# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack1l111l_opy_ = 2048
bstack11l11l1_opy_ = 7
def bstack11l1lll_opy_ (bstack1lllll1_opy_):
    global bstack1l1l111_opy_
    bstack1ll1111_opy_ = ord (bstack1lllll1_opy_ [-1])
    bstack111111_opy_ = bstack1lllll1_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack1ll1111_opy_ % len (bstack111111_opy_)
    bstack111l11l_opy_ = bstack111111_opy_ [:bstack1lll1l1_opy_] + bstack111111_opy_ [bstack1lll1l1_opy_:]
    if bstack1l11_opy_:
        bstack11ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l111l_opy_ - (bstack11l11ll_opy_ + bstack1ll1111_opy_) % bstack11l11l1_opy_) for bstack11l11ll_opy_, char in enumerate (bstack111l11l_opy_)])
    else:
        bstack11ll11_opy_ = str () .join ([chr (ord (char) - bstack1l111l_opy_ - (bstack11l11ll_opy_ + bstack1ll1111_opy_) % bstack11l11l1_opy_) for bstack11l11ll_opy_, char in enumerate (bstack111l11l_opy_)])
    return eval (bstack11ll11_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack11lll11l1l_opy_:
    def __init__(self):
        self._111l1l1l1l1_opy_ = deque()
        self._111l1l11lll_opy_ = {}
        self._111l1l1l111_opy_ = False
    def bstack111l1l1l1ll_opy_(self, test_name, bstack111l1l11111_opy_):
        bstack111l1l1l11l_opy_ = self._111l1l11lll_opy_.get(test_name, {})
        return bstack111l1l1l11l_opy_.get(bstack111l1l11111_opy_, 0)
    def bstack111l1l11ll1_opy_(self, test_name, bstack111l1l11111_opy_):
        bstack111l1l111l1_opy_ = self.bstack111l1l1l1ll_opy_(test_name, bstack111l1l11111_opy_)
        self.bstack111l1l111ll_opy_(test_name, bstack111l1l11111_opy_)
        return bstack111l1l111l1_opy_
    def bstack111l1l111ll_opy_(self, test_name, bstack111l1l11111_opy_):
        if test_name not in self._111l1l11lll_opy_:
            self._111l1l11lll_opy_[test_name] = {}
        bstack111l1l1l11l_opy_ = self._111l1l11lll_opy_[test_name]
        bstack111l1l111l1_opy_ = bstack111l1l1l11l_opy_.get(bstack111l1l11111_opy_, 0)
        bstack111l1l1l11l_opy_[bstack111l1l11111_opy_] = bstack111l1l111l1_opy_ + 1
    def bstack1l11l111l_opy_(self, bstack111l1l1111l_opy_, bstack111l1l11l1l_opy_):
        bstack111l1l11l11_opy_ = self.bstack111l1l11ll1_opy_(bstack111l1l1111l_opy_, bstack111l1l11l1l_opy_)
        event_name = bstack11ll11111l1_opy_[bstack111l1l11l1l_opy_]
        bstack1l1ll111l1l_opy_ = bstack11l1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᶡ").format(bstack111l1l1111l_opy_, event_name, bstack111l1l11l11_opy_)
        self._111l1l1l1l1_opy_.append(bstack1l1ll111l1l_opy_)
    def bstack1l1ll1l1ll_opy_(self):
        return len(self._111l1l1l1l1_opy_) == 0
    def bstack11lll111l_opy_(self):
        bstack111l1l1ll11_opy_ = self._111l1l1l1l1_opy_.popleft()
        return bstack111l1l1ll11_opy_
    def capturing(self):
        return self._111l1l1l111_opy_
    def bstack11l1lllll_opy_(self):
        self._111l1l1l111_opy_ = True
    def bstack111ll1111_opy_(self):
        self._111l1l1l111_opy_ = False