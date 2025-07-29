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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1lllll11_opy_, bstack1l11111l1_opy_, bstack111l11lll_opy_, bstack1l11l111l1_opy_, \
    bstack11l1l1ll11l_opy_
from bstack_utils.measure import measure
def bstack1l111l1ll1_opy_(bstack1111ll1l1ll_opy_):
    for driver in bstack1111ll1l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack11ll1ll1_opy_(driver, status, reason=bstack11l1lll_opy_ (u"ࠪࠫḬ")):
    bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
    if bstack11ll1llll1_opy_.bstack1111ll11l1_opy_():
        return
    bstack11lll1l111_opy_ = bstack1l111llll_opy_(bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧḭ"), bstack11l1lll_opy_ (u"ࠬ࠭Ḯ"), status, reason, bstack11l1lll_opy_ (u"࠭ࠧḯ"), bstack11l1lll_opy_ (u"ࠧࠨḰ"))
    driver.execute_script(bstack11lll1l111_opy_)
@measure(event_name=EVENTS.bstack1l111l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack1l1111l1l_opy_(page, status, reason=bstack11l1lll_opy_ (u"ࠨࠩḱ")):
    try:
        if page is None:
            return
        bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
        if bstack11ll1llll1_opy_.bstack1111ll11l1_opy_():
            return
        bstack11lll1l111_opy_ = bstack1l111llll_opy_(bstack11l1lll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬḲ"), bstack11l1lll_opy_ (u"ࠪࠫḳ"), status, reason, bstack11l1lll_opy_ (u"ࠫࠬḴ"), bstack11l1lll_opy_ (u"ࠬ࠭ḵ"))
        page.evaluate(bstack11l1lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢḶ"), bstack11lll1l111_opy_)
    except Exception as e:
        print(bstack11l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧḷ"), e)
def bstack1l111llll_opy_(type, name, status, reason, bstack1llll111_opy_, bstack11ll11l1_opy_):
    bstack1l1l111lll_opy_ = {
        bstack11l1lll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨḸ"): type,
        bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬḹ"): {}
    }
    if type == bstack11l1lll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬḺ"):
        bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧḻ")][bstack11l1lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫḼ")] = bstack1llll111_opy_
        bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩḽ")][bstack11l1lll_opy_ (u"ࠧࡥࡣࡷࡥࠬḾ")] = json.dumps(str(bstack11ll11l1_opy_))
    if type == bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩḿ"):
        bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬṀ")][bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨṁ")] = name
    if type == bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧṂ"):
        bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨṃ")][bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ṅ")] = status
        if status == bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧṅ") and str(reason) != bstack11l1lll_opy_ (u"ࠣࠤṆ"):
            bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬṇ")][bstack11l1lll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪṈ")] = json.dumps(str(reason))
    bstack11l111llll_opy_ = bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩṉ").format(json.dumps(bstack1l1l111lll_opy_))
    return bstack11l111llll_opy_
def bstack1l11l111ll_opy_(url, config, logger, bstack1l1l1lll1l_opy_=False):
    hostname = bstack1l11111l1_opy_(url)
    is_private = bstack1l11l111l1_opy_(hostname)
    try:
        if is_private or bstack1l1l1lll1l_opy_:
            file_path = bstack11l1lllll11_opy_(bstack11l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬṊ"), bstack11l1lll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬṋ"), logger)
            if os.environ.get(bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬṌ")) and eval(
                    os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ṍ"))):
                return
            if (bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ṏ") in config and not config[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧṏ")]):
                os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩṐ")] = str(True)
                bstack1111ll1l1l1_opy_ = {bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧṑ"): hostname}
                bstack11l1l1ll11l_opy_(bstack11l1lll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬṒ"), bstack11l1lll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬṓ"), bstack1111ll1l1l1_opy_, logger)
    except Exception as e:
        pass
def bstack111ll1l11_opy_(caps, bstack1111ll1ll11_opy_):
    if bstack11l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩṔ") in caps:
        caps[bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪṕ")][bstack11l1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩṖ")] = True
        if bstack1111ll1ll11_opy_:
            caps[bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬṗ")][bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧṘ")] = bstack1111ll1ll11_opy_
    else:
        caps[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫṙ")] = True
        if bstack1111ll1ll11_opy_:
            caps[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨṚ")] = bstack1111ll1ll11_opy_
def bstack111l111111l_opy_(bstack111l11l11l_opy_):
    bstack1111ll1l11l_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬṛ"), bstack11l1lll_opy_ (u"ࠩࠪṜ"))
    if bstack1111ll1l11l_opy_ == bstack11l1lll_opy_ (u"ࠪࠫṝ") or bstack1111ll1l11l_opy_ == bstack11l1lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬṞ"):
        threading.current_thread().testStatus = bstack111l11l11l_opy_
    else:
        if bstack111l11l11l_opy_ == bstack11l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬṟ"):
            threading.current_thread().testStatus = bstack111l11l11l_opy_