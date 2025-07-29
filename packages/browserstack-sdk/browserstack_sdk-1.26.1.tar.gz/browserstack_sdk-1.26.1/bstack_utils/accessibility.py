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
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll1lllll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lll11111l_opy_ as bstack11llll1111l_opy_, EVENTS
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.helper import bstack1lll11l11_opy_, bstack111l1lllll_opy_, bstack1lll11l1l_opy_, bstack11lll11l111_opy_, \
  bstack11lll111111_opy_, bstack11ll1lllll_opy_, get_host_info, bstack11lll1l1lll_opy_, bstack11lll1lll_opy_, bstack111l111111_opy_, bstack11lll1lll1l_opy_, bstack11llll11l11_opy_, bstack111l11lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l11l1lll_opy_ import get_logger
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11l1lll1l1_opy_ = bstack1lll1lll111_opy_()
@bstack111l111111_opy_(class_method=False)
def _11lll11ll11_opy_(driver, bstack1111l1ll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1lll_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧᕶ"): caps.get(bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᕷ"), None),
        bstack11l1lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᕸ"): bstack1111l1ll1l_opy_.get(bstack11l1lll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᕹ"), None),
        bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᕺ"): caps.get(bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᕻ"), None),
        bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᕼ"): caps.get(bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᕽ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᕾ") + str(error))
  return response
def on():
    if os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕿ"), None) is None or os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᖀ")] == bstack11l1lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᖁ"):
        return False
    return True
