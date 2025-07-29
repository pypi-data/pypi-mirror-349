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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111lll1ll_opy_, bstack1111ll1l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1lll1l_opy_(bstack1111l11ll1_opy_):
        bstack1111l11l1l_opy_ = []
        if bstack1111l11ll1_opy_:
            tokens = str(os.path.basename(bstack1111l11ll1_opy_)).split(bstack11l1lll_opy_ (u"ࠥࡣࠧဥ"))
            camelcase_name = bstack11l1lll_opy_ (u"ࠦࠥࠨဦ").join(t.title() for t in tokens)
            suite_name, bstack1111l11l11_opy_ = os.path.splitext(camelcase_name)
            bstack1111l11l1l_opy_.append(suite_name)
        return bstack1111l11l1l_opy_
    @staticmethod
    def bstack1111l111ll_opy_(typename):
        if bstack11l1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣဧ") in typename:
            return bstack11l1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢဨ")
        return bstack11l1lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣဩ")