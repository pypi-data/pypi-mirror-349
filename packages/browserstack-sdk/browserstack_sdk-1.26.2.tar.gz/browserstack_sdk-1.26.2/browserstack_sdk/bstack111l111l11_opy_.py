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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1l11l_opy_, bstack1111lll1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l11l_opy_ = bstack1111l1l11l_opy_
        self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11llll_opy_(bstack1111l11l11_opy_):
        bstack1111l111ll_opy_ = []
        if bstack1111l11l11_opy_:
            tokens = str(os.path.basename(bstack1111l11l11_opy_)).split(bstack111l11_opy_ (u"ࠥࡣࠧဥ"))
            camelcase_name = bstack111l11_opy_ (u"ࠦࠥࠨဦ").join(t.title() for t in tokens)
            suite_name, bstack1111l11l1l_opy_ = os.path.splitext(camelcase_name)
            bstack1111l111ll_opy_.append(suite_name)
        return bstack1111l111ll_opy_
    @staticmethod
    def bstack1111l11ll1_opy_(typename):
        if bstack111l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣဧ") in typename:
            return bstack111l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢဨ")
        return bstack111l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣဩ")