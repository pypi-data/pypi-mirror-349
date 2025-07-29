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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1l11l1l_opy_, bstack11ll11l111l_opy_
import tempfile
import json
bstack11l11111ll1_opy_ = os.getenv(bstack11l1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧᲉ"), None) or os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢᲊ"))
bstack111llllllll_opy_ = os.path.join(bstack11l1lll_opy_ (u"ࠨ࡬ࡰࡩࠥ᲋"), bstack11l1lll_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫ᲌"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l1lll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ᲍"),
      datefmt=bstack11l1lll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ᲎"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll11ll1_opy_():
  bstack111llll1ll1_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ᲏"), bstack11l1lll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᲐ"))
  return logging.DEBUG if bstack111llll1ll1_opy_.lower() == bstack11l1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥᲑ") else logging.INFO
def bstack1ll11111l11_opy_():
  global bstack11l11111ll1_opy_
  if os.path.exists(bstack11l11111ll1_opy_):
    os.remove(bstack11l11111ll1_opy_)
  if os.path.exists(bstack111llllllll_opy_):
    os.remove(bstack111llllllll_opy_)
def bstack1ll1l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1lllll1l11_opy_(config, log_level):
  bstack11l111111ll_opy_ = log_level
  if bstack11l1lll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᲒ") in config and config[bstack11l1lll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᲓ")] in bstack11ll1l11l1l_opy_:
    bstack11l111111ll_opy_ = bstack11ll1l11l1l_opy_[config[bstack11l1lll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᲔ")]]
  if config.get(bstack11l1lll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᲕ"), False):
    logging.getLogger().setLevel(bstack11l111111ll_opy_)
    return bstack11l111111ll_opy_
  global bstack11l11111ll1_opy_
  bstack1ll1l111l_opy_()
  bstack111lllll1l1_opy_ = logging.Formatter(
    fmt=bstack11l1lll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭Ზ"),
    datefmt=bstack11l1lll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩᲗ"),
  )
  bstack111lllll11l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l11111ll1_opy_)
  file_handler.setFormatter(bstack111lllll1l1_opy_)
  bstack111lllll11l_opy_.setFormatter(bstack111lllll1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111lllll11l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l1lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧᲘ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111lllll11l_opy_.setLevel(bstack11l111111ll_opy_)
  logging.getLogger().addHandler(bstack111lllll11l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111111ll_opy_
def bstack11l1111l1l1_opy_(config):
  try:
    bstack111lllll111_opy_ = set(bstack11ll11l111l_opy_)
    bstack11l11111111_opy_ = bstack11l1lll_opy_ (u"࠭ࠧᲙ")
    with open(bstack11l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᲚ")) as bstack111llllll11_opy_:
      bstack111llllll1l_opy_ = bstack111llllll11_opy_.read()
      bstack11l11111111_opy_ = re.sub(bstack11l1lll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᲛ"), bstack11l1lll_opy_ (u"ࠩࠪᲜ"), bstack111llllll1l_opy_, flags=re.M)
      bstack11l11111111_opy_ = re.sub(
        bstack11l1lll_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭Ო") + bstack11l1lll_opy_ (u"ࠫࢁ࠭Პ").join(bstack111lllll111_opy_) + bstack11l1lll_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᲟ"),
        bstack11l1lll_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᲠ"),
        bstack11l11111111_opy_, flags=re.M | re.I
      )
    def bstack111lllllll1_opy_(dic):
      bstack11l11111l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111lllll111_opy_:
          bstack11l11111l1l_opy_[key] = bstack11l1lll_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᲡ")
        else:
          if isinstance(value, dict):
            bstack11l11111l1l_opy_[key] = bstack111lllllll1_opy_(value)
          else:
            bstack11l11111l1l_opy_[key] = value
      return bstack11l11111l1l_opy_
    bstack11l11111l1l_opy_ = bstack111lllllll1_opy_(config)
    return {
      bstack11l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᲢ"): bstack11l11111111_opy_,
      bstack11l1lll_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᲣ"): json.dumps(bstack11l11111l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack11l1111l111_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11l1lll_opy_ (u"ࠪࡰࡴ࡭ࠧᲤ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l1111l11l_opy_ = os.path.join(log_dir, bstack11l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬᲥ"))
  if not os.path.exists(bstack11l1111l11l_opy_):
    bstack11l111111l1_opy_ = {
      bstack11l1lll_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨᲦ"): str(inipath),
      bstack11l1lll_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣᲧ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭Შ")), bstack11l1lll_opy_ (u"ࠨࡹࠪᲩ")) as bstack11l1111l1ll_opy_:
      bstack11l1111l1ll_opy_.write(json.dumps(bstack11l111111l1_opy_))
def bstack11l1111111l_opy_():
  try:
    bstack11l1111l11l_opy_ = os.path.join(os.getcwd(), bstack11l1lll_opy_ (u"ࠩ࡯ࡳ࡬࠭Ც"), bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᲫ"))
    if os.path.exists(bstack11l1111l11l_opy_):
      with open(bstack11l1111l11l_opy_, bstack11l1lll_opy_ (u"ࠫࡷ࠭Წ")) as bstack11l1111l1ll_opy_:
        bstack111lllll1ll_opy_ = json.load(bstack11l1111l1ll_opy_)
      return bstack111lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭Ჭ"), bstack11l1lll_opy_ (u"࠭ࠧᲮ")), bstack111lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩᲯ"), bstack11l1lll_opy_ (u"ࠨࠩᲰ"))
  except:
    pass
  return None, None
def bstack111llll1l1l_opy_():
  try:
    bstack11l1111l11l_opy_ = os.path.join(os.getcwd(), bstack11l1lll_opy_ (u"ࠩ࡯ࡳ࡬࠭Ჱ"), bstack11l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᲲ"))
    if os.path.exists(bstack11l1111l11l_opy_):
      os.remove(bstack11l1111l11l_opy_)
  except:
    pass
def bstack1ll1l1lll_opy_(config):
  from bstack_utils.helper import bstack11ll1llll1_opy_
  global bstack11l11111ll1_opy_
  try:
    if config.get(bstack11l1lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭Ჳ"), False):
      return
    uuid = os.getenv(bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᲴ")) if os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᲵ")) else bstack11ll1llll1_opy_.get_property(bstack11l1lll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤᲶ"))
    if not uuid or uuid == bstack11l1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ჷ"):
      return
    bstack111llll1lll_opy_ = [bstack11l1lll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᲸ"), bstack11l1lll_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᲹ"), bstack11l1lll_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᲺ"), bstack11l11111ll1_opy_, bstack111llllllll_opy_]
    bstack11l11111l11_opy_, root_path = bstack11l1111111l_opy_()
    if bstack11l11111l11_opy_ != None:
      bstack111llll1lll_opy_.append(bstack11l11111l11_opy_)
    if root_path != None:
      bstack111llll1lll_opy_.append(os.path.join(root_path, bstack11l1lll_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪ᲻")))
    bstack1ll1l111l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬ᲼") + uuid + bstack11l1lll_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᲽ"))
    with tarfile.open(output_file, bstack11l1lll_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᲾ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111llll1lll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l1111l1l1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l11111lll_opy_ = data.encode()
        tarinfo.size = len(bstack11l11111lll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l11111lll_opy_))
    bstack111lll1l1_opy_ = MultipartEncoder(
      fields= {
        bstack11l1lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᲿ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l1lll_opy_ (u"ࠪࡶࡧ࠭᳀")), bstack11l1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩ᳁")),
        bstack11l1lll_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᳂"): uuid
      }
    )
    response = requests.post(
      bstack11l1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣ᳃"),
      data=bstack111lll1l1_opy_,
      headers={bstack11l1lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭᳄"): bstack111lll1l1_opy_.content_type},
      auth=(config[bstack11l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᳅")], config[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᳆")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l1lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩ᳇") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l1lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪ᳈") + str(e))
  finally:
    try:
      bstack1ll11111l11_opy_()
      bstack111llll1l1l_opy_()
    except:
      pass