def bstack1llll1lll_opy_(config):
  return config.get(bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᖂ"), False) or any([p.get(bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᖃ"), False) == True for p in config.get(bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᖄ"), [])])
def bstack1l111l11ll_opy_(config, bstack1llll11l1_opy_):
  try:
    bstack11llll111ll_opy_ = config.get(bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᖅ"), False)
    if int(bstack1llll11l1_opy_) < len(config.get(bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᖆ"), [])) and config[bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᖇ")][bstack1llll11l1_opy_]:
      bstack11lll111l1l_opy_ = config[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᖈ")][bstack1llll11l1_opy_].get(bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᖉ"), None)
    else:
      bstack11lll111l1l_opy_ = config.get(bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᖊ"), None)
    if bstack11lll111l1l_opy_ != None:
      bstack11llll111ll_opy_ = bstack11lll111l1l_opy_
    bstack11lll1l11l1_opy_ = os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᖋ")) is not None and len(os.getenv(bstack11l1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᖌ"))) > 0 and os.getenv(bstack11l1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᖍ")) != bstack11l1lll_opy_ (u"ࠩࡱࡹࡱࡲࠧᖎ")
    return bstack11llll111ll_opy_ and bstack11lll1l11l1_opy_
  except Exception as error:
    logger.debug(bstack11l1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᖏ") + str(error))
  return False
def bstack1ll1l1l1ll_opy_(test_tags):
  bstack1ll1l111111_opy_ = os.getenv(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᖐ"))
  if bstack1ll1l111111_opy_ is None:
    return True
  bstack1ll1l111111_opy_ = json.loads(bstack1ll1l111111_opy_)
  try:
    include_tags = bstack1ll1l111111_opy_[bstack11l1lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᖑ")] if bstack11l1lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᖒ") in bstack1ll1l111111_opy_ and isinstance(bstack1ll1l111111_opy_[bstack11l1lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᖓ")], list) else []
    exclude_tags = bstack1ll1l111111_opy_[bstack11l1lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᖔ")] if bstack11l1lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᖕ") in bstack1ll1l111111_opy_ and isinstance(bstack1ll1l111111_opy_[bstack11l1lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᖖ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᖗ") + str(error))
  return False
def bstack11llll11lll_opy_(config, bstack11lll1ll11l_opy_, bstack11lll1l1l1l_opy_, bstack11llll11111_opy_):
  bstack11lll1l111l_opy_ = bstack11lll11l111_opy_(config)
  bstack11ll1llllll_opy_ = bstack11lll111111_opy_(config)
  if bstack11lll1l111l_opy_ is None or bstack11ll1llllll_opy_ is None:
    logger.error(bstack11l1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᖘ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᖙ"), bstack11l1lll_opy_ (u"ࠧࡼࡿࠪᖚ")))
    data = {
        bstack11l1lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᖛ"): config[bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᖜ")],
        bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᖝ"): config.get(bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᖞ"), os.path.basename(os.getcwd())),
        bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨᖟ"): bstack1lll11l11_opy_(),
        bstack11l1lll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᖠ"): config.get(bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᖡ"), bstack11l1lll_opy_ (u"ࠨࠩᖢ")),
        bstack11l1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᖣ"): {
            bstack11l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪᖤ"): bstack11lll1ll11l_opy_,
            bstack11l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᖥ"): bstack11lll1l1l1l_opy_,
            bstack11l1lll_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᖦ"): __version__,
            bstack11l1lll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᖧ"): bstack11l1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᖨ"),
            bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᖩ"): bstack11l1lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᖪ"),
            bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᖫ"): bstack11llll11111_opy_
        },
        bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᖬ"): settings,
        bstack11l1lll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ᖭ"): bstack11lll1l1lll_opy_(),
        bstack11l1lll_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭ᖮ"): bstack11ll1lllll_opy_(),
        bstack11l1lll_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩᖯ"): get_host_info(),
        bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᖰ"): bstack1lll11l1l_opy_(config)
    }
    headers = {
        bstack11l1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᖱ"): bstack11l1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᖲ"),
    }
    config = {
        bstack11l1lll_opy_ (u"ࠫࡦࡻࡴࡩࠩᖳ"): (bstack11lll1l111l_opy_, bstack11ll1llllll_opy_),
        bstack11l1lll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᖴ"): headers
    }
    response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"࠭ࡐࡐࡕࡗࠫᖵ"), bstack11llll1111l_opy_ + bstack11l1lll_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧᖶ"), data, config)
    bstack11lll11ll1l_opy_ = response.json()
    if bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᖷ")]:
      parsed = json.loads(os.getenv(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᖸ"), bstack11l1lll_opy_ (u"ࠪࡿࢂ࠭ᖹ")))
      parsed[bstack11l1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᖺ")] = bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠬࡪࡡࡵࡣࠪᖻ")][bstack11l1lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᖼ")]
      os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᖽ")] = json.dumps(parsed)
      bstack1lll11ll11_opy_.bstack11llll11_opy_(bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖾ")][bstack11l1lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᖿ")])
      bstack1lll11ll11_opy_.bstack11lll1ll1ll_opy_(bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠪࡨࡦࡺࡡࠨᗀ")][bstack11l1lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᗁ")])
      bstack1lll11ll11_opy_.store()
      return bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠬࡪࡡࡵࡣࠪᗂ")][bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᗃ")], bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡣࡷࡥࠬᗄ")][bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫᗅ")]
    else:
      logger.error(bstack11l1lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪᗆ") + bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗇ")])
      if bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗈ")] == bstack11l1lll_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧᗉ"):
        for bstack11llll111l1_opy_ in bstack11lll11ll1l_opy_[bstack11l1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᗊ")]:
          logger.error(bstack11llll111l1_opy_[bstack11l1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗋ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤᗌ") +  str(error))
    return None, None
def bstack11llll1l111_opy_():
  if os.getenv(bstack11l1lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᗍ")) is None:
    return {
        bstack11l1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᗎ"): bstack11l1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᗏ"),
        bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗐ"): bstack11l1lll_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬᗑ")
    }
  data = {bstack11l1lll_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨᗒ"): bstack1lll11l11_opy_()}
  headers = {
      bstack11l1lll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᗓ"): bstack11l1lll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪᗔ") + os.getenv(bstack11l1lll_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣᗕ")),
      bstack11l1lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᗖ"): bstack11l1lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᗗ")
  }
  response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"࠭ࡐࡖࡖࠪᗘ"), bstack11llll1111l_opy_ + bstack11l1lll_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩᗙ"), data, { bstack11l1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᗚ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1lll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥᗛ") + bstack111l1lllll_opy_().isoformat() + bstack11l1lll_opy_ (u"ࠪ࡞ࠬᗜ"))
      return {bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᗝ"): bstack11l1lll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᗞ"), bstack11l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᗟ"): bstack11l1lll_opy_ (u"ࠧࠨᗠ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦᗡ") + str(error))
    return {
        bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᗢ"): bstack11l1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᗣ"),
        bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗤ"): str(error)
    }
