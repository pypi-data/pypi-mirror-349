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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1l1l11lll1_opy_ import bstack11ll111l1_opy_
from browserstack_sdk.bstack111ll111l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack11111l11l_opy_():
  global CONFIG
  headers = {
        bstack11l1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll111l1_opy_(CONFIG, bstack1lll1l1ll_opy_)
  try:
    response = requests.get(bstack1lll1l1ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll11lll1_opy_ = response.json()[bstack11l1lll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1l111ll1_opy_.format(response.json()))
      return bstack1ll11lll1_opy_
    else:
      logger.debug(bstack111l1ll1l_opy_.format(bstack11l1lll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111l1ll1l_opy_.format(e))
def bstack11ll1l11_opy_(hub_url):
  global CONFIG
  url = bstack11l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l1lll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll111l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1llll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l11ll1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1ll1lll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack1llll1ll11_opy_():
  try:
    global bstack1ll1llll11_opy_
    bstack1ll11lll1_opy_ = bstack11111l11l_opy_()
    bstack11lllllll_opy_ = []
    results = []
    for bstack1llll11lll_opy_ in bstack1ll11lll1_opy_:
      bstack11lllllll_opy_.append(bstack111l1l1l_opy_(target=bstack11ll1l11_opy_,args=(bstack1llll11lll_opy_,)))
    for t in bstack11lllllll_opy_:
      t.start()
    for t in bstack11lllllll_opy_:
      results.append(t.join())
    bstack1lllll1l1_opy_ = {}
    for item in results:
      hub_url = item[bstack11l1lll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l1lll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1lllll1l1_opy_[hub_url] = latency
    bstack1111ll11_opy_ = min(bstack1lllll1l1_opy_, key= lambda x: bstack1lllll1l1_opy_[x])
    bstack1ll1llll11_opy_ = bstack1111ll11_opy_
    logger.debug(bstack1l11l1l1ll_opy_.format(bstack1111ll11_opy_))
  except Exception as e:
    logger.debug(bstack11lll1l1_opy_.format(e))
from browserstack_sdk.bstack1ll1ll1l11_opy_ import *
from browserstack_sdk.bstack11ll1l1l1_opy_ import *
from browserstack_sdk.bstack111l1ll1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1l11l1lll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack111l11l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack1l1ll11111_opy_():
    global bstack1ll1llll11_opy_
    try:
        bstack11l11111_opy_ = bstack111111ll1_opy_()
        bstack11lllll1l1_opy_(bstack11l11111_opy_)
        hub_url = bstack11l11111_opy_.get(bstack11l1lll_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11l1lll_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11l1lll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11l1lll_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11l1lll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11l1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1ll1llll11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack111111ll1_opy_():
    global CONFIG
    bstack1ll11lll1l_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11l1lll_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11l1lll_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1ll11lll1l_opy_, str):
        raise ValueError(bstack11l1lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l11111_opy_ = bstack1l1lllll11_opy_(bstack1ll11lll1l_opy_)
        return bstack11l11111_opy_
    except Exception as e:
        logger.error(bstack11l1lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1l1lllll11_opy_(bstack1ll11lll1l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11l1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11l1lll_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1lll1ll1l1_opy_ + bstack1ll11lll1l_opy_
        auth = (CONFIG[bstack11l1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1111l1ll1_opy_ = json.loads(response.text)
            return bstack1111l1ll1_opy_
    except ValueError as ve:
        logger.error(bstack11l1lll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11l1lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11lllll1l1_opy_(bstack1ll111ll11_opy_):
    global CONFIG
    if bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11l1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11l1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11l1lll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1ll111ll11_opy_:
        bstack1111lllll_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11l1lll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1111lllll_opy_)
        bstack11111lll1_opy_ = bstack1ll111ll11_opy_.get(bstack11l1lll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1l111l111l_opy_ = bstack11l1lll_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11111lll1_opy_)
        logger.debug(bstack11l1lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1l111l111l_opy_)
        bstack1ll1l1l111_opy_ = {
            bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11l1lll_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11l1lll_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11l1lll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1l111l111l_opy_
        }
        bstack1111lllll_opy_.update(bstack1ll1l1l111_opy_)
        logger.debug(bstack11l1lll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1111lllll_opy_)
        CONFIG[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1111lllll_opy_
        logger.debug(bstack11l1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1ll1l111_opy_():
    bstack11l11111_opy_ = bstack111111ll1_opy_()
    if not bstack11l11111_opy_[bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11l1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l11111_opy_[bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11l1lll_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1l1ll1l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
def bstack1ll1l1l1l_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l11l11l_opy_
        logger.debug(bstack11l1lll_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11l1lll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11l1lll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1ll111ll_opy_ = json.loads(response.text)
                bstack1111l111_opy_ = bstack1ll111ll_opy_.get(bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1111l111_opy_:
                    bstack11l1llllll_opy_ = bstack1111l111_opy_[0]
                    build_hashed_id = bstack11l1llllll_opy_.get(bstack11l1lll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11ll11lll1_opy_ = bstack1l1llll111_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11ll11lll1_opy_])
                    logger.info(bstack111ll111_opy_.format(bstack11ll11lll1_opy_))
                    bstack11ll1ll1l_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack11ll1ll1l_opy_ += bstack11l1lll_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack11ll1ll1l_opy_ != bstack11l1llllll_opy_.get(bstack11l1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1lll11l111_opy_.format(bstack11l1llllll_opy_.get(bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack11ll1ll1l_opy_))
                    return result
                else:
                    logger.debug(bstack11l1lll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11l1lll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11l1lll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11l1lll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1lll111111_opy_ import bstack1lll111111_opy_, bstack11lll11lll_opy_, bstack1llll1l1l1_opy_, bstack1llll1l111_opy_
from bstack_utils.measure import bstack11l1lll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll111ll1_opy_ import bstack11lll11l1l_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1l11l1lll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11ll1l1_opy_, bstack11lll1lll_opy_, bstack1ll1ll11_opy_, bstack111l11lll_opy_, \
  bstack1lll11l1l_opy_, \
  Notset, bstack11l1ll1l1l_opy_, \
  bstack1ll1l11l1_opy_, bstack1ll11l1l1l_opy_, bstack1l1lll11_opy_, bstack11ll1lllll_opy_, bstack1ll11lll_opy_, bstack1111llll_opy_, \
  bstack11l1l1l1l1_opy_, \
  bstack11l111ll1l_opy_, bstack111l11l11_opy_, bstack11l1lll1l_opy_, bstack11llll11ll_opy_, \
  bstack1l1111ll_opy_, bstack1lll111ll_opy_, bstack1llll1l11_opy_, bstack1l111111l1_opy_
from bstack_utils.bstack1lll1ll1ll_opy_ import bstack1ll11l1ll_opy_, bstack1l1l11l1_opy_
from bstack_utils.bstack11l1lllll1_opy_ import bstack1111l11l1_opy_
from bstack_utils.bstack111l1111_opy_ import bstack11ll1ll1_opy_, bstack1l1111l1l_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.bstack1lll11llll_opy_ import bstack1111ll1ll_opy_
from bstack_utils.proxy import bstack11l111l1_opy_, bstack1ll111l1_opy_, bstack111ll1lll_opy_, bstack1l1ll1lll1_opy_
from bstack_utils.bstack1llll11l1l_opy_ import bstack1llll11111_opy_
import bstack_utils.bstack11111l111_opy_ as bstack11lll1111_opy_
import bstack_utils.bstack11l1ll111_opy_ as bstack1l1lll1l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1l1lllll_opy_ import bstack1l11ll11_opy_
from bstack_utils.bstack1l11l1l1l1_opy_ import bstack1l1l1l1ll1_opy_
if os.getenv(bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack11l1l111_opy_()
else:
  os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack11l1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1111l1lll_opy_ = bstack11l1lll_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1l1ll1llll_opy_ = bstack11l1lll_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1l1111l1l1_opy_ = None
CONFIG = {}
bstack1l1l111ll_opy_ = {}
bstack1lll1l1l1_opy_ = {}
bstack111l111l1_opy_ = None
bstack1llllll111_opy_ = None
bstack1l1l1ll1l1_opy_ = None
bstack11l1ll11l_opy_ = -1
bstack1l1l11ll_opy_ = 0
bstack111llll11_opy_ = bstack11ll11lll_opy_
bstack11l1ll1ll_opy_ = 1
bstack1llll1ll1l_opy_ = False
bstack1l1ll1ll1l_opy_ = False
bstack1l11l1l11l_opy_ = bstack11l1lll_opy_ (u"ࠬ࠭ࢾ")
bstack11ll1l11l_opy_ = bstack11l1lll_opy_ (u"࠭ࠧࢿ")
bstack1l111111_opy_ = False
bstack1l1ll11ll_opy_ = True
bstack1l1lll11l_opy_ = bstack11l1lll_opy_ (u"ࠧࠨࣀ")
bstack11l111ll_opy_ = []
bstack1ll1llll11_opy_ = bstack11l1lll_opy_ (u"ࠨࠩࣁ")
bstack11l1ll1l1_opy_ = False
bstack11ll11ll11_opy_ = None
bstack111111ll_opy_ = None
bstack1l1lll1l1_opy_ = None
bstack1l11l1111_opy_ = -1
bstack11l111ll1_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠩࢁࠫࣂ")), bstack11l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack11l1lll_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1l11ll1ll1_opy_ = 0
bstack1l111lll11_opy_ = 0
bstack1ll11ll1_opy_ = []
bstack1ll1l1ll_opy_ = []
bstack1ll11l111l_opy_ = []
bstack11l1ll1lll_opy_ = []
bstack1ll111l1l1_opy_ = bstack11l1lll_opy_ (u"ࠬ࠭ࣅ")
bstack1ll11ll1l_opy_ = bstack11l1lll_opy_ (u"࠭ࠧࣆ")
bstack1l11111ll_opy_ = False
bstack1l1l1l1ll_opy_ = False
bstack1l1111l1ll_opy_ = {}
bstack11l1l11l1l_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11l1ll11ll_opy_ = None
bstack11l11l11_opy_ = None
bstack1lll1l111_opy_ = None
bstack1l1llllll1_opy_ = None
bstack1l1llll1l1_opy_ = None
bstack1lll11ll1l_opy_ = None
bstack11ll1l1lll_opy_ = None
bstack11l11lllll_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1l1lllll1l_opy_ = None
bstack1111l1l1_opy_ = None
bstack1llll1ll_opy_ = None
bstack1l1111ll1_opy_ = None
bstack1l11l11lll_opy_ = None
bstack1ll111111l_opy_ = None
bstack11llll11l1_opy_ = None
bstack1lll1lllll_opy_ = None
bstack1lll11ll_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack1lll1l11_opy_ = None
bstack111111l11_opy_ = None
thread_local = threading.local()
bstack111l1l11_opy_ = False
bstack1lll1l1l11_opy_ = bstack11l1lll_opy_ (u"ࠢࠣࣇ")
logger = bstack1l11l1lll_opy_.get_logger(__name__, bstack111llll11_opy_)
bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
percy = bstack1l11l1ll11_opy_()
bstack1l11l1111l_opy_ = bstack11lll11l1l_opy_()
bstack1l1ll111ll_opy_ = bstack111l1ll1_opy_()
def bstack11l11l1l_opy_():
  global CONFIG
  global bstack1l11111ll_opy_
  global bstack11ll1llll1_opy_
  testContextOptions = bstack11l1l1ll1l_opy_(CONFIG)
  if bstack1lll11l1l_opy_(CONFIG):
    if (bstack11l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack11l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack11l1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l11111ll_opy_ = True
    bstack11ll1llll1_opy_.bstack1l11lllll1_opy_(testContextOptions.get(bstack11l1lll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l11111ll_opy_ = True
    bstack11ll1llll1_opy_.bstack1l11lllll1_opy_(True)
def bstack1l1111111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111111111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l1lll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack11l1lll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1lll11l_opy_
      bstack1l1lll11l_opy_ += bstack11l1lll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack111llllll_opy_ = re.compile(bstack11l1lll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack1l1l111l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111llllll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l1lll_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack11l1lll_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1l1ll1l1l_opy_():
  global bstack111111l11_opy_
  if bstack111111l11_opy_ is None:
        bstack111111l11_opy_ = bstack1l111l1111_opy_()
  bstack1l1l11111l_opy_ = bstack111111l11_opy_
  if bstack1l1l11111l_opy_ and os.path.exists(os.path.abspath(bstack1l1l11111l_opy_)):
    fileName = bstack1l1l11111l_opy_
  if bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack11l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack111ll1l_opy_ = os.path.abspath(fileName)
  else:
    bstack111ll1l_opy_ = bstack11l1lll_opy_ (u"ࠩࠪࣗ")
  bstack11l1l1l11l_opy_ = os.getcwd()
  bstack1l1111lll1_opy_ = bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack1l11l11l1l_opy_ = bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack111ll1l_opy_)) and bstack11l1l1l11l_opy_ != bstack11l1lll_opy_ (u"ࠧࠨࣚ"):
    bstack111ll1l_opy_ = os.path.join(bstack11l1l1l11l_opy_, bstack1l1111lll1_opy_)
    if not os.path.exists(bstack111ll1l_opy_):
      bstack111ll1l_opy_ = os.path.join(bstack11l1l1l11l_opy_, bstack1l11l11l1l_opy_)
    if bstack11l1l1l11l_opy_ != os.path.dirname(bstack11l1l1l11l_opy_):
      bstack11l1l1l11l_opy_ = os.path.dirname(bstack11l1l1l11l_opy_)
    else:
      bstack11l1l1l11l_opy_ = bstack11l1lll_opy_ (u"ࠨࠢࣛ")
  bstack111111l11_opy_ = bstack111ll1l_opy_ if os.path.exists(bstack111ll1l_opy_) else None
  return bstack111111l11_opy_
def bstack11l1l1111_opy_():
  bstack111ll1l_opy_ = bstack1l1ll1l1l_opy_()
  if not os.path.exists(bstack111ll1l_opy_):
    bstack11l111lll1_opy_(
      bstack11l1llll1_opy_.format(os.getcwd()))
  try:
    with open(bstack111ll1l_opy_, bstack11l1lll_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack11l1lll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack111llllll_opy_)
      yaml.add_constructor(bstack11l1lll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1l1l111l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack111ll1l_opy_, bstack11l1lll_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l111lll1_opy_(bstack11l1lll1ll_opy_.format(str(exc)))
def bstack111l111l_opy_(config):
  bstack1ll111l11_opy_ = bstack1ll1l11l_opy_(config)
  for option in list(bstack1ll111l11_opy_):
    if option.lower() in bstack1ll1llllll_opy_ and option != bstack1ll1llllll_opy_[option.lower()]:
      bstack1ll111l11_opy_[bstack1ll1llllll_opy_[option.lower()]] = bstack1ll111l11_opy_[option]
      del bstack1ll111l11_opy_[option]
  return config
def bstack11l1lll11l_opy_():
  global bstack1lll1l1l1_opy_
  for key, bstack1111ll11l_opy_ in bstack1lll11lll_opy_.items():
    if isinstance(bstack1111ll11l_opy_, list):
      for var in bstack1111ll11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll1l1l1_opy_[key] = os.environ[var]
          break
    elif bstack1111ll11l_opy_ in os.environ and os.environ[bstack1111ll11l_opy_] and str(os.environ[bstack1111ll11l_opy_]).strip():
      bstack1lll1l1l1_opy_[key] = os.environ[bstack1111ll11l_opy_]
  if bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack1lll1l1l1_opy_[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack1lll1l1l1_opy_[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack11l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack11ll111lll_opy_():
  global bstack1l1l111ll_opy_
  global bstack1l1lll11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l1lll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack1l1l111ll_opy_[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack1l1l111ll_opy_[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11lll111l1_opy_ in bstack111lll11l_opy_.items():
    if isinstance(bstack11lll111l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11lll111l1_opy_:
          if idx < len(sys.argv) and bstack11l1lll_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack1l1l111ll_opy_:
            bstack1l1l111ll_opy_[key] = sys.argv[idx + 1]
            bstack1l1lll11l_opy_ += bstack11l1lll_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack11l1lll_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l1lll_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack11lll111l1_opy_.lower() == val.lower() and not key in bstack1l1l111ll_opy_:
          bstack1l1l111ll_opy_[key] = sys.argv[idx + 1]
          bstack1l1lll11l_opy_ += bstack11l1lll_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack11lll111l1_opy_ + bstack11l1lll_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l11l11l1_opy_(config):
  bstack1lll11lll1_opy_ = config.keys()
  for bstack111llll1l_opy_, bstack11ll1lll1_opy_ in bstack1l111l111_opy_.items():
    if bstack11ll1lll1_opy_ in bstack1lll11lll1_opy_:
      config[bstack111llll1l_opy_] = config[bstack11ll1lll1_opy_]
      del config[bstack11ll1lll1_opy_]
  for bstack111llll1l_opy_, bstack11ll1lll1_opy_ in bstack11llll11l_opy_.items():
    if isinstance(bstack11ll1lll1_opy_, list):
      for bstack1ll1l11lll_opy_ in bstack11ll1lll1_opy_:
        if bstack1ll1l11lll_opy_ in bstack1lll11lll1_opy_:
          config[bstack111llll1l_opy_] = config[bstack1ll1l11lll_opy_]
          del config[bstack1ll1l11lll_opy_]
          break
    elif bstack11ll1lll1_opy_ in bstack1lll11lll1_opy_:
      config[bstack111llll1l_opy_] = config[bstack11ll1lll1_opy_]
      del config[bstack11ll1lll1_opy_]
  for bstack1ll1l11lll_opy_ in list(config):
    for bstack1lll1l1l_opy_ in bstack11l1111l1_opy_:
      if bstack1ll1l11lll_opy_.lower() == bstack1lll1l1l_opy_.lower() and bstack1ll1l11lll_opy_ != bstack1lll1l1l_opy_:
        config[bstack1lll1l1l_opy_] = config[bstack1ll1l11lll_opy_]
        del config[bstack1ll1l11lll_opy_]
  bstack1ll1ll1lll_opy_ = [{}]
  if not config.get(bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack1ll1ll1lll_opy_ = config[bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack1ll1ll1lll_opy_:
    for bstack1ll1l11lll_opy_ in list(platform):
      for bstack1lll1l1l_opy_ in bstack11l1111l1_opy_:
        if bstack1ll1l11lll_opy_.lower() == bstack1lll1l1l_opy_.lower() and bstack1ll1l11lll_opy_ != bstack1lll1l1l_opy_:
          platform[bstack1lll1l1l_opy_] = platform[bstack1ll1l11lll_opy_]
          del platform[bstack1ll1l11lll_opy_]
  for bstack111llll1l_opy_, bstack11ll1lll1_opy_ in bstack11llll11l_opy_.items():
    for platform in bstack1ll1ll1lll_opy_:
      if isinstance(bstack11ll1lll1_opy_, list):
        for bstack1ll1l11lll_opy_ in bstack11ll1lll1_opy_:
          if bstack1ll1l11lll_opy_ in platform:
            platform[bstack111llll1l_opy_] = platform[bstack1ll1l11lll_opy_]
            del platform[bstack1ll1l11lll_opy_]
            break
      elif bstack11ll1lll1_opy_ in platform:
        platform[bstack111llll1l_opy_] = platform[bstack11ll1lll1_opy_]
        del platform[bstack11ll1lll1_opy_]
  for bstack1l11l1ll1l_opy_ in bstack1l1l1lll_opy_:
    if bstack1l11l1ll1l_opy_ in config:
      if not bstack1l1l1lll_opy_[bstack1l11l1ll1l_opy_] in config:
        config[bstack1l1l1lll_opy_[bstack1l11l1ll1l_opy_]] = {}
      config[bstack1l1l1lll_opy_[bstack1l11l1ll1l_opy_]].update(config[bstack1l11l1ll1l_opy_])
      del config[bstack1l11l1ll1l_opy_]
  for platform in bstack1ll1ll1lll_opy_:
    for bstack1l11l1ll1l_opy_ in bstack1l1l1lll_opy_:
      if bstack1l11l1ll1l_opy_ in list(platform):
        if not bstack1l1l1lll_opy_[bstack1l11l1ll1l_opy_] in platform:
          platform[bstack1l1l1lll_opy_[bstack1l11l1ll1l_opy_]] = {}
        platform[bstack1l1l1lll_opy_[bstack1l11l1ll1l_opy_]].update(platform[bstack1l11l1ll1l_opy_])
        del platform[bstack1l11l1ll1l_opy_]
  config = bstack111l111l_opy_(config)
  return config
def bstack1ll1111l_opy_(config):
  global bstack11ll1l11l_opy_
  bstack1lllll1l1l_opy_ = False
  if bstack11l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack11l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack11l1lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack11l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack11l11111_opy_ = bstack111111ll1_opy_()
      if bstack11l1lll_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack11l11111_opy_:
        if not bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack11l1lll_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack1lllll1l1l_opy_ = True
        bstack11ll1l11l_opy_ = config[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack11l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1lll11l1l_opy_(config) and bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack11l1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack1lllll1l1l_opy_:
    if not bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack11l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack11l1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1lll11l11_opy_ = datetime.datetime.now()
      bstack1ll1111l1l_opy_ = bstack1lll11l11_opy_.strftime(bstack11l1lll_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack11ll1111ll_opy_ = bstack11l1lll_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l1lll_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1ll1111l1l_opy_, hostname, bstack11ll1111ll_opy_)
      config[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack11l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack11ll1l11l_opy_ = config[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack11l1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1l111l1lll_opy_():
  bstack1l1lll1lll_opy_ =  bstack11ll1lllll_opy_()[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack1l1lll1lll_opy_ if bstack1l1lll1lll_opy_ else -1
def bstack11l11l1lll_opy_(bstack1l1lll1lll_opy_):
  global CONFIG
  if not bstack11l1lll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack11l1lll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack1l1lll1lll_opy_)
  )
def bstack11ll1l1l_opy_():
  global CONFIG
  if not bstack11l1lll_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1lll11l11_opy_ = datetime.datetime.now()
  bstack1ll1111l1l_opy_ = bstack1lll11l11_opy_.strftime(bstack11l1lll_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack11l1lll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1ll1111l1l_opy_
  )
def bstack1ll1111lll_opy_():
  global CONFIG
  if bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack11l1lll_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack11l1lll_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack11ll1l1l_opy_()
    os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack11l1lll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack1l1lll1lll_opy_ = bstack11l1lll_opy_ (u"ࠧࠨऩ")
  bstack1l111ll11l_opy_ = bstack1l111l1lll_opy_()
  if bstack1l111ll11l_opy_ != -1:
    bstack1l1lll1lll_opy_ = bstack11l1lll_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack1l111ll11l_opy_)
  if bstack1l1lll1lll_opy_ == bstack11l1lll_opy_ (u"ࠩࠪफ"):
    bstack1ll1l1111l_opy_ = bstack1l1ll1111_opy_(CONFIG[bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1ll1l1111l_opy_ != -1:
      bstack1l1lll1lll_opy_ = str(bstack1ll1l1111l_opy_)
  if bstack1l1lll1lll_opy_:
    bstack11l11l1lll_opy_(bstack1l1lll1lll_opy_)
    os.environ[bstack11l1lll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack11l11l111l_opy_(bstack1l1l11l11l_opy_, bstack1l1l1l111_opy_, path):
  bstack1l1ll1l11_opy_ = {
    bstack11l1lll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1l1l1l111_opy_
  }
  if os.path.exists(path):
    bstack1ll1llll1_opy_ = json.load(open(path, bstack11l1lll_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack1ll1llll1_opy_ = {}
  bstack1ll1llll1_opy_[bstack1l1l11l11l_opy_] = bstack1l1ll1l11_opy_
  with open(path, bstack11l1lll_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack1ll1llll1_opy_, outfile)
def bstack1l1ll1111_opy_(bstack1l1l11l11l_opy_):
  bstack1l1l11l11l_opy_ = str(bstack1l1l11l11l_opy_)
  bstack1lll11l11l_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠩࢁࠫल")), bstack11l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack1lll11l11l_opy_):
      os.makedirs(bstack1lll11l11l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠫࢃ࠭ऴ")), bstack11l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack11l1lll_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l1lll_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack11l1lll_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l1lll_opy_ (u"ࠩࡵࠫह")) as bstack1llllll1ll_opy_:
      bstack1l111ll1l1_opy_ = json.load(bstack1llllll1ll_opy_)
    if bstack1l1l11l11l_opy_ in bstack1l111ll1l1_opy_:
      bstack11ll1l1l11_opy_ = bstack1l111ll1l1_opy_[bstack1l1l11l11l_opy_][bstack11l1lll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack11l111l11_opy_ = int(bstack11ll1l1l11_opy_) + 1
      bstack11l11l111l_opy_(bstack1l1l11l11l_opy_, bstack11l111l11_opy_, file_path)
      return bstack11l111l11_opy_
    else:
      bstack11l11l111l_opy_(bstack1l1l11l11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11llll1ll_opy_.format(str(e)))
    return -1
def bstack1l11ll1l11_opy_(config):
  if not config[bstack11l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack1111l111l_opy_(config, index=0):
  global bstack1l111111_opy_
  bstack1ll11lll11_opy_ = {}
  caps = bstack1ll111l1l_opy_ + bstack11lll11ll1_opy_
  if config.get(bstack11l1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack11l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack1l111111_opy_:
    caps += bstack11lllll11l_opy_
  for key in config:
    if key in caps + [bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack1ll11lll11_opy_[key] = config[key]
  if bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack11l1l11l_opy_ in config[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack11l1l11l_opy_ in caps:
        continue
      bstack1ll11lll11_opy_[bstack11l1l11l_opy_] = config[bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack11l1l11l_opy_]
  bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack11l1lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack1ll11lll11_opy_:
    del (bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack1ll11lll11_opy_
def bstack1ll11l11l1_opy_(config):
  global bstack1l111111_opy_
  bstack11lll1l11l_opy_ = {}
  caps = bstack11lll11ll1_opy_
  if bstack1l111111_opy_:
    caps += bstack11lllll11l_opy_
  for key in caps:
    if key in config:
      bstack11lll1l11l_opy_[key] = config[key]
  return bstack11lll1l11l_opy_
def bstack11l11ll11l_opy_(bstack1ll11lll11_opy_, bstack11lll1l11l_opy_):
  bstack1l1l11ll1l_opy_ = {}
  for key in bstack1ll11lll11_opy_.keys():
    if key in bstack1l111l111_opy_:
      bstack1l1l11ll1l_opy_[bstack1l111l111_opy_[key]] = bstack1ll11lll11_opy_[key]
    else:
      bstack1l1l11ll1l_opy_[key] = bstack1ll11lll11_opy_[key]
  for key in bstack11lll1l11l_opy_:
    if key in bstack1l111l111_opy_:
      bstack1l1l11ll1l_opy_[bstack1l111l111_opy_[key]] = bstack11lll1l11l_opy_[key]
    else:
      bstack1l1l11ll1l_opy_[key] = bstack11lll1l11l_opy_[key]
  return bstack1l1l11ll1l_opy_
def bstack1l11l1ll_opy_(config, index=0):
  global bstack1l111111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll11111ll_opy_ = bstack1ll11ll1l1_opy_(bstack1l1111l11l_opy_, config, logger)
  bstack11lll1l11l_opy_ = bstack1ll11l11l1_opy_(config)
  bstack1lll1111l1_opy_ = bstack11lll11ll1_opy_
  bstack1lll1111l1_opy_ += bstack1l1l1l11l1_opy_
  bstack11lll1l11l_opy_ = update(bstack11lll1l11l_opy_, bstack1ll11111ll_opy_)
  if bstack1l111111_opy_:
    bstack1lll1111l1_opy_ += bstack11lllll11l_opy_
  if bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack111llll1_opy_ = bstack1ll11ll1l1_opy_(bstack1l1111l11l_opy_, config[bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1lll1111l1_opy_ += list(bstack111llll1_opy_.keys())
    for bstack11lll1ll1_opy_ in bstack1lll1111l1_opy_:
      if bstack11lll1ll1_opy_ in config[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack11lll1ll1_opy_ == bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack111llll1_opy_[bstack11lll1ll1_opy_] = str(config[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11lll1ll1_opy_] * 1.0)
          except:
            bstack111llll1_opy_[bstack11lll1ll1_opy_] = str(config[bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack11lll1ll1_opy_])
        else:
          bstack111llll1_opy_[bstack11lll1ll1_opy_] = config[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack11lll1ll1_opy_]
        del (config[bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack11lll1ll1_opy_])
    bstack11lll1l11l_opy_ = update(bstack11lll1l11l_opy_, bstack111llll1_opy_)
  bstack1ll11lll11_opy_ = bstack1111l111l_opy_(config, index)
  for bstack1ll1l11lll_opy_ in bstack11lll11ll1_opy_ + list(bstack1ll11111ll_opy_.keys()):
    if bstack1ll1l11lll_opy_ in bstack1ll11lll11_opy_:
      bstack11lll1l11l_opy_[bstack1ll1l11lll_opy_] = bstack1ll11lll11_opy_[bstack1ll1l11lll_opy_]
      del (bstack1ll11lll11_opy_[bstack1ll1l11lll_opy_])
  if bstack11l1ll1l1l_opy_(config):
    bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack11lll1l11l_opy_)
    caps[bstack11l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack1ll11lll11_opy_
  else:
    bstack1ll11lll11_opy_[bstack11l1lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack11l11ll11l_opy_(bstack1ll11lll11_opy_, bstack11lll1l11l_opy_))
    if bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack1ll1l11ll1_opy_():
  global bstack1ll1llll11_opy_
  global CONFIG
  if bstack111111111_opy_() <= version.parse(bstack11l1lll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1ll1llll11_opy_ != bstack11l1lll_opy_ (u"ࠬ࠭०"):
      return bstack11l1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1ll1llll11_opy_ + bstack11l1lll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack111lllll1_opy_
  if bstack1ll1llll11_opy_ != bstack11l1lll_opy_ (u"ࠨࠩ३"):
    return bstack11l1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1ll1llll11_opy_ + bstack11l1lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack11llllll1l_opy_
def bstack11ll11l11l_opy_(options):
  return hasattr(options, bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1l111ll_opy_(options, bstack1l11ll11ll_opy_):
  for bstack11l11ll1l1_opy_ in bstack1l11ll11ll_opy_:
    if bstack11l11ll1l1_opy_ in [bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack11l1lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack11l11ll1l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11l11ll1l1_opy_] = update(options._experimental_options[bstack11l11ll1l1_opy_],
                                                         bstack1l11ll11ll_opy_[bstack11l11ll1l1_opy_])
    else:
      options.add_experimental_option(bstack11l11ll1l1_opy_, bstack1l11ll11ll_opy_[bstack11l11ll1l1_opy_])
  if bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack1l11ll11ll_opy_:
    for arg in bstack1l11ll11ll_opy_[bstack11l1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack1l11ll11ll_opy_[bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack11l1lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack1l11ll11ll_opy_:
    for ext in bstack1l11ll11ll_opy_[bstack11l1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l11ll11ll_opy_[bstack11l1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack1l11ll1111_opy_(options, bstack1ll11l1l_opy_):
  if bstack11l1lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1ll11l1l_opy_:
    for bstack1lll1111l_opy_ in bstack1ll11l1l_opy_[bstack11l1lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack1lll1111l_opy_ in options._preferences:
        options._preferences[bstack1lll1111l_opy_] = update(options._preferences[bstack1lll1111l_opy_], bstack1ll11l1l_opy_[bstack11l1lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack1lll1111l_opy_])
      else:
        options.set_preference(bstack1lll1111l_opy_, bstack1ll11l1l_opy_[bstack11l1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack1lll1111l_opy_])
  if bstack11l1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1ll11l1l_opy_:
    for arg in bstack1ll11l1l_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1lll1llll_opy_(options, bstack1ll111l111_opy_):
  if bstack11l1lll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack1ll111l111_opy_:
    options.use_webview(bool(bstack1ll111l111_opy_[bstack11l1lll_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack1ll1l111ll_opy_(options, bstack1ll111l111_opy_)
def bstack111lll11_opy_(options, bstack1lll111l_opy_):
  for bstack1l1111llll_opy_ in bstack1lll111l_opy_:
    if bstack1l1111llll_opy_ in [bstack11l1lll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack11l1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack1l1111llll_opy_, bstack1lll111l_opy_[bstack1l1111llll_opy_])
  if bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1lll111l_opy_:
    for arg in bstack1lll111l_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack1lll111l_opy_:
    options.bstack11ll1111l1_opy_(bool(bstack1lll111l_opy_[bstack11l1lll_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack111ll1ll_opy_(options, bstack1l1l11l1l_opy_):
  for bstack111lllll_opy_ in bstack1l1l11l1l_opy_:
    if bstack111lllll_opy_ in [bstack11l1lll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack111lllll_opy_] = bstack1l1l11l1l_opy_[bstack111lllll_opy_]
  if bstack11l1lll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack1l1l11l1l_opy_:
    for bstack1l111ll11_opy_ in bstack1l1l11l1l_opy_[bstack11l1lll_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l1l11l1ll_opy_(
        bstack1l111ll11_opy_, bstack1l1l11l1l_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack1l111ll11_opy_])
  if bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack1l1l11l1l_opy_:
    for arg in bstack1l1l11l1l_opy_[bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack1llllll1l_opy_(options, caps):
  if not hasattr(options, bstack11l1lll_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack11l1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ"):
    options = bstack1l11111lll_opy_.bstack11l11l1l1l_opy_(bstack1l11lll11l_opy_=options, config=CONFIG)
  if options.KEY == bstack11l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ") and options.KEY in caps:
    bstack1ll1l111ll_opy_(options, caps[bstack11l1lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍")])
  elif options.KEY == bstack11l1lll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎") and options.KEY in caps:
    bstack1l11ll1111_opy_(options, caps[bstack11l1lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ")])
  elif options.KEY == bstack11l1lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ") and options.KEY in caps:
    bstack111lll11_opy_(options, caps[bstack11l1lll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑")])
  elif options.KEY == bstack11l1lll_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒") and options.KEY in caps:
    bstack1lll1llll_opy_(options, caps[bstack11l1lll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও")])
  elif options.KEY == bstack11l1lll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ") and options.KEY in caps:
    bstack111ll1ll_opy_(options, caps[bstack11l1lll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক")])
def bstack1l1ll1ll1_opy_(caps):
  global bstack1l111111_opy_
  if isinstance(os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")), str):
    bstack1l111111_opy_ = eval(os.getenv(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")))
  if bstack1l111111_opy_:
    if bstack1l1111111_opy_() < version.parse(bstack11l1lll_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬঘ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঙ")
    if bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ") in caps:
      browser = caps[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ")]
    elif bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ") in caps:
      browser = caps[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ")]
    browser = str(browser).lower()
    if browser == bstack11l1lll_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬঞ") or browser == bstack11l1lll_opy_ (u"࠭ࡩࡱࡣࡧࠫট"):
      browser = bstack11l1lll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧঠ")
    if browser == bstack11l1lll_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩড"):
      browser = bstack11l1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ")
    if browser not in [bstack11l1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ"), bstack11l1lll_opy_ (u"ࠫࡪࡪࡧࡦࠩত"), bstack11l1lll_opy_ (u"ࠬ࡯ࡥࠨথ"), bstack11l1lll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭দ"), bstack11l1lll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨধ")]:
      return None
    try:
      package = bstack11l1lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪন").format(browser)
      name = bstack11l1lll_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ঩")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll11l11l_opy_(options):
        return None
      for bstack1ll1l11lll_opy_ in caps.keys():
        options.set_capability(bstack1ll1l11lll_opy_, caps[bstack1ll1l11lll_opy_])
      bstack1llllll1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1l1l1l_opy_(options, bstack11lll1l1ll_opy_):
  if not bstack11ll11l11l_opy_(options):
    return
  for bstack1ll1l11lll_opy_ in bstack11lll1l1ll_opy_.keys():
    if bstack1ll1l11lll_opy_ in bstack1l1l1l11l1_opy_:
      continue
    if bstack1ll1l11lll_opy_ in options._caps and type(options._caps[bstack1ll1l11lll_opy_]) in [dict, list]:
      options._caps[bstack1ll1l11lll_opy_] = update(options._caps[bstack1ll1l11lll_opy_], bstack11lll1l1ll_opy_[bstack1ll1l11lll_opy_])
    else:
      options.set_capability(bstack1ll1l11lll_opy_, bstack11lll1l1ll_opy_[bstack1ll1l11lll_opy_])
  bstack1llllll1l_opy_(options, bstack11lll1l1ll_opy_)
  if bstack11l1lll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ") in options._caps:
    if options._caps[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")] and options._caps[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")].lower() != bstack11l1lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧভ"):
      del options._caps[bstack11l1lll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ম")]
def bstack1ll11ll1ll_opy_(proxy_config):
  if bstack11l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬয") in proxy_config:
    proxy_config[bstack11l1lll_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫর")] = proxy_config[bstack11l1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")]
    del (proxy_config[bstack11l1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")])
  if bstack11l1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳") in proxy_config and proxy_config[bstack11l1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴")].lower() != bstack11l1lll_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧ঵"):
    proxy_config[bstack11l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫশ")] = bstack11l1lll_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩষ")
  if bstack11l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨস") in proxy_config:
    proxy_config[bstack11l1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧহ")] = bstack11l1lll_opy_ (u"ࠬࡶࡡࡤࠩ঺")
  return proxy_config
def bstack1ll11l1l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻") in config:
    return proxy
  config[bstack11l1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")] = bstack1ll11ll1ll_opy_(config[bstack11l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  return proxy
def bstack1llll11ll_opy_(self):
  global CONFIG
  global bstack1l1lllll1l_opy_
  try:
    proxy = bstack111ll1lll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l1lll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨি")):
        proxies = bstack11l111l1_opy_(proxy, bstack1ll1l11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1lll11_opy_ = proxies.popitem()
          if bstack11l1lll_opy_ (u"ࠦ࠿࠵࠯ࠣী") in bstack1ll1lll11_opy_:
            return bstack1ll1lll11_opy_
          else:
            return bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨু") + bstack1ll1lll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥূ").format(str(e)))
  return bstack1l1lllll1l_opy_(self)
def bstack1llll1l1_opy_():
  global CONFIG
  return bstack1l1ll1lll1_opy_(CONFIG) and bstack1111llll_opy_() and bstack111111111_opy_() >= version.parse(bstack11l111l111_opy_)
def bstack11111llll_opy_():
  global CONFIG
  return (bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪৃ") in CONFIG or bstack11l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ") in CONFIG) and bstack11l1l1l1l1_opy_()
def bstack1ll1l11l_opy_(config):
  bstack1ll111l11_opy_ = {}
  if bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅") in config:
    bstack1ll111l11_opy_ = config[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆")]
  if bstack11l1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে") in config:
    bstack1ll111l11_opy_ = config[bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ")]
  proxy = bstack111ll1lll_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l1lll_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")) and os.path.isfile(proxy):
      bstack1ll111l11_opy_[bstack11l1lll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ৊")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l1lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ো")):
        proxies = bstack1ll111l1_opy_(config, bstack1ll1l11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1lll11_opy_ = proxies.popitem()
          if bstack11l1lll_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") in bstack1ll1lll11_opy_:
            parsed_url = urlparse(bstack1ll1lll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l1lll_opy_ (u"ࠥ࠾࠴࠵্ࠢ") + bstack1ll1lll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll111l11_opy_[bstack11l1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧৎ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll111l11_opy_[bstack11l1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ৏")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll111l11_opy_[bstack11l1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ৐")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll111l11_opy_[bstack11l1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ৑")] = str(parsed_url.password)
  return bstack1ll111l11_opy_
def bstack11l1l1ll1l_opy_(config):
  if bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒") in config:
    return config[bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓")]
  return {}
def bstack111ll1l11_opy_(caps):
  global bstack11ll1l11l_opy_
  if bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔") in caps:
    caps[bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕")][bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ৖")] = True
    if bstack11ll1l11l_opy_:
      caps[bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧৗ")][bstack11l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৘")] = bstack11ll1l11l_opy_
  else:
    caps[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭৙")] = True
    if bstack11ll1l11l_opy_:
      caps[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৚")] = bstack11ll1l11l_opy_
@measure(event_name=EVENTS.bstack1l11ll1lll_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11l1l11_opy_():
  global CONFIG
  if not bstack1lll11l1l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛") in CONFIG and bstack1llll1l11_opy_(CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়")]):
    if (
      bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়") in CONFIG
      and bstack1llll1l11_opy_(CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞")].get(bstack11l1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫয়")))
    ):
      logger.debug(bstack11l1lll_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤৠ"))
      return
    bstack1ll111l11_opy_ = bstack1ll1l11l_opy_(CONFIG)
    bstack11ll11111l_opy_(CONFIG[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬৡ")], bstack1ll111l11_opy_)
def bstack11ll11111l_opy_(key, bstack1ll111l11_opy_):
  global bstack1l1111l1l1_opy_
  logger.info(bstack11lll1lll1_opy_)
  try:
    bstack1l1111l1l1_opy_ = Local()
    bstack11lll1ll1l_opy_ = {bstack11l1lll_opy_ (u"ࠪ࡯ࡪࡿࠧৢ"): key}
    bstack11lll1ll1l_opy_.update(bstack1ll111l11_opy_)
    logger.debug(bstack11l11l11ll_opy_.format(str(bstack11lll1ll1l_opy_)).replace(key, bstack11l1lll_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨৣ")))
    bstack1l1111l1l1_opy_.start(**bstack11lll1ll1l_opy_)
    if bstack1l1111l1l1_opy_.isRunning():
      logger.info(bstack11ll11l1l1_opy_)
  except Exception as e:
    bstack11l111lll1_opy_(bstack1lll1111ll_opy_.format(str(e)))
def bstack1lllll11l1_opy_():
  global bstack1l1111l1l1_opy_
  if bstack1l1111l1l1_opy_.isRunning():
    logger.info(bstack1ll1lll111_opy_)
    bstack1l1111l1l1_opy_.stop()
  bstack1l1111l1l1_opy_ = None
def bstack1l11l11111_opy_(bstack1lllll11l_opy_=[]):
  global CONFIG
  bstack1l1ll11l1_opy_ = []
  bstack11lll1l1l_opy_ = [bstack11l1lll_opy_ (u"ࠬࡵࡳࠨ৤"), bstack11l1lll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৥"), bstack11l1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ০"), bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ১"), bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ২"), bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ৩")]
  try:
    for err in bstack1lllll11l_opy_:
      bstack11ll11ll_opy_ = {}
      for k in bstack11lll1l1l_opy_:
        val = CONFIG[bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৪")][int(err[bstack11l1lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ৫")])].get(k)
        if val:
          bstack11ll11ll_opy_[k] = val
      if(err[bstack11l1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৬")] != bstack11l1lll_opy_ (u"ࠧࠨ৭")):
        bstack11ll11ll_opy_[bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧ৮")] = {
          err[bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৯")]: err[bstack11l1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩৰ")]
        }
        bstack1l1ll11l1_opy_.append(bstack11ll11ll_opy_)
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ৱ") + str(e))
  finally:
    return bstack1l1ll11l1_opy_
def bstack11111ll11_opy_(file_name):
  bstack1lll1ll1_opy_ = []
  try:
    bstack1ll1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll1ll1l1_opy_):
      with open(bstack1ll1ll1l1_opy_) as f:
        bstack1lllllll1l_opy_ = json.load(f)
        bstack1lll1ll1_opy_ = bstack1lllllll1l_opy_
      os.remove(bstack1ll1ll1l1_opy_)
    return bstack1lll1ll1_opy_
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ৲") + str(e))
    return bstack1lll1ll1_opy_
def bstack11l1l11111_opy_():
  try:
      from bstack_utils.constants import bstack1l1111ll11_opy_, EVENTS
      from bstack_utils.helper import bstack11lll1lll_opy_, get_host_info, bstack11ll1llll1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1l1l1ll1l_opy_ = os.path.join(os.getcwd(), bstack11l1lll_opy_ (u"࠭࡬ࡰࡩࠪ৳"), bstack11l1lll_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ৴"))
      lock = FileLock(bstack1l1l1ll1l_opy_+bstack11l1lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ৵"))
      def bstack1ll1ll11l_opy_():
          try:
              with lock:
                  with open(bstack1l1l1ll1l_opy_, bstack11l1lll_opy_ (u"ࠤࡵࠦ৶"), encoding=bstack11l1lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ৷")) as file:
                      data = json.load(file)
                      config = {
                          bstack11l1lll_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ৸"): {
                              bstack11l1lll_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ৹"): bstack11l1lll_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤ৺"),
                          }
                      }
                      bstack1ll11llll1_opy_ = datetime.utcnow()
                      bstack1lll11l11_opy_ = bstack1ll11llll1_opy_.strftime(bstack11l1lll_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦ৻"))
                      bstack11ll111l11_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) if os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) else bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ৾"))
                      payload = {
                          bstack11l1lll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣ৿"): bstack11l1lll_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤ਀"),
                          bstack11l1lll_opy_ (u"ࠨࡤࡢࡶࡤࠦਁ"): {
                              bstack11l1lll_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨਂ"): bstack11ll111l11_opy_,
                              bstack11l1lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨਃ"): bstack1lll11l11_opy_,
                              bstack11l1lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ਄"): bstack11l1lll_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦਅ"),
                              bstack11l1lll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣਆ"): {
                                  bstack11l1lll_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢਇ"): data,
                                  bstack11l1lll_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"): bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"))
                              },
                              bstack11l1lll_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦਊ"): bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਋")),
                              bstack11l1lll_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨ਌"): get_host_info()
                          }
                      }
                      response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠦࡕࡕࡓࡕࠤ਍"), bstack1l1111ll11_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack11l1lll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack1l1111ll11_opy_, payload))
                      else:
                          logger.debug(bstack11l1lll_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡧࡱࡵࠤࢀࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࠣࡿࢂࠨਏ").format(bstack1l1111ll11_opy_, payload))
          except Exception as e:
              logger.debug(bstack11l1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡࡽࢀࠦਐ").format(e))
      bstack1ll1ll11l_opy_()
      bstack1ll11l1l1l_opy_(bstack1l1l1ll1l_opy_, logger)
  except:
    pass
def bstack1l111l1ll1_opy_():
  global bstack1lll1l1l11_opy_
  global bstack11l111ll_opy_
  global bstack1ll11ll1_opy_
  global bstack1ll1l1ll_opy_
  global bstack1ll11l111l_opy_
  global bstack1ll11ll1l_opy_
  global CONFIG
  bstack1ll1ll1l1l_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ਑"))
  if bstack1ll1ll1l1l_opy_ in [bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ਒"), bstack11l1lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩਓ")]:
    bstack1l1lll111l_opy_()
  percy.shutdown()
  if bstack1lll1l1l11_opy_:
    logger.warning(bstack1l1l1ll1_opy_.format(str(bstack1lll1l1l11_opy_)))
  else:
    try:
      bstack1ll1llll1_opy_ = bstack1ll1l11l1_opy_(bstack11l1lll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪਔ"), logger)
      if bstack1ll1llll1_opy_.get(bstack11l1lll_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")) and bstack1ll1llll1_opy_.get(bstack11l1lll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਖ")).get(bstack11l1lll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩਗ")):
        logger.warning(bstack1l1l1ll1_opy_.format(str(bstack1ll1llll1_opy_[bstack11l1lll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਘ")][bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਙ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.bstack1l1llll11l_opy_)
  logger.info(bstack1ll1ll111_opy_)
  global bstack1l1111l1l1_opy_
  if bstack1l1111l1l1_opy_:
    bstack1lllll11l1_opy_()
  try:
    for driver in bstack11l111ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11l111l1l_opy_)
  if bstack1ll11ll1l_opy_ == bstack11l1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ"):
    bstack1ll11l111l_opy_ = bstack11111ll11_opy_(bstack11l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਛ"))
  if bstack1ll11ll1l_opy_ == bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਜ") and len(bstack1ll1l1ll_opy_) == 0:
    bstack1ll1l1ll_opy_ = bstack11111ll11_opy_(bstack11l1lll_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਝ"))
    if len(bstack1ll1l1ll_opy_) == 0:
      bstack1ll1l1ll_opy_ = bstack11111ll11_opy_(bstack11l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਞ"))
  bstack11llllll1_opy_ = bstack11l1lll_opy_ (u"ࠨࠩਟ")
  if len(bstack1ll11ll1_opy_) > 0:
    bstack11llllll1_opy_ = bstack1l11l11111_opy_(bstack1ll11ll1_opy_)
  elif len(bstack1ll1l1ll_opy_) > 0:
    bstack11llllll1_opy_ = bstack1l11l11111_opy_(bstack1ll1l1ll_opy_)
  elif len(bstack1ll11l111l_opy_) > 0:
    bstack11llllll1_opy_ = bstack1l11l11111_opy_(bstack1ll11l111l_opy_)
  elif len(bstack11l1ll1lll_opy_) > 0:
    bstack11llllll1_opy_ = bstack1l11l11111_opy_(bstack11l1ll1lll_opy_)
  if bool(bstack11llllll1_opy_):
    bstack1ll1111111_opy_(bstack11llllll1_opy_)
  else:
    bstack1ll1111111_opy_()
  bstack1ll11l1l1l_opy_(bstack1l11llllll_opy_, logger)
  if bstack1ll1ll1l1l_opy_ not in [bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪਠ")]:
    bstack11l1l11111_opy_()
  bstack1l11l1lll_opy_.bstack1ll1l1lll_opy_(CONFIG)
  if len(bstack1ll11l111l_opy_) > 0:
    sys.exit(len(bstack1ll11l111l_opy_))
def bstack111l1lll_opy_(bstack1ll1llll1l_opy_, frame):
  global bstack11ll1llll1_opy_
  logger.error(bstack11l1l111l_opy_)
  bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ਡ"), bstack1ll1llll1l_opy_)
  if hasattr(signal, bstack11l1lll_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬਢ")):
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), signal.Signals(bstack1ll1llll1l_opy_).name)
  else:
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਤ"), bstack11l1lll_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫਥ"))
  if cli.is_running():
    bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.bstack1l1llll11l_opy_)
  bstack1ll1ll1l1l_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩਦ"))
  if bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩਧ") and not cli.is_enabled(CONFIG):
    bstack1lll11111l_opy_.stop(bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪਨ")))
  bstack1l111l1ll1_opy_()
  sys.exit(1)
def bstack11l111lll1_opy_(err):
  logger.critical(bstack1ll1l1l11l_opy_.format(str(err)))
  bstack1ll1111111_opy_(bstack1ll1l1l11l_opy_.format(str(err)), True)
  atexit.unregister(bstack1l111l1ll1_opy_)
  bstack1l1lll111l_opy_()
  sys.exit(1)
def bstack1lll1llll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1111111_opy_(message, True)
  atexit.unregister(bstack1l111l1ll1_opy_)
  bstack1l1lll111l_opy_()
  sys.exit(1)
def bstack1111l1l1l_opy_():
  global CONFIG
  global bstack1l1l111ll_opy_
  global bstack1lll1l1l1_opy_
  global bstack1l1ll11ll_opy_
  CONFIG = bstack11l1l1111_opy_()
  load_dotenv(CONFIG.get(bstack11l1lll_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬ਩")))
  bstack11l1lll11l_opy_()
  bstack11ll111lll_opy_()
  CONFIG = bstack1l11l11l1_opy_(CONFIG)
  update(CONFIG, bstack1lll1l1l1_opy_)
  update(CONFIG, bstack1l1l111ll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1ll1111l_opy_(CONFIG)
  bstack1l1ll11ll_opy_ = bstack1lll11l1l_opy_(CONFIG)
  os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨਪ")] = bstack1l1ll11ll_opy_.__str__().lower()
  bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧਫ"), bstack1l1ll11ll_opy_)
  if (bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in CONFIG and bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in bstack1l1l111ll_opy_) or (
          bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") in CONFIG and bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਯ") not in bstack1lll1l1l1_opy_):
    if os.getenv(bstack11l1lll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨਰ")):
      CONFIG[bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ਱")] = os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪਲ"))
    else:
      if not CONFIG.get(bstack11l1lll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥਲ਼"), bstack11l1lll_opy_ (u"ࠣࠤ਴")) in bstack1ll11ll111_opy_:
        bstack1ll1111lll_opy_()
  elif (bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਵ") not in CONFIG and bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਸ਼") in CONFIG) or (
          bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") in bstack1lll1l1l1_opy_ and bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") not in bstack1l1l111ll_opy_):
    del (CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਹ")])
  if bstack1l11ll1l11_opy_(CONFIG):
    bstack11l111lll1_opy_(bstack1l11ll1ll_opy_)
  Config.bstack1ll1l1l1l1_opy_().bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤ਺"), CONFIG[bstack11l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ਻")])
  bstack1lll11l1l1_opy_()
  bstack1l111llll1_opy_()
  if bstack1l111111_opy_ and not CONFIG.get(bstack11l1lll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯਼ࠧ"), bstack11l1lll_opy_ (u"ࠥࠦ਽")) in bstack1ll11ll111_opy_:
    CONFIG[bstack11l1lll_opy_ (u"ࠫࡦࡶࡰࠨਾ")] = bstack1lll11111_opy_(CONFIG)
    logger.info(bstack1lll1lll_opy_.format(CONFIG[bstack11l1lll_opy_ (u"ࠬࡧࡰࡱࠩਿ")]))
  if not bstack1l1ll11ll_opy_:
    CONFIG[bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੀ")] = [{}]
def bstack1l1ll11l11_opy_(config, bstack11ll1l11ll_opy_):
  global CONFIG
  global bstack1l111111_opy_
  CONFIG = config
  bstack1l111111_opy_ = bstack11ll1l11ll_opy_
def bstack1l111llll1_opy_():
  global CONFIG
  global bstack1l111111_opy_
  if bstack11l1lll_opy_ (u"ࠧࡢࡲࡳࠫੁ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack1l11llll1_opy_)
    bstack1l111111_opy_ = True
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧੂ"), True)
def bstack1lll11111_opy_(config):
  bstack1lllll1lll_opy_ = bstack11l1lll_opy_ (u"ࠩࠪ੃")
  app = config[bstack11l1lll_opy_ (u"ࠪࡥࡵࡶࠧ੄")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1ll11ll1_opy_:
      if os.path.exists(app):
        bstack1lllll1lll_opy_ = bstack1l1lll1ll1_opy_(config, app)
      elif bstack1ll1llll_opy_(app):
        bstack1lllll1lll_opy_ = app
      else:
        bstack11l111lll1_opy_(bstack11llll1l1_opy_.format(app))
    else:
      if bstack1ll1llll_opy_(app):
        bstack1lllll1lll_opy_ = app
      elif os.path.exists(app):
        bstack1lllll1lll_opy_ = bstack1l1lll1ll1_opy_(app)
      else:
        bstack11l111lll1_opy_(bstack1l1l1l1111_opy_)
  else:
    if len(app) > 2:
      bstack11l111lll1_opy_(bstack1l1l11l11_opy_)
    elif len(app) == 2:
      if bstack11l1lll_opy_ (u"ࠫࡵࡧࡴࡩࠩ੅") in app and bstack11l1lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੆") in app:
        if os.path.exists(app[bstack11l1lll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")]):
          bstack1lllll1lll_opy_ = bstack1l1lll1ll1_opy_(config, app[bstack11l1lll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬੈ")], app[bstack11l1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੉")])
        else:
          bstack11l111lll1_opy_(bstack11llll1l1_opy_.format(app))
      else:
        bstack11l111lll1_opy_(bstack1l1l11l11_opy_)
    else:
      for key in app:
        if key in bstack1ll11l1ll1_opy_:
          if key == bstack11l1lll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੊"):
            if os.path.exists(app[key]):
              bstack1lllll1lll_opy_ = bstack1l1lll1ll1_opy_(config, app[key])
            else:
              bstack11l111lll1_opy_(bstack11llll1l1_opy_.format(app))
          else:
            bstack1lllll1lll_opy_ = app[key]
        else:
          bstack11l111lll1_opy_(bstack11l1llll1l_opy_)
  return bstack1lllll1lll_opy_
def bstack1ll1llll_opy_(bstack1lllll1lll_opy_):
  import re
  bstack11ll111l_opy_ = re.compile(bstack11l1lll_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥੋ"))
  bstack1l11l11ll1_opy_ = re.compile(bstack11l1lll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣੌ"))
  if bstack11l1lll_opy_ (u"ࠬࡨࡳ࠻࠱࠲੍ࠫ") in bstack1lllll1lll_opy_ or re.fullmatch(bstack11ll111l_opy_, bstack1lllll1lll_opy_) or re.fullmatch(bstack1l11l11ll1_opy_, bstack1lllll1lll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l1111l111_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l1lll1ll1_opy_(config, path, bstack1l1ll1l111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l1lll_opy_ (u"࠭ࡲࡣࠩ੎")).read()).hexdigest()
  bstack1lll1lll1_opy_ = bstack1lll111l1_opy_(md5_hash)
  bstack1lllll1lll_opy_ = None
  if bstack1lll1lll1_opy_:
    logger.info(bstack1llll1l11l_opy_.format(bstack1lll1lll1_opy_, md5_hash))
    return bstack1lll1lll1_opy_
  bstack11llll111l_opy_ = datetime.datetime.now()
  bstack111lll1l1_opy_ = MultipartEncoder(
    fields={
      bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ੏"): (os.path.basename(path), open(os.path.abspath(path), bstack11l1lll_opy_ (u"ࠨࡴࡥࠫ੐")), bstack11l1lll_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ੑ")),
      bstack11l1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭੒"): bstack1l1ll1l111_opy_
    }
  )
  response = requests.post(bstack1l1l1111l1_opy_, data=bstack111lll1l1_opy_,
                           headers={bstack11l1lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ੓"): bstack111lll1l1_opy_.content_type},
                           auth=(config[bstack11l1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੔")], config[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੕")]))
  try:
    res = json.loads(response.text)
    bstack1lllll1lll_opy_ = res[bstack11l1lll_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ੖")]
    logger.info(bstack11l11l111_opy_.format(bstack1lllll1lll_opy_))
    bstack1ll1l11ll_opy_(md5_hash, bstack1lllll1lll_opy_)
    cli.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱ࡮ࡲࡥࡩࡥࡡࡱࡲࠥ੗"), datetime.datetime.now() - bstack11llll111l_opy_)
  except ValueError as err:
    bstack11l111lll1_opy_(bstack1l1ll111l_opy_.format(str(err)))
  return bstack1lllll1lll_opy_
def bstack1lll11l1l1_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l1ll1ll_opy_
  bstack11l1ll111l_opy_ = 1
  bstack1111111ll_opy_ = 1
  if bstack11l1lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘") in CONFIG:
    bstack1111111ll_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪਖ਼")]
  else:
    bstack1111111ll_opy_ = bstack11l111lll_opy_(framework_name, args) or 1
  if bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼") in CONFIG:
    bstack11l1ll111l_opy_ = len(CONFIG[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")])
  bstack11l1ll1ll_opy_ = int(bstack1111111ll_opy_) * int(bstack11l1ll111l_opy_)
def bstack11l111lll_opy_(framework_name, args):
  if framework_name == bstack11ll1lll_opy_ and args and bstack11l1lll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ") in args:
      bstack1llll11l11_opy_ = args.index(bstack11l1lll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ੝"))
      return int(args[bstack1llll11l11_opy_ + 1]) or 1
  return 1
def bstack1lll111l1_opy_(md5_hash):
  bstack1ll1ll11ll_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠨࢀࠪਫ਼")), bstack11l1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੟"), bstack11l1lll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੠"))
  if os.path.exists(bstack1ll1ll11ll_opy_):
    bstack1lll111l1l_opy_ = json.load(open(bstack1ll1ll11ll_opy_, bstack11l1lll_opy_ (u"ࠫࡷࡨࠧ੡")))
    if md5_hash in bstack1lll111l1l_opy_:
      bstack11lll11l_opy_ = bstack1lll111l1l_opy_[md5_hash]
      bstack1lll11l1_opy_ = datetime.datetime.now()
      bstack111l1l1ll_opy_ = datetime.datetime.strptime(bstack11lll11l_opy_[bstack11l1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ੢")], bstack11l1lll_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ੣"))
      if (bstack1lll11l1_opy_ - bstack111l1l1ll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11lll11l_opy_[bstack11l1lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ੤")]):
        return None
      return bstack11lll11l_opy_[bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫ੥")]
  else:
    return None
def bstack1ll1l11ll_opy_(md5_hash, bstack1lllll1lll_opy_):
  bstack1lll11l11l_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠩࢁࠫ੦")), bstack11l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ੧"))
  if not os.path.exists(bstack1lll11l11l_opy_):
    os.makedirs(bstack1lll11l11l_opy_)
  bstack1ll1ll11ll_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠫࢃ࠭੨")), bstack11l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੩"), bstack11l1lll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ੪"))
  bstack111l1lll1_opy_ = {
    bstack11l1lll_opy_ (u"ࠧࡪࡦࠪ੫"): bstack1lllll1lll_opy_,
    bstack11l1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੬"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1lll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੭")),
    bstack11l1lll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੮"): str(__version__)
  }
  if os.path.exists(bstack1ll1ll11ll_opy_):
    bstack1lll111l1l_opy_ = json.load(open(bstack1ll1ll11ll_opy_, bstack11l1lll_opy_ (u"ࠫࡷࡨࠧ੯")))
  else:
    bstack1lll111l1l_opy_ = {}
  bstack1lll111l1l_opy_[md5_hash] = bstack111l1lll1_opy_
  with open(bstack1ll1ll11ll_opy_, bstack11l1lll_opy_ (u"ࠧࡽࠫࠣੰ")) as outfile:
    json.dump(bstack1lll111l1l_opy_, outfile)
def bstack11l11lll11_opy_(self):
  return
def bstack11ll1l11l1_opy_(self):
  return
def bstack1llll11ll1_opy_(self):
  global bstack1111l1l1_opy_
  bstack1111l1l1_opy_(self)
def bstack1l1lllllll_opy_():
  global bstack1l1lll1l1_opy_
  bstack1l1lll1l1_opy_ = True
@measure(event_name=EVENTS.bstack1l1l1ll11_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack11llll1111_opy_(self):
  global bstack1l11l1l11l_opy_
  global bstack111l111l1_opy_
  global bstack1lll11ll1_opy_
  try:
    if bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ੱ") in bstack1l11l1l11l_opy_ and self.session_id != None and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫੲ"), bstack11l1lll_opy_ (u"ࠨࠩੳ")) != bstack11l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪੴ"):
      bstack1l1llllll_opy_ = bstack11l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪੵ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶")
      if bstack1l1llllll_opy_ == bstack11l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੷"):
        bstack1l1111ll_opy_(logger)
      if self != None:
        bstack11ll1ll1_opy_(self, bstack1l1llllll_opy_, bstack11l1lll_opy_ (u"࠭ࠬࠡࠩ੸").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l1lll_opy_ (u"ࠧࠨ੹")
    if bstack11l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ੺") in bstack1l11l1l11l_opy_ and getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੻"), None):
      bstack11ll1l111l_opy_.bstack11lll1ll11_opy_(self, bstack1l1111l1ll_opy_, logger, wait=True)
    if bstack11l1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ੼") in bstack1l11l1l11l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11ll1ll1_opy_(self, bstack11l1lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ੽"))
      bstack1l1lll1l1l_opy_.bstack1ll111lll_opy_(self)
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ੾") + str(e))
  bstack1lll11ll1_opy_(self)
  self.session_id = None
def bstack1lll1l111l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1lll1l11l1_opy_
    global bstack1l11l1l11l_opy_
    command_executor = kwargs.get(bstack11l1lll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩ੿"), bstack11l1lll_opy_ (u"ࠧࠨ઀"))
    bstack1llllll11l_opy_ = False
    if type(command_executor) == str and bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in command_executor:
      bstack1llllll11l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬં") in str(getattr(command_executor, bstack11l1lll_opy_ (u"ࠪࡣࡺࡸ࡬ࠨઃ"), bstack11l1lll_opy_ (u"ࠫࠬ઄"))):
      bstack1llllll11l_opy_ = True
    else:
      kwargs = bstack1l11111lll_opy_.bstack11l11l1l1l_opy_(bstack1l11lll11l_opy_=kwargs, config=CONFIG)
      return bstack11l1l11l1l_opy_(self, *args, **kwargs)
    if bstack1llllll11l_opy_:
      bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack11l1l1l1_opy_(CONFIG, bstack1l11l1l11l_opy_)
      if kwargs.get(bstack11l1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")):
        kwargs[bstack11l1lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")] = bstack1lll1l11l1_opy_(kwargs[bstack11l1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨઇ")], bstack1l11l1l11l_opy_, CONFIG, bstack1ll1111l11_opy_)
      elif kwargs.get(bstack11l1lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")):
        kwargs[bstack11l1lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")] = bstack1lll1l11l1_opy_(kwargs[bstack11l1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪઊ")], bstack1l11l1l11l_opy_, CONFIG, bstack1ll1111l11_opy_)
  except Exception as e:
    logger.error(bstack11l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦઋ").format(str(e)))
  return bstack11l1l11l1l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11111l1l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11111l11_opy_(self, command_executor=bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨઌ"), *args, **kwargs):
  global bstack111l111l1_opy_
  global bstack11l111ll_opy_
  bstack1l1l1l1l1_opy_ = bstack1lll1l111l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l111l11l_opy_.on():
    return bstack1l1l1l1l1_opy_
  try:
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪઍ").format(str(command_executor)))
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩ઎").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫએ") in command_executor._url:
      bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪઐ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ઑ") in command_executor):
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ઒"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ઓ"), None)
  bstack1lllllll11_opy_ = {}
  if self.capabilities is not None:
    bstack1lllllll11_opy_[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬઔ")] = self.capabilities.get(bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬક"))
    bstack1lllllll11_opy_[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪખ")] = self.capabilities.get(bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪગ"))
    bstack1lllllll11_opy_[bstack11l1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫઘ")] = self.capabilities.get(bstack11l1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩઙ"))
  if CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬચ"), False) and bstack1l11111lll_opy_.bstack11l1l1llll_opy_(bstack1lllllll11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack11l1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭છ") in bstack1l11l1l11l_opy_ or bstack11l1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭જ") in bstack1l11l1l11l_opy_:
    bstack1lll11111l_opy_.bstack111l1ll11_opy_(self)
  if bstack11l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨઝ") in bstack1l11l1l11l_opy_ and bstack1l1l1l1l1l_opy_ and bstack1l1l1l1l1l_opy_.get(bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩઞ"), bstack11l1lll_opy_ (u"ࠪࠫટ")) == bstack11l1lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬઠ"):
    bstack1lll11111l_opy_.bstack111l1ll11_opy_(self)
  bstack111l111l1_opy_ = self.session_id
  bstack11l111ll_opy_.append(self)
  return bstack1l1l1l1l1_opy_
def bstack1ll11llll_opy_(args):
  return bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ડ") in str(args)
def bstack11ll11l111_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll11ll_opy_
  global bstack111l1l11_opy_
  bstack1l11l11ll_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪઢ"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ણ"), None)
  bstack1l1l111l11_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨત"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫથ"), None)
  bstack1l111lllll_opy_ = getattr(self, bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪદ"), None) != None and getattr(self, bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫધ"), None) == True
  if not bstack111l1l11_opy_ and bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬન") in CONFIG and CONFIG[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭઩")] == True and bstack1lll11ll11_opy_.bstack1l1ll1ll11_opy_(driver_command) and (bstack1l111lllll_opy_ or bstack1l11l11ll_opy_) and not bstack1ll11llll_opy_(args):
    try:
      bstack111l1l11_opy_ = True
      logger.debug(bstack11l1lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩપ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11l1lll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ફ").format(str(err)))
    bstack111l1l11_opy_ = False
  response = bstack1lll11ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨબ") in str(bstack1l11l1l11l_opy_).lower() or bstack11l1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪભ") in str(bstack1l11l1l11l_opy_).lower()) and bstack11l111l11l_opy_.on():
    try:
      if driver_command == bstack11l1lll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨમ"):
        bstack1lll11111l_opy_.bstack1111lll1_opy_({
            bstack11l1lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫય"): response[bstack11l1lll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬર")],
            bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ઱"): bstack1lll11111l_opy_.current_test_uuid() if bstack1lll11111l_opy_.current_test_uuid() else bstack11l111l11l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11ll11l1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack11l11l1111_opy_(self, command_executor,
             desired_capabilities=None, bstack11l1llll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack111l111l1_opy_
  global bstack11l1ll11l_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1llll1ll1l_opy_
  global bstack1l1ll1ll1l_opy_
  global bstack1l11l1l11l_opy_
  global bstack11l1l11l1l_opy_
  global bstack11l111ll_opy_
  global bstack1l11l1111_opy_
  global bstack1l1111l1ll_opy_
  CONFIG[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪલ")] = str(bstack1l11l1l11l_opy_) + str(__version__)
  bstack1lllll111l_opy_ = os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧળ")]
  bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack11l1l1l1_opy_(CONFIG, bstack1l11l1l11l_opy_)
  CONFIG[bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭઴")] = bstack1lllll111l_opy_
  CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭વ")] = bstack1ll1111l11_opy_
  if CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬશ"),bstack11l1lll_opy_ (u"࠭ࠧષ")) and bstack11l1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭સ") in bstack1l11l1l11l_opy_:
    CONFIG[bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨહ")].pop(bstack11l1lll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ઺"), None)
    CONFIG[bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ઻")].pop(bstack11l1lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦ઼ࠩ"), None)
  command_executor = bstack1ll1l11ll1_opy_()
  logger.debug(bstack1l1l1111_opy_.format(command_executor))
  proxy = bstack1ll11l1l1_opy_(CONFIG, proxy)
  bstack1llll11l1_opy_ = 0 if bstack11l1ll11l_opy_ < 0 else bstack11l1ll11l_opy_
  try:
    if bstack1llll1ll1l_opy_ is True:
      bstack1llll11l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1ll1ll1l_opy_ is True:
      bstack1llll11l1_opy_ = int(threading.current_thread().name)
  except:
    bstack1llll11l1_opy_ = 0
  bstack11lll1l1ll_opy_ = bstack1l11l1ll_opy_(CONFIG, bstack1llll11l1_opy_)
  logger.debug(bstack1l111l1l11_opy_.format(str(bstack11lll1l1ll_opy_)))
  if bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩઽ") in CONFIG and bstack1llll1l11_opy_(CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪા")]):
    bstack111ll1l11_opy_(bstack11lll1l1ll_opy_)
  if bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack1llll11l1_opy_) and bstack1l11111lll_opy_.bstack11lll111_opy_(bstack11lll1l1ll_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1l11111lll_opy_.set_capabilities(bstack11lll1l1ll_opy_, CONFIG)
  if desired_capabilities:
    bstack111l11l1_opy_ = bstack1l11l11l1_opy_(desired_capabilities)
    bstack111l11l1_opy_[bstack11l1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧિ")] = bstack11l1ll1l1l_opy_(CONFIG)
    bstack111ll1l1_opy_ = bstack1l11l1ll_opy_(bstack111l11l1_opy_)
    if bstack111ll1l1_opy_:
      bstack11lll1l1ll_opy_ = update(bstack111ll1l1_opy_, bstack11lll1l1ll_opy_)
    desired_capabilities = None
  if options:
    bstack11l1l1l1l_opy_(options, bstack11lll1l1ll_opy_)
  if not options:
    options = bstack1l1ll1ll1_opy_(bstack11lll1l1ll_opy_)
  bstack1l1111l1ll_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫી"))[bstack1llll11l1_opy_]
  if proxy and bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩુ")):
    options.proxy(proxy)
  if options and bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩૂ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111111111_opy_() < version.parse(bstack11l1lll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪૃ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lll1l1ll_opy_)
  logger.info(bstack1l111ll1_opy_)
  bstack11l1lll1l1_opy_.end(EVENTS.bstack1111l11ll_opy_.value, EVENTS.bstack1111l11ll_opy_.value + bstack11l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧૄ"), EVENTS.bstack1111l11ll_opy_.value + bstack11l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦૅ"), status=True, failure=None, test_name=bstack1l1l1ll1l1_opy_)
  if bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡲࡵࡳ࡫࡯࡬ࡦࠩ૆") in kwargs:
    del kwargs[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡳࡶࡴ࡬ࡩ࡭ࡧࠪે")]
  if bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩૈ")):
    bstack11l1l11l1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩૉ")):
    bstack11l1l11l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack11l1llll_opy_=bstack11l1llll_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ૊")):
    bstack11l1l11l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11l1llll_opy_=bstack11l1llll_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l1l11l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11l1llll_opy_=bstack11l1llll_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack1llll11l1_opy_) and bstack1l11111lll_opy_.bstack11lll111_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧો")][bstack11l1lll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬૌ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l11111lll_opy_.set_capabilities(bstack11lll1l1ll_opy_, CONFIG)
  try:
    bstack11llll1lll_opy_ = bstack11l1lll_opy_ (u"ࠧࠨ્")
    if bstack111111111_opy_() >= version.parse(bstack11l1lll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ૎")):
      if self.caps is not None:
        bstack11llll1lll_opy_ = self.caps.get(bstack11l1lll_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ૏"))
    else:
      if self.capabilities is not None:
        bstack11llll1lll_opy_ = self.capabilities.get(bstack11l1lll_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥૐ"))
    if bstack11llll1lll_opy_:
      bstack11l1lll1l_opy_(bstack11llll1lll_opy_)
      if bstack111111111_opy_() <= version.parse(bstack11l1lll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ૑")):
        self.command_executor._url = bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ૒") + bstack1ll1llll11_opy_ + bstack11l1lll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ૓")
      else:
        self.command_executor._url = bstack11l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ૔") + bstack11llll1lll_opy_ + bstack11l1lll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ૕")
      logger.debug(bstack1l11111ll1_opy_.format(bstack11llll1lll_opy_))
    else:
      logger.debug(bstack1111l11l_opy_.format(bstack11l1lll_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ૖")))
  except Exception as e:
    logger.debug(bstack1111l11l_opy_.format(e))
  if bstack11l1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૗") in bstack1l11l1l11l_opy_:
    bstack1l1lll1l11_opy_(bstack11l1ll11l_opy_, bstack1l11l1111_opy_)
  bstack111l111l1_opy_ = self.session_id
  if bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૘") in bstack1l11l1l11l_opy_ or bstack11l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૙") in bstack1l11l1l11l_opy_ or bstack11l1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૚") in bstack1l11l1l11l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૛"), None)
  if bstack11l1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack1l11l1l11l_opy_ or bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack1l11l1l11l_opy_:
    bstack1lll11111l_opy_.bstack111l1ll11_opy_(self)
  if bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૞") in bstack1l11l1l11l_opy_ and bstack1l1l1l1l1l_opy_ and bstack1l1l1l1l1l_opy_.get(bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૟"), bstack11l1lll_opy_ (u"ࠬ࠭ૠ")) == bstack11l1lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૡ"):
    bstack1lll11111l_opy_.bstack111l1ll11_opy_(self)
  bstack11l111ll_opy_.append(self)
  if bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪૢ") in CONFIG and bstack11l1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ૣ") in CONFIG[bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૤")][bstack1llll11l1_opy_]:
    bstack1l1l1ll1l1_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥")][bstack1llll11l1_opy_][bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૦")]
  logger.debug(bstack1ll1l11l1l_opy_.format(bstack111l111l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1ll1l111_opy_
    def bstack11lll1l1l1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l1ll1l1_opy_
      if(bstack11l1lll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ૧") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"࠭ࡾࠨ૨")), bstack11l1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ૩"), bstack11l1lll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ૪")), bstack11l1lll_opy_ (u"ࠩࡺࠫ૫")) as fp:
          fp.write(bstack11l1lll_opy_ (u"ࠥࠦ૬"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l1lll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૭")))):
          with open(args[1], bstack11l1lll_opy_ (u"ࠬࡸࠧ૮")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l1lll_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬ૯") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1111l1lll_opy_)
            if bstack11l1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ૰") in CONFIG and str(CONFIG[bstack11l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ૱")]).lower() != bstack11l1lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ૲"):
                bstack111ll11ll_opy_ = bstack1ll1l111_opy_()
                bstack1l1ll1llll_opy_ = bstack11l1lll_opy_ (u"ࠪࠫࠬࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡁࠊࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡁࠊࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡣࡰࡰࡶࡳࡱ࡫࠮ࡦࡴࡵࡳࡷ࠮ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠤ࠯ࠤࡪࡾࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࠨࡽࡦࡨࡵ࡛ࡲ࡭ࡿࠪࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭࠱ࠐࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࠧࠨࠩ૳").format(bstack111ll11ll_opy_=bstack111ll11ll_opy_)
            lines.insert(1, bstack1l1ll1llll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l1lll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૴")), bstack11l1lll_opy_ (u"ࠬࡽࠧ૵")) as bstack1l111ll1l_opy_:
              bstack1l111ll1l_opy_.writelines(lines)
        CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ૶")] = str(bstack1l11l1l11l_opy_) + str(__version__)
        bstack1lllll111l_opy_ = os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ૷")]
        bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack11l1l1l1_opy_(CONFIG, bstack1l11l1l11l_opy_)
        CONFIG[bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ૸")] = bstack1lllll111l_opy_
        CONFIG[bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫૹ")] = bstack1ll1111l11_opy_
        bstack1llll11l1_opy_ = 0 if bstack11l1ll11l_opy_ < 0 else bstack11l1ll11l_opy_
        try:
          if bstack1llll1ll1l_opy_ is True:
            bstack1llll11l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1ll1ll1l_opy_ is True:
            bstack1llll11l1_opy_ = int(threading.current_thread().name)
        except:
          bstack1llll11l1_opy_ = 0
        CONFIG[bstack11l1lll_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥૺ")] = False
        CONFIG[bstack11l1lll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥૻ")] = True
        bstack11lll1l1ll_opy_ = bstack1l11l1ll_opy_(CONFIG, bstack1llll11l1_opy_)
        logger.debug(bstack1l111l1l11_opy_.format(str(bstack11lll1l1ll_opy_)))
        if CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩૼ")):
          bstack111ll1l11_opy_(bstack11lll1l1ll_opy_)
        if bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૽") in CONFIG and bstack11l1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૾") in CONFIG[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૿")][bstack1llll11l1_opy_]:
          bstack1l1l1ll1l1_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଀")][bstack1llll11l1_opy_][bstack11l1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଁ")]
        args.append(os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠫࢃ࠭ଂ")), bstack11l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"), bstack11l1lll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ଄")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lll1l1ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l1lll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤଅ"))
      bstack11l1ll1l1_opy_ = True
      return bstack1l1111ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11ll11111_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l1ll11l_opy_
    global bstack1l1l1ll1l1_opy_
    global bstack1llll1ll1l_opy_
    global bstack1l1ll1ll1l_opy_
    global bstack1l11l1l11l_opy_
    CONFIG[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪଆ")] = str(bstack1l11l1l11l_opy_) + str(__version__)
    bstack1lllll111l_opy_ = os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧଇ")]
    bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack11l1l1l1_opy_(CONFIG, bstack1l11l1l11l_opy_)
    CONFIG[bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଈ")] = bstack1lllll111l_opy_
    CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଉ")] = bstack1ll1111l11_opy_
    bstack1llll11l1_opy_ = 0 if bstack11l1ll11l_opy_ < 0 else bstack11l1ll11l_opy_
    try:
      if bstack1llll1ll1l_opy_ is True:
        bstack1llll11l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1ll1ll1l_opy_ is True:
        bstack1llll11l1_opy_ = int(threading.current_thread().name)
    except:
      bstack1llll11l1_opy_ = 0
    CONFIG[bstack11l1lll_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦଊ")] = True
    bstack11lll1l1ll_opy_ = bstack1l11l1ll_opy_(CONFIG, bstack1llll11l1_opy_)
    logger.debug(bstack1l111l1l11_opy_.format(str(bstack11lll1l1ll_opy_)))
    if CONFIG.get(bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪଋ")):
      bstack111ll1l11_opy_(bstack11lll1l1ll_opy_)
    if bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ") in CONFIG and bstack11l1lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଍") in CONFIG[bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଎")][bstack1llll11l1_opy_]:
      bstack1l1l1ll1l1_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଏ")][bstack1llll11l1_opy_][bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଐ")]
    import urllib
    import json
    if bstack11l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ଑") in CONFIG and str(CONFIG[bstack11l1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ଒")]).lower() != bstack11l1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ଓ"):
        bstack1l11ll11l1_opy_ = bstack1ll1l111_opy_()
        bstack111ll11ll_opy_ = bstack1l11ll11l1_opy_ + urllib.parse.quote(json.dumps(bstack11lll1l1ll_opy_))
    else:
        bstack111ll11ll_opy_ = bstack11l1lll_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪଔ") + urllib.parse.quote(json.dumps(bstack11lll1l1ll_opy_))
    browser = self.connect(bstack111ll11ll_opy_)
    return browser
except Exception as e:
    pass
def bstack11l1l11ll1_opy_():
    global bstack11l1ll1l1_opy_
    global bstack1l11l1l11l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lllll11ll_opy_
        global bstack11ll1llll1_opy_
        if not bstack1l1ll11ll_opy_:
          global bstack1lll1l11_opy_
          if not bstack1lll1l11_opy_:
            from bstack_utils.helper import bstack1l1l11ll1_opy_, bstack11ll1l1l1l_opy_, bstack11ll11l11_opy_
            bstack1lll1l11_opy_ = bstack1l1l11ll1_opy_()
            bstack11ll1l1l1l_opy_(bstack1l11l1l11l_opy_)
            bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack11l1l1l1_opy_(CONFIG, bstack1l11l1l11l_opy_)
            bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦକ"), bstack1ll1111l11_opy_)
          BrowserType.connect = bstack1lllll11ll_opy_
          return
        BrowserType.launch = bstack11ll11111_opy_
        bstack11l1ll1l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11lll1l1l1_opy_
      bstack11l1ll1l1_opy_ = True
    except Exception as e:
      pass
def bstack1lllll111_opy_(context, bstack111l111ll_opy_):
  try:
    context.page.evaluate(bstack11l1lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦଖ"), bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨଗ")+ json.dumps(bstack111l111ll_opy_) + bstack11l1lll_opy_ (u"ࠧࢃࡽࠣଘ"))
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣଙ").format(str(e), traceback.format_exc()))
def bstack1llll1llll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l1lll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଚ"), bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଛ") + json.dumps(message) + bstack11l1lll_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬଜ") + json.dumps(level) + bstack11l1lll_opy_ (u"ࠪࢁࢂ࠭ଝ"))
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦଞ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1lll111ll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11lll1l_opy_(self, url):
  global bstack1llll1ll_opy_
  try:
    bstack1l11l111ll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll11l1lll_opy_.format(str(err)))
  try:
    bstack1llll1ll_opy_(self, url)
  except Exception as e:
    try:
      bstack11l1ll1111_opy_ = str(e)
      if any(err_msg in bstack11l1ll1111_opy_ for err_msg in bstack1lllll11_opy_):
        bstack1l11l111ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll11l1lll_opy_.format(str(err)))
    raise e
def bstack1ll11l11_opy_(self):
  global bstack111111ll_opy_
  bstack111111ll_opy_ = self
  return
def bstack11lllll1ll_opy_(self):
  global bstack11ll11ll11_opy_
  bstack11ll11ll11_opy_ = self
  return
def bstack111111l1_opy_(test_name, bstack1l11lll1ll_opy_):
  global CONFIG
  if percy.bstack1lll1l11ll_opy_() == bstack11l1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥଟ"):
    bstack11ll1lll11_opy_ = os.path.relpath(bstack1l11lll1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11ll1lll11_opy_)
    bstack11l11ll1ll_opy_ = suite_name + bstack11l1lll_opy_ (u"ࠨ࠭ࠣଠ") + test_name
    threading.current_thread().percySessionName = bstack11l11ll1ll_opy_
def bstack111lll1ll_opy_(self, test, *args, **kwargs):
  global bstack11l1ll11ll_opy_
  test_name = None
  bstack1l11lll1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l11lll1ll_opy_ = str(test.source)
  bstack111111l1_opy_(test_name, bstack1l11lll1ll_opy_)
  bstack11l1ll11ll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1ll111_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack11l1l1lll_opy_(driver, bstack11l11ll1ll_opy_):
  if not bstack1l11111ll_opy_ and bstack11l11ll1ll_opy_:
      bstack1l1l111lll_opy_ = {
          bstack11l1lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଡ"): bstack11l1lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଢ"),
          bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଣ"): {
              bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨତ"): bstack11l11ll1ll_opy_
          }
      }
      bstack11l111llll_opy_ = bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩଥ").format(json.dumps(bstack1l1l111lll_opy_))
      driver.execute_script(bstack11l111llll_opy_)
  if bstack1llllll111_opy_:
      bstack1ll1111ll_opy_ = {
          bstack11l1lll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଦ"): bstack11l1lll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨଧ"),
          bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪନ"): {
              bstack11l1lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭଩"): bstack11l11ll1ll_opy_ + bstack11l1lll_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫପ"),
              bstack11l1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଫ"): bstack11l1lll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩବ")
          }
      }
      if bstack1llllll111_opy_.status == bstack11l1lll_opy_ (u"ࠬࡖࡁࡔࡕࠪଭ"):
          bstack11111lll_opy_ = bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫମ").format(json.dumps(bstack1ll1111ll_opy_))
          driver.execute_script(bstack11111lll_opy_)
          bstack11ll1ll1_opy_(driver, bstack11l1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଯ"))
      elif bstack1llllll111_opy_.status == bstack11l1lll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ର"):
          reason = bstack11l1lll_opy_ (u"ࠤࠥ଱")
          bstack1ll1lll11l_opy_ = bstack11l11ll1ll_opy_ + bstack11l1lll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫଲ")
          if bstack1llllll111_opy_.message:
              reason = str(bstack1llllll111_opy_.message)
              bstack1ll1lll11l_opy_ = bstack1ll1lll11l_opy_ + bstack11l1lll_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫଳ") + reason
          bstack1ll1111ll_opy_[bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ଴")] = {
              bstack11l1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬଵ"): bstack11l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ଶ"),
              bstack11l1lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ଷ"): bstack1ll1lll11l_opy_
          }
          bstack11111lll_opy_ = bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧସ").format(json.dumps(bstack1ll1111ll_opy_))
          driver.execute_script(bstack11111lll_opy_)
          bstack11ll1ll1_opy_(driver, bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪହ"), reason)
          bstack1lll111ll_opy_(reason, str(bstack1llllll111_opy_), str(bstack11l1ll11l_opy_), logger)
@measure(event_name=EVENTS.bstack1l11l1l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack11l1l1lll1_opy_(driver, test):
  if percy.bstack1lll1l11ll_opy_() == bstack11l1lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ଺") and percy.bstack1l1lll1ll_opy_() == bstack11l1lll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ଻"):
      bstack11l1l111ll_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦ଼ࠩ"), None)
      bstack111l1l1l1_opy_(driver, bstack11l1l111ll_opy_, test)
  if (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫଽ"), None) and
      bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧା"), None)) or (
      bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩି"), None) and
      bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬୀ"), None)):
      logger.info(bstack11l1lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦୁ"))
      bstack1l11111lll_opy_.bstack11l1l1ll1_opy_(driver, name=test.name, path=test.source)
def bstack1llll1l1l_opy_(test, bstack11l11ll1ll_opy_):
    try:
      bstack11llll111l_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪୂ")] = bstack11l11ll1ll_opy_
      if bstack1llllll111_opy_:
        if bstack1llllll111_opy_.status == bstack11l1lll_opy_ (u"࠭ࡐࡂࡕࡖࠫୃ"):
          data[bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧୄ")] = bstack11l1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ୅")
        elif bstack1llllll111_opy_.status == bstack11l1lll_opy_ (u"ࠩࡉࡅࡎࡒࠧ୆"):
          data[bstack11l1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪେ")] = bstack11l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୈ")
          if bstack1llllll111_opy_.message:
            data[bstack11l1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ୉")] = str(bstack1llllll111_opy_.message)
      user = CONFIG[bstack11l1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ୊")]
      key = CONFIG[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪୋ")]
      url = bstack11l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭ୌ").format(user, key, bstack111l111l1_opy_)
      headers = {
        bstack11l1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ୍"): bstack11l1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭୎"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡩࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠣ୏"), datetime.datetime.now() - bstack11llll111l_opy_)
    except Exception as e:
      logger.error(bstack1llllll1l1_opy_.format(str(e)))
def bstack1l1ll1l11l_opy_(test, bstack11l11ll1ll_opy_):
  global CONFIG
  global bstack11ll11ll11_opy_
  global bstack111111ll_opy_
  global bstack111l111l1_opy_
  global bstack1llllll111_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack11l11l11_opy_
  global bstack1lll1l111_opy_
  global bstack1l1llllll1_opy_
  global bstack1ll1ll1111_opy_
  global bstack11l111ll_opy_
  global bstack1l1111l1ll_opy_
  try:
    if not bstack111l111l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠬࢄࠧ୐")), bstack11l1lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭୑"), bstack11l1lll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ୒"))) as f:
        bstack1ll11111_opy_ = json.loads(bstack11l1lll_opy_ (u"ࠣࡽࠥ୓") + f.read().strip() + bstack11l1lll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ୔") + bstack11l1lll_opy_ (u"ࠥࢁࠧ୕"))
        bstack111l111l1_opy_ = bstack1ll11111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l111ll_opy_:
    for driver in bstack11l111ll_opy_:
      if bstack111l111l1_opy_ == driver.session_id:
        if test:
          bstack11l1l1lll1_opy_(driver, test)
        bstack11l1l1lll_opy_(driver, bstack11l11ll1ll_opy_)
  elif bstack111l111l1_opy_:
    bstack1llll1l1l_opy_(test, bstack11l11ll1ll_opy_)
  if bstack11ll11ll11_opy_:
    bstack1lll1l111_opy_(bstack11ll11ll11_opy_)
  if bstack111111ll_opy_:
    bstack1l1llllll1_opy_(bstack111111ll_opy_)
  if bstack1l1lll1l1_opy_:
    bstack1ll1ll1111_opy_()
def bstack1l111ll111_opy_(self, test, *args, **kwargs):
  bstack11l11ll1ll_opy_ = None
  if test:
    bstack11l11ll1ll_opy_ = str(test.name)
  bstack1l1ll1l11l_opy_(test, bstack11l11ll1ll_opy_)
  bstack11l11l11_opy_(self, test, *args, **kwargs)
def bstack11llllllll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1llll1l1_opy_
  global CONFIG
  global bstack11l111ll_opy_
  global bstack111l111l1_opy_
  bstack1llll11l_opy_ = None
  try:
    if bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୖ"), None) or bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୗ"), None):
      try:
        if not bstack111l111l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"࠭ࡾࠨ୘")), bstack11l1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୙"), bstack11l1lll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୚"))) as f:
            bstack1ll11111_opy_ = json.loads(bstack11l1lll_opy_ (u"ࠤࡾࠦ୛") + f.read().strip() + bstack11l1lll_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬଡ଼") + bstack11l1lll_opy_ (u"ࠦࢂࠨଢ଼"))
            bstack111l111l1_opy_ = bstack1ll11111_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11l111ll_opy_:
        for driver in bstack11l111ll_opy_:
          if bstack111l111l1_opy_ == driver.session_id:
            bstack1llll11l_opy_ = driver
    bstack11ll1l111_opy_ = bstack1l11111lll_opy_.bstack1ll1l1l1ll_opy_(test.tags)
    if bstack1llll11l_opy_:
      threading.current_thread().isA11yTest = bstack1l11111lll_opy_.bstack1lll1ll11l_opy_(bstack1llll11l_opy_, bstack11ll1l111_opy_)
      threading.current_thread().isAppA11yTest = bstack1l11111lll_opy_.bstack1lll1ll11l_opy_(bstack1llll11l_opy_, bstack11ll1l111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11ll1l111_opy_
      threading.current_thread().isAppA11yTest = bstack11ll1l111_opy_
  except:
    pass
  bstack1l1llll1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llllll111_opy_
  try:
    bstack1llllll111_opy_ = self._test
  except:
    bstack1llllll111_opy_ = self.test
def bstack1ll11111l1_opy_():
  global bstack11l111ll1_opy_
  try:
    if os.path.exists(bstack11l111ll1_opy_):
      os.remove(bstack11l111ll1_opy_)
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୞") + str(e))
def bstack1ll1l11l11_opy_():
  global bstack11l111ll1_opy_
  bstack1ll1llll1_opy_ = {}
  try:
    if not os.path.isfile(bstack11l111ll1_opy_):
      with open(bstack11l111ll1_opy_, bstack11l1lll_opy_ (u"࠭ࡷࠨୟ")):
        pass
      with open(bstack11l111ll1_opy_, bstack11l1lll_opy_ (u"ࠢࡸ࠭ࠥୠ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11l111ll1_opy_):
      bstack1ll1llll1_opy_ = json.load(open(bstack11l111ll1_opy_, bstack11l1lll_opy_ (u"ࠨࡴࡥࠫୡ")))
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫୢ") + str(e))
  finally:
    return bstack1ll1llll1_opy_
def bstack1l1lll1l11_opy_(platform_index, item_index):
  global bstack11l111ll1_opy_
  try:
    bstack1ll1llll1_opy_ = bstack1ll1l11l11_opy_()
    bstack1ll1llll1_opy_[item_index] = platform_index
    with open(bstack11l111ll1_opy_, bstack11l1lll_opy_ (u"ࠥࡻ࠰ࠨୣ")) as outfile:
      json.dump(bstack1ll1llll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ୤") + str(e))
def bstack111lll111_opy_(bstack11llll1l11_opy_):
  global CONFIG
  bstack11l1111l_opy_ = bstack11l1lll_opy_ (u"ࠬ࠭୥")
  if not bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୦") in CONFIG:
    logger.info(bstack11l1lll_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ୧"))
  try:
    platform = CONFIG[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୨")][bstack11llll1l11_opy_]
    if bstack11l1lll_opy_ (u"ࠩࡲࡷࠬ୩") in platform:
      bstack11l1111l_opy_ += str(platform[bstack11l1lll_opy_ (u"ࠪࡳࡸ࠭୪")]) + bstack11l1lll_opy_ (u"ࠫ࠱ࠦࠧ୫")
    if bstack11l1lll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୬") in platform:
      bstack11l1111l_opy_ += str(platform[bstack11l1lll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ୭")]) + bstack11l1lll_opy_ (u"ࠧ࠭ࠢࠪ୮")
    if bstack11l1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ୯") in platform:
      bstack11l1111l_opy_ += str(platform[bstack11l1lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭୰")]) + bstack11l1lll_opy_ (u"ࠪ࠰ࠥ࠭ୱ")
    if bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୲") in platform:
      bstack11l1111l_opy_ += str(platform[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ୳")]) + bstack11l1lll_opy_ (u"࠭ࠬࠡࠩ୴")
    if bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୵") in platform:
      bstack11l1111l_opy_ += str(platform[bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୶")]) + bstack11l1lll_opy_ (u"ࠩ࠯ࠤࠬ୷")
    if bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ୸") in platform:
      bstack11l1111l_opy_ += str(platform[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ୹")]) + bstack11l1lll_opy_ (u"ࠬ࠲ࠠࠨ୺")
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭୻") + str(e))
  finally:
    if bstack11l1111l_opy_[len(bstack11l1111l_opy_) - 2:] == bstack11l1lll_opy_ (u"ࠧ࠭ࠢࠪ୼"):
      bstack11l1111l_opy_ = bstack11l1111l_opy_[:-2]
    return bstack11l1111l_opy_
def bstack1l1l111l1l_opy_(path, bstack11l1111l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1l1l11l_opy_ = ET.parse(path)
    bstack11l1ll1l11_opy_ = bstack1l1l1l11l_opy_.getroot()
    bstack1l1l1l11ll_opy_ = None
    for suite in bstack11l1ll1l11_opy_.iter(bstack11l1lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ୽")):
      if bstack11l1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ୾") in suite.attrib:
        suite.attrib[bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ୿")] += bstack11l1lll_opy_ (u"ࠫࠥ࠭஀") + bstack11l1111l_opy_
        bstack1l1l1l11ll_opy_ = suite
    bstack11ll1111l_opy_ = None
    for robot in bstack11l1ll1l11_opy_.iter(bstack11l1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஁")):
      bstack11ll1111l_opy_ = robot
    bstack11l1ll11_opy_ = len(bstack11ll1111l_opy_.findall(bstack11l1lll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஂ")))
    if bstack11l1ll11_opy_ == 1:
      bstack11ll1111l_opy_.remove(bstack11ll1111l_opy_.findall(bstack11l1lll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ஃ"))[0])
      bstack1ll11l11ll_opy_ = ET.Element(bstack11l1lll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஄"), attrib={bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧஅ"): bstack11l1lll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪஆ"), bstack11l1lll_opy_ (u"ࠫ࡮ࡪࠧஇ"): bstack11l1lll_opy_ (u"ࠬࡹ࠰ࠨஈ")})
      bstack11ll1111l_opy_.insert(1, bstack1ll11l11ll_opy_)
      bstack1l11ll111l_opy_ = None
      for suite in bstack11ll1111l_opy_.iter(bstack11l1lll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஉ")):
        bstack1l11ll111l_opy_ = suite
      bstack1l11ll111l_opy_.append(bstack1l1l1l11ll_opy_)
      bstack11ll11ll1_opy_ = None
      for status in bstack1l1l1l11ll_opy_.iter(bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧஊ")):
        bstack11ll11ll1_opy_ = status
      bstack1l11ll111l_opy_.append(bstack11ll11ll1_opy_)
    bstack1l1l1l11l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭஋") + str(e))
def bstack1ll111lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11llll11l1_opy_
  global CONFIG
  if bstack11l1lll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ஌") in options:
    del options[bstack11l1lll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ஍")]
  bstack1l1ll1l11_opy_ = bstack1ll1l11l11_opy_()
  for bstack11l11l11l1_opy_ in bstack1l1ll1l11_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l1lll_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫஎ"), str(bstack11l11l11l1_opy_), bstack11l1lll_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩஏ"))
    bstack1l1l111l1l_opy_(path, bstack111lll111_opy_(bstack1l1ll1l11_opy_[bstack11l11l11l1_opy_]))
  bstack1ll11111l1_opy_()
  return bstack11llll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l111l11l_opy_(self, ff_profile_dir):
  global bstack1lll11ll1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll11ll1l_opy_(self, ff_profile_dir)
def bstack1l1l1llll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11ll1l11l_opy_
  bstack1l11ll1l1l_opy_ = []
  if bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஐ") in CONFIG:
    bstack1l11ll1l1l_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஑")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤஒ")],
      pabot_args[bstack11l1lll_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥஓ")],
      argfile,
      pabot_args.get(bstack11l1lll_opy_ (u"ࠥ࡬࡮ࡼࡥࠣஔ")),
      pabot_args[bstack11l1lll_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢக")],
      platform[0],
      bstack11ll1l11l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ஖")] or [(bstack11l1lll_opy_ (u"ࠨࠢ஗"), None)]
    for platform in enumerate(bstack1l11ll1l1l_opy_)
  ]
def bstack1llllll11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11ll1l1ll_opy_=bstack11l1lll_opy_ (u"ࠧࠨ஘")):
  global bstack11l11lllll_opy_
  self.platform_index = platform_index
  self.bstack1l1ll1111l_opy_ = bstack11ll1l1ll_opy_
  bstack11l11lllll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l11l11l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11l1l11ll_opy_
  global bstack1l1lll11l_opy_
  bstack1111ll1l_opy_ = copy.deepcopy(item)
  if not bstack11l1lll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪங") in item.options:
    bstack1111ll1l_opy_.options[bstack11l1lll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫச")] = []
  bstack1l1111l1_opy_ = bstack1111ll1l_opy_.options[bstack11l1lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஛")].copy()
  for v in bstack1111ll1l_opy_.options[bstack11l1lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ஜ")]:
    if bstack11l1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ஝") in v:
      bstack1l1111l1_opy_.remove(v)
    if bstack11l1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ஞ") in v:
      bstack1l1111l1_opy_.remove(v)
    if bstack11l1lll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫட") in v:
      bstack1l1111l1_opy_.remove(v)
  bstack1l1111l1_opy_.insert(0, bstack11l1lll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ஠").format(bstack1111ll1l_opy_.platform_index))
  bstack1l1111l1_opy_.insert(0, bstack11l1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩ஡").format(bstack1111ll1l_opy_.bstack1l1ll1111l_opy_))
  bstack1111ll1l_opy_.options[bstack11l1lll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஢")] = bstack1l1111l1_opy_
  if bstack1l1lll11l_opy_:
    bstack1111ll1l_opy_.options[bstack11l1lll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ண")].insert(0, bstack11l1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨத").format(bstack1l1lll11l_opy_))
  return bstack11l1l11ll_opy_(caller_id, datasources, is_last, bstack1111ll1l_opy_, outs_dir)
def bstack1l11lll11_opy_(command, item_index):
  if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ஥")):
    os.environ[bstack11l1lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ஦")] = json.dumps(CONFIG[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஧")][item_index % bstack1l1l11ll_opy_])
  global bstack1l1lll11l_opy_
  if bstack1l1lll11l_opy_:
    command[0] = command[0].replace(bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨந"), bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧன") + str(
      item_index) + bstack11l1lll_opy_ (u"ࠫࠥ࠭ப") + bstack1l1lll11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஫"),
                                    bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ஬") + str(item_index), 1)
def bstack1l1ll111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11ll1l1lll_opy_
  bstack1l11lll11_opy_(command, item_index)
  return bstack11ll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11llll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11ll1l1lll_opy_
  bstack1l11lll11_opy_(command, item_index)
  return bstack11ll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1111111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11ll1l1lll_opy_
  bstack1l11lll11_opy_(command, item_index)
  return bstack11ll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack111ll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack11ll1l1lll_opy_
  bstack1l11lll11_opy_(command, item_index)
  return bstack11ll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1ll1lll_opy_(self, runner, quiet=False, capture=True):
  global bstack1llll111ll_opy_
  bstack1l11lll111_opy_ = bstack1llll111ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11l1lll_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ஭")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l1lll_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬம")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11lll111_opy_
def bstack1ll11l1l11_opy_(runner, hook_name, context, element, bstack1l11l111_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l1ll111ll_opy_.bstack11lll1111l_opy_(hook_name, element)
    bstack1l11l111_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l1ll111ll_opy_.bstack111ll11l1_opy_(element)
      if hook_name not in [bstack11l1lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ய"), bstack11l1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ர")] and args and hasattr(args[0], bstack11l1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫற")):
        args[0].error_message = bstack11l1lll_opy_ (u"ࠬ࠭ல")
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨள").format(str(e)))
@measure(event_name=EVENTS.bstack11ll11l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_, hook_type=bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥழ"), bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l111l1l1_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    if runner.hooks.get(bstack11l1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧவ")).__name__ != bstack11l1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧஶ"):
      bstack1ll11l1l11_opy_(runner, name, context, runner, bstack1l11l111_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111l11ll_opy_(bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩஷ")) else context.browser
      runner.driver_initialised = bstack11l1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣஸ")
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩஹ").format(str(e)))
def bstack1lll1l1ll1_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    bstack1ll11l1l11_opy_(runner, name, context, context.feature, bstack1l11l111_opy_, *args)
    try:
      if not bstack1l11111ll_opy_:
        bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll_opy_(bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ஺")) else context.browser
        if is_driver_active(bstack1llll11l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ஻")
          bstack111l111ll_opy_ = str(runner.feature.name)
          bstack1lllll111_opy_(context, bstack111l111ll_opy_)
          bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭஼") + json.dumps(bstack111l111ll_opy_) + bstack11l1lll_opy_ (u"ࠩࢀࢁࠬ஽"))
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪா").format(str(e)))
def bstack1ll111ll1_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    if hasattr(context, bstack11l1lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ி")):
        bstack1l1ll111ll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11l1lll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧீ")) else context.feature
    bstack1ll11l1l11_opy_(runner, name, context, target, bstack1l11l111_opy_, *args)
@measure(event_name=EVENTS.bstack1l1lllll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1ll1ll1l_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l1ll111ll_opy_.start_test(context)
    bstack1ll11l1l11_opy_(runner, name, context, context.scenario, bstack1l11l111_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1lll1l1l_opy_.bstack1l1111lll_opy_(context, *args)
    try:
      bstack1llll11l_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬு"), context.browser)
      if is_driver_active(bstack1llll11l_opy_):
        bstack1lll11111l_opy_.bstack111l1ll11_opy_(bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ூ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l1lll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௃")
        if (not bstack1l11111ll_opy_):
          scenario_name = args[0].name
          feature_name = bstack111l111ll_opy_ = str(runner.feature.name)
          bstack111l111ll_opy_ = feature_name + bstack11l1lll_opy_ (u"ࠩࠣ࠱ࠥ࠭௄") + scenario_name
          if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௅"):
            bstack1lllll111_opy_(context, bstack111l111ll_opy_)
            bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩெ") + json.dumps(bstack111l111ll_opy_) + bstack11l1lll_opy_ (u"ࠬࢃࡽࠨே"))
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧை").format(str(e)))
@measure(event_name=EVENTS.bstack11ll11l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_, hook_type=bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦ௉"), bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1lll1l1111_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    bstack1ll11l1l11_opy_(runner, name, context, args[0], bstack1l11l111_opy_, *args)
    try:
      bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll_opy_(bstack11l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧொ")) else context.browser
      if is_driver_active(bstack1llll11l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢோ")
        bstack1l1ll111ll_opy_.bstack1111ll1l1_opy_(args[0])
        if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣௌ"):
          feature_name = bstack111l111ll_opy_ = str(runner.feature.name)
          bstack111l111ll_opy_ = feature_name + bstack11l1lll_opy_ (u"ࠫࠥ࠳ࠠࠨ்") + context.scenario.name
          bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௎") + json.dumps(bstack111l111ll_opy_) + bstack11l1lll_opy_ (u"࠭ࡽࡾࠩ௏"))
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫௐ").format(str(e)))
@measure(event_name=EVENTS.bstack11ll11l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_, hook_type=bstack11l1lll_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦ௑"), bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l1l1ll111_opy_(runner, name, context, bstack1l11l111_opy_, *args):
  bstack1l1ll111ll_opy_.bstack11111l11_opy_(args[0])
  try:
    bstack11l1l111l1_opy_ = args[0].status.name
    bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௒") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1llll11l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11l1lll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ௓")
        feature_name = bstack111l111ll_opy_ = str(runner.feature.name)
        bstack111l111ll_opy_ = feature_name + bstack11l1lll_opy_ (u"ࠫࠥ࠳ࠠࠨ௔") + context.scenario.name
        bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௕") + json.dumps(bstack111l111ll_opy_) + bstack11l1lll_opy_ (u"࠭ࡽࡾࠩ௖"))
    if str(bstack11l1l111l1_opy_).lower() == bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧௗ"):
      bstack1l111111ll_opy_ = bstack11l1lll_opy_ (u"ࠨࠩ௘")
      bstack1ll11111l_opy_ = bstack11l1lll_opy_ (u"ࠩࠪ௙")
      bstack11ll1l1ll1_opy_ = bstack11l1lll_opy_ (u"ࠪࠫ௚")
      try:
        import traceback
        bstack1l111111ll_opy_ = runner.exception.__class__.__name__
        bstack1ll111llll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll11111l_opy_ = bstack11l1lll_opy_ (u"ࠫࠥ࠭௛").join(bstack1ll111llll_opy_)
        bstack11ll1l1ll1_opy_ = bstack1ll111llll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11l1l111_opy_.format(str(e)))
      bstack1l111111ll_opy_ += bstack11ll1l1ll1_opy_
      bstack1llll1llll_opy_(context, json.dumps(str(args[0].name) + bstack11l1lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௜") + str(bstack1ll11111l_opy_)),
                          bstack11l1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௝"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௞"):
        bstack1l1111l1l_opy_(getattr(context, bstack11l1lll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭௟"), None), bstack11l1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௠"), bstack1l111111ll_opy_)
        bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௡") + json.dumps(str(args[0].name) + bstack11l1lll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ௢") + str(bstack1ll11111l_opy_)) + bstack11l1lll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ௣"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ௤"):
        bstack11ll1ll1_opy_(bstack1llll11l_opy_, bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௥"), bstack11l1lll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ௦") + str(bstack1l111111ll_opy_))
    else:
      bstack1llll1llll_opy_(context, bstack11l1lll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ௧"), bstack11l1lll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ௨"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௩"):
        bstack1l1111l1l_opy_(getattr(context, bstack11l1lll_opy_ (u"ࠬࡶࡡࡨࡧࠪ௪"), None), bstack11l1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௫"))
      bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௬") + json.dumps(str(args[0].name) + bstack11l1lll_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ௭")) + bstack11l1lll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ௮"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௯"):
        bstack11ll1ll1_opy_(bstack1llll11l_opy_, bstack11l1lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ௰"))
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ௱").format(str(e)))
  bstack1ll11l1l11_opy_(runner, name, context, args[0], bstack1l11l111_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l1111ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1ll11lllll_opy_(runner, name, context, bstack1l11l111_opy_, *args):
  bstack1l1ll111ll_opy_.end_test(args[0])
  try:
    bstack1l1l1llll1_opy_ = args[0].status.name
    bstack1llll11l_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௲"), context.browser)
    bstack1l1lll1l1l_opy_.bstack1ll111lll_opy_(bstack1llll11l_opy_)
    if str(bstack1l1l1llll1_opy_).lower() == bstack11l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௳"):
      bstack1l111111ll_opy_ = bstack11l1lll_opy_ (u"ࠨࠩ௴")
      bstack1ll11111l_opy_ = bstack11l1lll_opy_ (u"ࠩࠪ௵")
      bstack11ll1l1ll1_opy_ = bstack11l1lll_opy_ (u"ࠪࠫ௶")
      try:
        import traceback
        bstack1l111111ll_opy_ = runner.exception.__class__.__name__
        bstack1ll111llll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll11111l_opy_ = bstack11l1lll_opy_ (u"ࠫࠥ࠭௷").join(bstack1ll111llll_opy_)
        bstack11ll1l1ll1_opy_ = bstack1ll111llll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11l1l111_opy_.format(str(e)))
      bstack1l111111ll_opy_ += bstack11ll1l1ll1_opy_
      bstack1llll1llll_opy_(context, json.dumps(str(args[0].name) + bstack11l1lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௸") + str(bstack1ll11111l_opy_)),
                          bstack11l1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௹"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௺") or runner.driver_initialised == bstack11l1lll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ௻"):
        bstack1l1111l1l_opy_(getattr(context, bstack11l1lll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௼"), None), bstack11l1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ௽"), bstack1l111111ll_opy_)
        bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௾") + json.dumps(str(args[0].name) + bstack11l1lll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௿") + str(bstack1ll11111l_opy_)) + bstack11l1lll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ఀ"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఁ") or runner.driver_initialised == bstack11l1lll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨం"):
        bstack11ll1ll1_opy_(bstack1llll11l_opy_, bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩః"), bstack11l1lll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢఄ") + str(bstack1l111111ll_opy_))
    else:
      bstack1llll1llll_opy_(context, bstack11l1lll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧఅ"), bstack11l1lll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥఆ"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఇ") or runner.driver_initialised == bstack11l1lll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఈ"):
        bstack1l1111l1l_opy_(getattr(context, bstack11l1lll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ఉ"), None), bstack11l1lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤఊ"))
      bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨఋ") + json.dumps(str(args[0].name) + bstack11l1lll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣఌ")) + bstack11l1lll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ఍"))
      if runner.driver_initialised == bstack11l1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఎ") or runner.driver_initialised == bstack11l1lll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఏ"):
        bstack11ll1ll1_opy_(bstack1llll11l_opy_, bstack11l1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣఐ"))
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ఑").format(str(e)))
  bstack1ll11l1l11_opy_(runner, name, context, context.scenario, bstack1l11l111_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11ll1ll111_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l1lll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఒ")) else context.feature
    bstack1ll11l1l11_opy_(runner, name, context, target, bstack1l11l111_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11llll1ll1_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    try:
      bstack1llll11l_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఓ"), context.browser)
      bstack1l1lll1l_opy_ = bstack11l1lll_opy_ (u"ࠬ࠭ఔ")
      if context.failed is True:
        bstack11l111l1l1_opy_ = []
        bstack111lll1l_opy_ = []
        bstack11lllll11_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11l111l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll111llll_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1l1111_opy_ = bstack11l1lll_opy_ (u"࠭ࠠࠨక").join(bstack1ll111llll_opy_)
            bstack111lll1l_opy_.append(bstack1ll1l1111_opy_)
            bstack11lllll11_opy_.append(bstack1ll111llll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11l1l111_opy_.format(str(e)))
        bstack1l111111ll_opy_ = bstack11l1lll_opy_ (u"ࠧࠨఖ")
        for i in range(len(bstack11l111l1l1_opy_)):
          bstack1l111111ll_opy_ += bstack11l111l1l1_opy_[i] + bstack11lllll11_opy_[i] + bstack11l1lll_opy_ (u"ࠨ࡞ࡱࠫగ")
        bstack1l1lll1l_opy_ = bstack11l1lll_opy_ (u"ࠩࠣࠫఘ").join(bstack111lll1l_opy_)
        if runner.driver_initialised in [bstack11l1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦఙ"), bstack11l1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣచ")]:
          bstack1llll1llll_opy_(context, bstack1l1lll1l_opy_, bstack11l1lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦఛ"))
          bstack1l1111l1l_opy_(getattr(context, bstack11l1lll_opy_ (u"࠭ࡰࡢࡩࡨࠫజ"), None), bstack11l1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢఝ"), bstack1l111111ll_opy_)
          bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ఞ") + json.dumps(bstack1l1lll1l_opy_) + bstack11l1lll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩట"))
          bstack11ll1ll1_opy_(bstack1llll11l_opy_, bstack11l1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥఠ"), bstack11l1lll_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤడ") + str(bstack1l111111ll_opy_))
          bstack1l1111ll1l_opy_ = bstack11llll11ll_opy_(bstack1l1lll1l_opy_, runner.feature.name, logger)
          if (bstack1l1111ll1l_opy_ != None):
            bstack11l1ll1lll_opy_.append(bstack1l1111ll1l_opy_)
      else:
        if runner.driver_initialised in [bstack11l1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨఢ"), bstack11l1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥణ")]:
          bstack1llll1llll_opy_(context, bstack11l1lll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥత") + str(runner.feature.name) + bstack11l1lll_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥథ"), bstack11l1lll_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢద"))
          bstack1l1111l1l_opy_(getattr(context, bstack11l1lll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨధ"), None), bstack11l1lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦన"))
          bstack1llll11l_opy_.execute_script(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ఩") + json.dumps(bstack11l1lll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤప") + str(runner.feature.name) + bstack11l1lll_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤఫ")) + bstack11l1lll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧబ"))
          bstack11ll1ll1_opy_(bstack1llll11l_opy_, bstack11l1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩభ"))
          bstack1l1111ll1l_opy_ = bstack11llll11ll_opy_(bstack1l1lll1l_opy_, runner.feature.name, logger)
          if (bstack1l1111ll1l_opy_ != None):
            bstack11l1ll1lll_opy_.append(bstack1l1111ll1l_opy_)
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬమ").format(str(e)))
    bstack1ll11l1l11_opy_(runner, name, context, context.feature, bstack1l11l111_opy_, *args)
@measure(event_name=EVENTS.bstack11ll11l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_, hook_type=bstack11l1lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨయ"), bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1111ll111_opy_(runner, name, context, bstack1l11l111_opy_, *args):
    bstack1ll11l1l11_opy_(runner, name, context, runner, bstack1l11l111_opy_, *args)
def bstack1l1llll1l_opy_(self, name, context, *args):
  if bstack1l1ll11ll_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l1l11ll_opy_
    bstack1l111l11_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨర")][platform_index]
    os.environ[bstack11l1lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧఱ")] = json.dumps(bstack1l111l11_opy_)
  global bstack1l11l111_opy_
  if not hasattr(self, bstack11l1lll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬల")):
    self.driver_initialised = None
  bstack11111111l_opy_ = {
      bstack11l1lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬళ"): bstack1l111l1l1_opy_,
      bstack11l1lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪఴ"): bstack1lll1l1ll1_opy_,
      bstack11l1lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧవ"): bstack1ll111ll1_opy_,
      bstack11l1lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭శ"): bstack1ll1ll1l_opy_,
      bstack11l1lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪష"): bstack1lll1l1111_opy_,
      bstack11l1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪస"): bstack1l1l1ll111_opy_,
      bstack11l1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨహ"): bstack1ll11lllll_opy_,
      bstack11l1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫ఺"): bstack11ll1ll111_opy_,
      bstack11l1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ఻"): bstack11llll1ll1_opy_,
      bstack11l1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ఼࠭"): bstack1111ll111_opy_
  }
  handler = bstack11111111l_opy_.get(name, bstack1l11l111_opy_)
  handler(self, name, context, bstack1l11l111_opy_, *args)
  if name in [bstack11l1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫఽ"), bstack11l1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ా"), bstack11l1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩి")]:
    try:
      bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll_opy_(bstack11l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ీ")) else context.browser
      bstack111l11111_opy_ = (
        (name == bstack11l1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫు") and self.driver_initialised == bstack11l1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨూ")) or
        (name == bstack11l1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪృ") and self.driver_initialised == bstack11l1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧౄ")) or
        (name == bstack11l1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౅") and self.driver_initialised in [bstack11l1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣె"), bstack11l1lll_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢే")]) or
        (name == bstack11l1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬై") and self.driver_initialised == bstack11l1lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౉"))
      )
      if bstack111l11111_opy_:
        self.driver_initialised = None
        bstack1llll11l_opy_.quit()
    except Exception:
      pass
def bstack1ll1lll1l_opy_(config, startdir):
  return bstack11l1lll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣొ").format(bstack11l1lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥో"))
notset = Notset()
def bstack11l1l11l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11l11lll_opy_
  if str(name).lower() == bstack11l1lll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬౌ"):
    return bstack11l1lll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯్ࠧ")
  else:
    return bstack1l11l11lll_opy_(self, name, default, skip)
def bstack1l11llll_opy_(item, when):
  global bstack1ll111111l_opy_
  try:
    bstack1ll111111l_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll1l1llll_opy_():
  return
def bstack1l111llll_opy_(type, name, status, reason, bstack1llll111_opy_, bstack11ll11l1_opy_):
  bstack1l1l111lll_opy_ = {
    bstack11l1lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ౎"): type,
    bstack11l1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ౏"): {}
  }
  if type == bstack11l1lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ౐"):
    bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭౑")][bstack11l1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ౒")] = bstack1llll111_opy_
    bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౓")][bstack11l1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫ౔")] = json.dumps(str(bstack11ll11l1_opy_))
  if type == bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨౕ"):
    bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶౖࠫ")][bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౗")] = name
  if type == bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ౘ"):
    bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౙ")][bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౚ")] = status
    if status == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౛"):
      bstack1l1l111lll_opy_[bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౜")][bstack11l1lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨౝ")] = json.dumps(str(reason))
  bstack11l111llll_opy_ = bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౞").format(json.dumps(bstack1l1l111lll_opy_))
  return bstack11l111llll_opy_
def bstack11lll11l11_opy_(driver_command, response):
    if driver_command == bstack11l1lll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ౟"):
        bstack1lll11111l_opy_.bstack1111lll1_opy_({
            bstack11l1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪౠ"): response[bstack11l1lll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫౡ")],
            bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ౢ"): bstack1lll11111l_opy_.current_test_uuid()
        })
def bstack1111llll1_opy_(item, call, rep):
  global bstack1lll1lllll_opy_
  global bstack11l111ll_opy_
  global bstack1l11111ll_opy_
  name = bstack11l1lll_opy_ (u"ࠧࠨౣ")
  try:
    if rep.when == bstack11l1lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭౤"):
      bstack111l111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l11111ll_opy_:
          name = str(rep.nodeid)
          bstack11lll1l111_opy_ = bstack1l111llll_opy_(bstack11l1lll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౥"), name, bstack11l1lll_opy_ (u"ࠪࠫ౦"), bstack11l1lll_opy_ (u"ࠫࠬ౧"), bstack11l1lll_opy_ (u"ࠬ࠭౨"), bstack11l1lll_opy_ (u"࠭ࠧ౩"))
          threading.current_thread().bstack1l1l11ll11_opy_ = name
          for driver in bstack11l111ll_opy_:
            if bstack111l111l1_opy_ == driver.session_id:
              driver.execute_script(bstack11lll1l111_opy_)
      except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ౪").format(str(e)))
      try:
        bstack1llll11111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ౫"):
          status = bstack11l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౬") if rep.outcome.lower() == bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౭") else bstack11l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౮")
          reason = bstack11l1lll_opy_ (u"ࠬ࠭౯")
          if status == bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౰"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l1lll_opy_ (u"ࠧࡪࡰࡩࡳࠬ౱") if status == bstack11l1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౲") else bstack11l1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౳")
          data = name + bstack11l1lll_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ౴") if status == bstack11l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౵") else name + bstack11l1lll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ౶") + reason
          bstack1ll1lllll_opy_ = bstack1l111llll_opy_(bstack11l1lll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ౷"), bstack11l1lll_opy_ (u"ࠧࠨ౸"), bstack11l1lll_opy_ (u"ࠨࠩ౹"), bstack11l1lll_opy_ (u"ࠩࠪ౺"), level, data)
          for driver in bstack11l111ll_opy_:
            if bstack111l111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1lllll_opy_)
      except Exception as e:
        logger.debug(bstack11l1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ౻").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ౼").format(str(e)))
  bstack1lll1lllll_opy_(item, call, rep)
def bstack111l1l1l1_opy_(driver, bstack1l11111l1l_opy_, test=None):
  global bstack11l1ll11l_opy_
  if test != None:
    bstack11l11l1l11_opy_ = getattr(test, bstack11l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౽"), None)
    bstack1lllll1ll1_opy_ = getattr(test, bstack11l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ౾"), None)
    PercySDK.screenshot(driver, bstack1l11111l1l_opy_, bstack11l11l1l11_opy_=bstack11l11l1l11_opy_, bstack1lllll1ll1_opy_=bstack1lllll1ll1_opy_, bstack111l1llll_opy_=bstack11l1ll11l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l11111l1l_opy_)
@measure(event_name=EVENTS.bstack1111l1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11ll1l1_opy_(driver):
  if bstack1l11l1111l_opy_.bstack1l1ll1l1ll_opy_() is True or bstack1l11l1111l_opy_.capturing() is True:
    return
  bstack1l11l1111l_opy_.bstack11l1lllll_opy_()
  while not bstack1l11l1111l_opy_.bstack1l1ll1l1ll_opy_():
    bstack1lll1lll1l_opy_ = bstack1l11l1111l_opy_.bstack11lll111l_opy_()
    bstack111l1l1l1_opy_(driver, bstack1lll1lll1l_opy_)
  bstack1l11l1111l_opy_.bstack111ll1111_opy_()
def bstack1l111lll1_opy_(sequence, driver_command, response = None, bstack1lll111l11_opy_ = None, args = None):
    try:
      if sequence != bstack11l1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ౿"):
        return
      if percy.bstack1lll1l11ll_opy_() == bstack11l1lll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢಀ"):
        return
      bstack1lll1lll1l_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಁ"), None)
      for command in bstack1l11ll111_opy_:
        if command == driver_command:
          for driver in bstack11l111ll_opy_:
            bstack1l11ll1l1_opy_(driver)
      bstack1ll11ll11_opy_ = percy.bstack1l1lll1ll_opy_()
      if driver_command in bstack11l11llll_opy_[bstack1ll11ll11_opy_]:
        bstack1l11l1111l_opy_.bstack1l11l111l_opy_(bstack1lll1lll1l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1llll1ll1_opy_(framework_name):
  if bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧಂ")):
      return
  bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨಃ"), True)
  global bstack1l11l1l11l_opy_
  global bstack11l1ll1l1_opy_
  global bstack1l1l1l1ll_opy_
  bstack1l11l1l11l_opy_ = framework_name
  logger.info(bstack1l1lll1111_opy_.format(bstack1l11l1l11l_opy_.split(bstack11l1lll_opy_ (u"ࠬ࠳ࠧ಄"))[0]))
  bstack11l11l1l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1ll11ll_opy_:
      Service.start = bstack11l11lll11_opy_
      Service.stop = bstack11ll1l11l1_opy_
      webdriver.Remote.get = bstack1l11lll1l_opy_
      WebDriver.close = bstack1llll11ll1_opy_
      WebDriver.quit = bstack11llll1111_opy_
      webdriver.Remote.__init__ = bstack11l11l1111_opy_
    if not bstack1l1ll11ll_opy_:
        webdriver.Remote.__init__ = bstack1l11111l11_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack11ll11l111_opy_
    bstack11l1ll1l1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1ll11ll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1lllllll_opy_
  except Exception as e:
    pass
  bstack11l1l11ll1_opy_()
  if not bstack11l1ll1l1_opy_:
    bstack1lll1llll1_opy_(bstack11l1lll_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣಅ"), bstack11l1llll11_opy_)
  if bstack1llll1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._11l1ll1l_opy_ = bstack1llll11ll_opy_
    except Exception as e:
      logger.error(bstack1l1l1l111l_opy_.format(str(e)))
  if bstack11111llll_opy_():
    bstack11l111ll1l_opy_(CONFIG, logger)
  if (bstack11l1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಆ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1lll1l11ll_opy_() == bstack11l1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨಇ"):
          bstack1111l11l1_opy_(bstack1l111lll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l111l11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11lllll1ll_opy_
      except Exception as e:
        logger.warn(bstack1l1ll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll11l11_opy_
      except Exception as e:
        logger.debug(bstack11l1l11l11_opy_ + str(e))
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack1l1ll1ll_opy_)
    Output.start_test = bstack111lll1ll_opy_
    Output.end_test = bstack1l111ll111_opy_
    TestStatus.__init__ = bstack11llllllll_opy_
    QueueItem.__init__ = bstack1llllll11_opy_
    pabot._create_items = bstack1l1l1llll_opy_
    try:
      from pabot import __version__ as bstack1l111lll_opy_
      if version.parse(bstack1l111lll_opy_) >= version.parse(bstack11l1lll_opy_ (u"ࠩ࠷࠲࠷࠴࠰ࠨಈ")):
        pabot._run = bstack111ll1ll1_opy_
      elif version.parse(bstack1l111lll_opy_) >= version.parse(bstack11l1lll_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪಉ")):
        pabot._run = bstack1111111l1_opy_
      elif version.parse(bstack1l111lll_opy_) >= version.parse(bstack11l1lll_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫಊ")):
        pabot._run = bstack11llll111_opy_
      else:
        pabot._run = bstack1l1ll111l1_opy_
    except Exception as e:
      pabot._run = bstack1l1ll111l1_opy_
    pabot._create_command_for_execution = bstack11l11l11l_opy_
    pabot._report_results = bstack1ll111lll1_opy_
  if bstack11l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬಋ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack11llllll11_opy_)
    Runner.run_hook = bstack1l1llll1l_opy_
    Step.run = bstack1l1ll1lll_opy_
  if bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಌ") in str(framework_name).lower():
    if not bstack1l1ll11ll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll1lll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll1l1llll_opy_
      Config.getoption = bstack11l1l11l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1111llll1_opy_
    except Exception as e:
      pass
def bstack11lll111ll_opy_():
  global CONFIG
  if bstack11l1lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ಍") in CONFIG and int(CONFIG[bstack11l1lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಎ")]) > 1:
    logger.warn(bstack1l111ll1ll_opy_)
def bstack1lll111lll_opy_(arg, bstack1l111111l_opy_, bstack1lll1ll1_opy_=None):
  global CONFIG
  global bstack1ll1llll11_opy_
  global bstack1l111111_opy_
  global bstack1l1ll11ll_opy_
  global bstack11ll1llll1_opy_
  bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಏ")
  if bstack1l111111l_opy_ and isinstance(bstack1l111111l_opy_, str):
    bstack1l111111l_opy_ = eval(bstack1l111111l_opy_)
  CONFIG = bstack1l111111l_opy_[bstack11l1lll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪಐ")]
  bstack1ll1llll11_opy_ = bstack1l111111l_opy_[bstack11l1lll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ಑")]
  bstack1l111111_opy_ = bstack1l111111l_opy_[bstack11l1lll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧಒ")]
  bstack1l1ll11ll_opy_ = bstack1l111111l_opy_[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩಓ")]
  bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨಔ"), bstack1l1ll11ll_opy_)
  os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಕ")] = bstack1ll1ll1l1l_opy_
  os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨಖ")] = json.dumps(CONFIG)
  os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪಗ")] = bstack1ll1llll11_opy_
  os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬಘ")] = str(bstack1l111111_opy_)
  os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫಙ")] = str(True)
  if bstack1l1lll11_opy_(arg, [bstack11l1lll_opy_ (u"࠭࠭࡯ࠩಚ"), bstack11l1lll_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨಛ")]) != -1:
    os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩಜ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11l1l1ll_opy_)
    return
  bstack11ll11llll_opy_()
  global bstack11l1ll1ll_opy_
  global bstack11l1ll11l_opy_
  global bstack11ll1l11l_opy_
  global bstack1l1lll11l_opy_
  global bstack1ll1l1ll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1llll1ll1l_opy_
  arg.append(bstack11l1lll_opy_ (u"ࠤ࠰࡛ࠧಝ"))
  arg.append(bstack11l1lll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨಞ"))
  arg.append(bstack11l1lll_opy_ (u"ࠦ࠲࡝ࠢಟ"))
  arg.append(bstack11l1lll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦಠ"))
  global bstack11l1l11l1l_opy_
  global bstack1lll11ll1_opy_
  global bstack1lll11ll_opy_
  global bstack1l1llll1l1_opy_
  global bstack1lll11ll1l_opy_
  global bstack11l11lllll_opy_
  global bstack11l1l11ll_opy_
  global bstack1111l1l1_opy_
  global bstack1llll1ll_opy_
  global bstack1l1lllll1l_opy_
  global bstack1l11l11lll_opy_
  global bstack1ll111111l_opy_
  global bstack1lll1lllll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1l11l1l_opy_ = webdriver.Remote.__init__
    bstack1lll11ll1_opy_ = WebDriver.quit
    bstack1111l1l1_opy_ = WebDriver.close
    bstack1llll1ll_opy_ = WebDriver.get
    bstack1lll11ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1ll1lll1_opy_(CONFIG) and bstack1111llll_opy_():
    if bstack111111111_opy_() < version.parse(bstack11l111l111_opy_):
      logger.error(bstack11lllll1_opy_.format(bstack111111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1lllll1l_opy_ = RemoteConnection._11l1ll1l_opy_
      except Exception as e:
        logger.error(bstack1l1l1l111l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11l11lll_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll111111l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11111111_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lll1lllll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧಡ"))
  bstack11ll1l11l_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫಢ"), {}).get(bstack11l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಣ"))
  bstack1llll1ll1l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1l1l11lll_opy_():
      bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.CONNECT, bstack1llll1l111_opy_())
    platform_index = int(os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩತ"), bstack11l1lll_opy_ (u"ࠪ࠴ࠬಥ")))
  else:
    bstack1llll1ll1_opy_(bstack1ll1lll1ll_opy_)
  os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬದ")] = CONFIG[bstack11l1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಧ")]
  os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩನ")] = CONFIG[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ಩")]
  os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫಪ")] = bstack1l1ll11ll_opy_.__str__()
  from _pytest.config import main as bstack11l111l1ll_opy_
  bstack11l11l1l1_opy_ = []
  try:
    bstack1l11lllll_opy_ = bstack11l111l1ll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11ll111ll_opy_()
    if bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ಫ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l11l1l1_opy_.append(bstack11l1l1l11_opy_)
    try:
      bstack11l11l1ll_opy_ = (bstack11l11l1l1_opy_, int(bstack1l11lllll_opy_))
      bstack1lll1ll1_opy_.append(bstack11l11l1ll_opy_)
    except:
      bstack1lll1ll1_opy_.append((bstack11l11l1l1_opy_, bstack1l11lllll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l11l1l1_opy_.append({bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨಬ"): bstack11l1lll_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭ಭ") + os.environ.get(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಮ")), bstack11l1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬಯ"): traceback.format_exc(), bstack11l1lll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ರ"): int(os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨಱ")))})
    bstack1lll1ll1_opy_.append((bstack11l11l1l1_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack11l1lll_opy_ (u"ࠤࡵࡩࡹࡸࡩࡦࡵࠥಲ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11llll1l_opy_ = e.__class__.__name__
    print(bstack11l1lll_opy_ (u"ࠥࠩࡸࡀࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡧࡶࡸࠥࠫࡳࠣಳ") % (bstack11llll1l_opy_, e))
    return 1
def bstack1lllllllll_opy_(arg):
  global bstack1l111lll11_opy_
  bstack1llll1ll1_opy_(bstack1llll111l_opy_)
  os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ಴")] = str(bstack1l111111_opy_)
  retries = bstack1l1l1l1ll1_opy_.bstack11l1ll1ll1_opy_(CONFIG)
  status_code = 0
  if bstack1l1l1l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11lll11111_opy_
    status_code = bstack11lll11111_opy_(arg)
  if status_code != 0:
    bstack1l111lll11_opy_ = status_code
def bstack11l1l1l1ll_opy_():
  logger.info(bstack111l1l11l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫವ"), help=bstack11l1lll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧಶ"))
  parser.add_argument(bstack11l1lll_opy_ (u"ࠧ࠮ࡷࠪಷ"), bstack11l1lll_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬಸ"), help=bstack11l1lll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨಹ"))
  parser.add_argument(bstack11l1lll_opy_ (u"ࠪ࠱ࡰ࠭಺"), bstack11l1lll_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ಻"), help=bstack11l1lll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ಼࠭"))
  parser.add_argument(bstack11l1lll_opy_ (u"࠭࠭ࡧࠩಽ"), bstack11l1lll_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬಾ"), help=bstack11l1lll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಿ"))
  bstack11l1l1ll11_opy_ = parser.parse_args()
  try:
    bstack11l1lll111_opy_ = bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ೀ")
    if bstack11l1l1ll11_opy_.framework and bstack11l1l1ll11_opy_.framework not in (bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪು"), bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬೂ")):
      bstack11l1lll111_opy_ = bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫೃ")
    bstack1l1l1l1lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1lll111_opy_)
    bstack11l11llll1_opy_ = open(bstack1l1l1l1lll_opy_, bstack11l1lll_opy_ (u"࠭ࡲࠨೄ"))
    bstack111ll1l1l_opy_ = bstack11l11llll1_opy_.read()
    bstack11l11llll1_opy_.close()
    if bstack11l1l1ll11_opy_.username:
      bstack111ll1l1l_opy_ = bstack111ll1l1l_opy_.replace(bstack11l1lll_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ೅"), bstack11l1l1ll11_opy_.username)
    if bstack11l1l1ll11_opy_.key:
      bstack111ll1l1l_opy_ = bstack111ll1l1l_opy_.replace(bstack11l1lll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪೆ"), bstack11l1l1ll11_opy_.key)
    if bstack11l1l1ll11_opy_.framework:
      bstack111ll1l1l_opy_ = bstack111ll1l1l_opy_.replace(bstack11l1lll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೇ"), bstack11l1l1ll11_opy_.framework)
    file_name = bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ೈ")
    file_path = os.path.abspath(file_name)
    bstack1ll11l111_opy_ = open(file_path, bstack11l1lll_opy_ (u"ࠫࡼ࠭೉"))
    bstack1ll11l111_opy_.write(bstack111ll1l1l_opy_)
    bstack1ll11l111_opy_.close()
    logger.info(bstack11l1l1111l_opy_)
    try:
      os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧೊ")] = bstack11l1l1ll11_opy_.framework if bstack11l1l1ll11_opy_.framework != None else bstack11l1lll_opy_ (u"ࠨࠢೋ")
      config = yaml.safe_load(bstack111ll1l1l_opy_)
      config[bstack11l1lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧೌ")] = bstack11l1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶ್ࠧ")
      bstack1l1llll11_opy_(bstack1ll11l11l_opy_, config)
    except Exception as e:
      logger.debug(bstack1111lll1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llllllll_opy_.format(str(e)))
def bstack1l1llll11_opy_(bstack1lll1ll1l_opy_, config, bstack1l1ll11lll_opy_={}):
  global bstack1l1ll11ll_opy_
  global bstack1ll11ll1l_opy_
  global bstack11ll1llll1_opy_
  if not config:
    return
  bstack1l1l11l1l1_opy_ = bstack11l11ll111_opy_ if not bstack1l1ll11ll_opy_ else (
    bstack11l1lll1_opy_ if bstack11l1lll_opy_ (u"ࠩࡤࡴࡵ࠭೎") in config else (
        bstack1111111l_opy_ if config.get(bstack11l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ೏")) else bstack1ll1l1l11_opy_
    )
)
  bstack11llllll_opy_ = False
  bstack1l1l11l111_opy_ = False
  if bstack1l1ll11ll_opy_ is True:
      if bstack11l1lll_opy_ (u"ࠫࡦࡶࡰࠨ೐") in config:
          bstack11llllll_opy_ = True
      else:
          bstack1l1l11l111_opy_ = True
  bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack11l1l1l1_opy_(config, bstack1ll11ll1l_opy_)
  bstack1ll1lllll1_opy_ = bstack1l1l11l1_opy_()
  data = {
    bstack11l1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ೑"): config[bstack11l1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ೒")],
    bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ೓"): config[bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ೔")],
    bstack11l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ೕ"): bstack1lll1ll1l_opy_,
    bstack11l1lll_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೖ"): os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೗"), bstack1ll11ll1l_opy_),
    bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ೘"): bstack1ll111l1l1_opy_,
    bstack11l1lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨ೙"): bstack111l11l11_opy_(),
    bstack11l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೚"): {
      bstack11l1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೛"): str(config[bstack11l1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ೜")]) if bstack11l1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪೝ") in config else bstack11l1lll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧೞ"),
      bstack11l1lll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧ೟"): sys.version,
      bstack11l1lll_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨೠ"): bstack11ll1ll1l1_opy_(os.environ.get(bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩೡ"), bstack1ll11ll1l_opy_)),
      bstack11l1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪೢ"): bstack11l1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೣ"),
      bstack11l1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ೤"): bstack1l1l11l1l1_opy_,
      bstack11l1lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ೥"): bstack1ll1111l11_opy_,
      bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫ೦"): os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ೧")],
      bstack11l1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೨"): os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ೩"), bstack1ll11ll1l_opy_),
      bstack11l1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ೪"): bstack1ll11l1ll_opy_(os.environ.get(bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ೫"), bstack1ll11ll1l_opy_)),
      bstack11l1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೬"): bstack1ll1lllll1_opy_.get(bstack11l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೭")),
      bstack11l1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ೮"): bstack1ll1lllll1_opy_.get(bstack11l1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ೯")),
      bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೰"): config[bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೱ")] if config[bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೲ")] else bstack11l1lll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧೳ"),
      bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೴"): str(config[bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೵")]) if bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೶") in config else bstack11l1lll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೷"),
      bstack11l1lll_opy_ (u"ࠩࡲࡷࠬ೸"): sys.platform,
      bstack11l1lll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ೹"): socket.gethostname(),
      bstack11l1lll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭೺"): bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ೻"))
    }
  }
  if not bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭೼")) is None:
    data[bstack11l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೽")][bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡐࡩࡹࡧࡤࡢࡶࡤࠫ೾")] = {
      bstack11l1lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ೿"): bstack11l1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨഀ"),
      bstack11l1lll_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫഁ"): bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬം")),
      bstack11l1lll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱࡔࡵ࡮ࡤࡨࡶࠬഃ"): bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪഄ"))
    }
  if bstack1lll1ll1l_opy_ == bstack11lll11l1_opy_:
    data[bstack11l1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫഅ")][bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࠧആ")] = bstack1l111111l1_opy_(config)
    data[bstack11l1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ഇ")][bstack11l1lll_opy_ (u"ࠫ࡮ࡹࡐࡦࡴࡦࡽࡆࡻࡴࡰࡇࡱࡥࡧࡲࡥࡥࠩഈ")] = percy.bstack1lll1l1lll_opy_
    data[bstack11l1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഉ")][bstack11l1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡇࡻࡩ࡭ࡦࡌࡨࠬഊ")] = percy.percy_build_id
  if not bstack1l1l1l1ll1_opy_.bstack11l11lll1_opy_(CONFIG):
    data[bstack11l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഋ")][bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬഌ")] = bstack1l1l1l1ll1_opy_.bstack11l11lll1_opy_(CONFIG)
  update(data[bstack11l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ഍")], bstack1l1ll11lll_opy_)
  try:
    response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨഎ"), bstack1ll1ll11_opy_(bstack1ll11ll11l_opy_), data, {
      bstack11l1lll_opy_ (u"ࠫࡦࡻࡴࡩࠩഏ"): (config[bstack11l1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഐ")], config[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ഑")])
    })
    if response:
      logger.debug(bstack11111l1ll_opy_.format(bstack1lll1ll1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1lllll_opy_.format(str(e)))
def bstack11ll1ll1l1_opy_(framework):
  return bstack11l1lll_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦഒ").format(str(framework), __version__) if framework else bstack11l1lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഓ").format(
    __version__)
def bstack11ll11llll_opy_():
  global CONFIG
  global bstack111llll11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1111l1l1l_opy_()
    logger.debug(bstack1lllll1111_opy_.format(str(CONFIG)))
    bstack111llll11_opy_ = bstack1l11l1lll_opy_.bstack1lllll1l11_opy_(CONFIG, bstack111llll11_opy_)
    bstack11l11l1l_opy_()
  except Exception as e:
    logger.error(bstack11l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨഔ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1111ll1_opy_
  atexit.register(bstack1l111l1ll1_opy_)
  signal.signal(signal.SIGINT, bstack111l1lll_opy_)
  signal.signal(signal.SIGTERM, bstack111l1lll_opy_)
def bstack1ll1111ll1_opy_(exctype, value, traceback):
  global bstack11l111ll_opy_
  try:
    for driver in bstack11l111ll_opy_:
      bstack11ll1ll1_opy_(driver, bstack11l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪക"), bstack11l1lll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢഖ") + str(value))
  except Exception:
    pass
  logger.info(bstack1l1l111l1_opy_)
  bstack1ll1111111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1111111_opy_(message=bstack11l1lll_opy_ (u"ࠬ࠭ഗ"), bstack1ll1ll1ll_opy_ = False):
  global CONFIG
  bstack11l11l1ll1_opy_ = bstack11l1lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨഘ") if bstack1ll1ll1ll_opy_ else bstack11l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ങ")
  try:
    if message:
      bstack1l1ll11lll_opy_ = {
        bstack11l11l1ll1_opy_ : str(message)
      }
      bstack1l1llll11_opy_(bstack11lll11l1_opy_, CONFIG, bstack1l1ll11lll_opy_)
    else:
      bstack1l1llll11_opy_(bstack11lll11l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll1ll1ll_opy_.format(str(e)))
def bstack1l1l1ll1ll_opy_(bstack1l11l1ll1_opy_, size):
  bstack1l1l1ll11l_opy_ = []
  while len(bstack1l11l1ll1_opy_) > size:
    bstack11l11111l_opy_ = bstack1l11l1ll1_opy_[:size]
    bstack1l1l1ll11l_opy_.append(bstack11l11111l_opy_)
    bstack1l11l1ll1_opy_ = bstack1l11l1ll1_opy_[size:]
  bstack1l1l1ll11l_opy_.append(bstack1l11l1ll1_opy_)
  return bstack1l1l1ll11l_opy_
def bstack11111ll1l_opy_(args):
  if bstack11l1lll_opy_ (u"ࠨ࠯ࡰࠫച") in args and bstack11l1lll_opy_ (u"ࠩࡳࡨࡧ࠭ഛ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1111l11ll_opy_, stage=STAGE.bstack1l1l1l11_opy_)
def run_on_browserstack(bstack11111l1l_opy_=None, bstack1lll1ll1_opy_=None, bstack11ll1llll_opy_=False):
  global CONFIG
  global bstack1ll1llll11_opy_
  global bstack1l111111_opy_
  global bstack1ll11ll1l_opy_
  global bstack11ll1llll1_opy_
  bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠪࠫജ")
  bstack1ll11l1l1l_opy_(bstack1l11llllll_opy_, logger)
  if bstack11111l1l_opy_ and isinstance(bstack11111l1l_opy_, str):
    bstack11111l1l_opy_ = eval(bstack11111l1l_opy_)
  if bstack11111l1l_opy_:
    CONFIG = bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫഝ")]
    bstack1ll1llll11_opy_ = bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ഞ")]
    bstack1l111111_opy_ = bstack11111l1l_opy_[bstack11l1lll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨട")]
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩഠ"), bstack1l111111_opy_)
    bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഡ")
  bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫഢ"), uuid4().__str__())
  logger.info(bstack11l1lll_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨണ") + bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ത")));
  logger.debug(bstack11l1lll_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨഥ") + bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨദ")))
  if not bstack11ll1llll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11l1l1ll_opy_)
      return
    if sys.argv[1] == bstack11l1lll_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪധ") or sys.argv[1] == bstack11l1lll_opy_ (u"ࠨ࠯ࡹࠫന"):
      logger.info(bstack11l1lll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩഩ").format(__version__))
      return
    if sys.argv[1] == bstack11l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩപ"):
      bstack11l1l1l1ll_opy_()
      return
  args = sys.argv
  bstack11ll11llll_opy_()
  global bstack11l1ll1ll_opy_
  global bstack1l1l11ll_opy_
  global bstack1llll1ll1l_opy_
  global bstack1l1ll1ll1l_opy_
  global bstack11l1ll11l_opy_
  global bstack11ll1l11l_opy_
  global bstack1l1lll11l_opy_
  global bstack1ll11ll1_opy_
  global bstack1ll1l1ll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1l11ll1ll1_opy_
  bstack1l1l11ll_opy_ = len(CONFIG.get(bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഫ"), []))
  if not bstack1ll1ll1l1l_opy_:
    if args[1] == bstack11l1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬബ") or args[1] == bstack11l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧഭ"):
      bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧമ")
      args = args[2:]
    elif args[1] == bstack11l1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧയ"):
      bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨര")
      args = args[2:]
    elif args[1] == bstack11l1lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩറ"):
      bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪല")
      args = args[2:]
    elif args[1] == bstack11l1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ള"):
      bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧഴ")
      args = args[2:]
    elif args[1] == bstack11l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧവ"):
      bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨശ")
      args = args[2:]
    elif args[1] == bstack11l1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഷ"):
      bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪസ")
      args = args[2:]
    else:
      if not bstack11l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഹ") in CONFIG or str(CONFIG[bstack11l1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഺ")]).lower() in [bstack11l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ഻࠭"), bstack11l1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ഼")]:
        bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഽ")
        args = args[1:]
      elif str(CONFIG[bstack11l1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬാ")]).lower() == bstack11l1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩി"):
        bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪീ")
        args = args[1:]
      elif str(CONFIG[bstack11l1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨു")]).lower() == bstack11l1lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬൂ"):
        bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൃ")
        args = args[1:]
      elif str(CONFIG[bstack11l1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫൄ")]).lower() == bstack11l1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൅"):
        bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪെ")
        args = args[1:]
      elif str(CONFIG[bstack11l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧേ")]).lower() == bstack11l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬൈ"):
        bstack1ll1ll1l1l_opy_ = bstack11l1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭൉")
        args = args[1:]
      else:
        os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൊ")] = bstack1ll1ll1l1l_opy_
        bstack11l111lll1_opy_(bstack11l1111ll_opy_)
  os.environ[bstack11l1lll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩോ")] = bstack1ll1ll1l1l_opy_
  bstack1ll11ll1l_opy_ = bstack1ll1ll1l1l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l111l11l1_opy_ = bstack11ll11ll1l_opy_[bstack11l1lll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ൌ")] if bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ്ࠪ") and bstack1ll11lll_opy_() else bstack1ll1ll1l1l_opy_
      bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.bstack1ll11l1111_opy_, bstack1llll1l1l1_opy_(
        sdk_version=__version__,
        path_config=bstack1l1ll1l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l111l11l1_opy_,
        frameworks=[bstack1l111l11l1_opy_],
        framework_versions={
          bstack1l111l11l1_opy_: bstack1ll11l1ll_opy_(bstack11l1lll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪൎ") if bstack1ll1ll1l1l_opy_ in [bstack11l1lll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൏"), bstack11l1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൐"), bstack11l1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ൑")] else bstack1ll1ll1l1l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack11l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ൒"), None):
        CONFIG[bstack11l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ൓")] = cli.config.get(bstack11l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧൔ"), None)
    except Exception as e:
      bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.bstack1ll1ll1ll1_opy_, e.__traceback__, 1)
    if bstack1l111111_opy_:
      CONFIG[bstack11l1lll_opy_ (u"ࠦࡦࡶࡰࠣൕ")] = cli.config[bstack11l1lll_opy_ (u"ࠧࡧࡰࡱࠤൖ")]
      logger.info(bstack1lll1lll_opy_.format(CONFIG[bstack11l1lll_opy_ (u"࠭ࡡࡱࡲࠪൗ")]))
  else:
    bstack1lll111111_opy_.clear()
  global bstack1l1111ll1_opy_
  global bstack1lll1l11_opy_
  if bstack11111l1l_opy_:
    try:
      bstack11llll111l_opy_ = datetime.datetime.now()
      os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ൘")] = bstack1ll1ll1l1l_opy_
      bstack1l1llll11_opy_(bstack111111l1l_opy_, CONFIG)
      cli.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦ൙"), datetime.datetime.now() - bstack11llll111l_opy_)
    except Exception as e:
      logger.debug(bstack1l1l11llll_opy_.format(str(e)))
  global bstack11l1l11l1l_opy_
  global bstack1lll11ll1_opy_
  global bstack11l1ll11ll_opy_
  global bstack11l11l11_opy_
  global bstack1l1llllll1_opy_
  global bstack1lll1l111_opy_
  global bstack1l1llll1l1_opy_
  global bstack1lll11ll1l_opy_
  global bstack11ll1l1lll_opy_
  global bstack11l11lllll_opy_
  global bstack11l1l11ll_opy_
  global bstack1111l1l1_opy_
  global bstack1l11l111_opy_
  global bstack1llll111ll_opy_
  global bstack1llll1ll_opy_
  global bstack1l1lllll1l_opy_
  global bstack1l11l11lll_opy_
  global bstack1ll111111l_opy_
  global bstack11llll11l1_opy_
  global bstack1lll1lllll_opy_
  global bstack1lll11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1l11l1l_opy_ = webdriver.Remote.__init__
    bstack1lll11ll1_opy_ = WebDriver.quit
    bstack1111l1l1_opy_ = WebDriver.close
    bstack1llll1ll_opy_ = WebDriver.get
    bstack1lll11ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1111ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1l11ll1_opy_
    bstack1lll1l11_opy_ = bstack1l1l11ll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1ll1ll1111_opy_
    from QWeb.keywords import browser
    bstack1ll1ll1111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1ll1lll1_opy_(CONFIG) and bstack1111llll_opy_():
    if bstack111111111_opy_() < version.parse(bstack11l111l111_opy_):
      logger.error(bstack11lllll1_opy_.format(bstack111111111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1lllll1l_opy_ = RemoteConnection._11l1ll1l_opy_
      except Exception as e:
        logger.error(bstack1l1l1l111l_opy_.format(str(e)))
  if not CONFIG.get(bstack11l1lll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ൚"), False) and not bstack11111l1l_opy_:
    logger.info(bstack1lll1l1l1l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack11l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ൛") in CONFIG and str(CONFIG[bstack11l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ൜")]).lower() != bstack11l1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ൝"):
      bstack1l1ll11111_opy_()
    elif bstack1ll1ll1l1l_opy_ != bstack11l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൞") or (bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧൟ") and not bstack11111l1l_opy_):
      bstack1llll1ll11_opy_()
  if (bstack1ll1ll1l1l_opy_ in [bstack11l1lll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧൠ"), bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൡ"), bstack11l1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൢ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l111l11l_opy_
        bstack1lll1l111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1ll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1llllll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l1l11l11_opy_ + str(e))
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack1l1ll1ll_opy_)
    if bstack1ll1ll1l1l_opy_ != bstack11l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൣ"):
      bstack1ll11111l1_opy_()
    bstack11l1ll11ll_opy_ = Output.start_test
    bstack11l11l11_opy_ = Output.end_test
    bstack1l1llll1l1_opy_ = TestStatus.__init__
    bstack11ll1l1lll_opy_ = pabot._run
    bstack11l11lllll_opy_ = QueueItem.__init__
    bstack11l1l11ll_opy_ = pabot._create_command_for_execution
    bstack11llll11l1_opy_ = pabot._report_results
  if bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ൤"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack11llllll11_opy_)
    bstack1l11l111_opy_ = Runner.run_hook
    bstack1llll111ll_opy_ = Step.run
  if bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൥"):
    try:
      from _pytest.config import Config
      bstack1l11l11lll_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll111111l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11111111_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lll1lllll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ൦"))
  try:
    framework_name = bstack11l1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൧") if bstack1ll1ll1l1l_opy_ in [bstack11l1lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൨"), bstack11l1lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൩"), bstack11l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൪")] else bstack11ll1lll1l_opy_(bstack1ll1ll1l1l_opy_)
    bstack1lll1ll111_opy_ = {
      bstack11l1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭൫"): bstack11l1lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ൬") if bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൭") and bstack1ll11lll_opy_() else framework_name,
      bstack11l1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ൮"): bstack1ll11l1ll_opy_(framework_name),
      bstack11l1lll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ൯"): __version__,
      bstack11l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ൰"): bstack1ll1ll1l1l_opy_
    }
    if bstack1ll1ll1l1l_opy_ in bstack1l111lll1l_opy_ + bstack11ll1ll11_opy_:
      if bstack1l11111lll_opy_.bstack1llll1lll_opy_(CONFIG):
        if bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ൱") in CONFIG:
          os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭൲")] = os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ൳"), json.dumps(CONFIG[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൴")]))
          CONFIG[bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൵")].pop(bstack11l1lll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ൶"), None)
          CONFIG[bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ൷")].pop(bstack11l1lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ൸"), None)
        bstack1lll1ll111_opy_[bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൹")] = {
          bstack11l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫൺ"): bstack11l1lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩൻ"),
          bstack11l1lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩർ"): str(bstack111111111_opy_())
        }
    if bstack1ll1ll1l1l_opy_ not in [bstack11l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪൽ")] and not cli.is_running():
      bstack1llll111l1_opy_, bstack1lllll1ll_opy_ = bstack1lll11111l_opy_.launch(CONFIG, bstack1lll1ll111_opy_)
      if bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪൾ")) is not None and bstack1l11111lll_opy_.bstack1l1llll1ll_opy_(CONFIG) is None:
        value = bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫൿ")].get(bstack11l1lll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭඀"))
        if value is not None:
            CONFIG[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ඁ")] = value
        else:
          logger.debug(bstack11l1lll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧං"))
  except Exception as e:
    logger.debug(bstack11l111ll11_opy_.format(bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩඃ"), str(e)))
  if bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඄"):
    bstack1llll1ll1l_opy_ = True
    if bstack11111l1l_opy_ and bstack11ll1llll_opy_:
      bstack11ll1l11l_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧඅ"), {}).get(bstack11l1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ආ"))
      bstack1llll1ll1_opy_(bstack111l11ll1_opy_)
    elif bstack11111l1l_opy_:
      bstack11ll1l11l_opy_ = CONFIG.get(bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩඇ"), {}).get(bstack11l1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඈ"))
      global bstack11l111ll_opy_
      try:
        if bstack11111ll1l_opy_(bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඉ")]) and multiprocessing.current_process().name == bstack11l1lll_opy_ (u"ࠨ࠲ࠪඊ"):
          bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඋ")].remove(bstack11l1lll_opy_ (u"ࠪ࠱ࡲ࠭ඌ"))
          bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඍ")].remove(bstack11l1lll_opy_ (u"ࠬࡶࡤࡣࠩඎ"))
          bstack11111l1l_opy_[bstack11l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඏ")] = bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඐ")][0]
          with open(bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඑ")], bstack11l1lll_opy_ (u"ࠩࡵࠫඒ")) as f:
            bstack1lll1lll11_opy_ = f.read()
          bstack1llllllll1_opy_ = bstack11l1lll_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨඓ").format(str(bstack11111l1l_opy_))
          bstack1l11l11l11_opy_ = bstack1llllllll1_opy_ + bstack1lll1lll11_opy_
          bstack11lllll1l_opy_ = bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඔ")] + bstack11l1lll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧඕ")
          with open(bstack11lllll1l_opy_, bstack11l1lll_opy_ (u"࠭ࡷࠨඖ")):
            pass
          with open(bstack11lllll1l_opy_, bstack11l1lll_opy_ (u"ࠢࡸ࠭ࠥ඗")) as f:
            f.write(bstack1l11l11l11_opy_)
          import subprocess
          bstack11l111111_opy_ = subprocess.run([bstack11l1lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ඘"), bstack11lllll1l_opy_])
          if os.path.exists(bstack11lllll1l_opy_):
            os.unlink(bstack11lllll1l_opy_)
          os._exit(bstack11l111111_opy_.returncode)
        else:
          if bstack11111ll1l_opy_(bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඙")]):
            bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක")].remove(bstack11l1lll_opy_ (u"ࠫ࠲ࡳࠧඛ"))
            bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨග")].remove(bstack11l1lll_opy_ (u"࠭ࡰࡥࡤࠪඝ"))
            bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඞ")] = bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඟ")][0]
          bstack1llll1ll1_opy_(bstack111l11ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬච")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l1lll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬඡ")] = bstack11l1lll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ජ")
          mod_globals[bstack11l1lll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧඣ")] = os.path.abspath(bstack11111l1l_opy_[bstack11l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඤ")])
          exec(open(bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඥ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l1lll_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨඦ").format(str(e)))
          for driver in bstack11l111ll_opy_:
            bstack1lll1ll1_opy_.append({
              bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧට"): bstack11111l1l_opy_[bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඨ")],
              bstack11l1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪඩ"): str(e),
              bstack11l1lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫඪ"): multiprocessing.current_process().name
            })
            bstack11ll1ll1_opy_(driver, bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ණ"), bstack11l1lll_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥඬ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l111ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l111111_opy_, CONFIG, logger)
      bstack1l11l1l11_opy_()
      bstack11lll111ll_opy_()
      percy.bstack1111l1l11_opy_()
      bstack1l111111l_opy_ = {
        bstack11l1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫත"): args[0],
        bstack11l1lll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩථ"): CONFIG,
        bstack11l1lll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫද"): bstack1ll1llll11_opy_,
        bstack11l1lll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ධ"): bstack1l111111_opy_
      }
      if bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨන") in CONFIG:
        bstack1l111l1ll_opy_ = bstack11ll111l1_opy_(args, logger, CONFIG, bstack1l1ll11ll_opy_, bstack1l1l11ll_opy_)
        bstack1ll11ll1_opy_ = bstack1l111l1ll_opy_.bstack1l1ll11l1l_opy_(run_on_browserstack, bstack1l111111l_opy_, bstack11111ll1l_opy_(args))
      else:
        if bstack11111ll1l_opy_(args):
          bstack1l111111l_opy_[bstack11l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ඲")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l111111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1llll1ll1_opy_(bstack111l11ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l1lll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩඳ")] = bstack11l1lll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪප")
          mod_globals[bstack11l1lll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫඵ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩබ") or bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪභ"):
    percy.init(bstack1l111111_opy_, CONFIG, logger)
    percy.bstack1111l1l11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack1l1ll1ll_opy_)
    bstack1l11l1l11_opy_()
    bstack1llll1ll1_opy_(bstack11ll1lll_opy_)
    if bstack1l1ll11ll_opy_:
      bstack1lll11l1l1_opy_(bstack11ll1lll_opy_, args)
      if bstack11l1lll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪම") in args:
        i = args.index(bstack11l1lll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඹ"))
        args.pop(i)
        args.pop(i)
      if bstack11l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪය") not in CONFIG:
        CONFIG[bstack11l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫර")] = [{}]
        bstack1l1l11ll_opy_ = 1
      if bstack11l1ll1ll_opy_ == 0:
        bstack11l1ll1ll_opy_ = 1
      args.insert(0, str(bstack11l1ll1ll_opy_))
      args.insert(0, str(bstack11l1lll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ඼")))
    if bstack1lll11111l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11lllllll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111ll11l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l1lll_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥල"),
        ).parse_args(bstack11lllllll1_opy_)
        bstack11ll111111_opy_ = args.index(bstack11lllllll1_opy_[0]) if len(bstack11lllllll1_opy_) > 0 else len(args)
        args.insert(bstack11ll111111_opy_, str(bstack11l1lll_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ඾")))
        args.insert(bstack11ll111111_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ඿"))))
        if bstack1l1l1l1ll1_opy_.bstack1l1ll11l_opy_(CONFIG):
          args.insert(bstack11ll111111_opy_, str(bstack11l1lll_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪව")))
          args.insert(bstack11ll111111_opy_ + 1, str(bstack11l1lll_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨශ").format(bstack1l1l1l1ll1_opy_.bstack11l1ll1ll1_opy_(CONFIG))))
        if bstack1llll1l11_opy_(os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ෂ"))) and str(os.environ.get(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ස"), bstack11l1lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨහ"))) != bstack11l1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩළ"):
          for bstack1l1l1l1l_opy_ in bstack111ll11l_opy_:
            args.remove(bstack1l1l1l1l_opy_)
          bstack1ll111111_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩෆ")).split(bstack11l1lll_opy_ (u"࠭ࠬࠨ෇"))
          for bstack1l11lll1l1_opy_ in bstack1ll111111_opy_:
            args.append(bstack1l11lll1l1_opy_)
      except Exception as e:
        logger.error(bstack11l1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥ෈").format(e))
    pabot.main(args)
  elif bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෉"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack1l1ll1ll_opy_)
    for a in args:
      if bstack11l1lll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ්") in a:
        bstack11l1ll11l_opy_ = int(a.split(bstack11l1lll_opy_ (u"ࠪ࠾ࠬ෋"))[1])
      if bstack11l1lll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ෌") in a:
        bstack11ll1l11l_opy_ = str(a.split(bstack11l1lll_opy_ (u"ࠬࡀࠧ෍"))[1])
      if bstack11l1lll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭෎") in a:
        bstack1l1lll11l_opy_ = str(a.split(bstack11l1lll_opy_ (u"ࠧ࠻ࠩා"))[1])
    bstack1l1111l11_opy_ = None
    if bstack11l1lll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧැ") in args:
      i = args.index(bstack11l1lll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨෑ"))
      args.pop(i)
      bstack1l1111l11_opy_ = args.pop(i)
    if bstack1l1111l11_opy_ is not None:
      global bstack1l11l1111_opy_
      bstack1l11l1111_opy_ = bstack1l1111l11_opy_
    bstack1llll1ll1_opy_(bstack11ll1lll_opy_)
    run_cli(args)
    if bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧි") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1ll1_opy_.append(bstack11l1l1l11_opy_)
  elif bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫී"):
    bstack1ll1lll1l1_opy_ = bstack11ll1l111l_opy_(args, logger, CONFIG, bstack1l1ll11ll_opy_)
    bstack1ll1lll1l1_opy_.bstack11l1lll11_opy_()
    bstack1l11l1l11_opy_()
    bstack1l1ll1ll1l_opy_ = True
    bstack1l1l1l1ll_opy_ = bstack1ll1lll1l1_opy_.bstack11lll11ll_opy_()
    bstack1ll1lll1l1_opy_.bstack1l111111l_opy_(bstack1l11111ll_opy_)
    bstack11l11ll11_opy_ = bstack1ll1lll1l1_opy_.bstack1l1ll11l1l_opy_(bstack1lll111lll_opy_, {
      bstack11l1lll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ු"): bstack1ll1llll11_opy_,
      bstack11l1lll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ෕"): bstack1l111111_opy_,
      bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪූ"): bstack1l1ll11ll_opy_
    })
    try:
      bstack11l11l1l1_opy_, bstack1ll1ll11l1_opy_ = map(list, zip(*bstack11l11ll11_opy_))
      bstack1ll1l1ll_opy_ = bstack11l11l1l1_opy_[0]
      for status_code in bstack1ll1ll11l1_opy_:
        if status_code != 0:
          bstack1l11ll1ll1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11l1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨ෗").format(str(e)))
  elif bstack1ll1ll1l1l_opy_ == bstack11l1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ"):
    try:
      from behave.__main__ import main as bstack11lll11111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll1llll1_opy_(e, bstack11llllll11_opy_)
    bstack1l11l1l11_opy_()
    bstack1l1ll1ll1l_opy_ = True
    bstack1l1l11111_opy_ = 1
    if bstack11l1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪෙ") in CONFIG:
      bstack1l1l11111_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫේ")]
    if bstack11l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨෛ") in CONFIG:
      bstack1l11l1l1l_opy_ = int(bstack1l1l11111_opy_) * int(len(CONFIG[bstack11l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩො")]))
    else:
      bstack1l11l1l1l_opy_ = int(bstack1l1l11111_opy_)
    config = Configuration(args)
    bstack111111lll_opy_ = config.paths
    if len(bstack111111lll_opy_) == 0:
      import glob
      pattern = bstack11l1lll_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ෝ")
      bstack1lll1l11l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll1l11l_opy_)
      config = Configuration(args)
      bstack111111lll_opy_ = config.paths
    bstack11lll1ll_opy_ = [os.path.normpath(item) for item in bstack111111lll_opy_]
    bstack11ll111l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1lll111_opy_ = [item for item in bstack11ll111l1l_opy_ if item not in bstack11lll1ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l1lll_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩෞ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11lll1ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l111111_opy_)))
                    for bstack1l1l111111_opy_ in bstack11lll1ll_opy_]
    bstack1l11ll11l_opy_ = []
    for spec in bstack11lll1ll_opy_:
      bstack1111l1111_opy_ = []
      bstack1111l1111_opy_ += bstack1l1lll111_opy_
      bstack1111l1111_opy_.append(spec)
      bstack1l11ll11l_opy_.append(bstack1111l1111_opy_)
    execution_items = []
    for bstack1111l1111_opy_ in bstack1l11ll11l_opy_:
      if bstack11l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෟ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෠")]):
          item = {}
          item[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࠨ෡")] = bstack11l1lll_opy_ (u"ࠬࠦࠧ෢").join(bstack1111l1111_opy_)
          item[bstack11l1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෣")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࠫ෤")] = bstack11l1lll_opy_ (u"ࠨࠢࠪ෥").join(bstack1111l1111_opy_)
        item[bstack11l1lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ෦")] = 0
        execution_items.append(item)
    bstack1ll1l11111_opy_ = bstack1l1l1ll1ll_opy_(execution_items, bstack1l11l1l1l_opy_)
    for execution_item in bstack1ll1l11111_opy_:
      bstack11lll1llll_opy_ = []
      for item in execution_item:
        bstack11lll1llll_opy_.append(bstack111l1l1l_opy_(name=str(item[bstack11l1lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෧")]),
                                             target=bstack1lllllllll_opy_,
                                             args=(item[bstack11l1lll_opy_ (u"ࠫࡦࡸࡧࠨ෨")],)))
      for t in bstack11lll1llll_opy_:
        t.start()
      for t in bstack11lll1llll_opy_:
        t.join()
  else:
    bstack11l111lll1_opy_(bstack11l1111ll_opy_)
  if not bstack11111l1l_opy_:
    bstack1l1lll111l_opy_()
    if(bstack1ll1ll1l1l_opy_ in [bstack11l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෩"), bstack11l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෪")]):
      bstack11l1l11111_opy_()
  bstack1l11l1lll_opy_.bstack1ll1l111l_opy_()
def browserstack_initialize(bstack11l1l1l111_opy_=None):
  logger.info(bstack11l1lll_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪ෫") + str(bstack11l1l1l111_opy_))
  run_on_browserstack(bstack11l1l1l111_opy_, None, True)
@measure(event_name=EVENTS.bstack1l1l1lll11_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l1lll111l_opy_():
  global CONFIG
  global bstack1ll11ll1l_opy_
  global bstack1l11ll1ll1_opy_
  global bstack1l111lll11_opy_
  global bstack11ll1llll1_opy_
  bstack1l11ll11_opy_.bstack11111111_opy_()
  if cli.is_running():
    bstack1lll111111_opy_.invoke(bstack11lll11lll_opy_.bstack1l1llll11l_opy_)
  if bstack1ll11ll1l_opy_ == bstack11l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෬"):
    if not cli.is_enabled(CONFIG):
      bstack1lll11111l_opy_.stop()
  else:
    bstack1lll11111l_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11l111l11l_opy_.bstack1llll1111l_opy_()
  if bstack11l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭෭") in CONFIG and str(CONFIG[bstack11l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ෮")]).lower() != bstack11l1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ෯"):
    bstack1l111l1l1l_opy_, bstack11ll11lll1_opy_ = bstack1ll1l1l1l_opy_()
  else:
    bstack1l111l1l1l_opy_, bstack11ll11lll1_opy_ = get_build_link()
  bstack1llll1111_opy_(bstack1l111l1l1l_opy_)
  logger.info(bstack11l1lll_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭෰") + bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ෱"), bstack11l1lll_opy_ (u"ࠧࠨෲ")) + bstack11l1lll_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩෳ") + os.getenv(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ෴"), bstack11l1lll_opy_ (u"ࠪࠫ෵")))
  if bstack1l111l1l1l_opy_ is not None and bstack1l111l1lll_opy_() != -1:
    sessions = bstack1l1111111l_opy_(bstack1l111l1l1l_opy_)
    bstack1l11l1llll_opy_(sessions, bstack11ll11lll1_opy_)
  if bstack1ll11ll1l_opy_ == bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෶") and bstack1l11ll1ll1_opy_ != 0:
    sys.exit(bstack1l11ll1ll1_opy_)
  if bstack1ll11ll1l_opy_ == bstack11l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෷") and bstack1l111lll11_opy_ != 0:
    sys.exit(bstack1l111lll11_opy_)
def bstack1llll1111_opy_(new_id):
    global bstack1ll111l1l1_opy_
    bstack1ll111l1l1_opy_ = new_id
def bstack11ll1lll1l_opy_(bstack1ll111l11l_opy_):
  if bstack1ll111l11l_opy_:
    return bstack1ll111l11l_opy_.capitalize()
  else:
    return bstack11l1lll_opy_ (u"࠭ࠧ෸")
@measure(event_name=EVENTS.bstack1ll1l1ll11_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l1l1l1l11_opy_(bstack1l11lll1_opy_):
  if bstack11l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෹") in bstack1l11lll1_opy_ and bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭෺")] != bstack11l1lll_opy_ (u"ࠩࠪ෻"):
    return bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ෼")]
  else:
    bstack11l11ll1ll_opy_ = bstack11l1lll_opy_ (u"ࠦࠧ෽")
    if bstack11l1lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ෾") in bstack1l11lll1_opy_ and bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭෿")] != None:
      bstack11l11ll1ll_opy_ += bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ฀")] + bstack11l1lll_opy_ (u"ࠣ࠮ࠣࠦก")
      if bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠩࡲࡷࠬข")] == bstack11l1lll_opy_ (u"ࠥ࡭ࡴࡹࠢฃ"):
        bstack11l11ll1ll_opy_ += bstack11l1lll_opy_ (u"ࠦ࡮ࡕࡓࠡࠤค")
      bstack11l11ll1ll_opy_ += (bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩฅ")] or bstack11l1lll_opy_ (u"࠭ࠧฆ"))
      return bstack11l11ll1ll_opy_
    else:
      bstack11l11ll1ll_opy_ += bstack11ll1lll1l_opy_(bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨง")]) + bstack11l1lll_opy_ (u"ࠣࠢࠥจ") + (
              bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫฉ")] or bstack11l1lll_opy_ (u"ࠪࠫช")) + bstack11l1lll_opy_ (u"ࠦ࠱ࠦࠢซ")
      if bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠬࡵࡳࠨฌ")] == bstack11l1lll_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢญ"):
        bstack11l11ll1ll_opy_ += bstack11l1lll_opy_ (u"ࠢࡘ࡫ࡱࠤࠧฎ")
      bstack11l11ll1ll_opy_ += bstack1l11lll1_opy_[bstack11l1lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬฏ")] or bstack11l1lll_opy_ (u"ࠩࠪฐ")
      return bstack11l11ll1ll_opy_
@measure(event_name=EVENTS.bstack1l111l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1ll1l1ll1l_opy_(bstack11lllll111_opy_):
  if bstack11lllll111_opy_ == bstack11l1lll_opy_ (u"ࠥࡨࡴࡴࡥࠣฑ"):
    return bstack11l1lll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧฒ")
  elif bstack11lllll111_opy_ == bstack11l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧณ"):
    return bstack11l1lll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩด")
  elif bstack11lllll111_opy_ == bstack11l1lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢต"):
    return bstack11l1lll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨถ")
  elif bstack11lllll111_opy_ == bstack11l1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣท"):
    return bstack11l1lll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬธ")
  elif bstack11lllll111_opy_ == bstack11l1lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧน"):
    return bstack11l1lll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪบ")
  elif bstack11lllll111_opy_ == bstack11l1lll_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢป"):
    return bstack11l1lll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨผ")
  else:
    return bstack11l1lll_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬฝ") + bstack11ll1lll1l_opy_(
      bstack11lllll111_opy_) + bstack11l1lll_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨพ")
def bstack1ll111ll1l_opy_(session):
  return bstack11l1lll_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪฟ").format(
    session[bstack11l1lll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨภ")], bstack1l1l1l1l11_opy_(session), bstack1ll1l1ll1l_opy_(session[bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫม")]),
    bstack1ll1l1ll1l_opy_(session[bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ย")]),
    bstack11ll1lll1l_opy_(session[bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨร")] or session[bstack11l1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨฤ")] or bstack11l1lll_opy_ (u"ࠩࠪล")) + bstack11l1lll_opy_ (u"ࠥࠤࠧฦ") + (session[bstack11l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ว")] or bstack11l1lll_opy_ (u"ࠬ࠭ศ")),
    session[bstack11l1lll_opy_ (u"࠭࡯ࡴࠩษ")] + bstack11l1lll_opy_ (u"ࠢࠡࠤส") + session[bstack11l1lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬห")], session[bstack11l1lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫฬ")] or bstack11l1lll_opy_ (u"ࠪࠫอ"),
    session[bstack11l1lll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨฮ")] if session[bstack11l1lll_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩฯ")] else bstack11l1lll_opy_ (u"࠭ࠧะ"))
@measure(event_name=EVENTS.bstack1lll11l1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def bstack1l11l1llll_opy_(sessions, bstack11ll11lll1_opy_):
  try:
    bstack1l1l1111l_opy_ = bstack11l1lll_opy_ (u"ࠢࠣั")
    if not os.path.exists(bstack1lll1111_opy_):
      os.mkdir(bstack1lll1111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1lll_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭า")), bstack11l1lll_opy_ (u"ࠩࡵࠫำ")) as f:
      bstack1l1l1111l_opy_ = f.read()
    bstack1l1l1111l_opy_ = bstack1l1l1111l_opy_.replace(bstack11l1lll_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧิ"), str(len(sessions)))
    bstack1l1l1111l_opy_ = bstack1l1l1111l_opy_.replace(bstack11l1lll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫี"), bstack11ll11lll1_opy_)
    bstack1l1l1111l_opy_ = bstack1l1l1111l_opy_.replace(bstack11l1lll_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ึ"),
                                              sessions[0].get(bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪื")) if sessions[0] else bstack11l1lll_opy_ (u"ࠧࠨุ"))
    with open(os.path.join(bstack1lll1111_opy_, bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰูࠬ")), bstack11l1lll_opy_ (u"ࠩࡺฺࠫ")) as stream:
      stream.write(bstack1l1l1111l_opy_.split(bstack11l1lll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ฻"))[0])
      for session in sessions:
        stream.write(bstack1ll111ll1l_opy_(session))
      stream.write(bstack1l1l1111l_opy_.split(bstack11l1lll_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ฼"))[1])
    logger.info(bstack11l1lll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ฽").format(bstack1lll1111_opy_));
  except Exception as e:
    logger.debug(bstack1ll1l111l1_opy_.format(str(e)))
def bstack1l1111111l_opy_(bstack1l111l1l1l_opy_):
  global CONFIG
  try:
    bstack11llll111l_opy_ = datetime.datetime.now()
    host = bstack11l1lll_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ฾") if bstack11l1lll_opy_ (u"ࠧࡢࡲࡳࠫ฿") in CONFIG else bstack11l1lll_opy_ (u"ࠨࡣࡳ࡭ࠬเ")
    user = CONFIG[bstack11l1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫแ")]
    key = CONFIG[bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭โ")]
    bstack11l11lll1l_opy_ = bstack11l1lll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪใ") if bstack11l1lll_opy_ (u"ࠬࡧࡰࡱࠩไ") in CONFIG else (bstack11l1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪๅ") if CONFIG.get(bstack11l1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫๆ")) else bstack11l1lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ็"))
    url = bstack11l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴ่ࠧ").format(user, key, host, bstack11l11lll1l_opy_,
                                                                                bstack1l111l1l1l_opy_)
    headers = {
      bstack11l1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦ้ࠩ"): bstack11l1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴ๊ࠧ"),
    }
    proxies = bstack1ll111l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺ๋ࠢ"), datetime.datetime.now() - bstack11llll111l_opy_)
      return list(map(lambda session: session[bstack11l1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ์")], response.json()))
  except Exception as e:
    logger.debug(bstack111l1l111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1ll1l1lll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def get_build_link():
  global CONFIG
  global bstack1ll111l1l1_opy_
  try:
    if bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪํ") in CONFIG:
      bstack11llll111l_opy_ = datetime.datetime.now()
      host = bstack11l1lll_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ๎") if bstack11l1lll_opy_ (u"ࠩࡤࡴࡵ࠭๏") in CONFIG else bstack11l1lll_opy_ (u"ࠪࡥࡵ࡯ࠧ๐")
      user = CONFIG[bstack11l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭๑")]
      key = CONFIG[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ๒")]
      bstack11l11lll1l_opy_ = bstack11l1lll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ๓") if bstack11l1lll_opy_ (u"ࠧࡢࡲࡳࠫ๔") in CONFIG else bstack11l1lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ๕")
      url = bstack11l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ๖").format(user, key, host, bstack11l11lll1l_opy_)
      if cli.is_enabled(CONFIG):
        bstack11ll11lll1_opy_, bstack1l111l1l1l_opy_ = cli.bstack11l11lll_opy_()
        logger.info(bstack111ll111_opy_.format(bstack11ll11lll1_opy_))
        return [bstack1l111l1l1l_opy_, bstack11ll11lll1_opy_]
      else:
        headers = {
          bstack11l1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ๗"): bstack11l1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ๘"),
        }
        if bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๙") in CONFIG:
          params = {bstack11l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๚"): CONFIG[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๛")], bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๜"): CONFIG[bstack11l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๝")]}
        else:
          params = {bstack11l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ๞"): CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๟")]}
        proxies = bstack1ll111l1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l11111l_opy_ = response.json()[0][bstack11l1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ๠")]
          if bstack1l11111l_opy_:
            bstack11ll11lll1_opy_ = bstack1l11111l_opy_[bstack11l1lll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ๡")].split(bstack11l1lll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭๢"))[0] + bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ๣") + bstack1l11111l_opy_[
              bstack11l1lll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๤")]
            logger.info(bstack111ll111_opy_.format(bstack11ll11lll1_opy_))
            bstack1ll111l1l1_opy_ = bstack1l11111l_opy_[bstack11l1lll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭๥")]
            bstack11ll1ll1l_opy_ = CONFIG[bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๦")]
            if bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๧") in CONFIG:
              bstack11ll1ll1l_opy_ += bstack11l1lll_opy_ (u"࠭ࠠࠨ๨") + CONFIG[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๩")]
            if bstack11ll1ll1l_opy_ != bstack1l11111l_opy_[bstack11l1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭๪")]:
              logger.debug(bstack1lll11l111_opy_.format(bstack1l11111l_opy_[bstack11l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๫")], bstack11ll1ll1l_opy_))
            cli.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤ๬"), datetime.datetime.now() - bstack11llll111l_opy_)
            return [bstack1l11111l_opy_[bstack11l1lll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ๭")], bstack11ll11lll1_opy_]
    else:
      logger.warn(bstack1l1ll1l1l1_opy_)
  except Exception as e:
    logger.debug(bstack1llll1lll1_opy_.format(str(e)))
  return [None, None]
def bstack1l11l111ll_opy_(url, bstack1l1l1lll1l_opy_=False):
  global CONFIG
  global bstack1lll1l1l11_opy_
  if not bstack1lll1l1l11_opy_:
    hostname = bstack1l11111l1_opy_(url)
    is_private = bstack1l11l111l1_opy_(hostname)
    if (bstack11l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ๮") in CONFIG and not bstack1llll1l11_opy_(CONFIG[bstack11l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ๯")])) and (is_private or bstack1l1l1lll1l_opy_):
      bstack1lll1l1l11_opy_ = hostname
def bstack1l11111l1_opy_(url):
  return urlparse(url).hostname
def bstack1l11l111l1_opy_(hostname):
  for bstack11llll1l1l_opy_ in bstack11ll1l1111_opy_:
    regex = re.compile(bstack11llll1l1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111l11ll_opy_(bstack1l11ll1l_opy_):
  return True if bstack1l11ll1l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11l1ll11l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l1ll11l_opy_
  bstack11lll1l11_opy_ = not (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ๰"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ๱"), None))
  bstack1111lll11_opy_ = getattr(driver, bstack11l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ๲"), None) != True
  bstack1l1l111l11_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ๳"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭๴"), None)
  if bstack1l1l111l11_opy_:
    if not bstack1ll1ll111l_opy_():
      logger.warning(bstack11l1lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ๵"))
      return {}
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ๶"))
    logger.debug(perform_scan(driver, driver_command=bstack11l1lll_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧ๷")))
    results = bstack1ll111l1ll_opy_(bstack11l1lll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤ๸"))
    if results is not None and results.get(bstack11l1lll_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤ๹")) is not None:
        return results[bstack11l1lll_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥ๺")]
    logger.error(bstack11l1lll_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ๻"))
    return []
  if not bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack11l1ll11l_opy_) or (bstack1111lll11_opy_ and bstack11lll1l11_opy_):
    logger.warning(bstack11l1lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ๼"))
    return {}
  try:
    logger.debug(bstack11l1lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ๽"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1lll11ll11_opy_.bstack11l11ll1_opy_)
    return results
  except Exception:
    logger.error(bstack11l1lll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ๾"))
    return {}
@measure(event_name=EVENTS.bstack1ll1l1ll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l1ll11l_opy_
  bstack11lll1l11_opy_ = not (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ๿"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ຀"), None))
  bstack1111lll11_opy_ = getattr(driver, bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪກ"), None) != True
  bstack1l1l111l11_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຂ"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ຃"), None)
  if bstack1l1l111l11_opy_:
    if not bstack1ll1ll111l_opy_():
      logger.warning(bstack11l1lll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦຄ"))
      return {}
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ຅"))
    logger.debug(perform_scan(driver, driver_command=bstack11l1lll_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨຆ")))
    results = bstack1ll111l1ll_opy_(bstack11l1lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤງ"))
    if results is not None and results.get(bstack11l1lll_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦຈ")) is not None:
        return results[bstack11l1lll_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧຉ")]
    logger.error(bstack11l1lll_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢຊ"))
    return {}
  if not bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack11l1ll11l_opy_) or (bstack1111lll11_opy_ and bstack11lll1l11_opy_):
    logger.warning(bstack11l1lll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥ຋"))
    return {}
  try:
    logger.debug(bstack11l1lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬຌ"))
    logger.debug(perform_scan(driver))
    bstack1lll1ll11_opy_ = driver.execute_async_script(bstack1lll11ll11_opy_.bstack1ll1l1l1_opy_)
    return bstack1lll1ll11_opy_
  except Exception:
    logger.error(bstack11l1lll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤຍ"))
    return {}
def bstack1ll1ll111l_opy_():
  global CONFIG
  global bstack11l1ll11l_opy_
  bstack1l11llll11_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩຎ"), None) and bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຏ"), None)
  if not bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack11l1ll11l_opy_) or not bstack1l11llll11_opy_:
        logger.warning(bstack11l1lll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦຐ"))
        return False
  return True
def bstack1ll111l1ll_opy_(bstack1ll1111l1_opy_):
    bstack1l11llll1l_opy_ = bstack1lll11111l_opy_.current_test_uuid() if bstack1lll11111l_opy_.current_test_uuid() else bstack11l111l11l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1111ll1ll_opy_(bstack1l11llll1l_opy_, bstack1ll1111l1_opy_))
        try:
            return future.result(timeout=bstack1lllllll1_opy_)
        except TimeoutError:
            logger.error(bstack11l1lll_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦຑ").format(bstack1lllllll1_opy_))
        except Exception as ex:
            logger.debug(bstack11l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦຒ").format(bstack1ll1111l1_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11111ll1_opy_, stage=STAGE.bstack1l1l1lll1_opy_, bstack11l11ll1ll_opy_=bstack1l1l1ll1l1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l1ll11l_opy_
  bstack11lll1l11_opy_ = not (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຓ"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧດ"), None))
  bstack1llll1l1ll_opy_ = not (bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩຕ"), None) and bstack111l11lll_opy_(
          threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຖ"), None))
  bstack1111lll11_opy_ = getattr(driver, bstack11l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫທ"), None) != True
  if not bstack1l11111lll_opy_.bstack1l111l11ll_opy_(CONFIG, bstack11l1ll11l_opy_) or (bstack1111lll11_opy_ and bstack11lll1l11_opy_ and bstack1llll1l1ll_opy_):
    logger.warning(bstack11l1lll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢຘ"))
    return {}
  try:
    bstack1l1lll11l1_opy_ = bstack11l1lll_opy_ (u"࠭ࡡࡱࡲࠪນ") in CONFIG and CONFIG.get(bstack11l1lll_opy_ (u"ࠧࡢࡲࡳࠫບ"), bstack11l1lll_opy_ (u"ࠨࠩປ"))
    session_id = getattr(driver, bstack11l1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ຜ"), None)
    if not session_id:
      logger.warning(bstack11l1lll_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨຝ"))
      return {bstack11l1lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥພ"): bstack11l1lll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦຟ")}
    if bstack1l1lll11l1_opy_:
      try:
        bstack111l1111l_opy_ = {
              bstack11l1lll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪຠ"): os.environ.get(bstack11l1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬມ"), os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬຢ"), bstack11l1lll_opy_ (u"ࠩࠪຣ"))),
              bstack11l1lll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪ຤"): bstack1lll11111l_opy_.current_test_uuid() if bstack1lll11111l_opy_.current_test_uuid() else bstack11l111l11l_opy_.current_hook_uuid(),
              bstack11l1lll_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨລ"): os.environ.get(bstack11l1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ຦")),
              bstack11l1lll_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ວ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11l1lll_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬຨ"): os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ຩ"), bstack11l1lll_opy_ (u"ࠩࠪສ")),
              bstack11l1lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪຫ"): kwargs.get(bstack11l1lll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬຬ"), None) or bstack11l1lll_opy_ (u"ࠬ࠭ອ")
          }
        if not hasattr(thread_local, bstack11l1lll_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭ຮ")):
            scripts = {bstack11l1lll_opy_ (u"ࠧࡴࡥࡤࡲࠬຯ"): bstack1lll11ll11_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11ll1ll11l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11ll1ll11l_opy_[bstack11l1lll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ະ")] = bstack11ll1ll11l_opy_[bstack11l1lll_opy_ (u"ࠩࡶࡧࡦࡴࠧັ")] % json.dumps(bstack111l1111l_opy_)
        bstack1lll11ll11_opy_.bstack11llll11_opy_(bstack11ll1ll11l_opy_)
        bstack1lll11ll11_opy_.store()
        bstack1l11l1lll1_opy_ = driver.execute_script(bstack1lll11ll11_opy_.perform_scan)
      except Exception as bstack1l1lll11ll_opy_:
        logger.info(bstack11l1lll_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥາ") + str(bstack1l1lll11ll_opy_))
        bstack1l11l1lll1_opy_ = {bstack11l1lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥຳ"): str(bstack1l1lll11ll_opy_)}
    else:
      bstack1l11l1lll1_opy_ = driver.execute_async_script(bstack1lll11ll11_opy_.perform_scan, {bstack11l1lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬິ"): kwargs.get(bstack11l1lll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧີ"), None) or bstack11l1lll_opy_ (u"ࠧࠨຶ")})
    return bstack1l11l1lll1_opy_
  except Exception as err:
    logger.error(bstack11l1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥື").format(str(err)))
    return {}