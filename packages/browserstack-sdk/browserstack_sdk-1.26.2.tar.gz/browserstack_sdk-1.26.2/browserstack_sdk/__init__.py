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
from browserstack_sdk.bstack11lll1l1l1_opy_ import bstack1l111lll1_opy_
from browserstack_sdk.bstack1ll11ll1l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1l1lll11_opy_():
  global CONFIG
  headers = {
        bstack111l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1l11ll1l_opy_(CONFIG, bstack1l11llll1_opy_)
  try:
    response = requests.get(bstack1l11llll1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111l1l1l_opy_ = response.json()[bstack111l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1ll111l11_opy_.format(response.json()))
      return bstack1l111l1l1l_opy_
    else:
      logger.debug(bstack11ll111ll1_opy_.format(bstack111l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11ll111ll1_opy_.format(e))
def bstack1llllllll_opy_(hub_url):
  global CONFIG
  url = bstack111l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1l11ll1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l11l111l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1ll1l1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l111l11ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack1ll11lll_opy_():
  try:
    global bstack1ll11l1l_opy_
    bstack1l111l1l1l_opy_ = bstack1l1lll11_opy_()
    bstack11ll111l1_opy_ = []
    results = []
    for bstack11lll1ll1l_opy_ in bstack1l111l1l1l_opy_:
      bstack11ll111l1_opy_.append(bstack1ll11l11ll_opy_(target=bstack1llllllll_opy_,args=(bstack11lll1ll1l_opy_,)))
    for t in bstack11ll111l1_opy_:
      t.start()
    for t in bstack11ll111l1_opy_:
      results.append(t.join())
    bstack1l1l1l1l1_opy_ = {}
    for item in results:
      hub_url = item[bstack111l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1l1l1l1_opy_[hub_url] = latency
    bstack1l11ll1l_opy_ = min(bstack1l1l1l1l1_opy_, key= lambda x: bstack1l1l1l1l1_opy_[x])
    bstack1ll11l1l_opy_ = bstack1l11ll1l_opy_
    logger.debug(bstack1llll1ll_opy_.format(bstack1l11ll1l_opy_))
  except Exception as e:
    logger.debug(bstack111l11lll_opy_.format(e))
from browserstack_sdk.bstack111lll1l_opy_ import *
from browserstack_sdk.bstack11l1llll1l_opy_ import *
from browserstack_sdk.bstack1l111ll111_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1lll111lll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1l111ll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack1ll1l1l1l_opy_():
    global bstack1ll11l1l_opy_
    try:
        bstack11l1llll1_opy_ = bstack11l1l1ll11_opy_()
        bstack1l1l1l11l1_opy_(bstack11l1llll1_opy_)
        hub_url = bstack11l1llll1_opy_.get(bstack111l11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack111l11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack111l11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack111l11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1ll11l1l_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11l1l1ll11_opy_():
    global CONFIG
    bstack1l1l1lll1l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack111l11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack111l11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l1l1lll1l_opy_, str):
        raise ValueError(bstack111l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l1llll1_opy_ = bstack11l111llll_opy_(bstack1l1l1lll1l_opy_)
        return bstack11l1llll1_opy_
    except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack11l111llll_opy_(bstack1l1l1lll1l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack111l11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack11lll1l111_opy_ + bstack1l1l1lll1l_opy_
        auth = (CONFIG[bstack111l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1lll1111l1_opy_ = json.loads(response.text)
            return bstack1lll1111l1_opy_
    except ValueError as ve:
        logger.error(bstack111l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1l1l11l1_opy_(bstack1ll11l1111_opy_):
    global CONFIG
    if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack111l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack111l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack111l11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1ll11l1111_opy_:
        bstack11llll1111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack111l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11llll1111_opy_)
        bstack11l1l1l1l1_opy_ = bstack1ll11l1111_opy_.get(bstack111l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11llll1l11_opy_ = bstack111l11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11l1l1l1l1_opy_)
        logger.debug(bstack111l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11llll1l11_opy_)
        bstack1l1l11l11_opy_ = {
            bstack111l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack111l11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack111l11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack111l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack111l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11llll1l11_opy_
        }
        bstack11llll1111_opy_.update(bstack1l1l11l11_opy_)
        logger.debug(bstack111l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11llll1111_opy_)
        CONFIG[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11llll1111_opy_
        logger.debug(bstack111l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1ll111ll1_opy_():
    bstack11l1llll1_opy_ = bstack11l1l1ll11_opy_()
    if not bstack11l1llll1_opy_[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l1llll1_opy_[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack111l11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1ll1l111_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
def bstack1l1l1lll1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack111l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack111ll1ll1_opy_
        logger.debug(bstack111l11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack111l11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack111l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l11ll11l_opy_ = json.loads(response.text)
                bstack1l1lllll1_opy_ = bstack1l11ll11l_opy_.get(bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l1lllll1_opy_:
                    bstack1ll111111_opy_ = bstack1l1lllll1_opy_[0]
                    build_hashed_id = bstack1ll111111_opy_.get(bstack111l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1ll111l111_opy_ = bstack1l1lllll_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1ll111l111_opy_])
                    logger.info(bstack11ll111l1l_opy_.format(bstack1ll111l111_opy_))
                    bstack1l11l1111l_opy_ = CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l11l1111l_opy_ += bstack111l11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l11l1111l_opy_ != bstack1ll111111_opy_.get(bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l111ll1_opy_.format(bstack1ll111111_opy_.get(bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l11l1111l_opy_))
                    return result
                else:
                    logger.debug(bstack111l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack111l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack111l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack111l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll11l11l_opy_ import bstack1ll11l11l_opy_, bstack1l1111l1ll_opy_, bstack1l11111ll1_opy_, bstack11l1l1l1ll_opy_
from bstack_utils.measure import bstack11l11111l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l111lll_opy_ import bstack111ll111_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1lll111lll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll1l1l_opy_, bstack11l1111l_opy_, bstack1l1lll1ll_opy_, bstack1l1lllll1l_opy_, \
  bstack1l11111l1_opy_, \
  Notset, bstack1l1l1llll1_opy_, \
  bstack1llllll1l_opy_, bstack1lll11l1_opy_, bstack1l1l1ll1l_opy_, bstack11l1ll11ll_opy_, bstack11l11l11_opy_, bstack11l11ll11_opy_, \
  bstack1ll1ll11ll_opy_, \
  bstack11llll1l1_opy_, bstack11ll1ll1l1_opy_, bstack1lll11l11l_opy_, bstack11l1llllll_opy_, \
  bstack11111llll_opy_, bstack1ll111ll11_opy_, bstack1l1llll1_opy_, bstack1111llll1_opy_
from bstack_utils.bstack1ll1llll11_opy_ import bstack1ll1l11ll1_opy_, bstack1111l1ll1_opy_
from bstack_utils.bstack1lll11ll1l_opy_ import bstack1ll1l1l11_opy_
from bstack_utils.bstack1l11lll11l_opy_ import bstack11ll11l11_opy_, bstack11ll11ll_opy_
from bstack_utils.bstack11111ll1_opy_ import bstack11111ll1_opy_
from bstack_utils.bstack1ll111lll_opy_ import bstack1ll1111ll_opy_
from bstack_utils.proxy import bstack1ll1l1l111_opy_, bstack1l1l11ll1l_opy_, bstack11lllllll_opy_, bstack1l1l1l1ll1_opy_
from bstack_utils.bstack1l1l1111ll_opy_ import bstack1l1ll1111l_opy_
import bstack_utils.bstack1l11ll1111_opy_ as bstack11ll1ll1ll_opy_
import bstack_utils.bstack1l11l11l1l_opy_ as bstack1ll11111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack111l1ll1_opy_ import bstack1ll1l1llll_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack11ll11l11l_opy_
if os.getenv(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack11lll11l11_opy_()
else:
  os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack111l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1ll1llll1l_opy_ = bstack111l11_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1ll11111l1_opy_ = bstack111l11_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1llll1l1l1_opy_ = None
CONFIG = {}
bstack111lllll1_opy_ = {}
bstack11l11111_opy_ = {}
bstack1lll11l1ll_opy_ = None
bstack11ll1l1111_opy_ = None
bstack11lll11lll_opy_ = None
bstack1ll1111l1_opy_ = -1
bstack1l111l11_opy_ = 0
bstack1lll1l1l11_opy_ = bstack11llllll_opy_
bstack1ll1111l1l_opy_ = 1
bstack11lll1l11_opy_ = False
bstack11l1lll1_opy_ = False
bstack11llllllll_opy_ = bstack111l11_opy_ (u"ࠬ࠭ࢾ")
bstack1l11l11111_opy_ = bstack111l11_opy_ (u"࠭ࠧࢿ")
bstack1ll11ll11_opy_ = False
bstack11ll1l1l11_opy_ = True
bstack11ll1ll1l_opy_ = bstack111l11_opy_ (u"ࠧࠨࣀ")
bstack11111l1l_opy_ = []
bstack1ll11l1l_opy_ = bstack111l11_opy_ (u"ࠨࠩࣁ")
bstack111ll11ll_opy_ = False
bstack1l11l1l1_opy_ = None
bstack1l1ll11ll1_opy_ = None
bstack1l1111l1l_opy_ = None
bstack1l1l11l1ll_opy_ = -1
bstack11l1ll111l_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠩࢁࠫࣂ")), bstack111l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack111l11_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack11ll1l111_opy_ = 0
bstack1l11llllll_opy_ = 0
bstack1lll11ll_opy_ = []
bstack1l1l11ll11_opy_ = []
bstack1111ll11_opy_ = []
bstack11l111ll1l_opy_ = []
bstack1l1lll111l_opy_ = bstack111l11_opy_ (u"ࠬ࠭ࣅ")
bstack11lll11111_opy_ = bstack111l11_opy_ (u"࠭ࠧࣆ")
bstack1ll1lllll_opy_ = False
bstack11ll1l1l_opy_ = False
bstack1l1llll111_opy_ = {}
bstack11ll11lll1_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack1l11l1111_opy_ = None
bstack1l1111ll_opy_ = None
bstack1llllllll1_opy_ = None
bstack1llll1l11l_opy_ = None
bstack1111ll11l_opy_ = None
bstack1l1l11ll_opy_ = None
bstack1l1lll1111_opy_ = None
bstack111111ll_opy_ = None
bstack1l1111llll_opy_ = None
bstack111l1lll1_opy_ = None
bstack1l11ll11l1_opy_ = None
bstack1lll11l1l_opy_ = None
bstack11llll1ll1_opy_ = None
bstack1llll11ll1_opy_ = None
bstack1lllll1lll_opy_ = None
bstack1l111l1ll_opy_ = None
bstack1ll11l1l11_opy_ = None
bstack1ll1lll1_opy_ = None
bstack1l1l1lll_opy_ = None
bstack11ll11l1_opy_ = None
bstack1lll1111l_opy_ = None
thread_local = threading.local()
bstack1l1111111_opy_ = False
bstack1l1111l111_opy_ = bstack111l11_opy_ (u"ࠢࠣࣇ")
logger = bstack1lll111lll_opy_.get_logger(__name__, bstack1lll1l1l11_opy_)
bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
percy = bstack1111111ll_opy_()
bstack111ll11l_opy_ = bstack111ll111_opy_()
bstack11ll111l11_opy_ = bstack1l111ll111_opy_()
def bstack1ll1l1111_opy_():
  global CONFIG
  global bstack1ll1lllll_opy_
  global bstack111l111ll_opy_
  testContextOptions = bstack11ll1l11l_opy_(CONFIG)
  if bstack1l11111l1_opy_(CONFIG):
    if (bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack111l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack111l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1ll1lllll_opy_ = True
    bstack111l111ll_opy_.bstack11ll11ll11_opy_(testContextOptions.get(bstack111l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1ll1lllll_opy_ = True
    bstack111l111ll_opy_.bstack11ll11ll11_opy_(True)
def bstack1l11111l11_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1lll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1l1l11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111l11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack111l11_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11ll1ll1l_opy_
      bstack11ll1ll1l_opy_ += bstack111l11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack1l1111l11_opy_ = re.compile(bstack111l11_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack11l111l111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1111l11_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111l11_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack111l11_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack11l1ll1l1l_opy_():
  global bstack1lll1111l_opy_
  if bstack1lll1111l_opy_ is None:
        bstack1lll1111l_opy_ = bstack1l1l1l1l11_opy_()
  bstack1l111lll1l_opy_ = bstack1lll1111l_opy_
  if bstack1l111lll1l_opy_ and os.path.exists(os.path.abspath(bstack1l111lll1l_opy_)):
    fileName = bstack1l111lll1l_opy_
  if bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack1ll1lll_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll1lll_opy_ = bstack111l11_opy_ (u"ࠩࠪࣗ")
  bstack1l1l1111l_opy_ = os.getcwd()
  bstack111l1111l_opy_ = bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack1l111l1l_opy_ = bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack1ll1lll_opy_)) and bstack1l1l1111l_opy_ != bstack111l11_opy_ (u"ࠧࠨࣚ"):
    bstack1ll1lll_opy_ = os.path.join(bstack1l1l1111l_opy_, bstack111l1111l_opy_)
    if not os.path.exists(bstack1ll1lll_opy_):
      bstack1ll1lll_opy_ = os.path.join(bstack1l1l1111l_opy_, bstack1l111l1l_opy_)
    if bstack1l1l1111l_opy_ != os.path.dirname(bstack1l1l1111l_opy_):
      bstack1l1l1111l_opy_ = os.path.dirname(bstack1l1l1111l_opy_)
    else:
      bstack1l1l1111l_opy_ = bstack111l11_opy_ (u"ࠨࠢࣛ")
  bstack1lll1111l_opy_ = bstack1ll1lll_opy_ if os.path.exists(bstack1ll1lll_opy_) else None
  return bstack1lll1111l_opy_
def bstack1lll1ll1l_opy_():
  bstack1ll1lll_opy_ = bstack11l1ll1l1l_opy_()
  if not os.path.exists(bstack1ll1lll_opy_):
    bstack1ll11ll1_opy_(
      bstack11ll111111_opy_.format(os.getcwd()))
  try:
    with open(bstack1ll1lll_opy_, bstack111l11_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack111l11_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack1l1111l11_opy_)
      yaml.add_constructor(bstack111l11_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack11l111l111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1ll1lll_opy_, bstack111l11_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll11ll1_opy_(bstack11ll11l1l1_opy_.format(str(exc)))
def bstack1111ll1l1_opy_(config):
  bstack111ll1ll_opy_ = bstack1ll1ll11l1_opy_(config)
  for option in list(bstack111ll1ll_opy_):
    if option.lower() in bstack111l111l_opy_ and option != bstack111l111l_opy_[option.lower()]:
      bstack111ll1ll_opy_[bstack111l111l_opy_[option.lower()]] = bstack111ll1ll_opy_[option]
      del bstack111ll1ll_opy_[option]
  return config
def bstack1l111l1111_opy_():
  global bstack11l11111_opy_
  for key, bstack1l1ll1ll11_opy_ in bstack11ll1l111l_opy_.items():
    if isinstance(bstack1l1ll1ll11_opy_, list):
      for var in bstack1l1ll1ll11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l11111_opy_[key] = os.environ[var]
          break
    elif bstack1l1ll1ll11_opy_ in os.environ and os.environ[bstack1l1ll1ll11_opy_] and str(os.environ[bstack1l1ll1ll11_opy_]).strip():
      bstack11l11111_opy_[key] = os.environ[bstack1l1ll1ll11_opy_]
  if bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack11l11111_opy_[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack11l11111_opy_[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack111l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack1ll1l11l1l_opy_():
  global bstack111lllll1_opy_
  global bstack11ll1ll1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111l11_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l11lll1l_opy_ in bstack1llll1ll1l_opy_.items():
    if isinstance(bstack1l11lll1l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l11lll1l_opy_:
          if idx < len(sys.argv) and bstack111l11_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack111lllll1_opy_:
            bstack111lllll1_opy_[key] = sys.argv[idx + 1]
            bstack11ll1ll1l_opy_ += bstack111l11_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack111l11_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111l11_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack1l11lll1l_opy_.lower() == val.lower() and not key in bstack111lllll1_opy_:
          bstack111lllll1_opy_[key] = sys.argv[idx + 1]
          bstack11ll1ll1l_opy_ += bstack111l11_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack1l11lll1l_opy_ + bstack111l11_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll1lll1ll_opy_(config):
  bstack1llll11l1l_opy_ = config.keys()
  for bstack111llllll_opy_, bstack1l111llll_opy_ in bstack1lll1llll1_opy_.items():
    if bstack1l111llll_opy_ in bstack1llll11l1l_opy_:
      config[bstack111llllll_opy_] = config[bstack1l111llll_opy_]
      del config[bstack1l111llll_opy_]
  for bstack111llllll_opy_, bstack1l111llll_opy_ in bstack11l1ll1111_opy_.items():
    if isinstance(bstack1l111llll_opy_, list):
      for bstack1llll11111_opy_ in bstack1l111llll_opy_:
        if bstack1llll11111_opy_ in bstack1llll11l1l_opy_:
          config[bstack111llllll_opy_] = config[bstack1llll11111_opy_]
          del config[bstack1llll11111_opy_]
          break
    elif bstack1l111llll_opy_ in bstack1llll11l1l_opy_:
      config[bstack111llllll_opy_] = config[bstack1l111llll_opy_]
      del config[bstack1l111llll_opy_]
  for bstack1llll11111_opy_ in list(config):
    for bstack11lllllll1_opy_ in bstack11l11ll111_opy_:
      if bstack1llll11111_opy_.lower() == bstack11lllllll1_opy_.lower() and bstack1llll11111_opy_ != bstack11lllllll1_opy_:
        config[bstack11lllllll1_opy_] = config[bstack1llll11111_opy_]
        del config[bstack1llll11111_opy_]
  bstack1ll111l1_opy_ = [{}]
  if not config.get(bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack1ll111l1_opy_ = config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack1ll111l1_opy_:
    for bstack1llll11111_opy_ in list(platform):
      for bstack11lllllll1_opy_ in bstack11l11ll111_opy_:
        if bstack1llll11111_opy_.lower() == bstack11lllllll1_opy_.lower() and bstack1llll11111_opy_ != bstack11lllllll1_opy_:
          platform[bstack11lllllll1_opy_] = platform[bstack1llll11111_opy_]
          del platform[bstack1llll11111_opy_]
  for bstack111llllll_opy_, bstack1l111llll_opy_ in bstack11l1ll1111_opy_.items():
    for platform in bstack1ll111l1_opy_:
      if isinstance(bstack1l111llll_opy_, list):
        for bstack1llll11111_opy_ in bstack1l111llll_opy_:
          if bstack1llll11111_opy_ in platform:
            platform[bstack111llllll_opy_] = platform[bstack1llll11111_opy_]
            del platform[bstack1llll11111_opy_]
            break
      elif bstack1l111llll_opy_ in platform:
        platform[bstack111llllll_opy_] = platform[bstack1l111llll_opy_]
        del platform[bstack1l111llll_opy_]
  for bstack1llll1l111_opy_ in bstack1ll1ll11l_opy_:
    if bstack1llll1l111_opy_ in config:
      if not bstack1ll1ll11l_opy_[bstack1llll1l111_opy_] in config:
        config[bstack1ll1ll11l_opy_[bstack1llll1l111_opy_]] = {}
      config[bstack1ll1ll11l_opy_[bstack1llll1l111_opy_]].update(config[bstack1llll1l111_opy_])
      del config[bstack1llll1l111_opy_]
  for platform in bstack1ll111l1_opy_:
    for bstack1llll1l111_opy_ in bstack1ll1ll11l_opy_:
      if bstack1llll1l111_opy_ in list(platform):
        if not bstack1ll1ll11l_opy_[bstack1llll1l111_opy_] in platform:
          platform[bstack1ll1ll11l_opy_[bstack1llll1l111_opy_]] = {}
        platform[bstack1ll1ll11l_opy_[bstack1llll1l111_opy_]].update(platform[bstack1llll1l111_opy_])
        del platform[bstack1llll1l111_opy_]
  config = bstack1111ll1l1_opy_(config)
  return config
def bstack1l11l1lll_opy_(config):
  global bstack1l11l11111_opy_
  bstack1ll1111lll_opy_ = False
  if bstack111l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack111l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack111l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack111l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack11l1llll1_opy_ = bstack11l1l1ll11_opy_()
      if bstack111l11_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack11l1llll1_opy_:
        if not bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack111l11_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack1ll1111lll_opy_ = True
        bstack1l11l11111_opy_ = config[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack111l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1l11111l1_opy_(config) and bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack111l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack1ll1111lll_opy_:
    if not bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack11l11ll11l_opy_ = datetime.datetime.now()
      bstack1lll11l11_opy_ = bstack11l11ll11l_opy_.strftime(bstack111l11_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack11l1l1ll1l_opy_ = bstack111l11_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111l11_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1lll11l11_opy_, hostname, bstack11l1l1ll1l_opy_)
      config[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack111l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack1l11l11111_opy_ = config[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1lll1l111l_opy_():
  bstack111l11l1l_opy_ =  bstack11l1ll11ll_opy_()[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack111l11l1l_opy_ if bstack111l11l1l_opy_ else -1
def bstack1lllll11ll_opy_(bstack111l11l1l_opy_):
  global CONFIG
  if not bstack111l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack111l11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack111l11l1l_opy_)
  )
def bstack1l11lll1ll_opy_():
  global CONFIG
  if not bstack111l11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack11l11ll11l_opy_ = datetime.datetime.now()
  bstack1lll11l11_opy_ = bstack11l11ll11l_opy_.strftime(bstack111l11_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack111l11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1lll11l11_opy_
  )
def bstack1111l1l1l_opy_():
  global CONFIG
  if bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack111l11_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack111l11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack1l11lll1ll_opy_()
    os.environ[bstack111l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack111l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack111l11l1l_opy_ = bstack111l11_opy_ (u"ࠧࠨऩ")
  bstack1l1l1111_opy_ = bstack1lll1l111l_opy_()
  if bstack1l1l1111_opy_ != -1:
    bstack111l11l1l_opy_ = bstack111l11_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack1l1l1111_opy_)
  if bstack111l11l1l_opy_ == bstack111l11_opy_ (u"ࠩࠪफ"):
    bstack1ll1l11l_opy_ = bstack11l1l11ll1_opy_(CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1ll1l11l_opy_ != -1:
      bstack111l11l1l_opy_ = str(bstack1ll1l11l_opy_)
  if bstack111l11l1l_opy_:
    bstack1lllll11ll_opy_(bstack111l11l1l_opy_)
    os.environ[bstack111l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack11l1l11l_opy_(bstack11l1l1ll1_opy_, bstack1l11l1ll_opy_, path):
  bstack111l11111_opy_ = {
    bstack111l11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1l11l1ll_opy_
  }
  if os.path.exists(path):
    bstack1lll1ll1_opy_ = json.load(open(path, bstack111l11_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack1lll1ll1_opy_ = {}
  bstack1lll1ll1_opy_[bstack11l1l1ll1_opy_] = bstack111l11111_opy_
  with open(path, bstack111l11_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack1lll1ll1_opy_, outfile)
def bstack11l1l11ll1_opy_(bstack11l1l1ll1_opy_):
  bstack11l1l1ll1_opy_ = str(bstack11l1l1ll1_opy_)
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠩࢁࠫल")), bstack111l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack1l1l111l1_opy_):
      os.makedirs(bstack1l1l111l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠫࢃ࠭ऴ")), bstack111l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack111l11_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111l11_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack111l11_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111l11_opy_ (u"ࠩࡵࠫह")) as bstack11l11lll_opy_:
      bstack11l1l1llll_opy_ = json.load(bstack11l11lll_opy_)
    if bstack11l1l1ll1_opy_ in bstack11l1l1llll_opy_:
      bstack1lllllllll_opy_ = bstack11l1l1llll_opy_[bstack11l1l1ll1_opy_][bstack111l11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack1ll11lll11_opy_ = int(bstack1lllllllll_opy_) + 1
      bstack11l1l11l_opy_(bstack11l1l1ll1_opy_, bstack1ll11lll11_opy_, file_path)
      return bstack1ll11lll11_opy_
    else:
      bstack11l1l11l_opy_(bstack11l1l1ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1111l11l_opy_.format(str(e)))
    return -1
def bstack11l1ll1lll_opy_(config):
  if not config[bstack111l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack1l1l11111l_opy_(config, index=0):
  global bstack1ll11ll11_opy_
  bstack1lll1lll11_opy_ = {}
  caps = bstack1111ll1ll_opy_ + bstack1lll1l1111_opy_
  if config.get(bstack111l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack1ll11ll11_opy_:
    caps += bstack1l11ll11ll_opy_
  for key in config:
    if key in caps + [bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack1lll1lll11_opy_[key] = config[key]
  if bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack11l1ll11_opy_ in config[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack11l1ll11_opy_ in caps:
        continue
      bstack1lll1lll11_opy_[bstack11l1ll11_opy_] = config[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack11l1ll11_opy_]
  bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack111l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack1lll1lll11_opy_:
    del (bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack1lll1lll11_opy_
def bstack1llll1l1l_opy_(config):
  global bstack1ll11ll11_opy_
  bstack1111111l_opy_ = {}
  caps = bstack1lll1l1111_opy_
  if bstack1ll11ll11_opy_:
    caps += bstack1l11ll11ll_opy_
  for key in caps:
    if key in config:
      bstack1111111l_opy_[key] = config[key]
  return bstack1111111l_opy_
def bstack111111l1_opy_(bstack1lll1lll11_opy_, bstack1111111l_opy_):
  bstack11l11l11l1_opy_ = {}
  for key in bstack1lll1lll11_opy_.keys():
    if key in bstack1lll1llll1_opy_:
      bstack11l11l11l1_opy_[bstack1lll1llll1_opy_[key]] = bstack1lll1lll11_opy_[key]
    else:
      bstack11l11l11l1_opy_[key] = bstack1lll1lll11_opy_[key]
  for key in bstack1111111l_opy_:
    if key in bstack1lll1llll1_opy_:
      bstack11l11l11l1_opy_[bstack1lll1llll1_opy_[key]] = bstack1111111l_opy_[key]
    else:
      bstack11l11l11l1_opy_[key] = bstack1111111l_opy_[key]
  return bstack11l11l11l1_opy_
def bstack1l111111_opy_(config, index=0):
  global bstack1ll11ll11_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll11l111_opy_ = bstack1lll1l1l_opy_(bstack1111l1ll_opy_, config, logger)
  bstack1111111l_opy_ = bstack1llll1l1l_opy_(config)
  bstack1l1ll1lll_opy_ = bstack1lll1l1111_opy_
  bstack1l1ll1lll_opy_ += bstack1l1lll111_opy_
  bstack1111111l_opy_ = update(bstack1111111l_opy_, bstack1ll11l111_opy_)
  if bstack1ll11ll11_opy_:
    bstack1l1ll1lll_opy_ += bstack1l11ll11ll_opy_
  if bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1l1l1ll1ll_opy_ = bstack1lll1l1l_opy_(bstack1111l1ll_opy_, config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1l1ll1lll_opy_ += list(bstack1l1l1ll1ll_opy_.keys())
    for bstack1lll1lll1_opy_ in bstack1l1ll1lll_opy_:
      if bstack1lll1lll1_opy_ in config[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack1lll1lll1_opy_ == bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1l1l1ll1ll_opy_[bstack1lll1lll1_opy_] = str(config[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1lll1lll1_opy_] * 1.0)
          except:
            bstack1l1l1ll1ll_opy_[bstack1lll1lll1_opy_] = str(config[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1lll1lll1_opy_])
        else:
          bstack1l1l1ll1ll_opy_[bstack1lll1lll1_opy_] = config[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1lll1lll1_opy_]
        del (config[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1lll1lll1_opy_])
    bstack1111111l_opy_ = update(bstack1111111l_opy_, bstack1l1l1ll1ll_opy_)
  bstack1lll1lll11_opy_ = bstack1l1l11111l_opy_(config, index)
  for bstack1llll11111_opy_ in bstack1lll1l1111_opy_ + list(bstack1ll11l111_opy_.keys()):
    if bstack1llll11111_opy_ in bstack1lll1lll11_opy_:
      bstack1111111l_opy_[bstack1llll11111_opy_] = bstack1lll1lll11_opy_[bstack1llll11111_opy_]
      del (bstack1lll1lll11_opy_[bstack1llll11111_opy_])
  if bstack1l1l1llll1_opy_(config):
    bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack1111111l_opy_)
    caps[bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack1lll1lll11_opy_
  else:
    bstack1lll1lll11_opy_[bstack111l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack111111l1_opy_(bstack1lll1lll11_opy_, bstack1111111l_opy_))
    if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack1l1ll11l11_opy_():
  global bstack1ll11l1l_opy_
  global CONFIG
  if bstack11l1lll1l_opy_() <= version.parse(bstack111l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1ll11l1l_opy_ != bstack111l11_opy_ (u"ࠬ࠭०"):
      return bstack111l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1ll11l1l_opy_ + bstack111l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack111lllll_opy_
  if bstack1ll11l1l_opy_ != bstack111l11_opy_ (u"ࠨࠩ३"):
    return bstack111l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1ll11l1l_opy_ + bstack111l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack1ll1ll1111_opy_
def bstack11lll1llll_opy_(options):
  return hasattr(options, bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
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
def bstack1111l11l1_opy_(options, bstack1l1llll1ll_opy_):
  for bstack11l1ll1l11_opy_ in bstack1l1llll1ll_opy_:
    if bstack11l1ll1l11_opy_ in [bstack111l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack111l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack11l1ll1l11_opy_ in options._experimental_options:
      options._experimental_options[bstack11l1ll1l11_opy_] = update(options._experimental_options[bstack11l1ll1l11_opy_],
                                                         bstack1l1llll1ll_opy_[bstack11l1ll1l11_opy_])
    else:
      options.add_experimental_option(bstack11l1ll1l11_opy_, bstack1l1llll1ll_opy_[bstack11l1ll1l11_opy_])
  if bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack1l1llll1ll_opy_:
    for arg in bstack1l1llll1ll_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack1l1llll1ll_opy_[bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack111l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack1l1llll1ll_opy_:
    for ext in bstack1l1llll1ll_opy_[bstack111l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1llll1ll_opy_[bstack111l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack111lll111_opy_(options, bstack1lllll111_opy_):
  if bstack111l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1lllll111_opy_:
    for bstack11l1ll1l1_opy_ in bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack11l1ll1l1_opy_ in options._preferences:
        options._preferences[bstack11l1ll1l1_opy_] = update(options._preferences[bstack11l1ll1l1_opy_], bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack11l1ll1l1_opy_])
      else:
        options.set_preference(bstack11l1ll1l1_opy_, bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack11l1ll1l1_opy_])
  if bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1lllll111_opy_:
    for arg in bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1l111l111_opy_(options, bstack11111l11_opy_):
  if bstack111l11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack11111l11_opy_:
    options.use_webview(bool(bstack11111l11_opy_[bstack111l11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack1111l11l1_opy_(options, bstack11111l11_opy_)
def bstack1ll111lll1_opy_(options, bstack11ll1lll_opy_):
  for bstack1l11ll1l1l_opy_ in bstack11ll1lll_opy_:
    if bstack1l11ll1l1l_opy_ in [bstack111l11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack1l11ll1l1l_opy_, bstack11ll1lll_opy_[bstack1l11ll1l1l_opy_])
  if bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack11ll1lll_opy_:
    for arg in bstack11ll1lll_opy_[bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack111l11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack11ll1lll_opy_:
    options.bstack1llll11l1_opy_(bool(bstack11ll1lll_opy_[bstack111l11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack1l1111l1_opy_(options, bstack1ll1ll111l_opy_):
  for bstack1ll1lllll1_opy_ in bstack1ll1ll111l_opy_:
    if bstack1ll1lllll1_opy_ in [bstack111l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack1ll1lllll1_opy_] = bstack1ll1ll111l_opy_[bstack1ll1lllll1_opy_]
  if bstack111l11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack1ll1ll111l_opy_:
    for bstack11l1l1111l_opy_ in bstack1ll1ll111l_opy_[bstack111l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l111l1l11_opy_(
        bstack11l1l1111l_opy_, bstack1ll1ll111l_opy_[bstack111l11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack11l1l1111l_opy_])
  if bstack111l11_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack1ll1ll111l_opy_:
    for arg in bstack1ll1ll111l_opy_[bstack111l11_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack1ll11l1ll1_opy_(options, caps):
  if not hasattr(options, bstack111l11_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack111l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ"):
    options = bstack11lll1ll1_opy_.bstack11ll1111ll_opy_(bstack111l1l11l_opy_=options, config=CONFIG)
  if options.KEY == bstack111l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ") and options.KEY in caps:
    bstack1111l11l1_opy_(options, caps[bstack111l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঍")])
  elif options.KEY == bstack111l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎") and options.KEY in caps:
    bstack111lll111_opy_(options, caps[bstack111l11_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩএ")])
  elif options.KEY == bstack111l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ") and options.KEY in caps:
    bstack1ll111lll1_opy_(options, caps[bstack111l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ঑")])
  elif options.KEY == bstack111l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒") and options.KEY in caps:
    bstack1l111l111_opy_(options, caps[bstack111l11_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩও")])
  elif options.KEY == bstack111l11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ") and options.KEY in caps:
    bstack1l1111l1_opy_(options, caps[bstack111l11_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩক")])
def bstack11l1lll1ll_opy_(caps):
  global bstack1ll11ll11_opy_
  if isinstance(os.environ.get(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")), str):
    bstack1ll11ll11_opy_ = eval(os.getenv(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭গ")))
  if bstack1ll11ll11_opy_:
    if bstack1l11111l11_opy_() < version.parse(bstack111l11_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬঘ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঙ")
    if bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ") in caps:
      browser = caps[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧছ")]
    elif bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ") in caps:
      browser = caps[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬঝ")]
    browser = str(browser).lower()
    if browser == bstack111l11_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬঞ") or browser == bstack111l11_opy_ (u"࠭ࡩࡱࡣࡧࠫট"):
      browser = bstack111l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧঠ")
    if browser == bstack111l11_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩড"):
      browser = bstack111l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ")
    if browser not in [bstack111l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ"), bstack111l11_opy_ (u"ࠫࡪࡪࡧࡦࠩত"), bstack111l11_opy_ (u"ࠬ࡯ࡥࠨথ"), bstack111l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭দ"), bstack111l11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨধ")]:
      return None
    try:
      package = bstack111l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪন").format(browser)
      name = bstack111l11_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ঩")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11lll1llll_opy_(options):
        return None
      for bstack1llll11111_opy_ in caps.keys():
        options.set_capability(bstack1llll11111_opy_, caps[bstack1llll11111_opy_])
      bstack1ll11l1ll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll1ll1l1_opy_(options, bstack11l1lll111_opy_):
  if not bstack11lll1llll_opy_(options):
    return
  for bstack1llll11111_opy_ in bstack11l1lll111_opy_.keys():
    if bstack1llll11111_opy_ in bstack1l1lll111_opy_:
      continue
    if bstack1llll11111_opy_ in options._caps and type(options._caps[bstack1llll11111_opy_]) in [dict, list]:
      options._caps[bstack1llll11111_opy_] = update(options._caps[bstack1llll11111_opy_], bstack11l1lll111_opy_[bstack1llll11111_opy_])
    else:
      options.set_capability(bstack1llll11111_opy_, bstack11l1lll111_opy_[bstack1llll11111_opy_])
  bstack1ll11l1ll1_opy_(options, bstack11l1lll111_opy_)
  if bstack111l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ") in options._caps:
    if options._caps[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")] and options._caps[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪব")].lower() != bstack111l11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧভ"):
      del options._caps[bstack111l11_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ম")]
def bstack1l11111ll_opy_(proxy_config):
  if bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬয") in proxy_config:
    proxy_config[bstack111l11_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫর")] = proxy_config[bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")]
    del (proxy_config[bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨল")])
  if bstack111l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳") in proxy_config and proxy_config[bstack111l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ঴")].lower() != bstack111l11_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧ঵"):
    proxy_config[bstack111l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫশ")] = bstack111l11_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩষ")
  if bstack111l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨস") in proxy_config:
    proxy_config[bstack111l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧহ")] = bstack111l11_opy_ (u"ࠬࡶࡡࡤࠩ঺")
  return proxy_config
def bstack11l1l11l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻") in config:
    return proxy
  config[bstack111l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")] = bstack1l11111ll_opy_(config[bstack111l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  if proxy == None:
    proxy = Proxy(config[bstack111l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨা")])
  return proxy
def bstack1ll1l1ll1l_opy_(self):
  global CONFIG
  global bstack111l1lll1_opy_
  try:
    proxy = bstack11lllllll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111l11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨি")):
        proxies = bstack1ll1l1l111_opy_(proxy, bstack1l1ll11l11_opy_())
        if len(proxies) > 0:
          protocol, bstack1lllllll1_opy_ = proxies.popitem()
          if bstack111l11_opy_ (u"ࠦ࠿࠵࠯ࠣী") in bstack1lllllll1_opy_:
            return bstack1lllllll1_opy_
          else:
            return bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨু") + bstack1lllllll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥূ").format(str(e)))
  return bstack111l1lll1_opy_(self)
def bstack11lll11l1l_opy_():
  global CONFIG
  return bstack1l1l1l1ll1_opy_(CONFIG) and bstack11l11ll11_opy_() and bstack11l1lll1l_opy_() >= version.parse(bstack11l1ll111_opy_)
def bstack11ll1111_opy_():
  global CONFIG
  return (bstack111l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪৃ") in CONFIG or bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬৄ") in CONFIG) and bstack1ll1ll11ll_opy_()
def bstack1ll1ll11l1_opy_(config):
  bstack111ll1ll_opy_ = {}
  if bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅") in config:
    bstack111ll1ll_opy_ = config[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৆")]
  if bstack111l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে") in config:
    bstack111ll1ll_opy_ = config[bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫৈ")]
  proxy = bstack11lllllll_opy_(config)
  if proxy:
    if proxy.endswith(bstack111l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")) and os.path.isfile(proxy):
      bstack111ll1ll_opy_[bstack111l11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ৊")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111l11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ো")):
        proxies = bstack1l1l11ll1l_opy_(config, bstack1l1ll11l11_opy_())
        if len(proxies) > 0:
          protocol, bstack1lllllll1_opy_ = proxies.popitem()
          if bstack111l11_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") in bstack1lllllll1_opy_:
            parsed_url = urlparse(bstack1lllllll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111l11_opy_ (u"ࠥ࠾࠴࠵্ࠢ") + bstack1lllllll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111ll1ll_opy_[bstack111l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧৎ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111ll1ll_opy_[bstack111l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ৏")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111ll1ll_opy_[bstack111l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ৐")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111ll1ll_opy_[bstack111l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ৑")] = str(parsed_url.password)
  return bstack111ll1ll_opy_
def bstack11ll1l11l_opy_(config):
  if bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒") in config:
    return config[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ৓")]
  return {}
def bstack1l1ll1l111_opy_(caps):
  global bstack1l11l11111_opy_
  if bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔") in caps:
    caps[bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ৕")][bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ৖")] = True
    if bstack1l11l11111_opy_:
      caps[bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧৗ")][bstack111l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৘")] = bstack1l11l11111_opy_
  else:
    caps[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭৙")] = True
    if bstack1l11l11111_opy_:
      caps[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ৚")] = bstack1l11l11111_opy_
@measure(event_name=EVENTS.bstack1llll1ll11_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l11llll_opy_():
  global CONFIG
  if not bstack1l11111l1_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛") in CONFIG and bstack1l1llll1_opy_(CONFIG[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨড়")]):
    if (
      bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়") in CONFIG
      and bstack1l1llll1_opy_(CONFIG[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৞")].get(bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫয়")))
    ):
      logger.debug(bstack111l11_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤৠ"))
      return
    bstack111ll1ll_opy_ = bstack1ll1ll11l1_opy_(CONFIG)
    bstack1lll111l1_opy_(CONFIG[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬৡ")], bstack111ll1ll_opy_)
def bstack1lll111l1_opy_(key, bstack111ll1ll_opy_):
  global bstack1llll1l1l1_opy_
  logger.info(bstack1l111lllll_opy_)
  try:
    bstack1llll1l1l1_opy_ = Local()
    bstack1lll11l111_opy_ = {bstack111l11_opy_ (u"ࠪ࡯ࡪࡿࠧৢ"): key}
    bstack1lll11l111_opy_.update(bstack111ll1ll_opy_)
    logger.debug(bstack1ll111ll_opy_.format(str(bstack1lll11l111_opy_)).replace(key, bstack111l11_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨৣ")))
    bstack1llll1l1l1_opy_.start(**bstack1lll11l111_opy_)
    if bstack1llll1l1l1_opy_.isRunning():
      logger.info(bstack11l1l11111_opy_)
  except Exception as e:
    bstack1ll11ll1_opy_(bstack111l11ll_opy_.format(str(e)))
def bstack1ll11llll_opy_():
  global bstack1llll1l1l1_opy_
  if bstack1llll1l1l1_opy_.isRunning():
    logger.info(bstack1lllll1ll1_opy_)
    bstack1llll1l1l1_opy_.stop()
  bstack1llll1l1l1_opy_ = None
def bstack1ll111l1l_opy_(bstack11l1ll11l1_opy_=[]):
  global CONFIG
  bstack11l1l111l_opy_ = []
  bstack1llllll111_opy_ = [bstack111l11_opy_ (u"ࠬࡵࡳࠨ৤"), bstack111l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৥"), bstack111l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ০"), bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ১"), bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ২"), bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ৩")]
  try:
    for err in bstack11l1ll11l1_opy_:
      bstack11111ll11_opy_ = {}
      for k in bstack1llllll111_opy_:
        val = CONFIG[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৪")][int(err[bstack111l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ৫")])].get(k)
        if val:
          bstack11111ll11_opy_[k] = val
      if(err[bstack111l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৬")] != bstack111l11_opy_ (u"ࠧࠨ৭")):
        bstack11111ll11_opy_[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧ৮")] = {
          err[bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৯")]: err[bstack111l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩৰ")]
        }
        bstack11l1l111l_opy_.append(bstack11111ll11_opy_)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ৱ") + str(e))
  finally:
    return bstack11l1l111l_opy_
def bstack1l1l1l111_opy_(file_name):
  bstack1llll111l1_opy_ = []
  try:
    bstack1lll1l11l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lll1l11l1_opy_):
      with open(bstack1lll1l11l1_opy_) as f:
        bstack1l11ll1ll1_opy_ = json.load(f)
        bstack1llll111l1_opy_ = bstack1l11ll1ll1_opy_
      os.remove(bstack1lll1l11l1_opy_)
    return bstack1llll111l1_opy_
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧ৲") + str(e))
    return bstack1llll111l1_opy_
def bstack1lllll11_opy_():
  try:
      from bstack_utils.constants import bstack11lll11l_opy_, EVENTS
      from bstack_utils.helper import bstack11l1111l_opy_, get_host_info, bstack111l111ll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack111ll1l11_opy_ = os.path.join(os.getcwd(), bstack111l11_opy_ (u"࠭࡬ࡰࡩࠪ৳"), bstack111l11_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ৴"))
      lock = FileLock(bstack111ll1l11_opy_+bstack111l11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ৵"))
      def bstack111l1l1ll_opy_():
          try:
              with lock:
                  with open(bstack111ll1l11_opy_, bstack111l11_opy_ (u"ࠤࡵࠦ৶"), encoding=bstack111l11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ৷")) as file:
                      data = json.load(file)
                      config = {
                          bstack111l11_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ৸"): {
                              bstack111l11_opy_ (u"ࠧࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠦ৹"): bstack111l11_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠤ৺"),
                          }
                      }
                      bstack1l1llll1l_opy_ = datetime.utcnow()
                      bstack11l11ll11l_opy_ = bstack1l1llll1l_opy_.strftime(bstack111l11_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦ৻"))
                      bstack1ll1l1lll_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) if os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ৽")) else bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧ৾"))
                      payload = {
                          bstack111l11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣ৿"): bstack111l11_opy_ (u"ࠧࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤ਀"),
                          bstack111l11_opy_ (u"ࠨࡤࡢࡶࡤࠦਁ"): {
                              bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩࠨਂ"): bstack1ll1l1lll_opy_,
                              bstack111l11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࡡࡧࡥࡾࠨਃ"): bstack11l11ll11l_opy_,
                              bstack111l11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࠨ਄"): bstack111l11_opy_ (u"ࠥࡗࡉࡑࡆࡦࡣࡷࡹࡷ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࠦਅ"),
                              bstack111l11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣਆ"): {
                                  bstack111l11_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࡹࠢਇ"): data,
                                  bstack111l11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"): bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤਉ"))
                              },
                              bstack111l11_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦਊ"): bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਋")),
                              bstack111l11_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨ਌"): get_host_info()
                          }
                      }
                      response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠦࡕࡕࡓࡕࠤ਍"), bstack11lll11l_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack111l11_opy_ (u"ࠧࡊࡡࡵࡣࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack11lll11l_opy_, payload))
                      else:
                          logger.debug(bstack111l11_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡧࡱࡵࠤࢀࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࠣࡿࢂࠨਏ").format(bstack11lll11l_opy_, payload))
          except Exception as e:
              logger.debug(bstack111l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡࡽࢀࠦਐ").format(e))
      bstack111l1l1ll_opy_()
      bstack1lll11l1_opy_(bstack111ll1l11_opy_, logger)
  except:
    pass
def bstack1l11l11l_opy_():
  global bstack1l1111l111_opy_
  global bstack11111l1l_opy_
  global bstack1lll11ll_opy_
  global bstack1l1l11ll11_opy_
  global bstack1111ll11_opy_
  global bstack11lll11111_opy_
  global CONFIG
  bstack1l1ll1l11l_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ਑"))
  if bstack1l1ll1l11l_opy_ in [bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ਒"), bstack111l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩਓ")]:
    bstack1l11lllll_opy_()
  percy.shutdown()
  if bstack1l1111l111_opy_:
    logger.warning(bstack1ll11111ll_opy_.format(str(bstack1l1111l111_opy_)))
  else:
    try:
      bstack1lll1ll1_opy_ = bstack1llllll1l_opy_(bstack111l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪਔ"), logger)
      if bstack1lll1ll1_opy_.get(bstack111l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")) and bstack1lll1ll1_opy_.get(bstack111l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਖ")).get(bstack111l11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩਗ")):
        logger.warning(bstack1ll11111ll_opy_.format(str(bstack1lll1ll1_opy_[bstack111l11_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ਘ")][bstack111l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫਙ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.bstack11ll1l1l1_opy_)
  logger.info(bstack1ll11l1ll_opy_)
  global bstack1llll1l1l1_opy_
  if bstack1llll1l1l1_opy_:
    bstack1ll11llll_opy_()
  try:
    for driver in bstack11111l1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11ll1lll1l_opy_)
  if bstack11lll11111_opy_ == bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ"):
    bstack1111ll11_opy_ = bstack1l1l1l111_opy_(bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਛ"))
  if bstack11lll11111_opy_ == bstack111l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਜ") and len(bstack1l1l11ll11_opy_) == 0:
    bstack1l1l11ll11_opy_ = bstack1l1l1l111_opy_(bstack111l11_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਝ"))
    if len(bstack1l1l11ll11_opy_) == 0:
      bstack1l1l11ll11_opy_ = bstack1l1l1l111_opy_(bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਞ"))
  bstack1lllll1ll_opy_ = bstack111l11_opy_ (u"ࠨࠩਟ")
  if len(bstack1lll11ll_opy_) > 0:
    bstack1lllll1ll_opy_ = bstack1ll111l1l_opy_(bstack1lll11ll_opy_)
  elif len(bstack1l1l11ll11_opy_) > 0:
    bstack1lllll1ll_opy_ = bstack1ll111l1l_opy_(bstack1l1l11ll11_opy_)
  elif len(bstack1111ll11_opy_) > 0:
    bstack1lllll1ll_opy_ = bstack1ll111l1l_opy_(bstack1111ll11_opy_)
  elif len(bstack11l111ll1l_opy_) > 0:
    bstack1lllll1ll_opy_ = bstack1ll111l1l_opy_(bstack11l111ll1l_opy_)
  if bool(bstack1lllll1ll_opy_):
    bstack11ll1111l1_opy_(bstack1lllll1ll_opy_)
  else:
    bstack11ll1111l1_opy_()
  bstack1lll11l1_opy_(bstack1l1lll11ll_opy_, logger)
  if bstack1l1ll1l11l_opy_ not in [bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪਠ")]:
    bstack1lllll11_opy_()
  bstack1lll111lll_opy_.bstack1ll1llll_opy_(CONFIG)
  if len(bstack1111ll11_opy_) > 0:
    sys.exit(len(bstack1111ll11_opy_))
def bstack1111l1l11_opy_(bstack11lll1lll1_opy_, frame):
  global bstack111l111ll_opy_
  logger.error(bstack1llll11l11_opy_)
  bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ਡ"), bstack11lll1lll1_opy_)
  if hasattr(signal, bstack111l11_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬਢ")):
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), signal.Signals(bstack11lll1lll1_opy_).name)
  else:
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਤ"), bstack111l11_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫਥ"))
  if cli.is_running():
    bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.bstack11ll1l1l1_opy_)
  bstack1l1ll1l11l_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩਦ"))
  if bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩਧ") and not cli.is_enabled(CONFIG):
    bstack1l11l1l1ll_opy_.stop(bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪਨ")))
  bstack1l11l11l_opy_()
  sys.exit(1)
def bstack1ll11ll1_opy_(err):
  logger.critical(bstack1ll111111l_opy_.format(str(err)))
  bstack11ll1111l1_opy_(bstack1ll111111l_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11l11l_opy_)
  bstack1l11lllll_opy_()
  sys.exit(1)
def bstack1111111l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11ll1111l1_opy_(message, True)
  atexit.unregister(bstack1l11l11l_opy_)
  bstack1l11lllll_opy_()
  sys.exit(1)
def bstack1llll11l_opy_():
  global CONFIG
  global bstack111lllll1_opy_
  global bstack11l11111_opy_
  global bstack11ll1l1l11_opy_
  CONFIG = bstack1lll1ll1l_opy_()
  load_dotenv(CONFIG.get(bstack111l11_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬ਩")))
  bstack1l111l1111_opy_()
  bstack1ll1l11l1l_opy_()
  CONFIG = bstack1ll1lll1ll_opy_(CONFIG)
  update(CONFIG, bstack11l11111_opy_)
  update(CONFIG, bstack111lllll1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l11l1lll_opy_(CONFIG)
  bstack11ll1l1l11_opy_ = bstack1l11111l1_opy_(CONFIG)
  os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨਪ")] = bstack11ll1l1l11_opy_.__str__().lower()
  bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧਫ"), bstack11ll1l1l11_opy_)
  if (bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in CONFIG and bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in bstack111lllll1_opy_) or (
          bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") in CONFIG and bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਯ") not in bstack11l11111_opy_):
    if os.getenv(bstack111l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨਰ")):
      CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ਱")] = os.getenv(bstack111l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪਲ"))
    else:
      if not CONFIG.get(bstack111l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥਲ਼"), bstack111l11_opy_ (u"ࠣࠤ਴")) in bstack1l111ll11_opy_:
        bstack1111l1l1l_opy_()
  elif (bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਵ") not in CONFIG and bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਸ਼") in CONFIG) or (
          bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") in bstack11l11111_opy_ and bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਸ") not in bstack111lllll1_opy_):
    del (CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਹ")])
  if bstack11l1ll1lll_opy_(CONFIG):
    bstack1ll11ll1_opy_(bstack11l11l11l_opy_)
  Config.bstack11l11lll1l_opy_().bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤ਺"), CONFIG[bstack111l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ਻")])
  bstack1l11l1l11_opy_()
  bstack11111111_opy_()
  if bstack1ll11ll11_opy_ and not CONFIG.get(bstack111l11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯਼ࠧ"), bstack111l11_opy_ (u"ࠥࠦ਽")) in bstack1l111ll11_opy_:
    CONFIG[bstack111l11_opy_ (u"ࠫࡦࡶࡰࠨਾ")] = bstack11lll11ll1_opy_(CONFIG)
    logger.info(bstack1l1l1ll11_opy_.format(CONFIG[bstack111l11_opy_ (u"ࠬࡧࡰࡱࠩਿ")]))
  if not bstack11ll1l1l11_opy_:
    CONFIG[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੀ")] = [{}]
def bstack1ll111l1ll_opy_(config, bstack11lllll1l_opy_):
  global CONFIG
  global bstack1ll11ll11_opy_
  CONFIG = config
  bstack1ll11ll11_opy_ = bstack11lllll1l_opy_
def bstack11111111_opy_():
  global CONFIG
  global bstack1ll11ll11_opy_
  if bstack111l11_opy_ (u"ࠧࡢࡲࡳࠫੁ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1111111l1_opy_(e, bstack1l1l11l1l_opy_)
    bstack1ll11ll11_opy_ = True
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧੂ"), True)
def bstack11lll11ll1_opy_(config):
  bstack11ll1l1ll_opy_ = bstack111l11_opy_ (u"ࠩࠪ੃")
  app = config[bstack111l11_opy_ (u"ࠪࡥࡵࡶࠧ੄")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1l111l11_opy_:
      if os.path.exists(app):
        bstack11ll1l1ll_opy_ = bstack1ll1111l11_opy_(config, app)
      elif bstack1lll11ll1_opy_(app):
        bstack11ll1l1ll_opy_ = app
      else:
        bstack1ll11ll1_opy_(bstack1lll1111_opy_.format(app))
    else:
      if bstack1lll11ll1_opy_(app):
        bstack11ll1l1ll_opy_ = app
      elif os.path.exists(app):
        bstack11ll1l1ll_opy_ = bstack1ll1111l11_opy_(app)
      else:
        bstack1ll11ll1_opy_(bstack11lllll11l_opy_)
  else:
    if len(app) > 2:
      bstack1ll11ll1_opy_(bstack1l11l11l11_opy_)
    elif len(app) == 2:
      if bstack111l11_opy_ (u"ࠫࡵࡧࡴࡩࠩ੅") in app and bstack111l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੆") in app:
        if os.path.exists(app[bstack111l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")]):
          bstack11ll1l1ll_opy_ = bstack1ll1111l11_opy_(config, app[bstack111l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬੈ")], app[bstack111l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੉")])
        else:
          bstack1ll11ll1_opy_(bstack1lll1111_opy_.format(app))
      else:
        bstack1ll11ll1_opy_(bstack1l11l11l11_opy_)
    else:
      for key in app:
        if key in bstack1lll1l11ll_opy_:
          if key == bstack111l11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ੊"):
            if os.path.exists(app[key]):
              bstack11ll1l1ll_opy_ = bstack1ll1111l11_opy_(config, app[key])
            else:
              bstack1ll11ll1_opy_(bstack1lll1111_opy_.format(app))
          else:
            bstack11ll1l1ll_opy_ = app[key]
        else:
          bstack1ll11ll1_opy_(bstack11l111ll11_opy_)
  return bstack11ll1l1ll_opy_
def bstack1lll11ll1_opy_(bstack11ll1l1ll_opy_):
  import re
  bstack1ll11lllll_opy_ = re.compile(bstack111l11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥੋ"))
  bstack11ll1lll11_opy_ = re.compile(bstack111l11_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣੌ"))
  if bstack111l11_opy_ (u"ࠬࡨࡳ࠻࠱࠲੍ࠫ") in bstack11ll1l1ll_opy_ or re.fullmatch(bstack1ll11lllll_opy_, bstack11ll1l1ll_opy_) or re.fullmatch(bstack11ll1lll11_opy_, bstack11ll1l1ll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11l11l1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll1111l11_opy_(config, path, bstack11l1l11l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111l11_opy_ (u"࠭ࡲࡣࠩ੎")).read()).hexdigest()
  bstack11l1ll1ll1_opy_ = bstack1111l11l_opy_(md5_hash)
  bstack11ll1l1ll_opy_ = None
  if bstack11l1ll1ll1_opy_:
    logger.info(bstack111ll111l_opy_.format(bstack11l1ll1ll1_opy_, md5_hash))
    return bstack11l1ll1ll1_opy_
  bstack111l1l111_opy_ = datetime.datetime.now()
  bstack11l1llll11_opy_ = MultipartEncoder(
    fields={
      bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ੏"): (os.path.basename(path), open(os.path.abspath(path), bstack111l11_opy_ (u"ࠨࡴࡥࠫ੐")), bstack111l11_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ੑ")),
      bstack111l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭੒"): bstack11l1l11l11_opy_
    }
  )
  response = requests.post(bstack11lll1l1l_opy_, data=bstack11l1llll11_opy_,
                           headers={bstack111l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ੓"): bstack11l1llll11_opy_.content_type},
                           auth=(config[bstack111l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ੔")], config[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੕")]))
  try:
    res = json.loads(response.text)
    bstack11ll1l1ll_opy_ = res[bstack111l11_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ੖")]
    logger.info(bstack1l11lll11_opy_.format(bstack11ll1l1ll_opy_))
    bstack11111111l_opy_(md5_hash, bstack11ll1l1ll_opy_)
    cli.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱ࡮ࡲࡥࡩࡥࡡࡱࡲࠥ੗"), datetime.datetime.now() - bstack111l1l111_opy_)
  except ValueError as err:
    bstack1ll11ll1_opy_(bstack1l1ll1ll_opy_.format(str(err)))
  return bstack11ll1l1ll_opy_
def bstack1l11l1l11_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll1111l1l_opy_
  bstack1l1ll1l1_opy_ = 1
  bstack1l111llll1_opy_ = 1
  if bstack111l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘") in CONFIG:
    bstack1l111llll1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪਖ਼")]
  else:
    bstack1l111llll1_opy_ = bstack111111l1l_opy_(framework_name, args) or 1
  if bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼") in CONFIG:
    bstack1l1ll1l1_opy_ = len(CONFIG[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")])
  bstack1ll1111l1l_opy_ = int(bstack1l111llll1_opy_) * int(bstack1l1ll1l1_opy_)
def bstack111111l1l_opy_(framework_name, args):
  if framework_name == bstack1l1ll1l11_opy_ and args and bstack111l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ") in args:
      bstack11ll1l1l1l_opy_ = args.index(bstack111l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ੝"))
      return int(args[bstack11ll1l1l1l_opy_ + 1]) or 1
  return 1
def bstack1111l11l_opy_(md5_hash):
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠨࢀࠪਫ਼")), bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੟"), bstack111l11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੠"))
  if os.path.exists(bstack111ll1111_opy_):
    bstack1l1l1ll1_opy_ = json.load(open(bstack111ll1111_opy_, bstack111l11_opy_ (u"ࠫࡷࡨࠧ੡")))
    if md5_hash in bstack1l1l1ll1_opy_:
      bstack11lll11ll_opy_ = bstack1l1l1ll1_opy_[md5_hash]
      bstack1l1l111lll_opy_ = datetime.datetime.now()
      bstack1llllll1ll_opy_ = datetime.datetime.strptime(bstack11lll11ll_opy_[bstack111l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ੢")], bstack111l11_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ੣"))
      if (bstack1l1l111lll_opy_ - bstack1llllll1ll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11lll11ll_opy_[bstack111l11_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ੤")]):
        return None
      return bstack11lll11ll_opy_[bstack111l11_opy_ (u"ࠨ࡫ࡧࠫ੥")]
  else:
    return None
def bstack11111111l_opy_(md5_hash, bstack11ll1l1ll_opy_):
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠩࢁࠫ੦")), bstack111l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ੧"))
  if not os.path.exists(bstack1l1l111l1_opy_):
    os.makedirs(bstack1l1l111l1_opy_)
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠫࢃ࠭੨")), bstack111l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੩"), bstack111l11_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ੪"))
  bstack1l1llllll1_opy_ = {
    bstack111l11_opy_ (u"ࠧࡪࡦࠪ੫"): bstack11ll1l1ll_opy_,
    bstack111l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੬"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l11_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੭")),
    bstack111l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੮"): str(__version__)
  }
  if os.path.exists(bstack111ll1111_opy_):
    bstack1l1l1ll1_opy_ = json.load(open(bstack111ll1111_opy_, bstack111l11_opy_ (u"ࠫࡷࡨࠧ੯")))
  else:
    bstack1l1l1ll1_opy_ = {}
  bstack1l1l1ll1_opy_[md5_hash] = bstack1l1llllll1_opy_
  with open(bstack111ll1111_opy_, bstack111l11_opy_ (u"ࠧࡽࠫࠣੰ")) as outfile:
    json.dump(bstack1l1l1ll1_opy_, outfile)
def bstack1l111111l_opy_(self):
  return
def bstack1l1lll1ll1_opy_(self):
  return
def bstack11111lll1_opy_(self):
  global bstack1l11ll11l1_opy_
  bstack1l11ll11l1_opy_(self)
def bstack1l1l111l1l_opy_():
  global bstack1l1111l1l_opy_
  bstack1l1111l1l_opy_ = True
@measure(event_name=EVENTS.bstack1l1lll11l_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1lll11111l_opy_(self):
  global bstack11llllllll_opy_
  global bstack1lll11l1ll_opy_
  global bstack1ll1l111ll_opy_
  try:
    if bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ੱ") in bstack11llllllll_opy_ and self.session_id != None and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫੲ"), bstack111l11_opy_ (u"ࠨࠩੳ")) != bstack111l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪੴ"):
      bstack111llll1l_opy_ = bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪੵ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶")
      if bstack111llll1l_opy_ == bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੷"):
        bstack11111llll_opy_(logger)
      if self != None:
        bstack11ll11l11_opy_(self, bstack111llll1l_opy_, bstack111l11_opy_ (u"࠭ࠬࠡࠩ੸").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111l11_opy_ (u"ࠧࠨ੹")
    if bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ੺") in bstack11llllllll_opy_ and getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੻"), None):
      bstack11l1lll11_opy_.bstack1l11l1l111_opy_(self, bstack1l1llll111_opy_, logger, wait=True)
    if bstack111l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ੼") in bstack11llllllll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11ll11l11_opy_(self, bstack111l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ੽"))
      bstack1ll11111_opy_.bstack1l1l1l11ll_opy_(self)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ੾") + str(e))
  bstack1ll1l111ll_opy_(self)
  self.session_id = None
def bstack1ll1ll111_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1ll1llll_opy_
    global bstack11llllllll_opy_
    command_executor = kwargs.get(bstack111l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩ੿"), bstack111l11_opy_ (u"ࠧࠨ઀"))
    bstack1lll11ll11_opy_ = False
    if type(command_executor) == str and bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in command_executor:
      bstack1lll11ll11_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬં") in str(getattr(command_executor, bstack111l11_opy_ (u"ࠪࡣࡺࡸ࡬ࠨઃ"), bstack111l11_opy_ (u"ࠫࠬ઄"))):
      bstack1lll11ll11_opy_ = True
    else:
      kwargs = bstack11lll1ll1_opy_.bstack11ll1111ll_opy_(bstack111l1l11l_opy_=kwargs, config=CONFIG)
      return bstack11ll11lll1_opy_(self, *args, **kwargs)
    if bstack1lll11ll11_opy_:
      bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11ll1lllll_opy_(CONFIG, bstack11llllllll_opy_)
      if kwargs.get(bstack111l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")):
        kwargs[bstack111l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")] = bstack1l1ll1llll_opy_(kwargs[bstack111l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨઇ")], bstack11llllllll_opy_, CONFIG, bstack1l1ll111l_opy_)
      elif kwargs.get(bstack111l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")):
        kwargs[bstack111l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")] = bstack1l1ll1llll_opy_(kwargs[bstack111l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪઊ")], bstack11llllllll_opy_, CONFIG, bstack1l1ll111l_opy_)
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦઋ").format(str(e)))
  return bstack11ll11lll1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11llll111_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1l1lllll11_opy_(self, command_executor=bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨઌ"), *args, **kwargs):
  global bstack1lll11l1ll_opy_
  global bstack11111l1l_opy_
  bstack1l111l111l_opy_ = bstack1ll1ll111_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lllll1l1l_opy_.on():
    return bstack1l111l111l_opy_
  try:
    logger.debug(bstack111l11_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪઍ").format(str(command_executor)))
    logger.debug(bstack111l11_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩ઎").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫએ") in command_executor._url:
      bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪઐ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ઑ") in command_executor):
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ઒"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11llllll1_opy_ = getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ઓ"), None)
  bstack1ll1l1l11l_opy_ = {}
  if self.capabilities is not None:
    bstack1ll1l1l11l_opy_[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬઔ")] = self.capabilities.get(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬક"))
    bstack1ll1l1l11l_opy_[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪખ")] = self.capabilities.get(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪગ"))
    bstack1ll1l1l11l_opy_[bstack111l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫઘ")] = self.capabilities.get(bstack111l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩઙ"))
  if CONFIG.get(bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬચ"), False) and bstack11lll1ll1_opy_.bstack1lll1lllll_opy_(bstack1ll1l1l11l_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack111l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭છ") in bstack11llllllll_opy_ or bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭જ") in bstack11llllllll_opy_:
    bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(self)
  if bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨઝ") in bstack11llllllll_opy_ and bstack11llllll1_opy_ and bstack11llllll1_opy_.get(bstack111l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩઞ"), bstack111l11_opy_ (u"ࠪࠫટ")) == bstack111l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬઠ"):
    bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(self)
  bstack1lll11l1ll_opy_ = self.session_id
  bstack11111l1l_opy_.append(self)
  return bstack1l111l111l_opy_
def bstack1l1ll1l1ll_opy_(args):
  return bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ડ") in str(args)
def bstack1l1lll1lll_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1lll1_opy_
  global bstack1l1111111_opy_
  bstack11ll1llll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪઢ"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ણ"), None)
  bstack111111lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨત"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫથ"), None)
  bstack1l1l11lll1_opy_ = getattr(self, bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪદ"), None) != None and getattr(self, bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫધ"), None) == True
  if not bstack1l1111111_opy_ and bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬન") in CONFIG and CONFIG[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭઩")] == True and bstack11111ll1_opy_.bstack1ll11ll1l1_opy_(driver_command) and (bstack1l1l11lll1_opy_ or bstack11ll1llll_opy_) and not bstack1l1ll1l1ll_opy_(args):
    try:
      bstack1l1111111_opy_ = True
      logger.debug(bstack111l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩપ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ફ").format(str(err)))
    bstack1l1111111_opy_ = False
  response = bstack1ll1lll1_opy_(self, driver_command, *args, **kwargs)
  if (bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨબ") in str(bstack11llllllll_opy_).lower() or bstack111l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪભ") in str(bstack11llllllll_opy_).lower()) and bstack1lllll1l1l_opy_.on():
    try:
      if driver_command == bstack111l11_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨમ"):
        bstack1l11l1l1ll_opy_.bstack11lllll1l1_opy_({
            bstack111l11_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫય"): response[bstack111l11_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬર")],
            bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ઱"): bstack1l11l1l1ll_opy_.current_test_uuid() if bstack1l11l1l1ll_opy_.current_test_uuid() else bstack1lllll1l1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11lll111ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l1l1l11_opy_(self, command_executor,
             desired_capabilities=None, bstack11l1l1l11l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1lll11l1ll_opy_
  global bstack1ll1111l1_opy_
  global bstack11lll11lll_opy_
  global bstack11lll1l11_opy_
  global bstack11l1lll1_opy_
  global bstack11llllllll_opy_
  global bstack11ll11lll1_opy_
  global bstack11111l1l_opy_
  global bstack1l1l11l1ll_opy_
  global bstack1l1llll111_opy_
  CONFIG[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪલ")] = str(bstack11llllllll_opy_) + str(__version__)
  bstack1ll11l111l_opy_ = os.environ[bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧળ")]
  bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11ll1lllll_opy_(CONFIG, bstack11llllllll_opy_)
  CONFIG[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭઴")] = bstack1ll11l111l_opy_
  CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭વ")] = bstack1l1ll111l_opy_
  if CONFIG.get(bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬશ"),bstack111l11_opy_ (u"࠭ࠧષ")) and bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭સ") in bstack11llllllll_opy_:
    CONFIG[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨહ")].pop(bstack111l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ઺"), None)
    CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ઻")].pop(bstack111l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦ઼ࠩ"), None)
  command_executor = bstack1l1ll11l11_opy_()
  logger.debug(bstack111l11ll1_opy_.format(command_executor))
  proxy = bstack11l1l11l1_opy_(CONFIG, proxy)
  bstack1lll11lll1_opy_ = 0 if bstack1ll1111l1_opy_ < 0 else bstack1ll1111l1_opy_
  try:
    if bstack11lll1l11_opy_ is True:
      bstack1lll11lll1_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1lll1_opy_ is True:
      bstack1lll11lll1_opy_ = int(threading.current_thread().name)
  except:
    bstack1lll11lll1_opy_ = 0
  bstack11l1lll111_opy_ = bstack1l111111_opy_(CONFIG, bstack1lll11lll1_opy_)
  logger.debug(bstack11llllll11_opy_.format(str(bstack11l1lll111_opy_)))
  if bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩઽ") in CONFIG and bstack1l1llll1_opy_(CONFIG[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪા")]):
    bstack1l1ll1l111_opy_(bstack11l1lll111_opy_)
  if bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1lll11lll1_opy_) and bstack11lll1ll1_opy_.bstack1l1111lll1_opy_(bstack11l1lll111_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11lll1ll1_opy_.set_capabilities(bstack11l1lll111_opy_, CONFIG)
  if desired_capabilities:
    bstack11ll1ll11_opy_ = bstack1ll1lll1ll_opy_(desired_capabilities)
    bstack11ll1ll11_opy_[bstack111l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧિ")] = bstack1l1l1llll1_opy_(CONFIG)
    bstack111l1l1l1_opy_ = bstack1l111111_opy_(bstack11ll1ll11_opy_)
    if bstack111l1l1l1_opy_:
      bstack11l1lll111_opy_ = update(bstack111l1l1l1_opy_, bstack11l1lll111_opy_)
    desired_capabilities = None
  if options:
    bstack1lll1ll1l1_opy_(options, bstack11l1lll111_opy_)
  if not options:
    options = bstack11l1lll1ll_opy_(bstack11l1lll111_opy_)
  bstack1l1llll111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫી"))[bstack1lll11lll1_opy_]
  if proxy and bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩુ")):
    options.proxy(proxy)
  if options and bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩૂ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1lll1l_opy_() < version.parse(bstack111l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪૃ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1lll111_opy_)
  logger.info(bstack1lll1llll_opy_)
  bstack11l11111l_opy_.end(EVENTS.bstack11l111lll_opy_.value, EVENTS.bstack11l111lll_opy_.value + bstack111l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧૄ"), EVENTS.bstack11l111lll_opy_.value + bstack111l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦૅ"), status=True, failure=None, test_name=bstack11lll11lll_opy_)
  if bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡲࡵࡳ࡫࡯࡬ࡦࠩ૆") in kwargs:
    del kwargs[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡳࡶࡴ࡬ࡩ࡭ࡧࠪે")]
  if bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩૈ")):
    bstack11ll11lll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩૉ")):
    bstack11ll11lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack11l1l1l11l_opy_=bstack11l1l1l11l_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ૊")):
    bstack11ll11lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11l1l1l11l_opy_=bstack11l1l1l11l_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll11lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11l1l1l11l_opy_=bstack11l1l1l11l_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1lll11lll1_opy_) and bstack11lll1ll1_opy_.bstack1l1111lll1_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧો")][bstack111l11_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬૌ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11lll1ll1_opy_.set_capabilities(bstack11l1lll111_opy_, CONFIG)
  try:
    bstack1l1lll11l1_opy_ = bstack111l11_opy_ (u"ࠧࠨ્")
    if bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ૎")):
      if self.caps is not None:
        bstack1l1lll11l1_opy_ = self.caps.get(bstack111l11_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ૏"))
    else:
      if self.capabilities is not None:
        bstack1l1lll11l1_opy_ = self.capabilities.get(bstack111l11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥૐ"))
    if bstack1l1lll11l1_opy_:
      bstack1lll11l11l_opy_(bstack1l1lll11l1_opy_)
      if bstack11l1lll1l_opy_() <= version.parse(bstack111l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ૑")):
        self.command_executor._url = bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ૒") + bstack1ll11l1l_opy_ + bstack111l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ૓")
      else:
        self.command_executor._url = bstack111l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ૔") + bstack1l1lll11l1_opy_ + bstack111l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ૕")
      logger.debug(bstack1l1ll11l_opy_.format(bstack1l1lll11l1_opy_))
    else:
      logger.debug(bstack1l1l1lll11_opy_.format(bstack111l11_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ૖")))
  except Exception as e:
    logger.debug(bstack1l1l1lll11_opy_.format(e))
  if bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૗") in bstack11llllllll_opy_:
    bstack1l1l111l_opy_(bstack1ll1111l1_opy_, bstack1l1l11l1ll_opy_)
  bstack1lll11l1ll_opy_ = self.session_id
  if bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૘") in bstack11llllllll_opy_ or bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૙") in bstack11llllllll_opy_ or bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૚") in bstack11llllllll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11llllll1_opy_ = getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૛"), None)
  if bstack111l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ૜") in bstack11llllllll_opy_ or bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝") in bstack11llllllll_opy_:
    bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(self)
  if bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ૞") in bstack11llllllll_opy_ and bstack11llllll1_opy_ and bstack11llllll1_opy_.get(bstack111l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૟"), bstack111l11_opy_ (u"ࠬ࠭ૠ")) == bstack111l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૡ"):
    bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(self)
  bstack11111l1l_opy_.append(self)
  if bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪૢ") in CONFIG and bstack111l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ૣ") in CONFIG[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૤")][bstack1lll11lll1_opy_]:
    bstack11lll11lll_opy_ = CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥")][bstack1lll11lll1_opy_][bstack111l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૦")]
  logger.debug(bstack1l11111l1l_opy_.format(bstack1lll11l1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1ll111ll1_opy_
    def bstack11l1l1111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack111ll11ll_opy_
      if(bstack111l11_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ૧") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"࠭ࡾࠨ૨")), bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ૩"), bstack111l11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ૪")), bstack111l11_opy_ (u"ࠩࡺࠫ૫")) as fp:
          fp.write(bstack111l11_opy_ (u"ࠥࠦ૬"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111l11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૭")))):
          with open(args[1], bstack111l11_opy_ (u"ࠬࡸࠧ૮")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111l11_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬ૯") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1llll1l_opy_)
            if bstack111l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ૰") in CONFIG and str(CONFIG[bstack111l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ૱")]).lower() != bstack111l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ૲"):
                bstack11l11l1ll_opy_ = bstack1ll111ll1_opy_()
                bstack1ll11111l1_opy_ = bstack111l11_opy_ (u"ࠪࠫࠬࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡁࠊࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡁࠊࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡣࡰࡰࡶࡳࡱ࡫࠮ࡦࡴࡵࡳࡷ࠮ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠤ࠯ࠤࡪࡾࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࠨࡽࡦࡨࡵ࡛ࡲ࡭ࡿࠪࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭࠱ࠐࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࠧࠨࠩ૳").format(bstack11l11l1ll_opy_=bstack11l11l1ll_opy_)
            lines.insert(1, bstack1ll11111l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111l11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૴")), bstack111l11_opy_ (u"ࠬࡽࠧ૵")) as bstack1lll1l11_opy_:
              bstack1lll1l11_opy_.writelines(lines)
        CONFIG[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ૶")] = str(bstack11llllllll_opy_) + str(__version__)
        bstack1ll11l111l_opy_ = os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ૷")]
        bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11ll1lllll_opy_(CONFIG, bstack11llllllll_opy_)
        CONFIG[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ૸")] = bstack1ll11l111l_opy_
        CONFIG[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫૹ")] = bstack1l1ll111l_opy_
        bstack1lll11lll1_opy_ = 0 if bstack1ll1111l1_opy_ < 0 else bstack1ll1111l1_opy_
        try:
          if bstack11lll1l11_opy_ is True:
            bstack1lll11lll1_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l1lll1_opy_ is True:
            bstack1lll11lll1_opy_ = int(threading.current_thread().name)
        except:
          bstack1lll11lll1_opy_ = 0
        CONFIG[bstack111l11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥૺ")] = False
        CONFIG[bstack111l11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥૻ")] = True
        bstack11l1lll111_opy_ = bstack1l111111_opy_(CONFIG, bstack1lll11lll1_opy_)
        logger.debug(bstack11llllll11_opy_.format(str(bstack11l1lll111_opy_)))
        if CONFIG.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩૼ")):
          bstack1l1ll1l111_opy_(bstack11l1lll111_opy_)
        if bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૽") in CONFIG and bstack111l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૾") in CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૿")][bstack1lll11lll1_opy_]:
          bstack11lll11lll_opy_ = CONFIG[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଀")][bstack1lll11lll1_opy_][bstack111l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଁ")]
        args.append(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠫࢃ࠭ଂ")), bstack111l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"), bstack111l11_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ଄")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1lll111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111l11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤଅ"))
      bstack111ll11ll_opy_ = True
      return bstack11llll1ll1_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1l11l1ll11_opy_(self,
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
    global bstack1ll1111l1_opy_
    global bstack11lll11lll_opy_
    global bstack11lll1l11_opy_
    global bstack11l1lll1_opy_
    global bstack11llllllll_opy_
    CONFIG[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪଆ")] = str(bstack11llllllll_opy_) + str(__version__)
    bstack1ll11l111l_opy_ = os.environ[bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧଇ")]
    bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11ll1lllll_opy_(CONFIG, bstack11llllllll_opy_)
    CONFIG[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ଈ")] = bstack1ll11l111l_opy_
    CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ଉ")] = bstack1l1ll111l_opy_
    bstack1lll11lll1_opy_ = 0 if bstack1ll1111l1_opy_ < 0 else bstack1ll1111l1_opy_
    try:
      if bstack11lll1l11_opy_ is True:
        bstack1lll11lll1_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l1lll1_opy_ is True:
        bstack1lll11lll1_opy_ = int(threading.current_thread().name)
    except:
      bstack1lll11lll1_opy_ = 0
    CONFIG[bstack111l11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦଊ")] = True
    bstack11l1lll111_opy_ = bstack1l111111_opy_(CONFIG, bstack1lll11lll1_opy_)
    logger.debug(bstack11llllll11_opy_.format(str(bstack11l1lll111_opy_)))
    if CONFIG.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪଋ")):
      bstack1l1ll1l111_opy_(bstack11l1lll111_opy_)
    if bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ") in CONFIG and bstack111l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଍") in CONFIG[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଎")][bstack1lll11lll1_opy_]:
      bstack11lll11lll_opy_ = CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଏ")][bstack1lll11lll1_opy_][bstack111l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଐ")]
    import urllib
    import json
    if bstack111l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ଑") in CONFIG and str(CONFIG[bstack111l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ଒")]).lower() != bstack111l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ଓ"):
        bstack1l11lll1_opy_ = bstack1ll111ll1_opy_()
        bstack11l11l1ll_opy_ = bstack1l11lll1_opy_ + urllib.parse.quote(json.dumps(bstack11l1lll111_opy_))
    else:
        bstack11l11l1ll_opy_ = bstack111l11_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪଔ") + urllib.parse.quote(json.dumps(bstack11l1lll111_opy_))
    browser = self.connect(bstack11l11l1ll_opy_)
    return browser
except Exception as e:
    pass
def bstack11l1lll11l_opy_():
    global bstack111ll11ll_opy_
    global bstack11llllllll_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11ll11llll_opy_
        global bstack111l111ll_opy_
        if not bstack11ll1l1l11_opy_:
          global bstack11ll11l1_opy_
          if not bstack11ll11l1_opy_:
            from bstack_utils.helper import bstack1l11l1lll1_opy_, bstack1l1llllll_opy_, bstack1ll1lll1l_opy_
            bstack11ll11l1_opy_ = bstack1l11l1lll1_opy_()
            bstack1l1llllll_opy_(bstack11llllllll_opy_)
            bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11ll1lllll_opy_(CONFIG, bstack11llllllll_opy_)
            bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦକ"), bstack1l1ll111l_opy_)
          BrowserType.connect = bstack11ll11llll_opy_
          return
        BrowserType.launch = bstack1l11l1ll11_opy_
        bstack111ll11ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1l1111_opy_
      bstack111ll11ll_opy_ = True
    except Exception as e:
      pass
def bstack111l1l11_opy_(context, bstack11111l11l_opy_):
  try:
    context.page.evaluate(bstack111l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦଖ"), bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨଗ")+ json.dumps(bstack11111l11l_opy_) + bstack111l11_opy_ (u"ࠧࢃࡽࠣଘ"))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣଙ").format(str(e), traceback.format_exc()))
def bstack1lllll1l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଚ"), bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଛ") + json.dumps(message) + bstack111l11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬଜ") + json.dumps(level) + bstack111l11_opy_ (u"ࠪࢁࢂ࠭ଝ"))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦଞ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1l1ll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll11l1l1_opy_(self, url):
  global bstack1lll11l1l_opy_
  try:
    bstack11111ll1l_opy_(url)
  except Exception as err:
    logger.debug(bstack111lll1l1_opy_.format(str(err)))
  try:
    bstack1lll11l1l_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1111ll1l_opy_ = str(e)
      if any(err_msg in bstack1l1111ll1l_opy_ for err_msg in bstack1ll11ll11l_opy_):
        bstack11111ll1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111lll1l1_opy_.format(str(err)))
    raise e
def bstack1l1llll11_opy_(self):
  global bstack1l1ll11ll1_opy_
  bstack1l1ll11ll1_opy_ = self
  return
def bstack1lll111l_opy_(self):
  global bstack1l11l1l1_opy_
  bstack1l11l1l1_opy_ = self
  return
def bstack11lllll111_opy_(test_name, bstack11l111ll_opy_):
  global CONFIG
  if percy.bstack1111l1lll_opy_() == bstack111l11_opy_ (u"ࠧࡺࡲࡶࡧࠥଟ"):
    bstack1l1l1l1l1l_opy_ = os.path.relpath(bstack11l111ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1l1l1l1l_opy_)
    bstack1llll1111l_opy_ = suite_name + bstack111l11_opy_ (u"ࠨ࠭ࠣଠ") + test_name
    threading.current_thread().percySessionName = bstack1llll1111l_opy_
def bstack1ll11llll1_opy_(self, test, *args, **kwargs):
  global bstack1l11l1111_opy_
  test_name = None
  bstack11l111ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11l111ll_opy_ = str(test.source)
  bstack11lllll111_opy_(test_name, bstack11l111ll_opy_)
  bstack1l11l1111_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1llll1ll1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l11l1l11_opy_(driver, bstack1llll1111l_opy_):
  if not bstack1ll1lllll_opy_ and bstack1llll1111l_opy_:
      bstack1l1ll111ll_opy_ = {
          bstack111l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଡ"): bstack111l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଢ"),
          bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଣ"): {
              bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨତ"): bstack1llll1111l_opy_
          }
      }
      bstack111lll11_opy_ = bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩଥ").format(json.dumps(bstack1l1ll111ll_opy_))
      driver.execute_script(bstack111lll11_opy_)
  if bstack11ll1l1111_opy_:
      bstack11ll11111l_opy_ = {
          bstack111l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଦ"): bstack111l11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨଧ"),
          bstack111l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪନ"): {
              bstack111l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭଩"): bstack1llll1111l_opy_ + bstack111l11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫପ"),
              bstack111l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଫ"): bstack111l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩବ")
          }
      }
      if bstack11ll1l1111_opy_.status == bstack111l11_opy_ (u"ࠬࡖࡁࡔࡕࠪଭ"):
          bstack1l11l1llll_opy_ = bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫମ").format(json.dumps(bstack11ll11111l_opy_))
          driver.execute_script(bstack1l11l1llll_opy_)
          bstack11ll11l11_opy_(driver, bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଯ"))
      elif bstack11ll1l1111_opy_.status == bstack111l11_opy_ (u"ࠨࡈࡄࡍࡑ࠭ର"):
          reason = bstack111l11_opy_ (u"ࠤࠥ଱")
          bstack11l111l1_opy_ = bstack1llll1111l_opy_ + bstack111l11_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫଲ")
          if bstack11ll1l1111_opy_.message:
              reason = str(bstack11ll1l1111_opy_.message)
              bstack11l111l1_opy_ = bstack11l111l1_opy_ + bstack111l11_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫଳ") + reason
          bstack11ll11111l_opy_[bstack111l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ଴")] = {
              bstack111l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬଵ"): bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ଶ"),
              bstack111l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ଷ"): bstack11l111l1_opy_
          }
          bstack1l11l1llll_opy_ = bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧସ").format(json.dumps(bstack11ll11111l_opy_))
          driver.execute_script(bstack1l11l1llll_opy_)
          bstack11ll11l11_opy_(driver, bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪହ"), reason)
          bstack1ll111ll11_opy_(reason, str(bstack11ll1l1111_opy_), str(bstack1ll1111l1_opy_), logger)
@measure(event_name=EVENTS.bstack1lll111111_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l1111l1_opy_(driver, test):
  if percy.bstack1111l1lll_opy_() == bstack111l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ଺") and percy.bstack111ll1lll_opy_() == bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ଻"):
      bstack11l1l1lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦ଼ࠩ"), None)
      bstack1l11l111_opy_(driver, bstack11l1l1lll_opy_, test)
  if (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫଽ"), None) and
      bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧା"), None)) or (
      bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩି"), None) and
      bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬୀ"), None)):
      logger.info(bstack111l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦୁ"))
      bstack11lll1ll1_opy_.bstack1l1ll1ll1_opy_(driver, name=test.name, path=test.source)
def bstack1l1111111l_opy_(test, bstack1llll1111l_opy_):
    try:
      bstack111l1l111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪୂ")] = bstack1llll1111l_opy_
      if bstack11ll1l1111_opy_:
        if bstack11ll1l1111_opy_.status == bstack111l11_opy_ (u"࠭ࡐࡂࡕࡖࠫୃ"):
          data[bstack111l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧୄ")] = bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ୅")
        elif bstack11ll1l1111_opy_.status == bstack111l11_opy_ (u"ࠩࡉࡅࡎࡒࠧ୆"):
          data[bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪେ")] = bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୈ")
          if bstack11ll1l1111_opy_.message:
            data[bstack111l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ୉")] = str(bstack11ll1l1111_opy_.message)
      user = CONFIG[bstack111l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ୊")]
      key = CONFIG[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪୋ")]
      url = bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭ୌ").format(user, key, bstack1lll11l1ll_opy_)
      headers = {
        bstack111l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ୍"): bstack111l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭୎"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡩࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠣ୏"), datetime.datetime.now() - bstack111l1l111_opy_)
    except Exception as e:
      logger.error(bstack11l1l11lll_opy_.format(str(e)))
def bstack11l11l1111_opy_(test, bstack1llll1111l_opy_):
  global CONFIG
  global bstack1l11l1l1_opy_
  global bstack1l1ll11ll1_opy_
  global bstack1lll11l1ll_opy_
  global bstack11ll1l1111_opy_
  global bstack11lll11lll_opy_
  global bstack1l1111ll_opy_
  global bstack1llllllll1_opy_
  global bstack1llll1l11l_opy_
  global bstack1l1l1lll_opy_
  global bstack11111l1l_opy_
  global bstack1l1llll111_opy_
  try:
    if not bstack1lll11l1ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠬࢄࠧ୐")), bstack111l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭୑"), bstack111l11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ୒"))) as f:
        bstack1llll1llll_opy_ = json.loads(bstack111l11_opy_ (u"ࠣࡽࠥ୓") + f.read().strip() + bstack111l11_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ୔") + bstack111l11_opy_ (u"ࠥࢁࠧ୕"))
        bstack1lll11l1ll_opy_ = bstack1llll1llll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11111l1l_opy_:
    for driver in bstack11111l1l_opy_:
      if bstack1lll11l1ll_opy_ == driver.session_id:
        if test:
          bstack11l1111l1_opy_(driver, test)
        bstack11l11l1l11_opy_(driver, bstack1llll1111l_opy_)
  elif bstack1lll11l1ll_opy_:
    bstack1l1111111l_opy_(test, bstack1llll1111l_opy_)
  if bstack1l11l1l1_opy_:
    bstack1llllllll1_opy_(bstack1l11l1l1_opy_)
  if bstack1l1ll11ll1_opy_:
    bstack1llll1l11l_opy_(bstack1l1ll11ll1_opy_)
  if bstack1l1111l1l_opy_:
    bstack1l1l1lll_opy_()
def bstack1lllll111l_opy_(self, test, *args, **kwargs):
  bstack1llll1111l_opy_ = None
  if test:
    bstack1llll1111l_opy_ = str(test.name)
  bstack11l11l1111_opy_(test, bstack1llll1111l_opy_)
  bstack1l1111ll_opy_(self, test, *args, **kwargs)
def bstack111l1lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111ll11l_opy_
  global CONFIG
  global bstack11111l1l_opy_
  global bstack1lll11l1ll_opy_
  bstack1lll11lll_opy_ = None
  try:
    if bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୖ"), None) or bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୗ"), None):
      try:
        if not bstack1lll11l1ll_opy_:
          with open(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"࠭ࡾࠨ୘")), bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୙"), bstack111l11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ୚"))) as f:
            bstack1llll1llll_opy_ = json.loads(bstack111l11_opy_ (u"ࠤࡾࠦ୛") + f.read().strip() + bstack111l11_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬଡ଼") + bstack111l11_opy_ (u"ࠦࢂࠨଢ଼"))
            bstack1lll11l1ll_opy_ = bstack1llll1llll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11111l1l_opy_:
        for driver in bstack11111l1l_opy_:
          if bstack1lll11l1ll_opy_ == driver.session_id:
            bstack1lll11lll_opy_ = driver
    bstack1llll1111_opy_ = bstack11lll1ll1_opy_.bstack1lllll1111_opy_(test.tags)
    if bstack1lll11lll_opy_:
      threading.current_thread().isA11yTest = bstack11lll1ll1_opy_.bstack1111ll1l_opy_(bstack1lll11lll_opy_, bstack1llll1111_opy_)
      threading.current_thread().isAppA11yTest = bstack11lll1ll1_opy_.bstack1111ll1l_opy_(bstack1lll11lll_opy_, bstack1llll1111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1llll1111_opy_
      threading.current_thread().isAppA11yTest = bstack1llll1111_opy_
  except:
    pass
  bstack1111ll11l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11ll1l1111_opy_
  try:
    bstack11ll1l1111_opy_ = self._test
  except:
    bstack11ll1l1111_opy_ = self.test
def bstack11ll11lll_opy_():
  global bstack11l1ll111l_opy_
  try:
    if os.path.exists(bstack11l1ll111l_opy_):
      os.remove(bstack11l1ll111l_opy_)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୞") + str(e))
def bstack11l11llll1_opy_():
  global bstack11l1ll111l_opy_
  bstack1lll1ll1_opy_ = {}
  try:
    if not os.path.isfile(bstack11l1ll111l_opy_):
      with open(bstack11l1ll111l_opy_, bstack111l11_opy_ (u"࠭ࡷࠨୟ")):
        pass
      with open(bstack11l1ll111l_opy_, bstack111l11_opy_ (u"ࠢࡸ࠭ࠥୠ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11l1ll111l_opy_):
      bstack1lll1ll1_opy_ = json.load(open(bstack11l1ll111l_opy_, bstack111l11_opy_ (u"ࠨࡴࡥࠫୡ")))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫୢ") + str(e))
  finally:
    return bstack1lll1ll1_opy_
def bstack1l1l111l_opy_(platform_index, item_index):
  global bstack11l1ll111l_opy_
  try:
    bstack1lll1ll1_opy_ = bstack11l11llll1_opy_()
    bstack1lll1ll1_opy_[item_index] = platform_index
    with open(bstack11l1ll111l_opy_, bstack111l11_opy_ (u"ࠥࡻ࠰ࠨୣ")) as outfile:
      json.dump(bstack1lll1ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ୤") + str(e))
def bstack1l1l11l111_opy_(bstack1llll111_opy_):
  global CONFIG
  bstack1l1l1l11_opy_ = bstack111l11_opy_ (u"ࠬ࠭୥")
  if not bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୦") in CONFIG:
    logger.info(bstack111l11_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ୧"))
  try:
    platform = CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୨")][bstack1llll111_opy_]
    if bstack111l11_opy_ (u"ࠩࡲࡷࠬ୩") in platform:
      bstack1l1l1l11_opy_ += str(platform[bstack111l11_opy_ (u"ࠪࡳࡸ࠭୪")]) + bstack111l11_opy_ (u"ࠫ࠱ࠦࠧ୫")
    if bstack111l11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୬") in platform:
      bstack1l1l1l11_opy_ += str(platform[bstack111l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ୭")]) + bstack111l11_opy_ (u"ࠧ࠭ࠢࠪ୮")
    if bstack111l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ୯") in platform:
      bstack1l1l1l11_opy_ += str(platform[bstack111l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭୰")]) + bstack111l11_opy_ (u"ࠪ࠰ࠥ࠭ୱ")
    if bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୲") in platform:
      bstack1l1l1l11_opy_ += str(platform[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ୳")]) + bstack111l11_opy_ (u"࠭ࠬࠡࠩ୴")
    if bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୵") in platform:
      bstack1l1l1l11_opy_ += str(platform[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୶")]) + bstack111l11_opy_ (u"ࠩ࠯ࠤࠬ୷")
    if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ୸") in platform:
      bstack1l1l1l11_opy_ += str(platform[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ୹")]) + bstack111l11_opy_ (u"ࠬ࠲ࠠࠨ୺")
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭୻") + str(e))
  finally:
    if bstack1l1l1l11_opy_[len(bstack1l1l1l11_opy_) - 2:] == bstack111l11_opy_ (u"ࠧ࠭ࠢࠪ୼"):
      bstack1l1l1l11_opy_ = bstack1l1l1l11_opy_[:-2]
    return bstack1l1l1l11_opy_
def bstack1ll111llll_opy_(path, bstack1l1l1l11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1llllll11_opy_ = ET.parse(path)
    bstack1l11111lll_opy_ = bstack1llllll11_opy_.getroot()
    bstack11lll111l_opy_ = None
    for suite in bstack1l11111lll_opy_.iter(bstack111l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ୽")):
      if bstack111l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ୾") in suite.attrib:
        suite.attrib[bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ୿")] += bstack111l11_opy_ (u"ࠫࠥ࠭஀") + bstack1l1l1l11_opy_
        bstack11lll111l_opy_ = suite
    bstack1lll11llll_opy_ = None
    for robot in bstack1l11111lll_opy_.iter(bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஁")):
      bstack1lll11llll_opy_ = robot
    bstack11l1l1ll_opy_ = len(bstack1lll11llll_opy_.findall(bstack111l11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஂ")))
    if bstack11l1l1ll_opy_ == 1:
      bstack1lll11llll_opy_.remove(bstack1lll11llll_opy_.findall(bstack111l11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ஃ"))[0])
      bstack11ll1l1lll_opy_ = ET.Element(bstack111l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ஄"), attrib={bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧஅ"): bstack111l11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪஆ"), bstack111l11_opy_ (u"ࠫ࡮ࡪࠧஇ"): bstack111l11_opy_ (u"ࠬࡹ࠰ࠨஈ")})
      bstack1lll11llll_opy_.insert(1, bstack11ll1l1lll_opy_)
      bstack1l11l1l11l_opy_ = None
      for suite in bstack1lll11llll_opy_.iter(bstack111l11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬஉ")):
        bstack1l11l1l11l_opy_ = suite
      bstack1l11l1l11l_opy_.append(bstack11lll111l_opy_)
      bstack1l1ll1lll1_opy_ = None
      for status in bstack11lll111l_opy_.iter(bstack111l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧஊ")):
        bstack1l1ll1lll1_opy_ = status
      bstack1l11l1l11l_opy_.append(bstack1l1ll1lll1_opy_)
    bstack1llllll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭஋") + str(e))
def bstack1llll11ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l111l1ll_opy_
  global CONFIG
  if bstack111l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ஌") in options:
    del options[bstack111l11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ஍")]
  bstack111l11111_opy_ = bstack11l11llll1_opy_()
  for bstack1lll1l1ll_opy_ in bstack111l11111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫஎ"), str(bstack1lll1l1ll_opy_), bstack111l11_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩஏ"))
    bstack1ll111llll_opy_(path, bstack1l1l11l111_opy_(bstack111l11111_opy_[bstack1lll1l1ll_opy_]))
  bstack11ll11lll_opy_()
  return bstack1l111l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l1ll11l_opy_(self, ff_profile_dir):
  global bstack1l1l11ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1l11ll_opy_(self, ff_profile_dir)
def bstack1lllllll1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11l11111_opy_
  bstack11l1l1l1l_opy_ = []
  if bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஐ") in CONFIG:
    bstack11l1l1l1l_opy_ = CONFIG[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஑")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤஒ")],
      pabot_args[bstack111l11_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥஓ")],
      argfile,
      pabot_args.get(bstack111l11_opy_ (u"ࠥ࡬࡮ࡼࡥࠣஔ")),
      pabot_args[bstack111l11_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢக")],
      platform[0],
      bstack1l11l11111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111l11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ஖")] or [(bstack111l11_opy_ (u"ࠨࠢ஗"), None)]
    for platform in enumerate(bstack11l1l1l1l_opy_)
  ]
def bstack11l1l11ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1llllll_opy_=bstack111l11_opy_ (u"ࠧࠨ஘")):
  global bstack111111ll_opy_
  self.platform_index = platform_index
  self.bstack1111llll_opy_ = bstack1ll1llllll_opy_
  bstack111111ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11lll1111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1111llll_opy_
  global bstack11ll1ll1l_opy_
  bstack11l1l111ll_opy_ = copy.deepcopy(item)
  if not bstack111l11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪங") in item.options:
    bstack11l1l111ll_opy_.options[bstack111l11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫச")] = []
  bstack1l1ll1ll1l_opy_ = bstack11l1l111ll_opy_.options[bstack111l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஛")].copy()
  for v in bstack11l1l111ll_opy_.options[bstack111l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ஜ")]:
    if bstack111l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ஝") in v:
      bstack1l1ll1ll1l_opy_.remove(v)
    if bstack111l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ஞ") in v:
      bstack1l1ll1ll1l_opy_.remove(v)
    if bstack111l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫட") in v:
      bstack1l1ll1ll1l_opy_.remove(v)
  bstack1l1ll1ll1l_opy_.insert(0, bstack111l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ஠").format(bstack11l1l111ll_opy_.platform_index))
  bstack1l1ll1ll1l_opy_.insert(0, bstack111l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩ஡").format(bstack11l1l111ll_opy_.bstack1111llll_opy_))
  bstack11l1l111ll_opy_.options[bstack111l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஢")] = bstack1l1ll1ll1l_opy_
  if bstack11ll1ll1l_opy_:
    bstack11l1l111ll_opy_.options[bstack111l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ண")].insert(0, bstack111l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨத").format(bstack11ll1ll1l_opy_))
  return bstack1l1111llll_opy_(caller_id, datasources, is_last, bstack11l1l111ll_opy_, outs_dir)
def bstack1l11llll_opy_(command, item_index):
  if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ஥")):
    os.environ[bstack111l11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ஦")] = json.dumps(CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஧")][item_index % bstack1l111l11_opy_])
  global bstack11ll1ll1l_opy_
  if bstack11ll1ll1l_opy_:
    command[0] = command[0].replace(bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨந"), bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧன") + str(
      item_index) + bstack111l11_opy_ (u"ࠫࠥ࠭ப") + bstack11ll1ll1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஫"),
                                    bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ஬") + str(item_index), 1)
def bstack1l1111l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1lll1111_opy_
  bstack1l11llll_opy_(command, item_index)
  return bstack1l1lll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1lll1111_opy_
  bstack1l11llll_opy_(command, item_index)
  return bstack1l1lll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11l11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1lll1111_opy_
  bstack1l11llll_opy_(command, item_index)
  return bstack1l1lll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lll111ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l1lll1111_opy_
  bstack1l11llll_opy_(command, item_index)
  return bstack1l1lll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll111ll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111ll11l_opy_
  bstack1ll1lll11_opy_ = bstack1l111ll11l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111l11_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ஭")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111l11_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬம")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1lll11_opy_
def bstack11llll111l_opy_(runner, hook_name, context, element, bstack11l11ll1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11ll111l11_opy_.bstack1l1lll1l_opy_(hook_name, element)
    bstack11l11ll1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11ll111l11_opy_.bstack11l1lll1l1_opy_(element)
      if hook_name not in [bstack111l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ய"), bstack111l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ர")] and args and hasattr(args[0], bstack111l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫற")):
        args[0].error_message = bstack111l11_opy_ (u"ࠬ࠭ல")
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨள").format(str(e)))
@measure(event_name=EVENTS.bstack1llll1l11_opy_, stage=STAGE.bstack1l1l11ll1_opy_, hook_type=bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥழ"), bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l11lll11_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    if runner.hooks.get(bstack111l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧவ")).__name__ != bstack111l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧஶ"):
      bstack11llll111l_opy_(runner, name, context, runner, bstack11l11ll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111l111l1_opy_(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩஷ")) else context.browser
      runner.driver_initialised = bstack111l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣஸ")
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩஹ").format(str(e)))
def bstack1ll1l111l_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    bstack11llll111l_opy_(runner, name, context, context.feature, bstack11l11ll1_opy_, *args)
    try:
      if not bstack1ll1lllll_opy_:
        bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l111l1_opy_(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ஺")) else context.browser
        if is_driver_active(bstack1lll11lll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ஻")
          bstack11111l11l_opy_ = str(runner.feature.name)
          bstack111l1l11_opy_(context, bstack11111l11l_opy_)
          bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭஼") + json.dumps(bstack11111l11l_opy_) + bstack111l11_opy_ (u"ࠩࢀࢁࠬ஽"))
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪா").format(str(e)))
def bstack11lll111l1_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    if hasattr(context, bstack111l11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ி")):
        bstack11ll111l11_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack111l11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧீ")) else context.feature
    bstack11llll111l_opy_(runner, name, context, target, bstack11l11ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l11lllll1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll1lll11l_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack11ll111l11_opy_.start_test(context)
    bstack11llll111l_opy_(runner, name, context, context.scenario, bstack11l11ll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll11111_opy_.bstack1l11ll1ll_opy_(context, *args)
    try:
      bstack1lll11lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬு"), context.browser)
      if is_driver_active(bstack1lll11lll_opy_):
        bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ூ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௃")
        if (not bstack1ll1lllll_opy_):
          scenario_name = args[0].name
          feature_name = bstack11111l11l_opy_ = str(runner.feature.name)
          bstack11111l11l_opy_ = feature_name + bstack111l11_opy_ (u"ࠩࠣ࠱ࠥ࠭௄") + scenario_name
          if runner.driver_initialised == bstack111l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௅"):
            bstack111l1l11_opy_(context, bstack11111l11l_opy_)
            bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩெ") + json.dumps(bstack11111l11l_opy_) + bstack111l11_opy_ (u"ࠬࢃࡽࠨே"))
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧை").format(str(e)))
@measure(event_name=EVENTS.bstack1llll1l11_opy_, stage=STAGE.bstack1l1l11ll1_opy_, hook_type=bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦ௉"), bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll1111111_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    bstack11llll111l_opy_(runner, name, context, args[0], bstack11l11ll1_opy_, *args)
    try:
      bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l111l1_opy_(bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧொ")) else context.browser
      if is_driver_active(bstack1lll11lll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢோ")
        bstack11ll111l11_opy_.bstack1l1lll1l1l_opy_(args[0])
        if runner.driver_initialised == bstack111l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣௌ"):
          feature_name = bstack11111l11l_opy_ = str(runner.feature.name)
          bstack11111l11l_opy_ = feature_name + bstack111l11_opy_ (u"ࠫࠥ࠳ࠠࠨ்") + context.scenario.name
          bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௎") + json.dumps(bstack11111l11l_opy_) + bstack111l11_opy_ (u"࠭ࡽࡾࠩ௏"))
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫௐ").format(str(e)))
@measure(event_name=EVENTS.bstack1llll1l11_opy_, stage=STAGE.bstack1l1l11ll1_opy_, hook_type=bstack111l11_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦ௑"), bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11lll1l11l_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
  bstack11ll111l11_opy_.bstack11l11l111l_opy_(args[0])
  try:
    bstack1l111l1ll1_opy_ = args[0].status.name
    bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ௒") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1lll11lll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111l11_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ௓")
        feature_name = bstack11111l11l_opy_ = str(runner.feature.name)
        bstack11111l11l_opy_ = feature_name + bstack111l11_opy_ (u"ࠫࠥ࠳ࠠࠨ௔") + context.scenario.name
        bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௕") + json.dumps(bstack11111l11l_opy_) + bstack111l11_opy_ (u"࠭ࡽࡾࠩ௖"))
    if str(bstack1l111l1ll1_opy_).lower() == bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧௗ"):
      bstack1l111111ll_opy_ = bstack111l11_opy_ (u"ࠨࠩ௘")
      bstack1lll111ll_opy_ = bstack111l11_opy_ (u"ࠩࠪ௙")
      bstack1l1111lll_opy_ = bstack111l11_opy_ (u"ࠪࠫ௚")
      try:
        import traceback
        bstack1l111111ll_opy_ = runner.exception.__class__.__name__
        bstack1l1ll11ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll111ll_opy_ = bstack111l11_opy_ (u"ࠫࠥ࠭௛").join(bstack1l1ll11ll_opy_)
        bstack1l1111lll_opy_ = bstack1l1ll11ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1lll1l11_opy_.format(str(e)))
      bstack1l111111ll_opy_ += bstack1l1111lll_opy_
      bstack1lllll1l1_opy_(context, json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௜") + str(bstack1lll111ll_opy_)),
                          bstack111l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௝"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௞"):
        bstack11ll11ll_opy_(getattr(context, bstack111l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭௟"), None), bstack111l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௠"), bstack1l111111ll_opy_)
        bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௡") + json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ௢") + str(bstack1lll111ll_opy_)) + bstack111l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ௣"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ௤"):
        bstack11ll11l11_opy_(bstack1lll11lll_opy_, bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௥"), bstack111l11_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ௦") + str(bstack1l111111ll_opy_))
    else:
      bstack1lllll1l1_opy_(context, bstack111l11_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ௧"), bstack111l11_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ௨"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௩"):
        bstack11ll11ll_opy_(getattr(context, bstack111l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ௪"), None), bstack111l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௫"))
      bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௬") + json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ௭")) + bstack111l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ௮"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௯"):
        bstack11ll11l11_opy_(bstack1lll11lll_opy_, bstack111l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ௰"))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ௱").format(str(e)))
  bstack11llll111l_opy_(runner, name, context, args[0], bstack11l11ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l111ll1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1lll1111ll_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
  bstack11ll111l11_opy_.end_test(args[0])
  try:
    bstack111111l11_opy_ = args[0].status.name
    bstack1lll11lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ௲"), context.browser)
    bstack1ll11111_opy_.bstack1l1l1l11ll_opy_(bstack1lll11lll_opy_)
    if str(bstack111111l11_opy_).lower() == bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௳"):
      bstack1l111111ll_opy_ = bstack111l11_opy_ (u"ࠨࠩ௴")
      bstack1lll111ll_opy_ = bstack111l11_opy_ (u"ࠩࠪ௵")
      bstack1l1111lll_opy_ = bstack111l11_opy_ (u"ࠪࠫ௶")
      try:
        import traceback
        bstack1l111111ll_opy_ = runner.exception.__class__.__name__
        bstack1l1ll11ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll111ll_opy_ = bstack111l11_opy_ (u"ࠫࠥ࠭௷").join(bstack1l1ll11ll_opy_)
        bstack1l1111lll_opy_ = bstack1l1ll11ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1lll1l11_opy_.format(str(e)))
      bstack1l111111ll_opy_ += bstack1l1111lll_opy_
      bstack1lllll1l1_opy_(context, json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௸") + str(bstack1lll111ll_opy_)),
                          bstack111l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௹"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௺") or runner.driver_initialised == bstack111l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ௻"):
        bstack11ll11ll_opy_(getattr(context, bstack111l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௼"), None), bstack111l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ௽"), bstack1l111111ll_opy_)
        bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௾") + json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ௿") + str(bstack1lll111ll_opy_)) + bstack111l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ఀ"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఁ") or runner.driver_initialised == bstack111l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨం"):
        bstack11ll11l11_opy_(bstack1lll11lll_opy_, bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩః"), bstack111l11_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢఄ") + str(bstack1l111111ll_opy_))
    else:
      bstack1lllll1l1_opy_(context, bstack111l11_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧఅ"), bstack111l11_opy_ (u"ࠧ࡯࡮ࡧࡱࠥఆ"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఇ") or runner.driver_initialised == bstack111l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఈ"):
        bstack11ll11ll_opy_(getattr(context, bstack111l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ఉ"), None), bstack111l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤఊ"))
      bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨఋ") + json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣఌ")) + bstack111l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ఍"))
      if runner.driver_initialised == bstack111l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣఎ") or runner.driver_initialised == bstack111l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧఏ"):
        bstack11ll11l11_opy_(bstack1lll11lll_opy_, bstack111l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣఐ"))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ఑").format(str(e)))
  bstack11llll111l_opy_(runner, name, context, context.scenario, bstack11l11ll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1111ll11_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack111l11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఒ")) else context.feature
    bstack11llll111l_opy_(runner, name, context, target, bstack11l11ll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack111llll11_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    try:
      bstack1lll11lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఓ"), context.browser)
      bstack11111l1l1_opy_ = bstack111l11_opy_ (u"ࠬ࠭ఔ")
      if context.failed is True:
        bstack1l11lll1l1_opy_ = []
        bstack111llll1_opy_ = []
        bstack1l1l1l1111_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l11lll1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1ll11ll_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11l11l1_opy_ = bstack111l11_opy_ (u"࠭ࠠࠨక").join(bstack1l1ll11ll_opy_)
            bstack111llll1_opy_.append(bstack1ll11l11l1_opy_)
            bstack1l1l1l1111_opy_.append(bstack1l1ll11ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1lll1l11_opy_.format(str(e)))
        bstack1l111111ll_opy_ = bstack111l11_opy_ (u"ࠧࠨఖ")
        for i in range(len(bstack1l11lll1l1_opy_)):
          bstack1l111111ll_opy_ += bstack1l11lll1l1_opy_[i] + bstack1l1l1l1111_opy_[i] + bstack111l11_opy_ (u"ࠨ࡞ࡱࠫగ")
        bstack11111l1l1_opy_ = bstack111l11_opy_ (u"ࠩࠣࠫఘ").join(bstack111llll1_opy_)
        if runner.driver_initialised in [bstack111l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦఙ"), bstack111l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣచ")]:
          bstack1lllll1l1_opy_(context, bstack11111l1l1_opy_, bstack111l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦఛ"))
          bstack11ll11ll_opy_(getattr(context, bstack111l11_opy_ (u"࠭ࡰࡢࡩࡨࠫజ"), None), bstack111l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢఝ"), bstack1l111111ll_opy_)
          bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ఞ") + json.dumps(bstack11111l1l1_opy_) + bstack111l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩట"))
          bstack11ll11l11_opy_(bstack1lll11lll_opy_, bstack111l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥఠ"), bstack111l11_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤడ") + str(bstack1l111111ll_opy_))
          bstack11lll1l1_opy_ = bstack11l1llllll_opy_(bstack11111l1l1_opy_, runner.feature.name, logger)
          if (bstack11lll1l1_opy_ != None):
            bstack11l111ll1l_opy_.append(bstack11lll1l1_opy_)
      else:
        if runner.driver_initialised in [bstack111l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨఢ"), bstack111l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥణ")]:
          bstack1lllll1l1_opy_(context, bstack111l11_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥత") + str(runner.feature.name) + bstack111l11_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥథ"), bstack111l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢద"))
          bstack11ll11ll_opy_(getattr(context, bstack111l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨధ"), None), bstack111l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦన"))
          bstack1lll11lll_opy_.execute_script(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ఩") + json.dumps(bstack111l11_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤప") + str(runner.feature.name) + bstack111l11_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤఫ")) + bstack111l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧబ"))
          bstack11ll11l11_opy_(bstack1lll11lll_opy_, bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩభ"))
          bstack11lll1l1_opy_ = bstack11l1llllll_opy_(bstack11111l1l1_opy_, runner.feature.name, logger)
          if (bstack11lll1l1_opy_ != None):
            bstack11l111ll1l_opy_.append(bstack11lll1l1_opy_)
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬమ").format(str(e)))
    bstack11llll111l_opy_(runner, name, context, context.feature, bstack11l11ll1_opy_, *args)
@measure(event_name=EVENTS.bstack1llll1l11_opy_, stage=STAGE.bstack1l1l11ll1_opy_, hook_type=bstack111l11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡄࡰࡱࠨయ"), bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll111l1l1_opy_(runner, name, context, bstack11l11ll1_opy_, *args):
    bstack11llll111l_opy_(runner, name, context, runner, bstack11l11ll1_opy_, *args)
def bstack11l11l11ll_opy_(self, name, context, *args):
  if bstack11ll1l1l11_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l111l11_opy_
    bstack1l111l1l1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨర")][platform_index]
    os.environ[bstack111l11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧఱ")] = json.dumps(bstack1l111l1l1_opy_)
  global bstack11l11ll1_opy_
  if not hasattr(self, bstack111l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࡨࠬల")):
    self.driver_initialised = None
  bstack1l1l11111_opy_ = {
      bstack111l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬళ"): bstack11l11lll11_opy_,
      bstack111l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪఴ"): bstack1ll1l111l_opy_,
      bstack111l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡸࡦ࡭ࠧవ"): bstack11lll111l1_opy_,
      bstack111l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭శ"): bstack1ll1lll11l_opy_,
      bstack111l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠪష"): bstack1ll1111111_opy_,
      bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪస"): bstack11lll1l11l_opy_,
      bstack111l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨహ"): bstack1lll1111ll_opy_,
      bstack111l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡵࡣࡪࠫ఺"): bstack1l1111ll11_opy_,
      bstack111l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ఻"): bstack111llll11_opy_,
      bstack111l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ఼࠭"): bstack1ll111l1l1_opy_
  }
  handler = bstack1l1l11111_opy_.get(name, bstack11l11ll1_opy_)
  handler(self, name, context, bstack11l11ll1_opy_, *args)
  if name in [bstack111l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫఽ"), bstack111l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ా"), bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩి")]:
    try:
      bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l111l1_opy_(bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ీ")) else context.browser
      bstack11l11lll1_opy_ = (
        (name == bstack111l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫు") and self.driver_initialised == bstack111l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨూ")) or
        (name == bstack111l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪృ") and self.driver_initialised == bstack111l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧౄ")) or
        (name == bstack111l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౅") and self.driver_initialised in [bstack111l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣె"), bstack111l11_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢే")]) or
        (name == bstack111l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬై") and self.driver_initialised == bstack111l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౉"))
      )
      if bstack11l11lll1_opy_:
        self.driver_initialised = None
        bstack1lll11lll_opy_.quit()
    except Exception:
      pass
def bstack11l111l1l_opy_(config, startdir):
  return bstack111l11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣొ").format(bstack111l11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥో"))
notset = Notset()
def bstack1lllll11l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1llll11ll1_opy_
  if str(name).lower() == bstack111l11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬౌ"):
    return bstack111l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯్ࠧ")
  else:
    return bstack1llll11ll1_opy_(self, name, default, skip)
def bstack11l1llll_opy_(item, when):
  global bstack1lllll1lll_opy_
  try:
    bstack1lllll1lll_opy_(item, when)
  except Exception as e:
    pass
def bstack11l1ll1ll_opy_():
  return
def bstack1l11l111ll_opy_(type, name, status, reason, bstack11l1l1l111_opy_, bstack1l11ll1lll_opy_):
  bstack1l1ll111ll_opy_ = {
    bstack111l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ౎"): type,
    bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ౏"): {}
  }
  if type == bstack111l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ౐"):
    bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭౑")][bstack111l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ౒")] = bstack11l1l1l111_opy_
    bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౓")][bstack111l11_opy_ (u"࠭ࡤࡢࡶࡤࠫ౔")] = json.dumps(str(bstack1l11ll1lll_opy_))
  if type == bstack111l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨౕ"):
    bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶౖࠫ")][bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౗")] = name
  if type == bstack111l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ౘ"):
    bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౙ")][bstack111l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౚ")] = status
    if status == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౛"):
      bstack1l1ll111ll_opy_[bstack111l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౜")][bstack111l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨౝ")] = json.dumps(str(reason))
  bstack111lll11_opy_ = bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౞").format(json.dumps(bstack1l1ll111ll_opy_))
  return bstack111lll11_opy_
def bstack1lll1lll_opy_(driver_command, response):
    if driver_command == bstack111l11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ౟"):
        bstack1l11l1l1ll_opy_.bstack11lllll1l1_opy_({
            bstack111l11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪౠ"): response[bstack111l11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫౡ")],
            bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ౢ"): bstack1l11l1l1ll_opy_.current_test_uuid()
        })
def bstack11ll11l1ll_opy_(item, call, rep):
  global bstack1ll11l1l11_opy_
  global bstack11111l1l_opy_
  global bstack1ll1lllll_opy_
  name = bstack111l11_opy_ (u"ࠧࠨౣ")
  try:
    if rep.when == bstack111l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭౤"):
      bstack1lll11l1ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1lllll_opy_:
          name = str(rep.nodeid)
          bstack111l11l1_opy_ = bstack1l11l111ll_opy_(bstack111l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౥"), name, bstack111l11_opy_ (u"ࠪࠫ౦"), bstack111l11_opy_ (u"ࠫࠬ౧"), bstack111l11_opy_ (u"ࠬ࠭౨"), bstack111l11_opy_ (u"࠭ࠧ౩"))
          threading.current_thread().bstack11ll1lll1_opy_ = name
          for driver in bstack11111l1l_opy_:
            if bstack1lll11l1ll_opy_ == driver.session_id:
              driver.execute_script(bstack111l11l1_opy_)
      except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ౪").format(str(e)))
      try:
        bstack1l1ll1111l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ౫"):
          status = bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౬") if rep.outcome.lower() == bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౭") else bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౮")
          reason = bstack111l11_opy_ (u"ࠬ࠭౯")
          if status == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౰"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111l11_opy_ (u"ࠧࡪࡰࡩࡳࠬ౱") if status == bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౲") else bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౳")
          data = name + bstack111l11_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ౴") if status == bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ౵") else name + bstack111l11_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ౶") + reason
          bstack11l1l111l1_opy_ = bstack1l11l111ll_opy_(bstack111l11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ౷"), bstack111l11_opy_ (u"ࠧࠨ౸"), bstack111l11_opy_ (u"ࠨࠩ౹"), bstack111l11_opy_ (u"ࠩࠪ౺"), level, data)
          for driver in bstack11111l1l_opy_:
            if bstack1lll11l1ll_opy_ == driver.session_id:
              driver.execute_script(bstack11l1l111l1_opy_)
      except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ౻").format(str(e)))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ౼").format(str(e)))
  bstack1ll11l1l11_opy_(item, call, rep)
def bstack1l11l111_opy_(driver, bstack1llll111l_opy_, test=None):
  global bstack1ll1111l1_opy_
  if test != None:
    bstack11ll111lll_opy_ = getattr(test, bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౽"), None)
    bstack1ll1111l_opy_ = getattr(test, bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ౾"), None)
    PercySDK.screenshot(driver, bstack1llll111l_opy_, bstack11ll111lll_opy_=bstack11ll111lll_opy_, bstack1ll1111l_opy_=bstack1ll1111l_opy_, bstack1l1l1111l1_opy_=bstack1ll1111l1_opy_)
  else:
    PercySDK.screenshot(driver, bstack1llll111l_opy_)
@measure(event_name=EVENTS.bstack11l1lllll_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l11l1l_opy_(driver):
  if bstack111ll11l_opy_.bstack111111111_opy_() is True or bstack111ll11l_opy_.capturing() is True:
    return
  bstack111ll11l_opy_.bstack1ll1ll1ll1_opy_()
  while not bstack111ll11l_opy_.bstack111111111_opy_():
    bstack1ll1ll1ll_opy_ = bstack111ll11l_opy_.bstack1lll11111_opy_()
    bstack1l11l111_opy_(driver, bstack1ll1ll1ll_opy_)
  bstack111ll11l_opy_.bstack1l1l1l11l_opy_()
def bstack11l11ll1l_opy_(sequence, driver_command, response = None, bstack11ll1l11ll_opy_ = None, args = None):
    try:
      if sequence != bstack111l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ౿"):
        return
      if percy.bstack1111l1lll_opy_() == bstack111l11_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢಀ"):
        return
      bstack1ll1ll1ll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಁ"), None)
      for command in bstack11lllll1_opy_:
        if command == driver_command:
          for driver in bstack11111l1l_opy_:
            bstack11l11l1l_opy_(driver)
      bstack1111lllll_opy_ = percy.bstack111ll1lll_opy_()
      if driver_command in bstack1l11l11l1_opy_[bstack1111lllll_opy_]:
        bstack111ll11l_opy_.bstack1l1ll1l1l1_opy_(bstack1ll1ll1ll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l11111111_opy_(framework_name):
  if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧಂ")):
      return
  bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨಃ"), True)
  global bstack11llllllll_opy_
  global bstack111ll11ll_opy_
  global bstack11ll1l1l_opy_
  bstack11llllllll_opy_ = framework_name
  logger.info(bstack111l11l11_opy_.format(bstack11llllllll_opy_.split(bstack111l11_opy_ (u"ࠬ࠳ࠧ಄"))[0]))
  bstack1ll1l1111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11ll1l1l11_opy_:
      Service.start = bstack1l111111l_opy_
      Service.stop = bstack1l1lll1ll1_opy_
      webdriver.Remote.get = bstack1ll11l1l1_opy_
      WebDriver.close = bstack11111lll1_opy_
      WebDriver.quit = bstack1lll11111l_opy_
      webdriver.Remote.__init__ = bstack11l1l1l11_opy_
    if not bstack11ll1l1l11_opy_:
        webdriver.Remote.__init__ = bstack1l1lllll11_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1lll1lll_opy_
    bstack111ll11ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11ll1l1l11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1l111l1l_opy_
  except Exception as e:
    pass
  bstack11l1lll11l_opy_()
  if not bstack111ll11ll_opy_:
    bstack1111111l1_opy_(bstack111l11_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣಅ"), bstack11l1lllll1_opy_)
  if bstack11lll11l1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1l1ll11111_opy_ = bstack1ll1l1ll1l_opy_
    except Exception as e:
      logger.error(bstack11llll11l_opy_.format(str(e)))
  if bstack11ll1111_opy_():
    bstack11llll1l1_opy_(CONFIG, logger)
  if (bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಆ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1111l1lll_opy_() == bstack111l11_opy_ (u"ࠣࡶࡵࡹࡪࠨಇ"):
          bstack1ll1l1l11_opy_(bstack11l11ll1l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1l1ll11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll111l_opy_
      except Exception as e:
        logger.warn(bstack1l111l11l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1llll11_opy_
      except Exception as e:
        logger.debug(bstack11lll1ll11_opy_ + str(e))
    except Exception as e:
      bstack1111111l1_opy_(e, bstack1l111l11l1_opy_)
    Output.start_test = bstack1ll11llll1_opy_
    Output.end_test = bstack1lllll111l_opy_
    TestStatus.__init__ = bstack111l1lll_opy_
    QueueItem.__init__ = bstack11l1l11ll_opy_
    pabot._create_items = bstack1lllllll1l_opy_
    try:
      from pabot import __version__ as bstack11llllll1l_opy_
      if version.parse(bstack11llllll1l_opy_) >= version.parse(bstack111l11_opy_ (u"ࠩ࠷࠲࠷࠴࠰ࠨಈ")):
        pabot._run = bstack1lll111ll1_opy_
      elif version.parse(bstack11llllll1l_opy_) >= version.parse(bstack111l11_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪಉ")):
        pabot._run = bstack1l11l11lll_opy_
      elif version.parse(bstack11llllll1l_opy_) >= version.parse(bstack111l11_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫಊ")):
        pabot._run = bstack1ll1ll1l_opy_
      else:
        pabot._run = bstack1l1111l1l1_opy_
    except Exception as e:
      pabot._run = bstack1l1111l1l1_opy_
    pabot._create_command_for_execution = bstack11lll1111l_opy_
    pabot._report_results = bstack1llll11ll_opy_
  if bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬಋ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111111l1_opy_(e, bstack11ll11l1l_opy_)
    Runner.run_hook = bstack11l11l11ll_opy_
    Step.run = bstack1ll111ll1l_opy_
  if bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಌ") in str(framework_name).lower():
    if not bstack11ll1l1l11_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l111l1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11l1ll1ll_opy_
      Config.getoption = bstack1lllll11l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11ll11l1ll_opy_
    except Exception as e:
      pass
def bstack1ll1lll1l1_opy_():
  global CONFIG
  if bstack111l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ಍") in CONFIG and int(CONFIG[bstack111l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಎ")]) > 1:
    logger.warn(bstack1ll1l11l1_opy_)
def bstack1lll1ll11_opy_(arg, bstack1111lll11_opy_, bstack1llll111l1_opy_=None):
  global CONFIG
  global bstack1ll11l1l_opy_
  global bstack1ll11ll11_opy_
  global bstack11ll1l1l11_opy_
  global bstack111l111ll_opy_
  bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಏ")
  if bstack1111lll11_opy_ and isinstance(bstack1111lll11_opy_, str):
    bstack1111lll11_opy_ = eval(bstack1111lll11_opy_)
  CONFIG = bstack1111lll11_opy_[bstack111l11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪಐ")]
  bstack1ll11l1l_opy_ = bstack1111lll11_opy_[bstack111l11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ಑")]
  bstack1ll11ll11_opy_ = bstack1111lll11_opy_[bstack111l11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧಒ")]
  bstack11ll1l1l11_opy_ = bstack1111lll11_opy_[bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩಓ")]
  bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨಔ"), bstack11ll1l1l11_opy_)
  os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಕ")] = bstack1l1ll1l11l_opy_
  os.environ[bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨಖ")] = json.dumps(CONFIG)
  os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪಗ")] = bstack1ll11l1l_opy_
  os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬಘ")] = str(bstack1ll11ll11_opy_)
  os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫಙ")] = str(True)
  if bstack1l1l1ll1l_opy_(arg, [bstack111l11_opy_ (u"࠭࠭࡯ࠩಚ"), bstack111l11_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨಛ")]) != -1:
    os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩಜ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1l1l1ll_opy_)
    return
  bstack1ll11ll1ll_opy_()
  global bstack1ll1111l1l_opy_
  global bstack1ll1111l1_opy_
  global bstack1l11l11111_opy_
  global bstack11ll1ll1l_opy_
  global bstack1l1l11ll11_opy_
  global bstack11ll1l1l_opy_
  global bstack11lll1l11_opy_
  arg.append(bstack111l11_opy_ (u"ࠤ࠰࡛ࠧಝ"))
  arg.append(bstack111l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨಞ"))
  arg.append(bstack111l11_opy_ (u"ࠦ࠲࡝ࠢಟ"))
  arg.append(bstack111l11_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦಠ"))
  global bstack11ll11lll1_opy_
  global bstack1ll1l111ll_opy_
  global bstack1ll1lll1_opy_
  global bstack1111ll11l_opy_
  global bstack1l1l11ll_opy_
  global bstack111111ll_opy_
  global bstack1l1111llll_opy_
  global bstack1l11ll11l1_opy_
  global bstack1lll11l1l_opy_
  global bstack111l1lll1_opy_
  global bstack1llll11ll1_opy_
  global bstack1lllll1lll_opy_
  global bstack1ll11l1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll11lll1_opy_ = webdriver.Remote.__init__
    bstack1ll1l111ll_opy_ = WebDriver.quit
    bstack1l11ll11l1_opy_ = WebDriver.close
    bstack1lll11l1l_opy_ = WebDriver.get
    bstack1ll1lll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1l1l1ll1_opy_(CONFIG) and bstack11l11ll11_opy_():
    if bstack11l1lll1l_opy_() < version.parse(bstack11l1ll111_opy_):
      logger.error(bstack11l11l1ll1_opy_.format(bstack11l1lll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111l1lll1_opy_ = RemoteConnection._1l1ll11111_opy_
      except Exception as e:
        logger.error(bstack11llll11l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1llll11ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1lllll1lll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l11ll1l1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll11l1l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧಡ"))
  bstack1l11l11111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫಢ"), {}).get(bstack111l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಣ"))
  bstack11lll1l11_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11llll1l_opy_():
      bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.CONNECT, bstack11l1l1l1ll_opy_())
    platform_index = int(os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩತ"), bstack111l11_opy_ (u"ࠪ࠴ࠬಥ")))
  else:
    bstack1l11111111_opy_(bstack11lll1lll_opy_)
  os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬದ")] = CONFIG[bstack111l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಧ")]
  os.environ[bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩನ")] = CONFIG[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ಩")]
  os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫಪ")] = bstack11ll1l1l11_opy_.__str__()
  from _pytest.config import main as bstack1l11l111l_opy_
  bstack1lll1ll111_opy_ = []
  try:
    bstack1lll1l1ll1_opy_ = bstack1l11l111l_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1llll1lll_opy_()
    if bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ಫ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1ll111_opy_.append(bstack1ll1l1l1l1_opy_)
    try:
      bstack1l111l1lll_opy_ = (bstack1lll1ll111_opy_, int(bstack1lll1l1ll1_opy_))
      bstack1llll111l1_opy_.append(bstack1l111l1lll_opy_)
    except:
      bstack1llll111l1_opy_.append((bstack1lll1ll111_opy_, bstack1lll1l1ll1_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1lll1ll111_opy_.append({bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨಬ"): bstack111l11_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭ಭ") + os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಮ")), bstack111l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬಯ"): traceback.format_exc(), bstack111l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ರ"): int(os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨಱ")))})
    bstack1llll111l1_opy_.append((bstack1lll1ll111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack111l11_opy_ (u"ࠤࡵࡩࡹࡸࡩࡦࡵࠥಲ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack11llll11l1_opy_ = e.__class__.__name__
    print(bstack111l11_opy_ (u"ࠥࠩࡸࡀࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡧࡶࡸࠥࠫࡳࠣಳ") % (bstack11llll11l1_opy_, e))
    return 1
def bstack1l1l1lllll_opy_(arg):
  global bstack1l11llllll_opy_
  bstack1l11111111_opy_(bstack1l11ll111_opy_)
  os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ಴")] = str(bstack1ll11ll11_opy_)
  retries = bstack11ll11l11l_opy_.bstack1111lll1l_opy_(CONFIG)
  status_code = 0
  if bstack11ll11l11l_opy_.bstack1l1l1l111l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack11llll11ll_opy_
    status_code = bstack11llll11ll_opy_(arg)
  if status_code != 0:
    bstack1l11llllll_opy_ = status_code
def bstack1l111111l1_opy_():
  logger.info(bstack1l1l11lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫವ"), help=bstack111l11_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧಶ"))
  parser.add_argument(bstack111l11_opy_ (u"ࠧ࠮ࡷࠪಷ"), bstack111l11_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬಸ"), help=bstack111l11_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨಹ"))
  parser.add_argument(bstack111l11_opy_ (u"ࠪ࠱ࡰ࠭಺"), bstack111l11_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ಻"), help=bstack111l11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ಼࠭"))
  parser.add_argument(bstack111l11_opy_ (u"࠭࠭ࡧࠩಽ"), bstack111l11_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬಾ"), help=bstack111l11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಿ"))
  bstack1l1ll11l1_opy_ = parser.parse_args()
  try:
    bstack1ll1ll1l1_opy_ = bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ೀ")
    if bstack1l1ll11l1_opy_.framework and bstack1l1ll11l1_opy_.framework not in (bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪು"), bstack111l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬೂ")):
      bstack1ll1ll1l1_opy_ = bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫೃ")
    bstack11l1ll11l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1ll1l1_opy_)
    bstack1l11111l_opy_ = open(bstack11l1ll11l_opy_, bstack111l11_opy_ (u"࠭ࡲࠨೄ"))
    bstack1ll11ll111_opy_ = bstack1l11111l_opy_.read()
    bstack1l11111l_opy_.close()
    if bstack1l1ll11l1_opy_.username:
      bstack1ll11ll111_opy_ = bstack1ll11ll111_opy_.replace(bstack111l11_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ೅"), bstack1l1ll11l1_opy_.username)
    if bstack1l1ll11l1_opy_.key:
      bstack1ll11ll111_opy_ = bstack1ll11ll111_opy_.replace(bstack111l11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪೆ"), bstack1l1ll11l1_opy_.key)
    if bstack1l1ll11l1_opy_.framework:
      bstack1ll11ll111_opy_ = bstack1ll11ll111_opy_.replace(bstack111l11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೇ"), bstack1l1ll11l1_opy_.framework)
    file_name = bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ೈ")
    file_path = os.path.abspath(file_name)
    bstack11lll1111_opy_ = open(file_path, bstack111l11_opy_ (u"ࠫࡼ࠭೉"))
    bstack11lll1111_opy_.write(bstack1ll11ll111_opy_)
    bstack11lll1111_opy_.close()
    logger.info(bstack1l1ll11lll_opy_)
    try:
      os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧೊ")] = bstack1l1ll11l1_opy_.framework if bstack1l1ll11l1_opy_.framework != None else bstack111l11_opy_ (u"ࠨࠢೋ")
      config = yaml.safe_load(bstack1ll11ll111_opy_)
      config[bstack111l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧೌ")] = bstack111l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶ್ࠧ")
      bstack11l1l111_opy_(bstack1l11l11ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1111l111l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11ll1111l_opy_.format(str(e)))
def bstack11l1l111_opy_(bstack1111l1l1_opy_, config, bstack111ll1l1_opy_={}):
  global bstack11ll1l1l11_opy_
  global bstack11lll11111_opy_
  global bstack111l111ll_opy_
  if not config:
    return
  bstack11l111111_opy_ = bstack1ll11lll1_opy_ if not bstack11ll1l1l11_opy_ else (
    bstack11l111l1l1_opy_ if bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭೎") in config else (
        bstack11l11lllll_opy_ if config.get(bstack111l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ೏")) else bstack1lll1l1l1_opy_
    )
)
  bstack1l1lllllll_opy_ = False
  bstack11l11l1l1l_opy_ = False
  if bstack11ll1l1l11_opy_ is True:
      if bstack111l11_opy_ (u"ࠫࡦࡶࡰࠨ೐") in config:
          bstack1l1lllllll_opy_ = True
      else:
          bstack11l11l1l1l_opy_ = True
  bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11ll1lllll_opy_(config, bstack11lll11111_opy_)
  bstack1llll11lll_opy_ = bstack1111l1ll1_opy_()
  data = {
    bstack111l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ೑"): config[bstack111l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ೒")],
    bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ೓"): config[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ೔")],
    bstack111l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ೕ"): bstack1111l1l1_opy_,
    bstack111l11_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೖ"): os.environ.get(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೗"), bstack11lll11111_opy_),
    bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ೘"): bstack1l1lll111l_opy_,
    bstack111l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨ೙"): bstack11ll1ll1l1_opy_(),
    bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೚"): {
      bstack111l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೛"): str(config[bstack111l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ೜")]) if bstack111l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪೝ") in config else bstack111l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧೞ"),
      bstack111l11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧ೟"): sys.version,
      bstack111l11_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨೠ"): bstack11l11l111_opy_(os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩೡ"), bstack11lll11111_opy_)),
      bstack111l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪೢ"): bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೣ"),
      bstack111l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ೤"): bstack11l111111_opy_,
      bstack111l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ೥"): bstack1l1ll111l_opy_,
      bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫ೦"): os.environ[bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ೧")],
      bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೨"): os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ೩"), bstack11lll11111_opy_),
      bstack111l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ೪"): bstack1ll1l11ll1_opy_(os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ೫"), bstack11lll11111_opy_)),
      bstack111l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೬"): bstack1llll11lll_opy_.get(bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೭")),
      bstack111l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ೮"): bstack1llll11lll_opy_.get(bstack111l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ೯")),
      bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೰"): config[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೱ")] if config[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೲ")] else bstack111l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧೳ"),
      bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೴"): str(config[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೵")]) if bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೶") in config else bstack111l11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೷"),
      bstack111l11_opy_ (u"ࠩࡲࡷࠬ೸"): sys.platform,
      bstack111l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ೹"): socket.gethostname(),
      bstack111l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭೺"): bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ೻"))
    }
  }
  if not bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭೼")) is None:
    data[bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೽")][bstack111l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡐࡩࡹࡧࡤࡢࡶࡤࠫ೾")] = {
      bstack111l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ೿"): bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨഀ"),
      bstack111l11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫഁ"): bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬം")),
      bstack111l11_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱࡔࡵ࡮ࡤࡨࡶࠬഃ"): bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪഄ"))
    }
  if bstack1111l1l1_opy_ == bstack11l111l11l_opy_:
    data[bstack111l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫഅ")][bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࠧആ")] = bstack1111llll1_opy_(config)
    data[bstack111l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ഇ")][bstack111l11_opy_ (u"ࠫ࡮ࡹࡐࡦࡴࡦࡽࡆࡻࡴࡰࡇࡱࡥࡧࡲࡥࡥࠩഈ")] = percy.bstack1ll1l1ll_opy_
    data[bstack111l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഉ")][bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡇࡻࡩ࡭ࡦࡌࡨࠬഊ")] = percy.percy_build_id
  if not bstack11ll11l11l_opy_.bstack1ll11l1lll_opy_(CONFIG):
    data[bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഋ")][bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬഌ")] = bstack11ll11l11l_opy_.bstack1ll11l1lll_opy_(CONFIG)
  update(data[bstack111l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ഍")], bstack111ll1l1_opy_)
  try:
    response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨഎ"), bstack1l1lll1ll_opy_(bstack11lll1l1ll_opy_), data, {
      bstack111l11_opy_ (u"ࠫࡦࡻࡴࡩࠩഏ"): (config[bstack111l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഐ")], config[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ഑")])
    })
    if response:
      logger.debug(bstack1ll1l1lll1_opy_.format(bstack1111l1l1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l11l1l1l1_opy_.format(str(e)))
def bstack11l11l111_opy_(framework):
  return bstack111l11_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦഒ").format(str(framework), __version__) if framework else bstack111l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഓ").format(
    __version__)
def bstack1ll11ll1ll_opy_():
  global CONFIG
  global bstack1lll1l1l11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1llll11l_opy_()
    logger.debug(bstack11llll1l1l_opy_.format(str(CONFIG)))
    bstack1lll1l1l11_opy_ = bstack1lll111lll_opy_.bstack111ll1l1l_opy_(CONFIG, bstack1lll1l1l11_opy_)
    bstack1ll1l1111_opy_()
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨഔ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11ll1llll1_opy_
  atexit.register(bstack1l11l11l_opy_)
  signal.signal(signal.SIGINT, bstack1111l1l11_opy_)
  signal.signal(signal.SIGTERM, bstack1111l1l11_opy_)
def bstack11ll1llll1_opy_(exctype, value, traceback):
  global bstack11111l1l_opy_
  try:
    for driver in bstack11111l1l_opy_:
      bstack11ll11l11_opy_(driver, bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪക"), bstack111l11_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢഖ") + str(value))
  except Exception:
    pass
  logger.info(bstack1l11l11ll1_opy_)
  bstack11ll1111l1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11ll1111l1_opy_(message=bstack111l11_opy_ (u"ࠬ࠭ഗ"), bstack1111lll1_opy_ = False):
  global CONFIG
  bstack1111ll111_opy_ = bstack111l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨഘ") if bstack1111lll1_opy_ else bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ങ")
  try:
    if message:
      bstack111ll1l1_opy_ = {
        bstack1111ll111_opy_ : str(message)
      }
      bstack11l1l111_opy_(bstack11l111l11l_opy_, CONFIG, bstack111ll1l1_opy_)
    else:
      bstack11l1l111_opy_(bstack11l111l11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack111l1ll11_opy_.format(str(e)))
def bstack11ll1ll111_opy_(bstack1lllll1l11_opy_, size):
  bstack11ll11ll1l_opy_ = []
  while len(bstack1lllll1l11_opy_) > size:
    bstack1ll1l1ll1_opy_ = bstack1lllll1l11_opy_[:size]
    bstack11ll11ll1l_opy_.append(bstack1ll1l1ll1_opy_)
    bstack1lllll1l11_opy_ = bstack1lllll1l11_opy_[size:]
  bstack11ll11ll1l_opy_.append(bstack1lllll1l11_opy_)
  return bstack11ll11ll1l_opy_
def bstack1l1ll11l1l_opy_(args):
  if bstack111l11_opy_ (u"ࠨ࠯ࡰࠫച") in args and bstack111l11_opy_ (u"ࠩࡳࡨࡧ࠭ഛ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11l111lll_opy_, stage=STAGE.bstack1lll11l1l1_opy_)
def run_on_browserstack(bstack1l1l1l1lll_opy_=None, bstack1llll111l1_opy_=None, bstack1ll1l11ll_opy_=False):
  global CONFIG
  global bstack1ll11l1l_opy_
  global bstack1ll11ll11_opy_
  global bstack11lll11111_opy_
  global bstack111l111ll_opy_
  bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠪࠫജ")
  bstack1lll11l1_opy_(bstack1l1lll11ll_opy_, logger)
  if bstack1l1l1l1lll_opy_ and isinstance(bstack1l1l1l1lll_opy_, str):
    bstack1l1l1l1lll_opy_ = eval(bstack1l1l1l1lll_opy_)
  if bstack1l1l1l1lll_opy_:
    CONFIG = bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫഝ")]
    bstack1ll11l1l_opy_ = bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ഞ")]
    bstack1ll11ll11_opy_ = bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨട")]
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩഠ"), bstack1ll11ll11_opy_)
    bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഡ")
  bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫഢ"), uuid4().__str__())
  logger.info(bstack111l11_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨണ") + bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ത")));
  logger.debug(bstack111l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨഥ") + bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨദ")))
  if not bstack1ll1l11ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1l1l1ll_opy_)
      return
    if sys.argv[1] == bstack111l11_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪധ") or sys.argv[1] == bstack111l11_opy_ (u"ࠨ࠯ࡹࠫന"):
      logger.info(bstack111l11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩഩ").format(__version__))
      return
    if sys.argv[1] == bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩപ"):
      bstack1l111111l1_opy_()
      return
  args = sys.argv
  bstack1ll11ll1ll_opy_()
  global bstack1ll1111l1l_opy_
  global bstack1l111l11_opy_
  global bstack11lll1l11_opy_
  global bstack11l1lll1_opy_
  global bstack1ll1111l1_opy_
  global bstack1l11l11111_opy_
  global bstack11ll1ll1l_opy_
  global bstack1lll11ll_opy_
  global bstack1l1l11ll11_opy_
  global bstack11ll1l1l_opy_
  global bstack11ll1l111_opy_
  bstack1l111l11_opy_ = len(CONFIG.get(bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഫ"), []))
  if not bstack1l1ll1l11l_opy_:
    if args[1] == bstack111l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬബ") or args[1] == bstack111l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧഭ"):
      bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧമ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧയ"):
      bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨര")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩറ"):
      bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪല")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ള"):
      bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧഴ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧവ"):
      bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨശ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഷ"):
      bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪസ")
      args = args[2:]
    else:
      if not bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഹ") in CONFIG or str(CONFIG[bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഺ")]).lower() in [bstack111l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ഻࠭"), bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ഼")]:
        bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഽ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬാ")]).lower() == bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩി"):
        bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪീ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨു")]).lower() == bstack111l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬൂ"):
        bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൃ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫൄ")]).lower() == bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൅"):
        bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪെ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧേ")]).lower() == bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬൈ"):
        bstack1l1ll1l11l_opy_ = bstack111l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭൉")
        args = args[1:]
      else:
        os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൊ")] = bstack1l1ll1l11l_opy_
        bstack1ll11ll1_opy_(bstack1l11llll1l_opy_)
  os.environ[bstack111l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩോ")] = bstack1l1ll1l11l_opy_
  bstack11lll11111_opy_ = bstack1l1ll1l11l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack111ll11l1_opy_ = bstack1ll1l11lll_opy_[bstack111l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ൌ")] if bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ്ࠪ") and bstack11l11l11_opy_() else bstack1l1ll1l11l_opy_
      bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.bstack1lllllll11_opy_, bstack1l11111ll1_opy_(
        sdk_version=__version__,
        path_config=bstack11l1ll1l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack111ll11l1_opy_,
        frameworks=[bstack111ll11l1_opy_],
        framework_versions={
          bstack111ll11l1_opy_: bstack1ll1l11ll1_opy_(bstack111l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪൎ") if bstack1l1ll1l11l_opy_ in [bstack111l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൏"), bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൐"), bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ൑")] else bstack1l1ll1l11l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ൒"), None):
        CONFIG[bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ൓")] = cli.config.get(bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧൔ"), None)
    except Exception as e:
      bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.bstack11l1ll1l_opy_, e.__traceback__, 1)
    if bstack1ll11ll11_opy_:
      CONFIG[bstack111l11_opy_ (u"ࠦࡦࡶࡰࠣൕ")] = cli.config[bstack111l11_opy_ (u"ࠧࡧࡰࡱࠤൖ")]
      logger.info(bstack1l1l1ll11_opy_.format(CONFIG[bstack111l11_opy_ (u"࠭ࡡࡱࡲࠪൗ")]))
  else:
    bstack1ll11l11l_opy_.clear()
  global bstack11llll1ll1_opy_
  global bstack11ll11l1_opy_
  if bstack1l1l1l1lll_opy_:
    try:
      bstack111l1l111_opy_ = datetime.datetime.now()
      os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ൘")] = bstack1l1ll1l11l_opy_
      bstack11l1l111_opy_(bstack1l1llll11l_opy_, CONFIG)
      cli.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦ൙"), datetime.datetime.now() - bstack111l1l111_opy_)
    except Exception as e:
      logger.debug(bstack11l1111ll_opy_.format(str(e)))
  global bstack11ll11lll1_opy_
  global bstack1ll1l111ll_opy_
  global bstack1l11l1111_opy_
  global bstack1l1111ll_opy_
  global bstack1llll1l11l_opy_
  global bstack1llllllll1_opy_
  global bstack1111ll11l_opy_
  global bstack1l1l11ll_opy_
  global bstack1l1lll1111_opy_
  global bstack111111ll_opy_
  global bstack1l1111llll_opy_
  global bstack1l11ll11l1_opy_
  global bstack11l11ll1_opy_
  global bstack1l111ll11l_opy_
  global bstack1lll11l1l_opy_
  global bstack111l1lll1_opy_
  global bstack1llll11ll1_opy_
  global bstack1lllll1lll_opy_
  global bstack1l111l1ll_opy_
  global bstack1ll11l1l11_opy_
  global bstack1ll1lll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll11lll1_opy_ = webdriver.Remote.__init__
    bstack1ll1l111ll_opy_ = WebDriver.quit
    bstack1l11ll11l1_opy_ = WebDriver.close
    bstack1lll11l1l_opy_ = WebDriver.get
    bstack1ll1lll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11llll1ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11l1lll1_opy_
    bstack11ll11l1_opy_ = bstack1l11l1lll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1l1lll_opy_
    from QWeb.keywords import browser
    bstack1l1l1lll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1l1l1ll1_opy_(CONFIG) and bstack11l11ll11_opy_():
    if bstack11l1lll1l_opy_() < version.parse(bstack11l1ll111_opy_):
      logger.error(bstack11l11l1ll1_opy_.format(bstack11l1lll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111l1lll1_opy_ = RemoteConnection._1l1ll11111_opy_
      except Exception as e:
        logger.error(bstack11llll11l_opy_.format(str(e)))
  if not CONFIG.get(bstack111l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ൚"), False) and not bstack1l1l1l1lll_opy_:
    logger.info(bstack11lll11l1_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack111l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ൛") in CONFIG and str(CONFIG[bstack111l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ൜")]).lower() != bstack111l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ൝"):
      bstack1ll1l1l1l_opy_()
    elif bstack1l1ll1l11l_opy_ != bstack111l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൞") or (bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧൟ") and not bstack1l1l1l1lll_opy_):
      bstack1ll11lll_opy_()
  if (bstack1l1ll1l11l_opy_ in [bstack111l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧൠ"), bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൡ"), bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൢ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1l1ll11l_opy_
        bstack1llllllll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l111l11l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1llll1l11l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11lll1ll11_opy_ + str(e))
    except Exception as e:
      bstack1111111l1_opy_(e, bstack1l111l11l1_opy_)
    if bstack1l1ll1l11l_opy_ != bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൣ"):
      bstack11ll11lll_opy_()
    bstack1l11l1111_opy_ = Output.start_test
    bstack1l1111ll_opy_ = Output.end_test
    bstack1111ll11l_opy_ = TestStatus.__init__
    bstack1l1lll1111_opy_ = pabot._run
    bstack111111ll_opy_ = QueueItem.__init__
    bstack1l1111llll_opy_ = pabot._create_command_for_execution
    bstack1l111l1ll_opy_ = pabot._report_results
  if bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ൤"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111111l1_opy_(e, bstack11ll11l1l_opy_)
    bstack11l11ll1_opy_ = Runner.run_hook
    bstack1l111ll11l_opy_ = Step.run
  if bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൥"):
    try:
      from _pytest.config import Config
      bstack1llll11ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1lllll1lll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l11ll1l1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll11l1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ൦"))
  try:
    framework_name = bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൧") if bstack1l1ll1l11l_opy_ in [bstack111l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൨"), bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൩"), bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൪")] else bstack11l111lll1_opy_(bstack1l1ll1l11l_opy_)
    bstack1llllll1l1_opy_ = {
      bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭൫"): bstack111l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ൬") if bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൭") and bstack11l11l11_opy_() else framework_name,
      bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ൮"): bstack1ll1l11ll1_opy_(framework_name),
      bstack111l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ൯"): __version__,
      bstack111l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ൰"): bstack1l1ll1l11l_opy_
    }
    if bstack1l1ll1l11l_opy_ in bstack11llll1ll_opy_ + bstack1l1l1ll111_opy_:
      if bstack11lll1ll1_opy_.bstack1ll11l1l1l_opy_(CONFIG):
        if bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ൱") in CONFIG:
          os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭൲")] = os.getenv(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ൳"), json.dumps(CONFIG[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൴")]))
          CONFIG[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൵")].pop(bstack111l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ൶"), None)
          CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ൷")].pop(bstack111l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ൸"), None)
        bstack1llllll1l1_opy_[bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൹")] = {
          bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫൺ"): bstack111l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩൻ"),
          bstack111l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩർ"): str(bstack11l1lll1l_opy_())
        }
    if bstack1l1ll1l11l_opy_ not in [bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪൽ")] and not cli.is_running():
      bstack11l111ll1_opy_, bstack1llll1lll1_opy_ = bstack1l11l1l1ll_opy_.launch(CONFIG, bstack1llllll1l1_opy_)
      if bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪൾ")) is not None and bstack11lll1ll1_opy_.bstack1l1l111ll_opy_(CONFIG) is None:
        value = bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫൿ")].get(bstack111l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭඀"))
        if value is not None:
            CONFIG[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ඁ")] = value
        else:
          logger.debug(bstack111l11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧං"))
  except Exception as e:
    logger.debug(bstack1lll111l11_opy_.format(bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩඃ"), str(e)))
  if bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඄"):
    bstack11lll1l11_opy_ = True
    if bstack1l1l1l1lll_opy_ and bstack1ll1l11ll_opy_:
      bstack1l11l11111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧඅ"), {}).get(bstack111l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ආ"))
      bstack1l11111111_opy_(bstack1lll1l111_opy_)
    elif bstack1l1l1l1lll_opy_:
      bstack1l11l11111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩඇ"), {}).get(bstack111l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඈ"))
      global bstack11111l1l_opy_
      try:
        if bstack1l1ll11l1l_opy_(bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඉ")]) and multiprocessing.current_process().name == bstack111l11_opy_ (u"ࠨ࠲ࠪඊ"):
          bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඋ")].remove(bstack111l11_opy_ (u"ࠪ࠱ࡲ࠭ඌ"))
          bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඍ")].remove(bstack111l11_opy_ (u"ࠬࡶࡤࡣࠩඎ"))
          bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඏ")] = bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඐ")][0]
          with open(bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඑ")], bstack111l11_opy_ (u"ࠩࡵࠫඒ")) as f:
            bstack1ll1ll1l11_opy_ = f.read()
          bstack1l1l11llll_opy_ = bstack111l11_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨඓ").format(str(bstack1l1l1l1lll_opy_))
          bstack11ll11111_opy_ = bstack1l1l11llll_opy_ + bstack1ll1ll1l11_opy_
          bstack111lll11l_opy_ = bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඔ")] + bstack111l11_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧඕ")
          with open(bstack111lll11l_opy_, bstack111l11_opy_ (u"࠭ࡷࠨඖ")):
            pass
          with open(bstack111lll11l_opy_, bstack111l11_opy_ (u"ࠢࡸ࠭ࠥ඗")) as f:
            f.write(bstack11ll11111_opy_)
          import subprocess
          bstack11ll1ll11l_opy_ = subprocess.run([bstack111l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ඘"), bstack111lll11l_opy_])
          if os.path.exists(bstack111lll11l_opy_):
            os.unlink(bstack111lll11l_opy_)
          os._exit(bstack11ll1ll11l_opy_.returncode)
        else:
          if bstack1l1ll11l1l_opy_(bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඙")]):
            bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක")].remove(bstack111l11_opy_ (u"ࠫ࠲ࡳࠧඛ"))
            bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨග")].remove(bstack111l11_opy_ (u"࠭ࡰࡥࡤࠪඝ"))
            bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඞ")] = bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඟ")][0]
          bstack1l11111111_opy_(bstack1lll1l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬච")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111l11_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬඡ")] = bstack111l11_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ජ")
          mod_globals[bstack111l11_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧඣ")] = os.path.abspath(bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඤ")])
          exec(open(bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඥ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111l11_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨඦ").format(str(e)))
          for driver in bstack11111l1l_opy_:
            bstack1llll111l1_opy_.append({
              bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧට"): bstack1l1l1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඨ")],
              bstack111l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪඩ"): str(e),
              bstack111l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫඪ"): multiprocessing.current_process().name
            })
            bstack11ll11l11_opy_(driver, bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ණ"), bstack111l11_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥඬ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11111l1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll11ll11_opy_, CONFIG, logger)
      bstack11l11llll_opy_()
      bstack1ll1lll1l1_opy_()
      percy.bstack111l1111_opy_()
      bstack1111lll11_opy_ = {
        bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫත"): args[0],
        bstack111l11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩථ"): CONFIG,
        bstack111l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫද"): bstack1ll11l1l_opy_,
        bstack111l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ධ"): bstack1ll11ll11_opy_
      }
      if bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨන") in CONFIG:
        bstack11l111l11_opy_ = bstack1l111lll1_opy_(args, logger, CONFIG, bstack11ll1l1l11_opy_, bstack1l111l11_opy_)
        bstack1lll11ll_opy_ = bstack11l111l11_opy_.bstack1llll111ll_opy_(run_on_browserstack, bstack1111lll11_opy_, bstack1l1ll11l1l_opy_(args))
      else:
        if bstack1l1ll11l1l_opy_(args):
          bstack1111lll11_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ඲")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1111lll11_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11111111_opy_(bstack1lll1l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111l11_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩඳ")] = bstack111l11_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪප")
          mod_globals[bstack111l11_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫඵ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩබ") or bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪභ"):
    percy.init(bstack1ll11ll11_opy_, CONFIG, logger)
    percy.bstack111l1111_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1111111l1_opy_(e, bstack1l111l11l1_opy_)
    bstack11l11llll_opy_()
    bstack1l11111111_opy_(bstack1l1ll1l11_opy_)
    if bstack11ll1l1l11_opy_:
      bstack1l11l1l11_opy_(bstack1l1ll1l11_opy_, args)
      if bstack111l11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪම") in args:
        i = args.index(bstack111l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඹ"))
        args.pop(i)
        args.pop(i)
      if bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪය") not in CONFIG:
        CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫර")] = [{}]
        bstack1l111l11_opy_ = 1
      if bstack1ll1111l1l_opy_ == 0:
        bstack1ll1111l1l_opy_ = 1
      args.insert(0, str(bstack1ll1111l1l_opy_))
      args.insert(0, str(bstack111l11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ඼")))
    if bstack1l11l1l1ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l111ll1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1l1111l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111l11_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥල"),
        ).parse_args(bstack1l111ll1l_opy_)
        bstack1ll1l1ll11_opy_ = args.index(bstack1l111ll1l_opy_[0]) if len(bstack1l111ll1l_opy_) > 0 else len(args)
        args.insert(bstack1ll1l1ll11_opy_, str(bstack111l11_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ඾")))
        args.insert(bstack1ll1l1ll11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ඿"))))
        if bstack11ll11l11l_opy_.bstack1l1l1l111l_opy_(CONFIG):
          args.insert(bstack1ll1l1ll11_opy_, str(bstack111l11_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪව")))
          args.insert(bstack1ll1l1ll11_opy_ + 1, str(bstack111l11_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨශ").format(bstack11ll11l11l_opy_.bstack1111lll1l_opy_(CONFIG))))
        if bstack1l1llll1_opy_(os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ෂ"))) and str(os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ස"), bstack111l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨහ"))) != bstack111l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩළ"):
          for bstack1lll1l1l1l_opy_ in bstack1ll1l1111l_opy_:
            args.remove(bstack1lll1l1l1l_opy_)
          bstack1lll1lll1l_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩෆ")).split(bstack111l11_opy_ (u"࠭ࠬࠨ෇"))
          for bstack11ll111l_opy_ in bstack1lll1lll1l_opy_:
            args.append(bstack11ll111l_opy_)
      except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥ෈").format(e))
    pabot.main(args)
  elif bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෉"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1111111l1_opy_(e, bstack1l111l11l1_opy_)
    for a in args:
      if bstack111l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ්") in a:
        bstack1ll1111l1_opy_ = int(a.split(bstack111l11_opy_ (u"ࠪ࠾ࠬ෋"))[1])
      if bstack111l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ෌") in a:
        bstack1l11l11111_opy_ = str(a.split(bstack111l11_opy_ (u"ࠬࡀࠧ෍"))[1])
      if bstack111l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭෎") in a:
        bstack11ll1ll1l_opy_ = str(a.split(bstack111l11_opy_ (u"ࠧ࠻ࠩා"))[1])
    bstack1lllll11l1_opy_ = None
    if bstack111l11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧැ") in args:
      i = args.index(bstack111l11_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨෑ"))
      args.pop(i)
      bstack1lllll11l1_opy_ = args.pop(i)
    if bstack1lllll11l1_opy_ is not None:
      global bstack1l1l11l1ll_opy_
      bstack1l1l11l1ll_opy_ = bstack1lllll11l1_opy_
    bstack1l11111111_opy_(bstack1l1ll1l11_opy_)
    run_cli(args)
    if bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧි") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1llll111l1_opy_.append(bstack1ll1l1l1l1_opy_)
  elif bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫී"):
    bstack11lllll11_opy_ = bstack11l1lll11_opy_(args, logger, CONFIG, bstack11ll1l1l11_opy_)
    bstack11lllll11_opy_.bstack1l1l11l1_opy_()
    bstack11l11llll_opy_()
    bstack11l1lll1_opy_ = True
    bstack11ll1l1l_opy_ = bstack11lllll11_opy_.bstack1l1ll1111_opy_()
    bstack11lllll11_opy_.bstack1111lll11_opy_(bstack1ll1lllll_opy_)
    bstack1ll1l11l11_opy_ = bstack11lllll11_opy_.bstack1llll111ll_opy_(bstack1lll1ll11_opy_, {
      bstack111l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ු"): bstack1ll11l1l_opy_,
      bstack111l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ෕"): bstack1ll11ll11_opy_,
      bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪූ"): bstack11ll1l1l11_opy_
    })
    try:
      bstack1lll1ll111_opy_, bstack1ll1lll111_opy_ = map(list, zip(*bstack1ll1l11l11_opy_))
      bstack1l1l11ll11_opy_ = bstack1lll1ll111_opy_[0]
      for status_code in bstack1ll1lll111_opy_:
        if status_code != 0:
          bstack11ll1l111_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨ෗").format(str(e)))
  elif bstack1l1ll1l11l_opy_ == bstack111l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ"):
    try:
      from behave.__main__ import main as bstack11llll11ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1111111l1_opy_(e, bstack11ll11l1l_opy_)
    bstack11l11llll_opy_()
    bstack11l1lll1_opy_ = True
    bstack111lll1ll_opy_ = 1
    if bstack111l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪෙ") in CONFIG:
      bstack111lll1ll_opy_ = CONFIG[bstack111l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫේ")]
    if bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨෛ") in CONFIG:
      bstack1ll1l111l1_opy_ = int(bstack111lll1ll_opy_) * int(len(CONFIG[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩො")]))
    else:
      bstack1ll1l111l1_opy_ = int(bstack111lll1ll_opy_)
    config = Configuration(args)
    bstack1l11lll111_opy_ = config.paths
    if len(bstack1l11lll111_opy_) == 0:
      import glob
      pattern = bstack111l11_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ෝ")
      bstack1ll1ll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1ll11_opy_)
      config = Configuration(args)
      bstack1l11lll111_opy_ = config.paths
    bstack1ll1l11111_opy_ = [os.path.normpath(item) for item in bstack1l11lll111_opy_]
    bstack1lll111l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack11l1l11l1l_opy_ = [item for item in bstack1lll111l1l_opy_ if item not in bstack1ll1l11111_opy_]
    import platform as pf
    if pf.system().lower() == bstack111l11_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩෞ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l11111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1l1lll1_opy_)))
                    for bstack11l1l1lll1_opy_ in bstack1ll1l11111_opy_]
    bstack1l111l11l_opy_ = []
    for spec in bstack1ll1l11111_opy_:
      bstack1ll1ll1lll_opy_ = []
      bstack1ll1ll1lll_opy_ += bstack11l1l11l1l_opy_
      bstack1ll1ll1lll_opy_.append(spec)
      bstack1l111l11l_opy_.append(bstack1ll1ll1lll_opy_)
    execution_items = []
    for bstack1ll1ll1lll_opy_ in bstack1l111l11l_opy_:
      if bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෟ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෠")]):
          item = {}
          item[bstack111l11_opy_ (u"ࠫࡦࡸࡧࠨ෡")] = bstack111l11_opy_ (u"ࠬࠦࠧ෢").join(bstack1ll1ll1lll_opy_)
          item[bstack111l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෣")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111l11_opy_ (u"ࠧࡢࡴࡪࠫ෤")] = bstack111l11_opy_ (u"ࠨࠢࠪ෥").join(bstack1ll1ll1lll_opy_)
        item[bstack111l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ෦")] = 0
        execution_items.append(item)
    bstack1l111ll1ll_opy_ = bstack11ll1ll111_opy_(execution_items, bstack1ll1l111l1_opy_)
    for execution_item in bstack1l111ll1ll_opy_:
      bstack1lll1ll1ll_opy_ = []
      for item in execution_item:
        bstack1lll1ll1ll_opy_.append(bstack1ll11l11ll_opy_(name=str(item[bstack111l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෧")]),
                                             target=bstack1l1l1lllll_opy_,
                                             args=(item[bstack111l11_opy_ (u"ࠫࡦࡸࡧࠨ෨")],)))
      for t in bstack1lll1ll1ll_opy_:
        t.start()
      for t in bstack1lll1ll1ll_opy_:
        t.join()
  else:
    bstack1ll11ll1_opy_(bstack1l11llll1l_opy_)
  if not bstack1l1l1l1lll_opy_:
    bstack1l11lllll_opy_()
    if(bstack1l1ll1l11l_opy_ in [bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෩"), bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෪")]):
      bstack1lllll11_opy_()
  bstack1lll111lll_opy_.bstack1l1l1l1ll_opy_()
def browserstack_initialize(bstack11l1l1l1_opy_=None):
  logger.info(bstack111l11_opy_ (u"ࠧࡓࡷࡱࡲ࡮ࡴࡧࠡࡕࡇࡏࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡳ࠻ࠢࠪ෫") + str(bstack11l1l1l1_opy_))
  run_on_browserstack(bstack11l1l1l1_opy_, None, True)
@measure(event_name=EVENTS.bstack1ll111l11l_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1l11lllll_opy_():
  global CONFIG
  global bstack11lll11111_opy_
  global bstack11ll1l111_opy_
  global bstack1l11llllll_opy_
  global bstack111l111ll_opy_
  bstack1ll1l1llll_opy_.bstack1l11ll1l11_opy_()
  if cli.is_running():
    bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.bstack11ll1l1l1_opy_)
  if bstack11lll11111_opy_ == bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෬"):
    if not cli.is_enabled(CONFIG):
      bstack1l11l1l1ll_opy_.stop()
  else:
    bstack1l11l1l1ll_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1lllll1l1l_opy_.bstack111l1ll1l_opy_()
  if bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭෭") in CONFIG and str(CONFIG[bstack111l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ෮")]).lower() != bstack111l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ෯"):
    bstack11llll11_opy_, bstack1ll111l111_opy_ = bstack1l1l1lll1_opy_()
  else:
    bstack11llll11_opy_, bstack1ll111l111_opy_ = get_build_link()
  bstack11ll11l111_opy_(bstack11llll11_opy_)
  logger.info(bstack111l11_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭෰") + bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ෱"), bstack111l11_opy_ (u"ࠧࠨෲ")) + bstack111l11_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩෳ") + os.getenv(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ෴"), bstack111l11_opy_ (u"ࠪࠫ෵")))
  if bstack11llll11_opy_ is not None and bstack1lll1l111l_opy_() != -1:
    sessions = bstack1111l111_opy_(bstack11llll11_opy_)
    bstack1ll1llll1_opy_(sessions, bstack1ll111l111_opy_)
  if bstack11lll11111_opy_ == bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෶") and bstack11ll1l111_opy_ != 0:
    sys.exit(bstack11ll1l111_opy_)
  if bstack11lll11111_opy_ == bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෷") and bstack1l11llllll_opy_ != 0:
    sys.exit(bstack1l11llllll_opy_)
def bstack11ll11l111_opy_(new_id):
    global bstack1l1lll111l_opy_
    bstack1l1lll111l_opy_ = new_id
def bstack11l111lll1_opy_(bstack11111lll_opy_):
  if bstack11111lll_opy_:
    return bstack11111lll_opy_.capitalize()
  else:
    return bstack111l11_opy_ (u"࠭ࠧ෸")
@measure(event_name=EVENTS.bstack1llll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1l1lll1l1_opy_(bstack11l11l1lll_opy_):
  if bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෹") in bstack11l11l1lll_opy_ and bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭෺")] != bstack111l11_opy_ (u"ࠩࠪ෻"):
    return bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ෼")]
  else:
    bstack1llll1111l_opy_ = bstack111l11_opy_ (u"ࠦࠧ෽")
    if bstack111l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ෾") in bstack11l11l1lll_opy_ and bstack11l11l1lll_opy_[bstack111l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭෿")] != None:
      bstack1llll1111l_opy_ += bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ฀")] + bstack111l11_opy_ (u"ࠣ࠮ࠣࠦก")
      if bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠩࡲࡷࠬข")] == bstack111l11_opy_ (u"ࠥ࡭ࡴࡹࠢฃ"):
        bstack1llll1111l_opy_ += bstack111l11_opy_ (u"ࠦ࡮ࡕࡓࠡࠤค")
      bstack1llll1111l_opy_ += (bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩฅ")] or bstack111l11_opy_ (u"࠭ࠧฆ"))
      return bstack1llll1111l_opy_
    else:
      bstack1llll1111l_opy_ += bstack11l111lll1_opy_(bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨง")]) + bstack111l11_opy_ (u"ࠣࠢࠥจ") + (
              bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫฉ")] or bstack111l11_opy_ (u"ࠪࠫช")) + bstack111l11_opy_ (u"ࠦ࠱ࠦࠢซ")
      if bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠬࡵࡳࠨฌ")] == bstack111l11_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢญ"):
        bstack1llll1111l_opy_ += bstack111l11_opy_ (u"ࠢࡘ࡫ࡱࠤࠧฎ")
      bstack1llll1111l_opy_ += bstack11l11l1lll_opy_[bstack111l11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬฏ")] or bstack111l11_opy_ (u"ࠩࠪฐ")
      return bstack1llll1111l_opy_
@measure(event_name=EVENTS.bstack11111l111_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11llll1lll_opy_(bstack1l11ll1l1_opy_):
  if bstack1l11ll1l1_opy_ == bstack111l11_opy_ (u"ࠥࡨࡴࡴࡥࠣฑ"):
    return bstack111l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧฒ")
  elif bstack1l11ll1l1_opy_ == bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧณ"):
    return bstack111l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩด")
  elif bstack1l11ll1l1_opy_ == bstack111l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢต"):
    return bstack111l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨถ")
  elif bstack1l11ll1l1_opy_ == bstack111l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣท"):
    return bstack111l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬธ")
  elif bstack1l11ll1l1_opy_ == bstack111l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧน"):
    return bstack111l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪบ")
  elif bstack1l11ll1l1_opy_ == bstack111l11_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢป"):
    return bstack111l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨผ")
  else:
    return bstack111l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬฝ") + bstack11l111lll1_opy_(
      bstack1l11ll1l1_opy_) + bstack111l11_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨพ")
def bstack11lllll1ll_opy_(session):
  return bstack111l11_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪฟ").format(
    session[bstack111l11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨภ")], bstack1l1lll1l1_opy_(session), bstack11llll1lll_opy_(session[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫม")]),
    bstack11llll1lll_opy_(session[bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ย")]),
    bstack11l111lll1_opy_(session[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨร")] or session[bstack111l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨฤ")] or bstack111l11_opy_ (u"ࠩࠪล")) + bstack111l11_opy_ (u"ࠥࠤࠧฦ") + (session[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ว")] or bstack111l11_opy_ (u"ࠬ࠭ศ")),
    session[bstack111l11_opy_ (u"࠭࡯ࡴࠩษ")] + bstack111l11_opy_ (u"ࠢࠡࠤส") + session[bstack111l11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬห")], session[bstack111l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫฬ")] or bstack111l11_opy_ (u"ࠪࠫอ"),
    session[bstack111l11_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨฮ")] if session[bstack111l11_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩฯ")] else bstack111l11_opy_ (u"࠭ࠧะ"))
@measure(event_name=EVENTS.bstack1ll11l11_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll1llll1_opy_(sessions, bstack1ll111l111_opy_):
  try:
    bstack1ll1l1l1_opy_ = bstack111l11_opy_ (u"ࠢࠣั")
    if not os.path.exists(bstack1l11l1l1l_opy_):
      os.mkdir(bstack1l11l1l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l11_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭า")), bstack111l11_opy_ (u"ࠩࡵࠫำ")) as f:
      bstack1ll1l1l1_opy_ = f.read()
    bstack1ll1l1l1_opy_ = bstack1ll1l1l1_opy_.replace(bstack111l11_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧิ"), str(len(sessions)))
    bstack1ll1l1l1_opy_ = bstack1ll1l1l1_opy_.replace(bstack111l11_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫี"), bstack1ll111l111_opy_)
    bstack1ll1l1l1_opy_ = bstack1ll1l1l1_opy_.replace(bstack111l11_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ึ"),
                                              sessions[0].get(bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪื")) if sessions[0] else bstack111l11_opy_ (u"ࠧࠨุ"))
    with open(os.path.join(bstack1l11l1l1l_opy_, bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰูࠬ")), bstack111l11_opy_ (u"ࠩࡺฺࠫ")) as stream:
      stream.write(bstack1ll1l1l1_opy_.split(bstack111l11_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ฻"))[0])
      for session in sessions:
        stream.write(bstack11lllll1ll_opy_(session))
      stream.write(bstack1ll1l1l1_opy_.split(bstack111l11_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ฼"))[1])
    logger.info(bstack111l11_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ฽").format(bstack1l11l1l1l_opy_));
  except Exception as e:
    logger.debug(bstack1l111lll11_opy_.format(str(e)))
def bstack1111l111_opy_(bstack11llll11_opy_):
  global CONFIG
  try:
    bstack111l1l111_opy_ = datetime.datetime.now()
    host = bstack111l11_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ฾") if bstack111l11_opy_ (u"ࠧࡢࡲࡳࠫ฿") in CONFIG else bstack111l11_opy_ (u"ࠨࡣࡳ࡭ࠬเ")
    user = CONFIG[bstack111l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫแ")]
    key = CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭โ")]
    bstack1l1llll1l1_opy_ = bstack111l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪใ") if bstack111l11_opy_ (u"ࠬࡧࡰࡱࠩไ") in CONFIG else (bstack111l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪๅ") if CONFIG.get(bstack111l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫๆ")) else bstack111l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ็"))
    url = bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴ่ࠧ").format(user, key, host, bstack1l1llll1l1_opy_,
                                                                                bstack11llll11_opy_)
    headers = {
      bstack111l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦ้ࠩ"): bstack111l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴ๊ࠧ"),
    }
    proxies = bstack1l1l11ll1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࡡ࡯࡭ࡸࡺ๋ࠢ"), datetime.datetime.now() - bstack111l1l111_opy_)
      return list(map(lambda session: session[bstack111l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ์")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l111111_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11ll1l11l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def get_build_link():
  global CONFIG
  global bstack1l1lll111l_opy_
  try:
    if bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪํ") in CONFIG:
      bstack111l1l111_opy_ = datetime.datetime.now()
      host = bstack111l11_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ๎") if bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭๏") in CONFIG else bstack111l11_opy_ (u"ࠪࡥࡵ࡯ࠧ๐")
      user = CONFIG[bstack111l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭๑")]
      key = CONFIG[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ๒")]
      bstack1l1llll1l1_opy_ = bstack111l11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ๓") if bstack111l11_opy_ (u"ࠧࡢࡲࡳࠫ๔") in CONFIG else bstack111l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ๕")
      url = bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ๖").format(user, key, host, bstack1l1llll1l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1ll111l111_opy_, bstack11llll11_opy_ = cli.bstack1111l1111_opy_()
        logger.info(bstack11ll111l1l_opy_.format(bstack1ll111l111_opy_))
        return [bstack11llll11_opy_, bstack1ll111l111_opy_]
      else:
        headers = {
          bstack111l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ๗"): bstack111l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ๘"),
        }
        if bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๙") in CONFIG:
          params = {bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๚"): CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๛")], bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๜"): CONFIG[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๝")]}
        else:
          params = {bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ๞"): CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๟")]}
        proxies = bstack1l1l11ll1l_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1ll11lll1l_opy_ = response.json()[0][bstack111l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ๠")]
          if bstack1ll11lll1l_opy_:
            bstack1ll111l111_opy_ = bstack1ll11lll1l_opy_[bstack111l11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ๡")].split(bstack111l11_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭๢"))[0] + bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ๣") + bstack1ll11lll1l_opy_[
              bstack111l11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๤")]
            logger.info(bstack11ll111l1l_opy_.format(bstack1ll111l111_opy_))
            bstack1l1lll111l_opy_ = bstack1ll11lll1l_opy_[bstack111l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭๥")]
            bstack1l11l1111l_opy_ = CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๦")]
            if bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๧") in CONFIG:
              bstack1l11l1111l_opy_ += bstack111l11_opy_ (u"࠭ࠠࠨ๨") + CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๩")]
            if bstack1l11l1111l_opy_ != bstack1ll11lll1l_opy_[bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭๪")]:
              logger.debug(bstack1l111ll1_opy_.format(bstack1ll11lll1l_opy_[bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๫")], bstack1l11l1111l_opy_))
            cli.bstack1l1ll111l1_opy_(bstack111l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡨࡵࡪ࡮ࡧࡣࡱ࡯࡮࡬ࠤ๬"), datetime.datetime.now() - bstack111l1l111_opy_)
            return [bstack1ll11lll1l_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ๭")], bstack1ll111l111_opy_]
    else:
      logger.warn(bstack11ll1l11_opy_)
  except Exception as e:
    logger.debug(bstack1l1l11l11l_opy_.format(str(e)))
  return [None, None]
def bstack11111ll1l_opy_(url, bstack1ll1111ll1_opy_=False):
  global CONFIG
  global bstack1l1111l111_opy_
  if not bstack1l1111l111_opy_:
    hostname = bstack1l1111ll1_opy_(url)
    is_private = bstack11ll11ll1_opy_(hostname)
    if (bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ๮") in CONFIG and not bstack1l1llll1_opy_(CONFIG[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ๯")])) and (is_private or bstack1ll1111ll1_opy_):
      bstack1l1111l111_opy_ = hostname
def bstack1l1111ll1_opy_(url):
  return urlparse(url).hostname
def bstack11ll11ll1_opy_(hostname):
  for bstack11ll111ll_opy_ in bstack1llll1l1ll_opy_:
    regex = re.compile(bstack11ll111ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111l111l1_opy_(bstack11111l1ll_opy_):
  return True if bstack11111l1ll_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll11111l_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll1111l1_opy_
  bstack1l1l1llll_opy_ = not (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ๰"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ๱"), None))
  bstack11lll111_opy_ = getattr(driver, bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ๲"), None) != True
  bstack111111lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ๳"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭๴"), None)
  if bstack111111lll_opy_:
    if not bstack1l11l1ll1_opy_():
      logger.warning(bstack111l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ๵"))
      return {}
    logger.debug(bstack111l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ๶"))
    logger.debug(perform_scan(driver, driver_command=bstack111l11_opy_ (u"ࠧࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠧ๷")))
    results = bstack1l11llll11_opy_(bstack111l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤ๸"))
    if results is not None and results.get(bstack111l11_opy_ (u"ࠤ࡬ࡷࡸࡻࡥࡴࠤ๹")) is not None:
        return results[bstack111l11_opy_ (u"ࠥ࡭ࡸࡹࡵࡦࡵࠥ๺")]
    logger.error(bstack111l11_opy_ (u"ࠦࡓࡵࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ๻"))
    return []
  if not bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1ll1111l1_opy_) or (bstack11lll111_opy_ and bstack1l1l1llll_opy_):
    logger.warning(bstack111l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ๼"))
    return {}
  try:
    logger.debug(bstack111l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ๽"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11111ll1_opy_.bstack1111l11ll_opy_)
    return results
  except Exception:
    logger.error(bstack111l11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ๾"))
    return {}
@measure(event_name=EVENTS.bstack11ll1ll1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll1111l1_opy_
  bstack1l1l1llll_opy_ = not (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ๿"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ຀"), None))
  bstack11lll111_opy_ = getattr(driver, bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪກ"), None) != True
  bstack111111lll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຂ"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ຃"), None)
  if bstack111111lll_opy_:
    if not bstack1l11l1ll1_opy_():
      logger.warning(bstack111l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦຄ"))
      return {}
    logger.debug(bstack111l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ຅"))
    logger.debug(perform_scan(driver, driver_command=bstack111l11_opy_ (u"ࠨࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠨຆ")))
    results = bstack1l11llll11_opy_(bstack111l11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤງ"))
    if results is not None and results.get(bstack111l11_opy_ (u"ࠥࡷࡺࡳ࡭ࡢࡴࡼࠦຈ")) is not None:
        return results[bstack111l11_opy_ (u"ࠦࡸࡻ࡭࡮ࡣࡵࡽࠧຉ")]
    logger.error(bstack111l11_opy_ (u"ࠧࡔ࡯ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠢࡖࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢຊ"))
    return {}
  if not bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1ll1111l1_opy_) or (bstack11lll111_opy_ and bstack1l1l1llll_opy_):
    logger.warning(bstack111l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥ຋"))
    return {}
  try:
    logger.debug(bstack111l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬຌ"))
    logger.debug(perform_scan(driver))
    bstack1llllll11l_opy_ = driver.execute_async_script(bstack11111ll1_opy_.bstack1l1ll1l1l_opy_)
    return bstack1llllll11l_opy_
  except Exception:
    logger.error(bstack111l11_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤຍ"))
    return {}
def bstack1l11l1ll1_opy_():
  global CONFIG
  global bstack1ll1111l1_opy_
  bstack1lll1l11l_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩຎ"), None) and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຏ"), None)
  if not bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1ll1111l1_opy_) or not bstack1lll1l11l_opy_:
        logger.warning(bstack111l11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦຐ"))
        return False
  return True
def bstack1l11llll11_opy_(bstack1l1l1l1l_opy_):
    bstack111l1l1l_opy_ = bstack1l11l1l1ll_opy_.current_test_uuid() if bstack1l11l1l1ll_opy_.current_test_uuid() else bstack1lllll1l1l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1ll1111ll_opy_(bstack111l1l1l_opy_, bstack1l1l1l1l_opy_))
        try:
            return future.result(timeout=bstack1l11ll11_opy_)
        except TimeoutError:
            logger.error(bstack111l11_opy_ (u"࡚ࠧࡩ࡮ࡧࡲࡹࡹࠦࡡࡧࡶࡨࡶࠥࢁࡽࡴࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠦຑ").format(bstack1l11ll11_opy_))
        except Exception as ex:
            logger.debug(bstack111l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡸࡥࡵࡴ࡬ࡩࡻ࡯࡮ࡨࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࡽࢀࠦຒ").format(bstack1l1l1l1l_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l11ll1ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1ll1111l1_opy_
  bstack1l1l1llll_opy_ = not (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫຓ"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧດ"), None))
  bstack11ll1l1ll1_opy_ = not (bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩຕ"), None) and bstack1l1lllll1l_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຖ"), None))
  bstack11lll111_opy_ = getattr(driver, bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫທ"), None) != True
  if not bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1ll1111l1_opy_) or (bstack11lll111_opy_ and bstack1l1l1llll_opy_ and bstack11ll1l1ll1_opy_):
    logger.warning(bstack111l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢຘ"))
    return {}
  try:
    bstack1l1ll111_opy_ = bstack111l11_opy_ (u"࠭ࡡࡱࡲࠪນ") in CONFIG and CONFIG.get(bstack111l11_opy_ (u"ࠧࡢࡲࡳࠫບ"), bstack111l11_opy_ (u"ࠨࠩປ"))
    session_id = getattr(driver, bstack111l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ຜ"), None)
    if not session_id:
      logger.warning(bstack111l11_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡤࡳ࡫ࡹࡩࡷࠨຝ"))
      return {bstack111l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥພ"): bstack111l11_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠦຟ")}
    if bstack1l1ll111_opy_:
      try:
        bstack11lll1ll_opy_ = {
              bstack111l11_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪຠ"): os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬມ"), os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬຢ"), bstack111l11_opy_ (u"ࠩࠪຣ"))),
              bstack111l11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪ຤"): bstack1l11l1l1ll_opy_.current_test_uuid() if bstack1l11l1l1ll_opy_.current_test_uuid() else bstack1lllll1l1l_opy_.current_hook_uuid(),
              bstack111l11_opy_ (u"ࠫࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠨລ"): os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ຦")),
              bstack111l11_opy_ (u"࠭ࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ວ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack111l11_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬຨ"): os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ຩ"), bstack111l11_opy_ (u"ࠩࠪສ")),
              bstack111l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪຫ"): kwargs.get(bstack111l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬຬ"), None) or bstack111l11_opy_ (u"ࠬ࠭ອ")
          }
        if not hasattr(thread_local, bstack111l11_opy_ (u"࠭ࡢࡢࡵࡨࡣࡦࡶࡰࡠࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹ࠭ຮ")):
            scripts = {bstack111l11_opy_ (u"ࠧࡴࡥࡤࡲࠬຯ"): bstack11111ll1_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1lll1l1lll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1lll1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ະ")] = bstack1lll1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡶࡧࡦࡴࠧັ")] % json.dumps(bstack11lll1ll_opy_)
        bstack11111ll1_opy_.bstack1l11ll111l_opy_(bstack1lll1l1lll_opy_)
        bstack11111ll1_opy_.store()
        bstack1l1l11l1l1_opy_ = driver.execute_script(bstack11111ll1_opy_.perform_scan)
      except Exception as bstack111111ll1_opy_:
        logger.info(bstack111l11_opy_ (u"ࠥࡅࡵࡶࡩࡶ࡯ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠥາ") + str(bstack111111ll1_opy_))
        bstack1l1l11l1l1_opy_ = {bstack111l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥຳ"): str(bstack111111ll1_opy_)}
    else:
      bstack1l1l11l1l1_opy_ = driver.execute_async_script(bstack11111ll1_opy_.perform_scan, {bstack111l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬິ"): kwargs.get(bstack111l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧີ"), None) or bstack111l11_opy_ (u"ࠧࠨຶ")})
    return bstack1l1l11l1l1_opy_
  except Exception as err:
    logger.error(bstack111l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠠࡼࡿࠥື").format(str(err)))
    return {}