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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1ll1l1_opy_ = {}
        bstack11l1111ll1_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃຸࠪ"), bstack111l11_opy_ (u"ູࠪࠫ"))
        if not bstack11l1111ll1_opy_:
            return bstack1l1ll1l1_opy_
        try:
            bstack11l1111lll_opy_ = json.loads(bstack11l1111ll1_opy_)
            if bstack111l11_opy_ (u"ࠦࡴࡹ຺ࠢ") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠧࡵࡳࠣົ")] = bstack11l1111lll_opy_[bstack111l11_opy_ (u"ࠨ࡯ࡴࠤຼ")]
            if bstack111l11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦຽ") in bstack11l1111lll_opy_ or bstack111l11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ຾") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ຿")] = bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢເ"), bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢແ")))
            if bstack111l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨໂ") in bstack11l1111lll_opy_ or bstack111l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦໃ") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧໄ")] = bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ໅"), bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢໆ")))
            if bstack111l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ໇") in bstack11l1111lll_opy_ or bstack111l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ່ࠧ") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ້")] = bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮໊ࠣ"), bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮໋ࠣ")))
            if bstack111l11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ໌") in bstack11l1111lll_opy_ or bstack111l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨໍ") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ໎")] = bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ໏"), bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ໐")))
            if bstack111l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ໑") in bstack11l1111lll_opy_ or bstack111l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ໒") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໓")] = bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ໔"), bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ໕")))
            if bstack111l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ໖") in bstack11l1111lll_opy_ or bstack111l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ໗") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໘")] = bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ໙"), bstack11l1111lll_opy_.get(bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ໚")))
            if bstack111l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ໛") in bstack11l1111lll_opy_:
                bstack1l1ll1l1_opy_[bstack111l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧໜ")] = bstack11l1111lll_opy_[bstack111l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨໝ")]
        except Exception as error:
            logger.error(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦໞ") +  str(error))
        return bstack1l1ll1l1_opy_