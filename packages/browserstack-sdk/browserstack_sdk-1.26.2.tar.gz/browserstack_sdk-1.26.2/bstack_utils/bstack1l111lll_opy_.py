# coding: UTF-8
import sys
bstack11l_opy_ = sys.version_info [0] == 2
bstack11l1_opy_ = 2048
bstack1l1l1l_opy_ = 7
def bstack111l11_opy_ (bstack111111l_opy_):
    global bstack11lllll_opy_
    bstack111l11l_opy_ = ord (bstack111111l_opy_ [-1])
    bstack11l1ll_opy_ = bstack111111l_opy_ [:-1]
    bstack11l11l1_opy_ = bstack111l11l_opy_ % len (bstack11l1ll_opy_)
    bstack11111ll_opy_ = bstack11l1ll_opy_ [:bstack11l11l1_opy_] + bstack11l1ll_opy_ [bstack11l11l1_opy_:]
    if bstack11l_opy_:
        bstack1llllll1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1_opy_ - (bstack11lll_opy_ + bstack111l11l_opy_) % bstack1l1l1l_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    else:
        bstack1llllll1_opy_ = str () .join ([chr (ord (char) - bstack11l1_opy_ - (bstack11lll_opy_ + bstack111l11l_opy_) % bstack1l1l1l_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    return eval (bstack1llllll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack111ll111_opy_:
    def __init__(self):
        self._111l11llll1_opy_ = deque()
        self._111l1l111ll_opy_ = {}
        self._111l1l11l1l_opy_ = False
    def bstack111l1l11111_opy_(self, test_name, bstack111l1l11l11_opy_):
        bstack111l11lllll_opy_ = self._111l1l111ll_opy_.get(test_name, {})
        return bstack111l11lllll_opy_.get(bstack111l1l11l11_opy_, 0)
    def bstack111l11lll1l_opy_(self, test_name, bstack111l1l11l11_opy_):
        bstack111l1l1l111_opy_ = self.bstack111l1l11111_opy_(test_name, bstack111l1l11l11_opy_)
        self.bstack111l1l1111l_opy_(test_name, bstack111l1l11l11_opy_)
        return bstack111l1l1l111_opy_
    def bstack111l1l1111l_opy_(self, test_name, bstack111l1l11l11_opy_):
        if test_name not in self._111l1l111ll_opy_:
            self._111l1l111ll_opy_[test_name] = {}
        bstack111l11lllll_opy_ = self._111l1l111ll_opy_[test_name]
        bstack111l1l1l111_opy_ = bstack111l11lllll_opy_.get(bstack111l1l11l11_opy_, 0)
        bstack111l11lllll_opy_[bstack111l1l11l11_opy_] = bstack111l1l1l111_opy_ + 1
    def bstack1l1ll1l1l1_opy_(self, bstack111l1l11lll_opy_, bstack111l1l111l1_opy_):
        bstack111l1l11ll1_opy_ = self.bstack111l11lll1l_opy_(bstack111l1l11lll_opy_, bstack111l1l111l1_opy_)
        event_name = bstack11ll111l1ll_opy_[bstack111l1l111l1_opy_]
        bstack1l1ll11l11l_opy_ = bstack111l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᶬ").format(bstack111l1l11lll_opy_, event_name, bstack111l1l11ll1_opy_)
        self._111l11llll1_opy_.append(bstack1l1ll11l11l_opy_)
    def bstack111111111_opy_(self):
        return len(self._111l11llll1_opy_) == 0
    def bstack1lll11111_opy_(self):
        bstack111l11lll11_opy_ = self._111l11llll1_opy_.popleft()
        return bstack111l11lll11_opy_
    def capturing(self):
        return self._111l1l11l1l_opy_
    def bstack1ll1ll1ll1_opy_(self):
        self._111l1l11l1l_opy_ = True
    def bstack1l1l1l11l_opy_(self):
        self._111l1l11l1l_opy_ = False