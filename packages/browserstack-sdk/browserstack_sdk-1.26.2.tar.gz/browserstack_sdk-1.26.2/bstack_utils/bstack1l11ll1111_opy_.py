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
import datetime
import threading
from bstack_utils.helper import bstack11ll1llllll_opy_, bstack11l1ll11ll_opy_, get_host_info, bstack11l1lll1l1l_opy_, \
 bstack1l11111l1_opy_, bstack1l1lllll1l_opy_, bstack111l11111l_opy_, bstack11l11l1l111_opy_, bstack11l11ll11l_opy_
import bstack_utils.accessibility as bstack11lll1ll1_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1lllll1l1l_opy_
from bstack_utils.percy import bstack1111111ll_opy_
from bstack_utils.config import Config
bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack1111111ll_opy_()
@bstack111l11111l_opy_(class_method=False)
def bstack1111l11ll1l_opy_(bs_config, bstack1llllll1l1_opy_):
  try:
    data = {
        bstack111l11_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᾧ"): bstack111l11_opy_ (u"ࠬࡰࡳࡰࡰࠪᾨ"),
        bstack111l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᾩ"): bs_config.get(bstack111l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᾪ"), bstack111l11_opy_ (u"ࠨࠩᾫ")),
        bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᾬ"): bs_config.get(bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᾭ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᾮ"): bs_config.get(bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᾯ")),
        bstack111l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᾰ"): bs_config.get(bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᾱ"), bstack111l11_opy_ (u"ࠨࠩᾲ")),
        bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᾳ"): bstack11l11ll11l_opy_(),
        bstack111l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᾴ"): bstack11l1lll1l1l_opy_(bs_config),
        bstack111l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧ᾵"): get_host_info(),
        bstack111l11_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᾶ"): bstack11l1ll11ll_opy_(),
        bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᾷ"): os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭Ᾰ")),
        bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭Ᾱ"): os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᾺ"), False),
        bstack111l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬΆ"): bstack11ll1llllll_opy_(),
        bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᾼ"): bstack11111ll1l11_opy_(bs_config),
        bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩ᾽"): bstack11111ll1lll_opy_(bstack1llllll1l1_opy_),
        bstack111l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫι"): bstack11111ll111l_opy_(bs_config, bstack1llllll1l1_opy_.get(bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ᾿"), bstack111l11_opy_ (u"ࠨࠩ῀"))),
        bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ῁"): bstack1l11111l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦῂ").format(str(error)))
    return None
def bstack11111ll1lll_opy_(framework):
  return {
    bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫῃ"): framework.get(bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ῄ"), bstack111l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭῅")),
    bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪῆ"): framework.get(bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬῇ")),
    bstack111l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ὲ"): framework.get(bstack111l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨΈ")),
    bstack111l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭Ὴ"): bstack111l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬΉ"),
    bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ῌ"): framework.get(bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ῍"))
  }
def bstack11ll1lllll_opy_(bs_config, framework):
  bstack1l1lllllll_opy_ = False
  bstack11l11l1l1l_opy_ = False
  bstack11111ll1111_opy_ = False
  if bstack111l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ῎") in bs_config:
    bstack11111ll1111_opy_ = True
  elif bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭῏") in bs_config:
    bstack1l1lllllll_opy_ = True
  else:
    bstack11l11l1l1l_opy_ = True
  bstack1l1ll111l_opy_ = {
    bstack111l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪῐ"): bstack1lllll1l1l_opy_.bstack11111ll1l1l_opy_(bs_config, framework),
    bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫῑ"): bstack11lll1ll1_opy_.bstack1ll11l1l1l_opy_(bs_config),
    bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫῒ"): bs_config.get(bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬΐ"), False),
    bstack111l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ῔"): bstack11l11l1l1l_opy_,
    bstack111l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ῕"): bstack1l1lllllll_opy_,
    bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ῖ"): bstack11111ll1111_opy_
  }
  return bstack1l1ll111l_opy_
