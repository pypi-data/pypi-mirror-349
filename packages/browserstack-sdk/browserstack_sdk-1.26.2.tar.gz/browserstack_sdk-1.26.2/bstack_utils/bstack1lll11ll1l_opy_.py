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
class bstack1ll1l1l11_opy_:
    def __init__(self, handler):
        self._1111ll1l1ll_opy_ = None
        self.handler = handler
        self._1111ll1l1l1_opy_ = self.bstack1111ll1l11l_opy_()
        self.patch()
    def patch(self):
        self._1111ll1l1ll_opy_ = self._1111ll1l1l1_opy_.execute
        self._1111ll1l1l1_opy_.execute = self.bstack1111ll1ll11_opy_()
    def bstack1111ll1ll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧḵ"), driver_command, None, this, args)
            response = self._1111ll1l1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧḶ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1111ll1l1l1_opy_.execute = self._1111ll1l1ll_opy_
    @staticmethod
    def bstack1111ll1l11l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver