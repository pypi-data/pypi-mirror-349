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
import threading
import logging
logger = logging.getLogger(__name__)
bstack1111lllll11_opy_ = 1000
bstack1111lllllll_opy_ = 2
class bstack111l1111111_opy_:
    def __init__(self, handler, bstack1111lll1lll_opy_=bstack1111lllll11_opy_, bstack1111llll11l_opy_=bstack1111lllllll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1111lll1lll_opy_ = bstack1111lll1lll_opy_
        self.bstack1111llll11l_opy_ = bstack1111llll11l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack11111lll1l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1111llll111_opy_()
    def bstack1111llll111_opy_(self):
        self.bstack11111lll1l_opy_ = threading.Event()
        def bstack1111llllll1_opy_():
            self.bstack11111lll1l_opy_.wait(self.bstack1111llll11l_opy_)
            if not self.bstack11111lll1l_opy_.is_set():
                self.bstack1111lllll1l_opy_()
        self.timer = threading.Thread(target=bstack1111llllll1_opy_, daemon=True)
        self.timer.start()
    def bstack1111llll1l1_opy_(self):
        try:
            if self.bstack11111lll1l_opy_ and not self.bstack11111lll1l_opy_.is_set():
                self.bstack11111lll1l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫḔ") + (str(e) or bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤḕ")))
        finally:
            self.timer = None
    def bstack1111lll1ll1_opy_(self):
        if self.timer:
            self.bstack1111llll1l1_opy_()
        self.bstack1111llll111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1111lll1lll_opy_:
                threading.Thread(target=self.bstack1111lllll1l_opy_).start()
    def bstack1111lllll1l_opy_(self, source = bstack11l1lll_opy_ (u"ࠩࠪḖ")):
        with self.lock:
            if not self.queue:
                self.bstack1111lll1ll1_opy_()
                return
            data = self.queue[:self.bstack1111lll1lll_opy_]
            del self.queue[:self.bstack1111lll1lll_opy_]
        self.handler(data)
        if source != bstack11l1lll_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬḗ"):
            self.bstack1111lll1ll1_opy_()
    def shutdown(self):
        self.bstack1111llll1l1_opy_()
        while self.queue:
            self.bstack1111lllll1l_opy_(source=bstack11l1lll_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭Ḙ"))