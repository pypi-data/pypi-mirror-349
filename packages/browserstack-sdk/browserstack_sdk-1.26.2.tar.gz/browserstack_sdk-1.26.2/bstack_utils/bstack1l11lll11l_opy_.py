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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11l11l_opy_, bstack1l1111ll1_opy_, bstack1l1lllll1l_opy_, bstack11ll11ll1_opy_, \
    bstack11l111lll11_opy_
from bstack_utils.measure import measure
def bstack1l11l11l_opy_(bstack1111ll11l1l_opy_):
    for driver in bstack1111ll11l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11111l111_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack11ll11l11_opy_(driver, status, reason=bstack111l11_opy_ (u"ࠧࠨḷ")):
    bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
    if bstack111l111ll_opy_.bstack1111llll11_opy_():
        return
    bstack111l11l1_opy_ = bstack1l11l111ll_opy_(bstack111l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫḸ"), bstack111l11_opy_ (u"ࠩࠪḹ"), status, reason, bstack111l11_opy_ (u"ࠪࠫḺ"), bstack111l11_opy_ (u"ࠫࠬḻ"))
    driver.execute_script(bstack111l11l1_opy_)
@measure(event_name=EVENTS.bstack11111l111_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack11ll11ll_opy_(page, status, reason=bstack111l11_opy_ (u"ࠬ࠭Ḽ")):
    try:
        if page is None:
            return
        bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
        if bstack111l111ll_opy_.bstack1111llll11_opy_():
            return
        bstack111l11l1_opy_ = bstack1l11l111ll_opy_(bstack111l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩḽ"), bstack111l11_opy_ (u"ࠧࠨḾ"), status, reason, bstack111l11_opy_ (u"ࠨࠩḿ"), bstack111l11_opy_ (u"ࠩࠪṀ"))
        page.evaluate(bstack111l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦṁ"), bstack111l11l1_opy_)
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤṂ"), e)
def bstack1l11l111ll_opy_(type, name, status, reason, bstack11l1l1l111_opy_, bstack1l11ll1lll_opy_):
    bstack1l1ll111ll_opy_ = {
        bstack111l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬṃ"): type,
        bstack111l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩṄ"): {}
    }
    if type == bstack111l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩṅ"):
        bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫṆ")][bstack111l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨṇ")] = bstack11l1l1l111_opy_
        bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ṉ")][bstack111l11_opy_ (u"ࠫࡩࡧࡴࡢࠩṉ")] = json.dumps(str(bstack1l11ll1lll_opy_))
    if type == bstack111l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ṋ"):
        bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩṋ")][bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṌ")] = name
    if type == bstack111l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫṍ"):
        bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬṎ")][bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪṏ")] = status
        if status == bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫṐ") and str(reason) != bstack111l11_opy_ (u"ࠧࠨṑ"):
            bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩṒ")][bstack111l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧṓ")] = json.dumps(str(reason))
    bstack111lll11_opy_ = bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭Ṕ").format(json.dumps(bstack1l1ll111ll_opy_))
    return bstack111lll11_opy_
def bstack11111ll1l_opy_(url, config, logger, bstack1ll1111ll1_opy_=False):
    hostname = bstack1l1111ll1_opy_(url)
    is_private = bstack11ll11ll1_opy_(hostname)
    try:
        if is_private or bstack1ll1111ll1_opy_:
            file_path = bstack11l1l11l11l_opy_(bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩṕ"), bstack111l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩṖ"), logger)
            if os.environ.get(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩṗ")) and eval(
                    os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪṘ"))):
                return
            if (bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪṙ") in config and not config[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫṚ")]):
                os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ṛ")] = str(True)
                bstack1111ll11lll_opy_ = {bstack111l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫṜ"): hostname}
                bstack11l111lll11_opy_(bstack111l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩṝ"), bstack111l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩṞ"), bstack1111ll11lll_opy_, logger)
    except Exception as e:
        pass
def bstack1l1ll1l111_opy_(caps, bstack1111ll11ll1_opy_):
    if bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ṟ") in caps:
        caps[bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧṠ")][bstack111l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ṡ")] = True
        if bstack1111ll11ll1_opy_:
            caps[bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩṢ")][bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫṣ")] = bstack1111ll11ll1_opy_
    else:
        caps[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨṤ")] = True
        if bstack1111ll11ll1_opy_:
            caps[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬṥ")] = bstack1111ll11ll1_opy_
def bstack1111lllll1l_opy_(bstack111ll11ll1_opy_):
    bstack1111ll1l111_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩṦ"), bstack111l11_opy_ (u"࠭ࠧṧ"))
    if bstack1111ll1l111_opy_ == bstack111l11_opy_ (u"ࠧࠨṨ") or bstack1111ll1l111_opy_ == bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩṩ"):
        threading.current_thread().testStatus = bstack111ll11ll1_opy_
    else:
        if bstack111ll11ll1_opy_ == bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩṪ"):
            threading.current_thread().testStatus = bstack111ll11ll1_opy_