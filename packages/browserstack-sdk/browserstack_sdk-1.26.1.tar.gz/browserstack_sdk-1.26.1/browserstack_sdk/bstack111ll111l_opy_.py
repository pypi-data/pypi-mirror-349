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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11l1ll111l_opy_ = {}
        bstack11l1111lll_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃຸࠪ"), bstack11l1lll_opy_ (u"ູࠪࠫ"))
        if not bstack11l1111lll_opy_:
            return bstack11l1ll111l_opy_
        try:
            bstack11l1111ll1_opy_ = json.loads(bstack11l1111lll_opy_)
            if bstack11l1lll_opy_ (u"ࠦࡴࡹ຺ࠢ") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠧࡵࡳࠣົ")] = bstack11l1111ll1_opy_[bstack11l1lll_opy_ (u"ࠨ࡯ࡴࠤຼ")]
            if bstack11l1lll_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦຽ") in bstack11l1111ll1_opy_ or bstack11l1lll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ຾") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ຿")] = bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢເ"), bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢແ")))
            if bstack11l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨໂ") in bstack11l1111ll1_opy_ or bstack11l1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦໃ") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧໄ")] = bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ໅"), bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢໆ")))
            if bstack11l1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ໇") in bstack11l1111ll1_opy_ or bstack11l1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ່ࠧ") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ້")] = bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮໊ࠣ"), bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮໋ࠣ")))
            if bstack11l1lll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ໌") in bstack11l1111ll1_opy_ or bstack11l1lll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨໍ") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ໎")] = bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ໏"), bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ໐")))
            if bstack11l1lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ໑") in bstack11l1111ll1_opy_ or bstack11l1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ໒") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໓")] = bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ໔"), bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ໕")))
            if bstack11l1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ໖") in bstack11l1111ll1_opy_ or bstack11l1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ໗") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ໘")] = bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ໙"), bstack11l1111ll1_opy_.get(bstack11l1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ໚")))
            if bstack11l1lll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ໛") in bstack11l1111ll1_opy_:
                bstack11l1ll111l_opy_[bstack11l1lll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧໜ")] = bstack11l1111ll1_opy_[bstack11l1lll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨໝ")]
        except Exception as error:
            logger.error(bstack11l1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦໞ") +  str(error))
        return bstack11l1ll111l_opy_