def bstack11lll11l1l1_opy_(bstack11ll1lllll1_opy_):
    return re.match(bstack11l1lll_opy_ (u"ࡷ࠭࡞࡝ࡦ࠮ࠬࡡ࠴࡜ࡥ࠭ࠬࡃࠩ࠭ᗥ"), bstack11ll1lllll1_opy_.strip()) is not None
def bstack11lll111_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11llll11ll1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llll11ll1_opy_ = desired_capabilities
        else:
          bstack11llll11ll1_opy_ = {}
        bstack11lll1lll11_opy_ = (bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᗦ"), bstack11l1lll_opy_ (u"ࠧࠨᗧ")).lower() or caps.get(bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᗨ"), bstack11l1lll_opy_ (u"ࠩࠪᗩ")).lower())
        if bstack11lll1lll11_opy_ == bstack11l1lll_opy_ (u"ࠪ࡭ࡴࡹࠧᗪ"):
            return True
        if bstack11lll1lll11_opy_ == bstack11l1lll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᗫ"):
            bstack11lll11l1ll_opy_ = str(float(caps.get(bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᗬ")) or bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗭ"), {}).get(bstack11l1lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᗮ"),bstack11l1lll_opy_ (u"ࠨࠩᗯ"))))
            if bstack11lll1lll11_opy_ == bstack11l1lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᗰ") and int(bstack11lll11l1ll_opy_.split(bstack11l1lll_opy_ (u"ࠪ࠲ࠬᗱ"))[0]) < float(bstack11lll11llll_opy_):
                logger.warning(str(bstack11lll1ll1l1_opy_))
                return False
            return True
        bstack1ll11lllll1_opy_ = caps.get(bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗲ"), {}).get(bstack11l1lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᗳ"), caps.get(bstack11l1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᗴ"), bstack11l1lll_opy_ (u"ࠧࠨᗵ")))
        if bstack1ll11lllll1_opy_:
            logger.warning(bstack11l1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᗶ"))
            return False
        browser = caps.get(bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᗷ"), bstack11l1lll_opy_ (u"ࠪࠫᗸ")).lower() or bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᗹ"), bstack11l1lll_opy_ (u"ࠬ࠭ᗺ")).lower()
        if browser != bstack11l1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᗻ"):
            logger.warning(bstack11l1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᗼ"))
            return False
        browser_version = caps.get(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗽ")) or caps.get(bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᗾ")) or bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗿ")) or bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘀ"), {}).get(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘁ")) or bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘂ"), {}).get(bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᘃ"))
        bstack1ll1l1111l1_opy_ = bstack11lll1lllll_opy_.bstack1ll1l1llll1_opy_
        bstack11lll11l11l_opy_ = False
        if config is not None:
          bstack11lll11l11l_opy_ = bstack11l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᘄ") in config and str(config[bstack11l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᘅ")]).lower() != bstack11l1lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᘆ")
        if os.environ.get(bstack11l1lll_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᘇ"), bstack11l1lll_opy_ (u"ࠬ࠭ᘈ")).lower() == bstack11l1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫᘉ") or bstack11lll11l11l_opy_:
          bstack1ll1l1111l1_opy_ = bstack11lll1lllll_opy_.bstack1ll1l1l1lll_opy_
        if browser_version and browser_version != bstack11l1lll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᘊ") and int(browser_version.split(bstack11l1lll_opy_ (u"ࠨ࠰ࠪᘋ"))[0]) <= bstack1ll1l1111l1_opy_:
          logger.warning(bstack1lll11ll111_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࡲ࡯࡮ࡠࡣ࠴࠵ࡾࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡹࡩࡷࡹࡩࡰࡰࢀ࠲ࠬᘌ"))
          return False
        if not options:
          bstack1ll11l1lll1_opy_ = caps.get(bstack11l1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᘍ")) or bstack11llll11ll1_opy_.get(bstack11l1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘎ"), {})
          if bstack11l1lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᘏ") in bstack1ll11l1lll1_opy_.get(bstack11l1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫᘐ"), []):
              logger.warning(bstack11l1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᘑ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᘒ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1lll1ll1_opy_ = config.get(bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘓ"), {})
    bstack1ll1lll1ll1_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᘔ")] = os.getenv(bstack11l1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘕ"))
    bstack11llll11l1l_opy_ = json.loads(os.getenv(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᘖ"), bstack11l1lll_opy_ (u"࠭ࡻࡾࠩᘗ"))).get(bstack11l1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘘ"))
    if not config[bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᘙ")].get(bstack11l1lll_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣᘚ")):
      if bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘛ") in caps:
        caps[bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘜ")][bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘝ")] = bstack1ll1lll1ll1_opy_
        caps[bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘞ")][bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᘟ")][bstack11l1lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᘠ")] = bstack11llll11l1l_opy_
      else:
        caps[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᘡ")] = bstack1ll1lll1ll1_opy_
        caps[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘢ")][bstack11l1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘣ")] = bstack11llll11l1l_opy_
  except Exception as error:
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨᘤ") +  str(error))
def bstack1lll1ll11l_opy_(driver, bstack11lll11lll1_opy_):
  try:
    setattr(driver, bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᘥ"), True)
    session = driver.session_id
    if session:
      bstack11lll1111l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1111l1_opy_ = False
      bstack11lll1111l1_opy_ = url.scheme in [bstack11l1lll_opy_ (u"ࠢࡩࡶࡷࡴࠧᘦ"), bstack11l1lll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᘧ")]
      if bstack11lll1111l1_opy_:
        if bstack11lll11lll1_opy_:
          logger.info(bstack11l1lll_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤᘨ"))
      return bstack11lll11lll1_opy_
  except Exception as e:
    logger.error(bstack11l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘩ") + str(e))
    return False
def bstack11l1l1ll1_opy_(driver, name, path):
  try:
    bstack1ll1l1111ll_opy_ = {
        bstack11l1lll_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᘪ"): threading.current_thread().current_test_uuid,
        bstack11l1lll_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᘫ"): os.environ.get(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᘬ"), bstack11l1lll_opy_ (u"ࠧࠨᘭ")),
        bstack11l1lll_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᘮ"): os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᘯ"), bstack11l1lll_opy_ (u"ࠪࠫᘰ"))
    }
    bstack1ll1l11llll_opy_ = bstack11l1lll1l1_opy_.bstack1ll1l11l1ll_opy_(EVENTS.bstack11111ll1_opy_.value)
    logger.debug(bstack11l1lll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᘱ"))
    try:
      if (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᘲ"), None) and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᘳ"), None)):
        scripts = {bstack11l1lll_opy_ (u"ࠧࡴࡥࡤࡲࠬᘴ"): bstack1lll11ll11_opy_.perform_scan}
        bstack11lll1l1l11_opy_ = json.loads(scripts[bstack11l1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᘵ")].replace(bstack11l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘶ"), bstack11l1lll_opy_ (u"ࠥࠦᘷ")))
        bstack11lll1l1l11_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᘸ")][bstack11l1lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᘹ")] = None
        scripts[bstack11l1lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘺ")] = bstack11l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘻ") + json.dumps(bstack11lll1l1l11_opy_)
        bstack1lll11ll11_opy_.bstack11llll11_opy_(scripts)
        bstack1lll11ll11_opy_.store()
        logger.debug(driver.execute_script(bstack1lll11ll11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1lll11ll11_opy_.perform_scan, {bstack11l1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᘼ"): name}))
      bstack11l1lll1l1_opy_.end(EVENTS.bstack11111ll1_opy_.value, bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘽ"), bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘾ"), True, None)
    except Exception as error:
      bstack11l1lll1l1_opy_.end(EVENTS.bstack11111ll1_opy_.value, bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘿ"), bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᙀ"), False, str(error))
    bstack1ll1l11llll_opy_ = bstack11l1lll1l1_opy_.bstack11lll1l1111_opy_(EVENTS.bstack1ll1l11lll1_opy_.value)
    bstack11l1lll1l1_opy_.mark(bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᙁ"))
    try:
      if (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᙂ"), None) and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᙃ"), None)):
        scripts = {bstack11l1lll_opy_ (u"ࠩࡶࡧࡦࡴࠧᙄ"): bstack1lll11ll11_opy_.perform_scan}
        bstack11lll1l1l11_opy_ = json.loads(scripts[bstack11l1lll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᙅ")].replace(bstack11l1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᙆ"), bstack11l1lll_opy_ (u"ࠧࠨᙇ")))
        bstack11lll1l1l11_opy_[bstack11l1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᙈ")][bstack11l1lll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᙉ")] = None
        scripts[bstack11l1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᙊ")] = bstack11l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᙋ") + json.dumps(bstack11lll1l1l11_opy_)
        bstack1lll11ll11_opy_.bstack11llll11_opy_(scripts)
        bstack1lll11ll11_opy_.store()
        logger.debug(driver.execute_script(bstack1lll11ll11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1lll11ll11_opy_.bstack11lll1111ll_opy_, bstack1ll1l1111ll_opy_))
      bstack11l1lll1l1_opy_.end(bstack1ll1l11llll_opy_, bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᙌ"), bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᙍ"),True, None)
    except Exception as error:
      bstack11l1lll1l1_opy_.end(bstack1ll1l11llll_opy_, bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᙎ"), bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᙏ"),False, str(error))
    logger.info(bstack11l1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᙐ"))
  except Exception as bstack1ll11ll1l1l_opy_:
    logger.error(bstack11l1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᙑ") + str(path) + bstack11l1lll_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᙒ") + str(bstack1ll11ll1l1l_opy_))
