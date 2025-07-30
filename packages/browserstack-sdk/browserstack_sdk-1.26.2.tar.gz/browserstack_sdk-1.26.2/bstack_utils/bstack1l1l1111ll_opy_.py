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
from bstack_utils.bstack1l11lll11l_opy_ import bstack1111lllll1l_opy_
def bstack1111lllllll_opy_(fixture_name):
    if fixture_name.startswith(bstack111l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᷬ")):
        return bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᷭ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᷮ")):
        return bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᷯ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᷰ")):
        return bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᷱ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᷲ")):
        return bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᷳ")
def bstack111l1111ll1_opy_(fixture_name):
    return bool(re.match(bstack111l11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᷴ"), fixture_name))
def bstack1111llllll1_opy_(fixture_name):
    return bool(re.match(bstack111l11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ᷵"), fixture_name))
def bstack111l111l1l1_opy_(fixture_name):
    return bool(re.match(bstack111l11_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ᷶"), fixture_name))
def bstack111l111111l_opy_(fixture_name):
    if fixture_name.startswith(bstack111l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᷷")):
        return bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ᷸"), bstack111l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ᷹࠭")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦ᷺ࠩ")):
        return bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ᷻"), bstack111l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ᷼")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧ᷽ࠪ")):
        return bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ᷾"), bstack111l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋ᷿ࠫ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫḀ")):
        return bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫḁ"), bstack111l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭Ḃ")
    return None, None
def bstack111l1111l11_opy_(hook_name):
    if hook_name in [bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪḃ"), bstack111l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧḄ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l11111l1_opy_(hook_name):
    if hook_name in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧḅ"), bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ḇ")]:
        return bstack111l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ḇ")
    elif hook_name in [bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨḈ"), bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨḉ")]:
        return bstack111l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨḊ")
    elif hook_name in [bstack111l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩḋ"), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨḌ")]:
        return bstack111l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫḍ")
    elif hook_name in [bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪḎ"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪḏ")]:
        return bstack111l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭Ḑ")
    return hook_name
def bstack111l11111ll_opy_(node, scenario):
    if hasattr(node, bstack111l11_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ḑ")):
        parts = node.nodeid.rsplit(bstack111l11_opy_ (u"ࠧࡡࠢḒ"))
        params = parts[-1]
        return bstack111l11_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨḓ").format(scenario.name, params)
    return scenario.name
def bstack111l1111111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩḔ")):
            examples = list(node.callspec.params[bstack111l11_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧḕ")].values())
        return examples
    except:
        return []
def bstack111l1111l1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l111l11l_opy_(report):
    try:
        status = bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩḖ")
        if report.passed or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧḗ"))):
            status = bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫḘ")
        elif report.skipped:
            status = bstack111l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ḙ")
        bstack1111lllll1l_opy_(status)
    except:
        pass
def bstack1l1ll1111l_opy_(status):
    try:
        bstack111l111l111_opy_ = bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ḛ")
        if status == bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧḛ"):
            bstack111l111l111_opy_ = bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨḜ")
        elif status == bstack111l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪḝ"):
            bstack111l111l111_opy_ = bstack111l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫḞ")
        bstack1111lllll1l_opy_(bstack111l111l111_opy_)
    except:
        pass
def bstack111l1111lll_opy_(item=None, report=None, summary=None, extra=None):
    return