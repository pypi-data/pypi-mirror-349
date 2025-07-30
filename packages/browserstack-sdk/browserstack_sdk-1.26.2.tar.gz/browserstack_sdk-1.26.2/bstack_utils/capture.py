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
import builtins
import logging
class bstack111llllll1_opy_:
    def __init__(self, handler):
        self._11ll1l1ll11_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1l1l11l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᛧ"), bstack111l11_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᛨ"), bstack111l11_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᛩ"), bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᛪ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1l1l1ll_opy_
        self._11ll1l1ll1l_opy_()
    def _11ll1l1l1ll_opy_(self, *args, **kwargs):
        self._11ll1l1ll11_opy_(*args, **kwargs)
        message = bstack111l11_opy_ (u"ࠨࠢࠪ᛫").join(map(str, args)) + bstack111l11_opy_ (u"ࠩ࡟ࡲࠬ᛬")
        self._log_message(bstack111l11_opy_ (u"ࠪࡍࡓࡌࡏࠨ᛭"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᛮ"): level, bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᛯ"): msg})
    def _11ll1l1ll1l_opy_(self):
        for level, bstack11ll1l1l111_opy_ in self._11ll1l1l11l_opy_.items():
            setattr(logging, level, self._11ll1l1l1l1_opy_(level, bstack11ll1l1l111_opy_))
    def _11ll1l1l1l1_opy_(self, level, bstack11ll1l1l111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll1l1l111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1l1ll11_opy_
        for level, bstack11ll1l1l111_opy_ in self._11ll1l1l11l_opy_.items():
            setattr(logging, level, bstack11ll1l1l111_opy_)