def bstack11lll111l11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l1lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᙓ")) and str(caps.get(bstack11l1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᙔ"))).lower() == bstack11l1lll_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᙕ"):
        bstack11lll11l1ll_opy_ = caps.get(bstack11l1lll_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᙖ")) or caps.get(bstack11l1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᙗ"))
        if bstack11lll11l1ll_opy_ and int(str(bstack11lll11l1ll_opy_)) < bstack11lll11llll_opy_:
            return False
    return True
def bstack1l1llll1ll_opy_(config):
  if bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᙘ") in config:
        return config[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᙙ")]
  for platform in config.get(bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᙚ"), []):
      if bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᙛ") in platform:
          return platform[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙜ")]
  return None
def bstack11l1l1llll_opy_(bstack1lllllll11_opy_):
  try:
    browser_name = bstack1lllllll11_opy_[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᙝ")]
    browser_version = bstack1lllllll11_opy_[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᙞ")]
    chrome_options = bstack1lllllll11_opy_[bstack11l1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩᙟ")]
    try:
        bstack11lll1ll111_opy_ = int(browser_version.split(bstack11l1lll_opy_ (u"ࠩ࠱ࠫᙠ"))[0])
    except ValueError as e:
        logger.error(bstack11l1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡲࡻ࡫ࡲࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠢᙡ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11l1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᙢ")):
        logger.warning(bstack11l1lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᙣ"))
        return False
    if bstack11lll1ll111_opy_ < bstack11lll1lllll_opy_.bstack1ll1l1l1lll_opy_:
        logger.warning(bstack1lll11ll111_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡪࡴࡨࡷࠥࡉࡨࡳࡱࡰࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡻࡄࡑࡑࡗ࡙ࡇࡎࡕࡕ࠱ࡑࡎࡔࡉࡎࡗࡐࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡕࡑࡒࡒࡖ࡙ࡋࡄࡠࡅࡋࡖࡔࡓࡅࡠࡘࡈࡖࡘࡏࡏࡏࡿࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠧᙤ"))
        return False
    if chrome_options and any(bstack11l1lll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᙥ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11l1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᙦ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11l1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢᙧ") + str(e))
    return False
def bstack11l11l1l1l_opy_(bstack1l11lll11l_opy_, config):
    try:
      bstack1ll11l1ll11_opy_ = bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᙨ") in config and config[bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᙩ")] == True
      bstack11lll11l11l_opy_ = bstack11l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᙪ") in config and str(config[bstack11l1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᙫ")]).lower() != bstack11l1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᙬ")
      if not (bstack1ll11l1ll11_opy_ and (not bstack1lll11l1l_opy_(config) or bstack11lll11l11l_opy_)):
        return bstack1l11lll11l_opy_
      bstack11llll1l1l1_opy_ = bstack1lll11ll11_opy_.bstack11llll1l11l_opy_
      if bstack11llll1l1l1_opy_ is None:
        logger.debug(bstack11l1lll_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨࠦ᙭"))
        return bstack1l11lll11l_opy_
      bstack11lll1llll1_opy_ = int(str(bstack11llll11l11_opy_()).split(bstack11l1lll_opy_ (u"ࠩ࠱ࠫ᙮"))[0])
      logger.debug(bstack11l1lll_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥᙯ") + str(bstack11lll1llll1_opy_) + bstack11l1lll_opy_ (u"ࠦࠧᙰ"))
      if bstack11lll1llll1_opy_ == 3 and isinstance(bstack1l11lll11l_opy_, dict) and bstack11l1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᙱ") in bstack1l11lll11l_opy_ and bstack11llll1l1l1_opy_ is not None:
        if bstack11l1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᙲ") not in bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᙳ")]:
          bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᙴ")][bstack11l1lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᙵ")] = {}
        if bstack11l1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᙶ") in bstack11llll1l1l1_opy_:
          if bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᙷ") not in bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᙸ")][bstack11l1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᙹ")]:
            bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᙺ")][bstack11l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙻ")][bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᙼ")] = []
          for arg in bstack11llll1l1l1_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᙽ")]:
            if arg not in bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᙾ")][bstack11l1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᙿ")][bstack11l1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫ ")]:
              bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚁ")][bstack11l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚂ")][bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᚃ")].append(arg)
        if bstack11l1lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚄ") in bstack11llll1l1l1_opy_:
          if bstack11l1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᚅ") not in bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᚆ")][bstack11l1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚇ")]:
            bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚈ")][bstack11l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚉ")][bstack11l1lll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᚊ")] = []
          for ext in bstack11llll1l1l1_opy_[bstack11l1lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚋ")]:
            if ext not in bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚌ")][bstack11l1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚍ")][bstack11l1lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᚎ")]:
              bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚏ")][bstack11l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚐ")][bstack11l1lll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᚑ")].append(ext)
        if bstack11l1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᚒ") in bstack11llll1l1l1_opy_:
          if bstack11l1lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᚓ") not in bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᚔ")][bstack11l1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚕ")]:
            bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚖ")][bstack11l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚗ")][bstack11l1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᚘ")] = {}
          bstack11lll1lll1l_opy_(bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᚙ")][bstack11l1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚚ")][bstack11l1lll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᚛")],
                    bstack11llll1l1l1_opy_[bstack11l1lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᚜")])
        os.environ[bstack11l1lll_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᚝")] = bstack11l1lll_opy_ (u"ࠨࡶࡵࡹࡪ࠭᚞")
        return bstack1l11lll11l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l11lll11l_opy_, ChromeOptions):
          chrome_options = bstack1l11lll11l_opy_
        elif isinstance(bstack1l11lll11l_opy_, dict):
          for value in bstack1l11lll11l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l11lll11l_opy_, dict):
            bstack1l11lll11l_opy_[bstack11l1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᚟")] = chrome_options
          else:
            bstack1l11lll11l_opy_ = chrome_options
        if bstack11llll1l1l1_opy_ is not None:
          if bstack11l1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚠ") in bstack11llll1l1l1_opy_:
                bstack11lll1l1ll1_opy_ = chrome_options.arguments or []
                new_args = bstack11llll1l1l1_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᚡ")]
                for arg in new_args:
                    if arg not in bstack11lll1l1ll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack11l1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᚢ") in bstack11llll1l1l1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11l1lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᚣ"), [])
                bstack11lll111ll1_opy_ = bstack11llll1l1l1_opy_[bstack11l1lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᚤ")]
                for extension in bstack11lll111ll1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11l1lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᚥ") in bstack11llll1l1l1_opy_:
                bstack11lll1l11ll_opy_ = chrome_options.experimental_options.get(bstack11l1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᚦ"), {})
                bstack11lll111lll_opy_ = bstack11llll1l1l1_opy_[bstack11l1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᚧ")]
                bstack11lll1lll1l_opy_(bstack11lll1l11ll_opy_, bstack11lll111lll_opy_)
                chrome_options.add_experimental_option(bstack11l1lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᚨ"), bstack11lll1l11ll_opy_)
        os.environ[bstack11l1lll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᚩ")] = bstack11l1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫᚪ")
        return bstack1l11lll11l_opy_
    except Exception as e:
      logger.error(bstack11l1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᚫ") + str(e))
      return bstack1l11lll11l_opy_