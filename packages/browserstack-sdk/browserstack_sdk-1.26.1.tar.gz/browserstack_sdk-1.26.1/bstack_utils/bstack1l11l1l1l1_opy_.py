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
bstack111lll1lll1_opy_ = {bstack11l1lll_opy_ (u"ࠬࡸࡥࡵࡴࡼࡘࡪࡹࡴࡴࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫᴖ")}
class bstack1l1l1l1ll1_opy_:
    @staticmethod
    def bstack1l1ll11l_opy_(config: dict) -> bool:
        bstack111lll1llll_opy_ = config.get(bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᴗ"), {}).get(bstack11l1lll_opy_ (u"ࠧࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ᴘ"), {})
        return bstack111lll1llll_opy_.get(bstack11l1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᴙ"), False)
    @staticmethod
    def bstack11l1ll1ll1_opy_(config: dict) -> int:
        bstack111lll1llll_opy_ = config.get(bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴚ"), {}).get(bstack11l1lll_opy_ (u"ࠪࡶࡪࡺࡲࡺࡖࡨࡷࡹࡹࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩᴛ"), {})
        retries = 0
        if bstack1l1l1l1ll1_opy_.bstack1l1ll11l_opy_(config):
            retries = bstack111lll1llll_opy_.get(bstack11l1lll_opy_ (u"ࠫࡲࡧࡸࡓࡧࡷࡶ࡮࡫ࡳࠨᴜ"), 1)
        return retries
    @staticmethod
    def bstack11l11lll1_opy_(config: dict) -> dict:
        bstack111lll1ll1l_opy_ = config.get(bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴝ"), {})
        return {
            key: value for key, value in bstack111lll1ll1l_opy_.items() if key in bstack111lll1lll1_opy_
        }