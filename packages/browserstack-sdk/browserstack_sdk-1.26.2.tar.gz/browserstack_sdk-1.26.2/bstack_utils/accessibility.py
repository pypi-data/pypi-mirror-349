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
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll1111l1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llll11ll1_opy_ as bstack11lll11l1ll_opy_, EVENTS
from bstack_utils.bstack11111ll1_opy_ import bstack11111ll1_opy_
from bstack_utils.helper import bstack11l11ll11l_opy_, bstack111l1l1111_opy_, bstack1l11111l1_opy_, bstack11ll1lllll1_opy_, \
  bstack11lll11l1l1_opy_, bstack11l1ll11ll_opy_, get_host_info, bstack11ll1llllll_opy_, bstack11l1111l_opy_, bstack111l11111l_opy_, bstack11lll1l1l1l_opy_, bstack11lll111111_opy_, bstack1l1lllll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1lll111lll_opy_ import get_logger
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11l11111l_opy_ = bstack1ll1ll1ll11_opy_()
@bstack111l11111l_opy_(class_method=False)
def _11lll1ll111_opy_(driver, bstack1111lll1ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111l11_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫᖁ"): caps.get(bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᖂ"), None),
        bstack111l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᖃ"): bstack1111lll1ll_opy_.get(bstack111l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᖄ"), None),
        bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᖅ"): caps.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᖆ"), None),
        bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᖇ"): caps.get(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᖈ"), None)
    }
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᖉ") + str(error))
  return response
def on():
    if os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᖊ"), None) is None or os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᖋ")] == bstack111l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᖌ"):
        return False
    return True
def bstack1ll11l1l1l_opy_(config):
  return config.get(bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᖍ"), False) or any([p.get(bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᖎ"), False) == True for p in config.get(bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᖏ"), [])])
def bstack1l11l1ll1l_opy_(config, bstack1lll11lll1_opy_):
  try:
    bstack11lll1l11l1_opy_ = config.get(bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᖐ"), False)
    if int(bstack1lll11lll1_opy_) < len(config.get(bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᖑ"), [])) and config[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᖒ")][bstack1lll11lll1_opy_]:
      bstack11lll1lll1l_opy_ = config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᖓ")][bstack1lll11lll1_opy_].get(bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᖔ"), None)
    else:
      bstack11lll1lll1l_opy_ = config.get(bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᖕ"), None)
    if bstack11lll1lll1l_opy_ != None:
      bstack11lll1l11l1_opy_ = bstack11lll1lll1l_opy_
    bstack11llll11l1l_opy_ = os.getenv(bstack111l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖖ")) is not None and len(os.getenv(bstack111l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᖗ"))) > 0 and os.getenv(bstack111l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᖘ")) != bstack111l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᖙ")
    return bstack11lll1l11l1_opy_ and bstack11llll11l1l_opy_
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᖚ") + str(error))
  return False
