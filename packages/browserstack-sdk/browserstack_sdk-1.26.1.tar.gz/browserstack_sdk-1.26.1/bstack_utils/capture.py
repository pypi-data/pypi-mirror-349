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
import builtins
import logging
class bstack111llll11l_opy_:
    def __init__(self, handler):
        self._11ll1l1ll1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1l1l1ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l1lll_opy_ (u"ࠧࡪࡰࡩࡳࠬᛜ"), bstack11l1lll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᛝ"), bstack11l1lll_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᛞ"), bstack11l1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᛟ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1l1llll_opy_
        self._11ll1l1lll1_opy_()
    def _11ll1l1llll_opy_(self, *args, **kwargs):
        self._11ll1l1ll1l_opy_(*args, **kwargs)
        message = bstack11l1lll_opy_ (u"ࠫࠥ࠭ᛠ").join(map(str, args)) + bstack11l1lll_opy_ (u"ࠬࡢ࡮ࠨᛡ")
        self._log_message(bstack11l1lll_opy_ (u"࠭ࡉࡏࡈࡒࠫᛢ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᛣ"): level, bstack11l1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᛤ"): msg})
    def _11ll1l1lll1_opy_(self):
        for level, bstack11ll1l1ll11_opy_ in self._11ll1l1l1ll_opy_.items():
            setattr(logging, level, self._11ll1l1l1l1_opy_(level, bstack11ll1l1ll11_opy_))
    def _11ll1l1l1l1_opy_(self, level, bstack11ll1l1ll11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll1l1ll11_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1l1ll1l_opy_
        for level, bstack11ll1l1ll11_opy_ in self._11ll1l1l1ll_opy_.items():
            setattr(logging, level, bstack11ll1l1ll11_opy_)