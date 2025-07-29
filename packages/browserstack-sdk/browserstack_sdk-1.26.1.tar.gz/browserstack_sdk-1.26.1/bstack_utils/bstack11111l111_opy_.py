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
import datetime
import threading
from bstack_utils.helper import bstack11lll1l1lll_opy_, bstack11ll1lllll_opy_, get_host_info, bstack11l1ll11l1l_opy_, \
 bstack1lll11l1l_opy_, bstack111l11lll_opy_, bstack111l111111_opy_, bstack11l1l1lll11_opy_, bstack1lll11l11_opy_
import bstack_utils.accessibility as bstack1l11111lll_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l111l11l_opy_
from bstack_utils.percy import bstack1l11l1ll11_opy_
from bstack_utils.config import Config
bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l11l1ll11_opy_()
@bstack111l111111_opy_(class_method=False)
def bstack11111llllll_opy_(bs_config, bstack1lll1ll111_opy_):
  try:
    data = {
        bstack11l1lll_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧᾜ"): bstack11l1lll_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ᾝ"),
        bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨᾞ"): bs_config.get(bstack11l1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᾟ"), bstack11l1lll_opy_ (u"ࠫࠬᾠ")),
        bstack11l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᾡ"): bs_config.get(bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᾢ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᾣ"): bs_config.get(bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᾤ")),
        bstack11l1lll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᾥ"): bs_config.get(bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᾦ"), bstack11l1lll_opy_ (u"ࠫࠬᾧ")),
        bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾨ"): bstack1lll11l11_opy_(),
        bstack11l1lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᾩ"): bstack11l1ll11l1l_opy_(bs_config),
        bstack11l1lll_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪᾪ"): get_host_info(),
        bstack11l1lll_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩᾫ"): bstack11ll1lllll_opy_(),
        bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᾬ"): os.environ.get(bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᾭ")),
        bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩᾮ"): os.environ.get(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪᾯ"), False),
        bstack11l1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨᾰ"): bstack11lll1l1lll_opy_(),
        bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᾱ"): bstack11111ll11l1_opy_(bs_config),
        bstack11l1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬᾲ"): bstack11111lll111_opy_(bstack1lll1ll111_opy_),
        bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᾳ"): bstack11111l1llll_opy_(bs_config, bstack1lll1ll111_opy_.get(bstack11l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᾴ"), bstack11l1lll_opy_ (u"ࠫࠬ᾵"))),
        bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᾶ"): bstack1lll11l1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᾷ").format(str(error)))
    return None
def bstack11111lll111_opy_(framework):
  return {
    bstack11l1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᾸ"): framework.get(bstack11l1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᾹ"), bstack11l1lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᾺ")),
    bstack11l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ά"): framework.get(bstack11l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᾼ")),
    bstack11l1lll_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ᾽"): framework.get(bstack11l1lll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫι")),
    bstack11l1lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ᾿"): bstack11l1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ῀"),
    bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ῁"): framework.get(bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪῂ"))
  }
def bstack11l1l1l1_opy_(bs_config, framework):
  bstack11llllll_opy_ = False
  bstack1l1l11l111_opy_ = False
  bstack11111ll1l1l_opy_ = False
  if bstack11l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨῃ") in bs_config:
    bstack11111ll1l1l_opy_ = True
  elif bstack11l1lll_opy_ (u"ࠬࡧࡰࡱࠩῄ") in bs_config:
    bstack11llllll_opy_ = True
  else:
    bstack1l1l11l111_opy_ = True
  bstack1ll1111l11_opy_ = {
    bstack11l1lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭῅"): bstack11l111l11l_opy_.bstack11111ll1l11_opy_(bs_config, framework),
    bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧῆ"): bstack1l11111lll_opy_.bstack1llll1lll_opy_(bs_config),
    bstack11l1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧῇ"): bs_config.get(bstack11l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨῈ"), False),
    bstack11l1lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬΈ"): bstack1l1l11l111_opy_,
    bstack11l1lll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪῊ"): bstack11llllll_opy_,
    bstack11l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩΉ"): bstack11111ll1l1l_opy_
  }
  return bstack1ll1111l11_opy_