@bstack111l11111l_opy_(class_method=False)
def bstack11111ll1l11_opy_(bs_config):
  try:
    bstack11111ll11ll_opy_ = json.loads(os.getenv(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫῗ"), bstack111l11_opy_ (u"ࠫࢀࢃࠧῘ")))
    bstack11111ll11ll_opy_ = bstack11111ll1ll1_opy_(bs_config, bstack11111ll11ll_opy_)
    return {
        bstack111l11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧῙ"): bstack11111ll11ll_opy_
    }
  except Exception as error:
    logger.error(bstack111l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧῚ").format(str(error)))
    return {}
def bstack11111ll1ll1_opy_(bs_config, bstack11111ll11ll_opy_):
  if ((bstack111l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫΊ") in bs_config or not bstack1l11111l1_opy_(bs_config)) and bstack11lll1ll1_opy_.bstack1ll11l1l1l_opy_(bs_config)):
    bstack11111ll11ll_opy_[bstack111l11_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ῜")] = True
  return bstack11111ll11ll_opy_
def bstack1111l111l1l_opy_(array, bstack11111l1l1ll_opy_, bstack11111ll11l1_opy_):
  result = {}
  for o in array:
    key = o[bstack11111l1l1ll_opy_]
    result[key] = o[bstack11111ll11l1_opy_]
  return result
def bstack1111l11lll1_opy_(bstack1111l1l1_opy_=bstack111l11_opy_ (u"ࠩࠪ῝")):
  bstack11111l1ll1l_opy_ = bstack11lll1ll1_opy_.on()
  bstack11111l1llll_opy_ = bstack1lllll1l1l_opy_.on()
  bstack11111l1lll1_opy_ = percy.bstack1111l1lll_opy_()
  if bstack11111l1lll1_opy_ and not bstack11111l1llll_opy_ and not bstack11111l1ll1l_opy_:
    return bstack1111l1l1_opy_ not in [bstack111l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ῞"), bstack111l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ῟")]
  elif bstack11111l1ll1l_opy_ and not bstack11111l1llll_opy_:
    return bstack1111l1l1_opy_ not in [bstack111l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ῠ"), bstack111l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨῡ"), bstack111l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫῢ")]
  return bstack11111l1ll1l_opy_ or bstack11111l1llll_opy_ or bstack11111l1lll1_opy_
@bstack111l11111l_opy_(class_method=False)
def bstack11111lllll1_opy_(bstack1111l1l1_opy_, test=None):
  bstack11111l1ll11_opy_ = bstack11lll1ll1_opy_.on()
  if not bstack11111l1ll11_opy_ or bstack1111l1l1_opy_ not in [bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪΰ")] or test == None:
    return None
  return {
    bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩῤ"): bstack11111l1ll11_opy_ and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩῥ"), None) == True and bstack11lll1ll1_opy_.bstack1lllll1111_opy_(test[bstack111l11_opy_ (u"ࠫࡹࡧࡧࡴࠩῦ")])
  }
def bstack11111ll111l_opy_(bs_config, framework):
  bstack1l1lllllll_opy_ = False
  bstack11l11l1l1l_opy_ = False
  bstack11111ll1111_opy_ = False
  if bstack111l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩῧ") in bs_config:
    bstack11111ll1111_opy_ = True
  elif bstack111l11_opy_ (u"࠭ࡡࡱࡲࠪῨ") in bs_config:
    bstack1l1lllllll_opy_ = True
  else:
    bstack11l11l1l1l_opy_ = True
  bstack1l1ll111l_opy_ = {
    bstack111l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧῩ"): bstack1lllll1l1l_opy_.bstack11111ll1l1l_opy_(bs_config, framework),
    bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨῪ"): bstack11lll1ll1_opy_.bstack1l1l111ll_opy_(bs_config),
    bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨΎ"): bs_config.get(bstack111l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩῬ"), False),
    bstack111l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭῭"): bstack11l11l1l1l_opy_,
    bstack111l11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ΅"): bstack1l1lllllll_opy_,
    bstack111l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ`"): bstack11111ll1111_opy_
  }
  return bstack1l1ll111l_opy_