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
bstack111lll1ll1l_opy_ = {bstack111l11_opy_ (u"ࠩࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨᴡ")}
class bstack11ll11l11l_opy_:
    @staticmethod
    def bstack1l1l1l111l_opy_(config: dict) -> bool:
        bstack111lll1l1ll_opy_ = config.get(bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧᴢ"), {}).get(bstack111l11_opy_ (u"ࠫࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠪᴣ"), {})
        return bstack111lll1l1ll_opy_.get(bstack111l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ᴤ"), False)
    @staticmethod
    def bstack1111lll1l_opy_(config: dict) -> int:
        bstack111lll1l1ll_opy_ = config.get(bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᴥ"), {}).get(bstack111l11_opy_ (u"ࠧࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ᴦ"), {})
        retries = 0
        if bstack11ll11l11l_opy_.bstack1l1l1l111l_opy_(config):
            retries = bstack111lll1l1ll_opy_.get(bstack111l11_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬᴧ"), 1)
        return retries
    @staticmethod
    def bstack1ll11l1lll_opy_(config: dict) -> dict:
        bstack111lll1ll11_opy_ = config.get(bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴨ"), {})
        return {
            key: value for key, value in bstack111lll1ll11_opy_.items() if key in bstack111lll1ll1l_opy_
        }