@bstack111l111111_opy_(class_method=False)
def bstack11111ll11l1_opy_(bs_config):
  try:
    bstack11111ll11ll_opy_ = json.loads(os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧῌ"), bstack11l1lll_opy_ (u"ࠧࡼࡿࠪ῍")))
    bstack11111ll11ll_opy_ = bstack11111lll11l_opy_(bs_config, bstack11111ll11ll_opy_)
    return {
        bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ῎"): bstack11111ll11ll_opy_
    }
  except Exception as error:
    logger.error(bstack11l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ῏").format(str(error)))
    return {}
def bstack11111lll11l_opy_(bs_config, bstack11111ll11ll_opy_):
  if ((bstack11l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧῐ") in bs_config or not bstack1lll11l1l_opy_(bs_config)) and bstack1l11111lll_opy_.bstack1llll1lll_opy_(bs_config)):
    bstack11111ll11ll_opy_[bstack11l1lll_opy_ (u"ࠦ࡮ࡴࡣ࡭ࡷࡧࡩࡊࡴࡣࡰࡦࡨࡨࡊࡾࡴࡦࡰࡶ࡭ࡴࡴࠢῑ")] = True
  return bstack11111ll11ll_opy_
def bstack11111lllll1_opy_(array, bstack11111ll1lll_opy_, bstack11111ll111l_opy_):
  result = {}
  for o in array:
    key = o[bstack11111ll1lll_opy_]
    result[key] = o[bstack11111ll111l_opy_]
  return result
def bstack11111llll11_opy_(bstack1lll1ll1l_opy_=bstack11l1lll_opy_ (u"ࠬ࠭ῒ")):
  bstack11111lll1l1_opy_ = bstack1l11111lll_opy_.on()
  bstack11111lll1ll_opy_ = bstack11l111l11l_opy_.on()
  bstack11111ll1ll1_opy_ = percy.bstack1lll1l11ll_opy_()
  if bstack11111ll1ll1_opy_ and not bstack11111lll1ll_opy_ and not bstack11111lll1l1_opy_:
    return bstack1lll1ll1l_opy_ not in [bstack11l1lll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪΐ"), bstack11l1lll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ῔")]
  elif bstack11111lll1l1_opy_ and not bstack11111lll1ll_opy_:
    return bstack1lll1ll1l_opy_ not in [bstack11l1lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ῕"), bstack11l1lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫῖ"), bstack11l1lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧῗ")]
  return bstack11111lll1l1_opy_ or bstack11111lll1ll_opy_ or bstack11111ll1ll1_opy_
@bstack111l111111_opy_(class_method=False)
def bstack1111l1111ll_opy_(bstack1lll1ll1l_opy_, test=None):
  bstack11111ll1111_opy_ = bstack1l11111lll_opy_.on()
  if not bstack11111ll1111_opy_ or bstack1lll1ll1l_opy_ not in [bstack11l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ῐ")] or test == None:
    return None
  return {
    bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬῙ"): bstack11111ll1111_opy_ and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬῚ"), None) == True and bstack1l11111lll_opy_.bstack1ll1l1l1ll_opy_(test[bstack11l1lll_opy_ (u"ࠧࡵࡣࡪࡷࠬΊ")])
  }
def bstack11111l1llll_opy_(bs_config, framework):
  bstack11llllll_opy_ = False
  bstack1l1l11l111_opy_ = False
  bstack11111ll1l1l_opy_ = False
  if bstack11l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ῜") in bs_config:
    bstack11111ll1l1l_opy_ = True
  elif bstack11l1lll_opy_ (u"ࠩࡤࡴࡵ࠭῝") in bs_config:
    bstack11llllll_opy_ = True
  else:
    bstack1l1l11l111_opy_ = True
  bstack1ll1111l11_opy_ = {
    bstack11l1lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ῞"): bstack11l111l11l_opy_.bstack11111ll1l11_opy_(bs_config, framework),
    bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ῟"): bstack1l11111lll_opy_.bstack1l1llll1ll_opy_(bs_config),
    bstack11l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫῠ"): bs_config.get(bstack11l1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬῡ"), False),
    bstack11l1lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩῢ"): bstack1l1l11l111_opy_,
    bstack11l1lll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧΰ"): bstack11llllll_opy_,
    bstack11l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ῤ"): bstack11111ll1l1l_opy_
  }
  return bstack1ll1111l11_opy_