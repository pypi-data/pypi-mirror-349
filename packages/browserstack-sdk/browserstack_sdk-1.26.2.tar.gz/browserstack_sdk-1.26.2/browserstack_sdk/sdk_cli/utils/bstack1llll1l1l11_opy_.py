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
import re
from typing import List, Dict, Any
from bstack_utils.bstack1lll111lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lllll1l111_opy_:
    bstack111l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡻࡴࡪ࡮࡬ࡸࡾࠦ࡭ࡦࡶ࡫ࡳࡩࡹࠠࡵࡱࠣࡷࡪࡺࠠࡢࡰࡧࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࠣࡱࡪࡺࡡࡥࡣࡷࡥ࠳ࠐࠠࠡࠢࠣࡍࡹࠦ࡭ࡢ࡫ࡱࡸࡦ࡯࡮ࡴࠢࡷࡻࡴࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡳࡪࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࡇࡤࡧ࡭ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡧࡱࡸࡷࡿࠠࡪࡵࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡤࡨࠤࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡤࠡࡣࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢ࠻ࠢࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡻࡧ࡬ࡶࡧࡶࠦ࠿࡛ࠦ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡤ࡫ࠥࡼࡡ࡭ࡷࡨࡷࡢࠐࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠨࠢࠣᕍ")
    _11lllllllll_opy_: Dict[str, Dict[str, Any]] = {}
    _11llllllll1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack11111l1ll_opy_: str, key_value: str, bstack1l11111111l_opy_: bool = False) -> None:
        if not bstack11111l1ll_opy_ or not key_value or bstack11111l1ll_opy_.strip() == bstack111l11_opy_ (u"ࠣࠤᕎ") or key_value.strip() == bstack111l11_opy_ (u"ࠤࠥᕏ"):
            logger.error(bstack111l11_opy_ (u"ࠥ࡯ࡪࡿ࡟࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢ࡮ࡩࡾࡥࡶࡢ࡮ࡸࡩࠥࡳࡵࡴࡶࠣࡦࡪࠦ࡮ࡰࡰ࠰ࡲࡺࡲ࡬ࠡࡣࡱࡨࠥࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠣᕐ"))
        values: List[str] = bstack1lllll1l111_opy_.bstack11lllllll11_opy_(key_value)
        bstack11lllllll1l_opy_ = {bstack111l11_opy_ (u"ࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣᕑ"): bstack111l11_opy_ (u"ࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨᕒ"), bstack111l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᕓ"): values}
        bstack1l111111111_opy_ = bstack1lllll1l111_opy_._11llllllll1_opy_ if bstack1l11111111l_opy_ else bstack1lllll1l111_opy_._11lllllllll_opy_
        if bstack11111l1ll_opy_ in bstack1l111111111_opy_:
            bstack1l1111111ll_opy_ = bstack1l111111111_opy_[bstack11111l1ll_opy_]
            bstack1l111111l11_opy_ = bstack1l1111111ll_opy_.get(bstack111l11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᕔ"), [])
            for val in values:
                if val not in bstack1l111111l11_opy_:
                    bstack1l111111l11_opy_.append(val)
            bstack1l1111111ll_opy_[bstack111l11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᕕ")] = bstack1l111111l11_opy_
        else:
            bstack1l111111111_opy_[bstack11111l1ll_opy_] = bstack11lllllll1l_opy_
    @staticmethod
    def bstack1l1111lll11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lllll1l111_opy_._11lllllllll_opy_
    @staticmethod
    def bstack1l1111111l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lllll1l111_opy_._11llllllll1_opy_
    @staticmethod
    def bstack11lllllll11_opy_(bstack11llllll1ll_opy_: str) -> List[str]:
        bstack111l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡱ࡮࡬ࡸࡸࠦࡴࡩࡧࠣ࡭ࡳࡶࡵࡵࠢࡶࡸࡷ࡯࡮ࡨࠢࡥࡽࠥࡩ࡯࡮࡯ࡤࡷࠥࡽࡨࡪ࡮ࡨࠤࡷ࡫ࡳࡱࡧࡦࡸ࡮ࡴࡧࠡࡦࡲࡹࡧࡲࡥ࠮ࡳࡸࡳࡹ࡫ࡤࠡࡵࡸࡦࡸࡺࡲࡪࡰࡪࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡪࡾࡡ࡮ࡲ࡯ࡩ࠿ࠦࠧࡢ࠮ࠣࠦࡧ࠲ࡣࠣ࠮ࠣࡨࠬࠦ࠭࠿ࠢ࡞ࠫࡦ࠭ࠬࠡࠩࡥ࠰ࡨ࠭ࠬࠡࠩࡧࠫࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᕖ")
        pattern = re.compile(bstack111l11_opy_ (u"ࡵࠫࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨࡼࠩ࡝ࡡ࠰ࡢ࠱ࠩࠨᕗ"))
        result = []
        for match in pattern.finditer(bstack11llllll1ll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack111l11_opy_ (u"࡚ࠦࡺࡩ࡭࡫ࡷࡽࠥࡩ࡬ࡢࡵࡶࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤ࡮ࡴࡳࡵࡣࡱࡸ࡮ࡧࡴࡦࡦࠥᕘ"))