def bstack1lllll1111_opy_(test_tags):
  bstack1ll1ll111l1_opy_ = os.getenv(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᖛ"))
  if bstack1ll1ll111l1_opy_ is None:
    return True
  bstack1ll1ll111l1_opy_ = json.loads(bstack1ll1ll111l1_opy_)
  try:
    include_tags = bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᖜ")] if bstack111l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᖝ") in bstack1ll1ll111l1_opy_ and isinstance(bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᖞ")], list) else []
    exclude_tags = bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᖟ")] if bstack111l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᖠ") in bstack1ll1ll111l1_opy_ and isinstance(bstack1ll1ll111l1_opy_[bstack111l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᖡ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᖢ") + str(error))
  return False
def bstack11lll111lll_opy_(config, bstack11lll111ll1_opy_, bstack11lll1ll11l_opy_, bstack11lll1l1l11_opy_):
  bstack11lll1l1111_opy_ = bstack11ll1lllll1_opy_(config)
  bstack11lll1111ll_opy_ = bstack11lll11l1l1_opy_(config)
  if bstack11lll1l1111_opy_ is None or bstack11lll1111ll_opy_ is None:
    logger.error(bstack111l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᖣ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖤ"), bstack111l11_opy_ (u"ࠫࢀࢃࠧᖥ")))
    data = {
        bstack111l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᖦ"): config[bstack111l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᖧ")],
        bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᖨ"): config.get(bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᖩ"), os.path.basename(os.getcwd())),
        bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᖪ"): bstack11l11ll11l_opy_(),
        bstack111l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᖫ"): config.get(bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᖬ"), bstack111l11_opy_ (u"ࠬ࠭ᖭ")),
        bstack111l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᖮ"): {
            bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᖯ"): bstack11lll111ll1_opy_,
            bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᖰ"): bstack11lll1ll11l_opy_,
            bstack111l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖱ"): __version__,
            bstack111l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᖲ"): bstack111l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᖳ"),
            bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᖴ"): bstack111l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᖵ"),
            bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᖶ"): bstack11lll1l1l11_opy_
        },
        bstack111l11_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᖷ"): settings,
        bstack111l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪᖸ"): bstack11ll1llllll_opy_(),
        bstack111l11_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪᖹ"): bstack11l1ll11ll_opy_(),
        bstack111l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭ᖺ"): get_host_info(),
        bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᖻ"): bstack1l11111l1_opy_(config)
    }
    headers = {
        bstack111l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᖼ"): bstack111l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᖽ"),
    }
    config = {
        bstack111l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᖾ"): (bstack11lll1l1111_opy_, bstack11lll1111ll_opy_),
        bstack111l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᖿ"): headers
    }
    response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᗀ"), bstack11lll11l1ll_opy_ + bstack111l11_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫᗁ"), data, config)
    bstack11ll1llll11_opy_ = response.json()
    if bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᗂ")]:
      parsed = json.loads(os.getenv(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᗃ"), bstack111l11_opy_ (u"ࠧࡼࡿࠪᗄ")))
      parsed[bstack111l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗅ")] = bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᗆ")][bstack111l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗇ")]
      os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᗈ")] = json.dumps(parsed)
      bstack11111ll1_opy_.bstack1l11ll111l_opy_(bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠬࡪࡡࡵࡣࠪᗉ")][bstack111l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᗊ")])
      bstack11111ll1_opy_.bstack11lll1lll11_opy_(bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᗋ")][bstack111l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᗌ")])
      bstack11111ll1_opy_.store()
      return bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᗍ")][bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᗎ")], bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᗏ")][bstack111l11_opy_ (u"ࠬ࡯ࡤࠨᗐ")]
    else:
      logger.error(bstack111l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧᗑ") + bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗒ")])
      if bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗓ")] == bstack111l11_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫᗔ"):
        for bstack11lll11ll11_opy_ in bstack11ll1llll11_opy_[bstack111l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᗕ")]:
          logger.error(bstack11lll11ll11_opy_[bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗖ")])
      return None, None
  except Exception as error:
    logger.error(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨᗗ") +  str(error))
    return None, None
def bstack11llll1111l_opy_():
  if os.getenv(bstack111l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᗘ")) is None:
    return {
        bstack111l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᗙ"): bstack111l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᗚ"),
        bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᗛ"): bstack111l11_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩᗜ")
    }
  data = {bstack111l11_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬᗝ"): bstack11l11ll11l_opy_()}
  headers = {
      bstack111l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᗞ"): bstack111l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧᗟ") + os.getenv(bstack111l11_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧᗠ")),
      bstack111l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᗡ"): bstack111l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᗢ")
  }
  response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠪࡔ࡚࡚ࠧᗣ"), bstack11lll11l1ll_opy_ + bstack111l11_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ᗤ"), data, { bstack111l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᗥ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢᗦ") + bstack111l1l1111_opy_().isoformat() + bstack111l11_opy_ (u"࡛ࠧࠩᗧ"))
      return {bstack111l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᗨ"): bstack111l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᗩ"), bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗪ"): bstack111l11_opy_ (u"ࠫࠬᗫ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣᗬ") + str(error))
    return {
        bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᗭ"): bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᗮ"),
        bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗯ"): str(error)
    }
def bstack11lll11llll_opy_(bstack11lll1ll1l1_opy_):
    return re.match(bstack111l11_opy_ (u"ࡴࠪࡢࡡࡪࠫࠩ࡞࠱ࡠࡩ࠱ࠩࡀࠦࠪᗰ"), bstack11lll1ll1l1_opy_.strip()) is not None
def bstack1l1111lll1_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11lll1lllll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll1lllll_opy_ = desired_capabilities
        else:
          bstack11lll1lllll_opy_ = {}
        bstack11lll1l1ll1_opy_ = (bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᗱ"), bstack111l11_opy_ (u"ࠫࠬᗲ")).lower() or caps.get(bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᗳ"), bstack111l11_opy_ (u"࠭ࠧᗴ")).lower())
        if bstack11lll1l1ll1_opy_ == bstack111l11_opy_ (u"ࠧࡪࡱࡶࠫᗵ"):
            return True
        if bstack11lll1l1ll1_opy_ == bstack111l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᗶ"):
            bstack11llll111l1_opy_ = str(float(caps.get(bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᗷ")) or bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗸ"), {}).get(bstack111l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᗹ"),bstack111l11_opy_ (u"ࠬ࠭ᗺ"))))
            if bstack11lll1l1ll1_opy_ == bstack111l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᗻ") and int(bstack11llll111l1_opy_.split(bstack111l11_opy_ (u"ࠧ࠯ࠩᗼ"))[0]) < float(bstack11llll11lll_opy_):
                logger.warning(str(bstack11lll111l1l_opy_))
                return False
            return True
        bstack1ll1l111111_opy_ = caps.get(bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗽ"), {}).get(bstack111l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᗾ"), caps.get(bstack111l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᗿ"), bstack111l11_opy_ (u"ࠫࠬᘀ")))
        if bstack1ll1l111111_opy_:
            logger.warning(bstack111l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᘁ"))
            return False
        browser = caps.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᘂ"), bstack111l11_opy_ (u"ࠧࠨᘃ")).lower() or bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᘄ"), bstack111l11_opy_ (u"ࠩࠪᘅ")).lower()
        if browser != bstack111l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᘆ"):
            logger.warning(bstack111l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᘇ"))
            return False
        browser_version = caps.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘈ")) or caps.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᘉ")) or bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘊ")) or bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘋ"), {}).get(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᘌ")) or bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘍ"), {}).get(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᘎ"))
        bstack1ll1l1llll1_opy_ = bstack11lll1111l1_opy_.bstack1ll1l11ll11_opy_
        bstack11lll1l111l_opy_ = False
        if config is not None:
          bstack11lll1l111l_opy_ = bstack111l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᘏ") in config and str(config[bstack111l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᘐ")]).lower() != bstack111l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᘑ")
        if os.environ.get(bstack111l11_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᘒ"), bstack111l11_opy_ (u"ࠩࠪᘓ")).lower() == bstack111l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᘔ") or bstack11lll1l111l_opy_:
          bstack1ll1l1llll1_opy_ = bstack11lll1111l1_opy_.bstack1ll1l1l1111_opy_
        if browser_version and browser_version != bstack111l11_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᘕ") and int(browser_version.split(bstack111l11_opy_ (u"ࠬ࠴ࠧᘖ"))[0]) <= bstack1ll1l1llll1_opy_:
          logger.warning(bstack1lll1l11111_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼ࡯࡬ࡲࡤࡧ࠱࠲ࡻࡢࡷࡺࡶࡰࡰࡴࡷࡩࡩࡥࡣࡩࡴࡲࡱࡪࡥࡶࡦࡴࡶ࡭ࡴࡴࡽ࠯ࠩᘗ"))
          return False
        if not options:
          bstack1ll11l1llll_opy_ = caps.get(bstack111l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᘘ")) or bstack11lll1lllll_opy_.get(bstack111l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘙ"), {})
          if bstack111l11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᘚ") in bstack1ll11l1llll_opy_.get(bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᘛ"), []):
              logger.warning(bstack111l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᘜ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᘝ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llll11l111_opy_ = config.get(bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘞ"), {})
    bstack1llll11l111_opy_[bstack111l11_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᘟ")] = os.getenv(bstack111l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘠ"))
    bstack11lll11l111_opy_ = json.loads(os.getenv(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᘡ"), bstack111l11_opy_ (u"ࠪࡿࢂ࠭ᘢ"))).get(bstack111l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘣ"))
    if not config[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᘤ")].get(bstack111l11_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᘥ")):
      if bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘦ") in caps:
        caps[bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘧ")][bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘨ")] = bstack1llll11l111_opy_
        caps[bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘩ")][bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᘪ")][bstack111l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘫ")] = bstack11lll11l111_opy_
      else:
        caps[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘬ")] = bstack1llll11l111_opy_
        caps[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘭ")][bstack111l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᘮ")] = bstack11lll11l111_opy_
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥᘯ") +  str(error))
def bstack1111ll1l_opy_(driver, bstack11ll1llll1l_opy_):
  try:
    setattr(driver, bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᘰ"), True)
    session = driver.session_id
    if session:
      bstack11lll11111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll11111l_opy_ = False
      bstack11lll11111l_opy_ = url.scheme in [bstack111l11_opy_ (u"ࠦ࡭ࡺࡴࡱࠤᘱ"), bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᘲ")]
      if bstack11lll11111l_opy_:
        if bstack11ll1llll1l_opy_:
          logger.info(bstack111l11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨᘳ"))
      return bstack11ll1llll1l_opy_
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᘴ") + str(e))
    return False
def bstack1l1ll1ll1_opy_(driver, name, path):
  try:
    bstack1ll1l1ll1l1_opy_ = {
        bstack111l11_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᘵ"): threading.current_thread().current_test_uuid,
        bstack111l11_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᘶ"): os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᘷ"), bstack111l11_opy_ (u"ࠫࠬᘸ")),
        bstack111l11_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩᘹ"): os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᘺ"), bstack111l11_opy_ (u"ࠧࠨᘻ"))
    }
    bstack1ll1l11ll1l_opy_ = bstack11l11111l_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack11l11ll1ll_opy_.value)
    logger.debug(bstack111l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᘼ"))
    try:
      if (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᘽ"), None) and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᘾ"), None)):
        scripts = {bstack111l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᘿ"): bstack11111ll1_opy_.perform_scan}
        bstack11lll11ll1l_opy_ = json.loads(scripts[bstack111l11_opy_ (u"ࠧࡹࡣࡢࡰࠥᙀ")].replace(bstack111l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᙁ"), bstack111l11_opy_ (u"ࠢࠣᙂ")))
        bstack11lll11ll1l_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᙃ")][bstack111l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩᙄ")] = None
        scripts[bstack111l11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᙅ")] = bstack111l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᙆ") + json.dumps(bstack11lll11ll1l_opy_)
        bstack11111ll1_opy_.bstack1l11ll111l_opy_(scripts)
        bstack11111ll1_opy_.store()
        logger.debug(driver.execute_script(bstack11111ll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11111ll1_opy_.perform_scan, {bstack111l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᙇ"): name}))
      bstack11l11111l_opy_.end(EVENTS.bstack11l11ll1ll_opy_.value, bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᙈ"), bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᙉ"), True, None)
    except Exception as error:
      bstack11l11111l_opy_.end(EVENTS.bstack11l11ll1ll_opy_.value, bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᙊ"), bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᙋ"), False, str(error))
    bstack1ll1l11ll1l_opy_ = bstack11l11111l_opy_.bstack11llll11111_opy_(EVENTS.bstack1ll1l11l1ll_opy_.value)
    bstack11l11111l_opy_.mark(bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᙌ"))
    try:
      if (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᙍ"), None) and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᙎ"), None)):
        scripts = {bstack111l11_opy_ (u"࠭ࡳࡤࡣࡱࠫᙏ"): bstack11111ll1_opy_.perform_scan}
        bstack11lll11ll1l_opy_ = json.loads(scripts[bstack111l11_opy_ (u"ࠢࡴࡥࡤࡲࠧᙐ")].replace(bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᙑ"), bstack111l11_opy_ (u"ࠤࠥᙒ")))
        bstack11lll11ll1l_opy_[bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᙓ")][bstack111l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᙔ")] = None
        scripts[bstack111l11_opy_ (u"ࠧࡹࡣࡢࡰࠥᙕ")] = bstack111l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᙖ") + json.dumps(bstack11lll11ll1l_opy_)
        bstack11111ll1_opy_.bstack1l11ll111l_opy_(scripts)
        bstack11111ll1_opy_.store()
        logger.debug(driver.execute_script(bstack11111ll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11111ll1_opy_.bstack11llll11l11_opy_, bstack1ll1l1ll1l1_opy_))
      bstack11l11111l_opy_.end(bstack1ll1l11ll1l_opy_, bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᙗ"), bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᙘ"),True, None)
    except Exception as error:
      bstack11l11111l_opy_.end(bstack1ll1l11ll1l_opy_, bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᙙ"), bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᙚ"),False, str(error))
    logger.info(bstack111l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᙛ"))
  except Exception as bstack1ll11llll11_opy_:
    logger.error(bstack111l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᙜ") + str(path) + bstack111l11_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᙝ") + str(bstack1ll11llll11_opy_))
