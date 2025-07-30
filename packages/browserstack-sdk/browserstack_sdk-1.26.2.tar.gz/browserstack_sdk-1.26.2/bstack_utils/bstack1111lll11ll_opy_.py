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
import threading
import logging
logger = logging.getLogger(__name__)
bstack1111lll1ll1_opy_ = 1000
bstack1111llll111_opy_ = 2
class bstack1111llll1ll_opy_:
    def __init__(self, handler, bstack1111lllll11_opy_=bstack1111lll1ll1_opy_, bstack1111lll11l1_opy_=bstack1111llll111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1111lllll11_opy_ = bstack1111lllll11_opy_
        self.bstack1111lll11l1_opy_ = bstack1111lll11l1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack11111lllll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1111llll1l1_opy_()
    def bstack1111llll1l1_opy_(self):
        self.bstack11111lllll_opy_ = threading.Event()
        def bstack1111llll11l_opy_():
            self.bstack11111lllll_opy_.wait(self.bstack1111lll11l1_opy_)
            if not self.bstack11111lllll_opy_.is_set():
                self.bstack1111lll1lll_opy_()
        self.timer = threading.Thread(target=bstack1111llll11l_opy_, daemon=True)
        self.timer.start()
    def bstack1111lll1l11_opy_(self):
        try:
            if self.bstack11111lllll_opy_ and not self.bstack11111lllll_opy_.is_set():
                self.bstack11111lllll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨḟ") + (str(e) or bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨḠ")))
        finally:
            self.timer = None
    def bstack1111lll1l1l_opy_(self):
        if self.timer:
            self.bstack1111lll1l11_opy_()
        self.bstack1111llll1l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1111lllll11_opy_:
                threading.Thread(target=self.bstack1111lll1lll_opy_).start()
    def bstack1111lll1lll_opy_(self, source = bstack111l11_opy_ (u"࠭ࠧḡ")):
        with self.lock:
            if not self.queue:
                self.bstack1111lll1l1l_opy_()
                return
            data = self.queue[:self.bstack1111lllll11_opy_]
            del self.queue[:self.bstack1111lllll11_opy_]
        self.handler(data)
        if source != bstack111l11_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩḢ"):
            self.bstack1111lll1l1l_opy_()
    def shutdown(self):
        self.bstack1111lll1l11_opy_()
        while self.queue:
            self.bstack1111lll1lll_opy_(source=bstack111l11_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪḣ"))