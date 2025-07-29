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
import re
from bstack_utils.bstack111l1111_opy_ import bstack111l111111l_opy_
def bstack111l11111l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1lll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᷡ")):
        return bstack11l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᷢ")
    elif fixture_name.startswith(bstack11l1lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᷣ")):
        return bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᷤ")
    elif fixture_name.startswith(bstack11l1lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᷥ")):
        return bstack11l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᷦ")
    elif fixture_name.startswith(bstack11l1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᷧ")):
        return bstack11l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᷨ")
def bstack111l1111l11_opy_(fixture_name):
    return bool(re.match(bstack11l1lll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᷩ"), fixture_name))
def bstack111l111lll1_opy_(fixture_name):
    return bool(re.match(bstack11l1lll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᷪ"), fixture_name))
def bstack111l111ll1l_opy_(fixture_name):
    return bool(re.match(bstack11l1lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᷫ"), fixture_name))
def bstack111l111l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᷬ")):
        return bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᷭ"), bstack11l1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᷮ")
    elif fixture_name.startswith(bstack11l1lll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᷯ")):
        return bstack11l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᷰ"), bstack11l1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᷱ")
    elif fixture_name.startswith(bstack11l1lll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᷲ")):
        return bstack11l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᷳ"), bstack11l1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᷴ")
    elif fixture_name.startswith(bstack11l1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᷵")):
        return bstack11l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ᷶"), bstack11l1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍ᷷ࠩ")
    return None, None
def bstack111l1111l1l_opy_(hook_name):
    if hook_name in [bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ᷸࠭"), bstack11l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ᷹ࠪ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l111l1l1_opy_(hook_name):
    if hook_name in [bstack11l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰ᷺ࠪ"), bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ᷻")]:
        return bstack11l1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ᷼")
    elif hook_name in [bstack11l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨ᷽ࠫ"), bstack11l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ᷾")]:
        return bstack11l1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏ᷿ࠫ")
    elif hook_name in [bstack11l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬḀ"), bstack11l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫḁ")]:
        return bstack11l1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧḂ")
    elif hook_name in [bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ḃ"), bstack11l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ḅ")]:
        return bstack11l1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩḅ")
    return hook_name
def bstack111l1111ll1_opy_(node, scenario):
    if hasattr(node, bstack11l1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩḆ")):
        parts = node.nodeid.rsplit(bstack11l1lll_opy_ (u"ࠣ࡝ࠥḇ"))
        params = parts[-1]
        return bstack11l1lll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤḈ").format(scenario.name, params)
    return scenario.name
def bstack111l1111lll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1lll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬḉ")):
            examples = list(node.callspec.params[bstack11l1lll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪḊ")].values())
        return examples
    except:
        return []
def bstack111l111l111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l111ll11_opy_(report):
    try:
        status = bstack11l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬḋ")
        if report.passed or (report.failed and hasattr(report, bstack11l1lll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣḌ"))):
            status = bstack11l1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧḍ")
        elif report.skipped:
            status = bstack11l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩḎ")
        bstack111l111111l_opy_(status)
    except:
        pass
def bstack1llll11111_opy_(status):
    try:
        bstack111l11111ll_opy_ = bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩḏ")
        if status == bstack11l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪḐ"):
            bstack111l11111ll_opy_ = bstack11l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫḑ")
        elif status == bstack11l1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ḓ"):
            bstack111l11111ll_opy_ = bstack11l1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧḓ")
        bstack111l111111l_opy_(bstack111l11111ll_opy_)
    except:
        pass
def bstack111l111l1ll_opy_(item=None, report=None, summary=None, extra=None):
    return