def bstack11lll1l11ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack111l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᙞ")) and str(caps.get(bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᙟ"))).lower() == bstack111l11_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᙠ"):
        bstack11llll111l1_opy_ = caps.get(bstack111l11_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᙡ")) or caps.get(bstack111l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᙢ"))
        if bstack11llll111l1_opy_ and int(str(bstack11llll111l1_opy_)) < bstack11llll11lll_opy_:
            return False
    return True
def bstack1l1l111ll_opy_(config):
  if bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙣ") in config:
        return config[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᙤ")]
  for platform in config.get(bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᙥ"), []):
      if bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᙦ") in platform:
          return platform[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᙧ")]
  return None
def bstack1lll1lllll_opy_(bstack1ll1l1l11l_opy_):
  try:
    browser_name = bstack1ll1l1l11l_opy_[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᙨ")]
    browser_version = bstack1ll1l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᙩ")]
    chrome_options = bstack1ll1l1l11l_opy_[bstack111l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙪ")]
    try:
        bstack11lll111l11_opy_ = int(browser_version.split(bstack111l11_opy_ (u"࠭࠮ࠨᙫ"))[0])
    except ValueError as e:
        logger.error(bstack111l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠦᙬ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack111l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ᙭")):
        logger.warning(bstack111l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ᙮"))
        return False
    if bstack11lll111l11_opy_ < bstack11lll1111l1_opy_.bstack1ll1l1l1111_opy_:
        logger.warning(bstack1lll1l11111_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹ࡮ࡸࡥࡴࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡹࡩࡷࡹࡩࡰࡰࠣࡿࡈࡕࡎࡔࡖࡄࡒ࡙࡙࠮ࡎࡋࡑࡍࡒ࡛ࡍࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖ࡙ࡕࡖࡏࡓࡖࡈࡈࡤࡉࡈࡓࡑࡐࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࢃࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠫᙯ"))
        return False
    if chrome_options and any(bstack111l11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᙰ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack111l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᙱ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡵࡱࡲࡲࡶࡹࠦࡦࡰࡴࠣࡰࡴࡩࡡ࡭ࠢࡆ࡬ࡷࡵ࡭ࡦ࠼ࠣࠦᙲ") + str(e))
    return False
def bstack11ll1111ll_opy_(bstack111l1l11l_opy_, config):
    try:
      bstack1ll1ll11111_opy_ = bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᙳ") in config and config[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᙴ")] == True
      bstack11lll1l111l_opy_ = bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᙵ") in config and str(config[bstack111l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᙶ")]).lower() != bstack111l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᙷ")
      if not (bstack1ll1ll11111_opy_ and (not bstack1l11111l1_opy_(config) or bstack11lll1l111l_opy_)):
        return bstack111l1l11l_opy_
      bstack11lll1l1lll_opy_ = bstack11111ll1_opy_.bstack11lll11lll1_opy_
      if bstack11lll1l1lll_opy_ is None:
        logger.debug(bstack111l11_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡧࠣࡒࡴࡴࡥࠣᙸ"))
        return bstack111l1l11l_opy_
      bstack11llll1l111_opy_ = int(str(bstack11lll111111_opy_()).split(bstack111l11_opy_ (u"࠭࠮ࠨᙹ"))[0])
      logger.debug(bstack111l11_opy_ (u"ࠢࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡨࡪࡺࡥࡤࡶࡨࡨ࠿ࠦࠢᙺ") + str(bstack11llll1l111_opy_) + bstack111l11_opy_ (u"ࠣࠤᙻ"))
      if bstack11llll1l111_opy_ == 3 and isinstance(bstack111l1l11l_opy_, dict) and bstack111l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᙼ") in bstack111l1l11l_opy_ and bstack11lll1l1lll_opy_ is not None:
        if bstack111l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᙽ") not in bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᙾ")]:
          bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᙿ")][bstack111l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ ")] = {}
        if bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬᚁ") in bstack11lll1l1lll_opy_:
          if bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᚂ") not in bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚃ")][bstack111l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚄ")]:
            bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚅ")][bstack111l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚆ")][bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᚇ")] = []
          for arg in bstack11lll1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬᚈ")]:
            if arg not in bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚉ")][bstack111l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚊ")][bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚋ")]:
              bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚌ")][bstack111l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚍ")][bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᚎ")].append(arg)
        if bstack111l11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᚏ") in bstack11lll1l1lll_opy_:
          if bstack111l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᚐ") not in bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚑ")][bstack111l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚒ")]:
            bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚓ")][bstack111l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚔ")][bstack111l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᚕ")] = []
          for ext in bstack11lll1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᚖ")]:
            if ext not in bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚗ")][bstack111l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚘ")][bstack111l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚙ")]:
              bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚚ")][bstack111l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᚛")][bstack111l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᚜")].append(ext)
        if bstack111l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᚝") in bstack11lll1l1lll_opy_:
          if bstack111l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᚞") not in bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᚟")][bstack111l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚠ")]:
            bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚡ")][bstack111l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚢ")][bstack111l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᚣ")] = {}
          bstack11lll1l1l1l_opy_(bstack111l1l11l_opy_[bstack111l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚤ")][bstack111l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚥ")][bstack111l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᚦ")],
                    bstack11lll1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᚧ")])
        os.environ[bstack111l11_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᚨ")] = bstack111l11_opy_ (u"ࠬࡺࡲࡶࡧࠪᚩ")
        return bstack111l1l11l_opy_
      else:
        chrome_options = None
        if isinstance(bstack111l1l11l_opy_, ChromeOptions):
          chrome_options = bstack111l1l11l_opy_
        elif isinstance(bstack111l1l11l_opy_, dict):
          for value in bstack111l1l11l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack111l1l11l_opy_, dict):
            bstack111l1l11l_opy_[bstack111l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚪ")] = chrome_options
          else:
            bstack111l1l11l_opy_ = chrome_options
        if bstack11lll1l1lll_opy_ is not None:
          if bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬᚫ") in bstack11lll1l1lll_opy_:
                bstack11lll1llll1_opy_ = chrome_options.arguments or []
                new_args = bstack11lll1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᚬ")]
                for arg in new_args:
                    if arg not in bstack11lll1llll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack111l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᚭ") in bstack11lll1l1lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack111l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚮ"), [])
                bstack11lll11l11l_opy_ = bstack11lll1l1lll_opy_[bstack111l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᚯ")]
                for extension in bstack11lll11l11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack111l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᚰ") in bstack11lll1l1lll_opy_:
                bstack11lll1ll1ll_opy_ = chrome_options.experimental_options.get(bstack111l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᚱ"), {})
                bstack11llll111ll_opy_ = bstack11lll1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᚲ")]
                bstack11lll1l1l1l_opy_(bstack11lll1ll1ll_opy_, bstack11llll111ll_opy_)
                chrome_options.add_experimental_option(bstack111l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᚳ"), bstack11lll1ll1ll_opy_)
        os.environ[bstack111l11_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᚴ")] = bstack111l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᚵ")
        return bstack111l1l11l_opy_
    except Exception as e:
      logger.error(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡨࡩ࡯࡮ࡨࠢࡱࡳࡳ࠳ࡂࡔࠢ࡬ࡲ࡫ࡸࡡࠡࡣ࠴࠵ࡾࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠤᚶ") + str(e))
      return bstack111l1l11l_opy_