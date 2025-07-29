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
class bstack1111l11l1_opy_:
    def __init__(self, handler):
        self._1111ll1llll_opy_ = None
        self.handler = handler
        self._1111ll1ll1l_opy_ = self.bstack1111ll1lll1_opy_()
        self.patch()
    def patch(self):
        self._1111ll1llll_opy_ = self._1111ll1ll1l_opy_.execute
        self._1111ll1ll1l_opy_.execute = self.bstack1111lll1111_opy_()
    def bstack1111lll1111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣḪ"), driver_command, None, this, args)
            response = self._1111ll1llll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1lll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣḫ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1111ll1ll1l_opy_.execute = self._1111ll1llll_opy_
    @staticmethod
    def bstack1111ll1lll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver