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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll111llll_opy_, bstack11ll11ll1ll_opy_
import tempfile
import json
bstack11l11111l1l_opy_ = os.getenv(bstack111l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᲔ"), None) or os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᲕ"))
bstack11l1111l111_opy_ = os.path.join(bstack111l11_opy_ (u"ࠥࡰࡴ࡭ࠢᲖ"), bstack111l11_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᲗ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111l11_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᲘ"),
      datefmt=bstack111l11_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᲙ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1111111_opy_():
  bstack111lllll1l1_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᲚ"), bstack111l11_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᲛ"))
  return logging.DEBUG if bstack111lllll1l1_opy_.lower() == bstack111l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᲜ") else logging.INFO
def bstack1l1lllll1ll_opy_():
  global bstack11l11111l1l_opy_
  if os.path.exists(bstack11l11111l1l_opy_):
    os.remove(bstack11l11111l1l_opy_)
  if os.path.exists(bstack11l1111l111_opy_):
    os.remove(bstack11l1111l111_opy_)
def bstack1l1l1l1ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack111ll1l1l_opy_(config, log_level):
  bstack111llllll1l_opy_ = log_level
  if bstack111l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᲝ") in config and config[bstack111l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭Პ")] in bstack11ll111llll_opy_:
    bstack111llllll1l_opy_ = bstack11ll111llll_opy_[config[bstack111l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᲟ")]]
  if config.get(bstack111l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᲠ"), False):
    logging.getLogger().setLevel(bstack111llllll1l_opy_)
    return bstack111llllll1l_opy_
  global bstack11l11111l1l_opy_
  bstack1l1l1l1ll_opy_()
  bstack111llll1lll_opy_ = logging.Formatter(
    fmt=bstack111l11_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᲡ"),
    datefmt=bstack111l11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭Ტ"),
  )
  bstack111lllll11l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l11111l1l_opy_)
  file_handler.setFormatter(bstack111llll1lll_opy_)
  bstack111lllll11l_opy_.setFormatter(bstack111llll1lll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111lllll11l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᲣ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111lllll11l_opy_.setLevel(bstack111llllll1l_opy_)
  logging.getLogger().addHandler(bstack111lllll11l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111llllll1l_opy_
def bstack111llllll11_opy_(config):
  try:
    bstack111llll1l11_opy_ = set(bstack11ll11ll1ll_opy_)
    bstack11l1111111l_opy_ = bstack111l11_opy_ (u"ࠪࠫᲤ")
    with open(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᲥ")) as bstack11l1111l11l_opy_:
      bstack11l11111l11_opy_ = bstack11l1111l11l_opy_.read()
      bstack11l1111111l_opy_ = re.sub(bstack111l11_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭Ღ"), bstack111l11_opy_ (u"࠭ࠧᲧ"), bstack11l11111l11_opy_, flags=re.M)
      bstack11l1111111l_opy_ = re.sub(
        bstack111l11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᲨ") + bstack111l11_opy_ (u"ࠨࡾࠪᲩ").join(bstack111llll1l11_opy_) + bstack111l11_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᲪ"),
        bstack111l11_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᲫ"),
        bstack11l1111111l_opy_, flags=re.M | re.I
      )
    def bstack111llll1l1l_opy_(dic):
      bstack11l111111ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack111llll1l11_opy_:
          bstack11l111111ll_opy_[key] = bstack111l11_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᲬ")
        else:
          if isinstance(value, dict):
            bstack11l111111ll_opy_[key] = bstack111llll1l1l_opy_(value)
          else:
            bstack11l111111ll_opy_[key] = value
      return bstack11l111111ll_opy_
    bstack11l111111ll_opy_ = bstack111llll1l1l_opy_(config)
    return {
      bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᲭ"): bstack11l1111111l_opy_,
      bstack111l11_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᲮ"): json.dumps(bstack11l111111ll_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11111ll1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack111l11_opy_ (u"ࠧ࡭ࡱࡪࠫᲯ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l111111l1_opy_ = os.path.join(log_dir, bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩᲰ"))
  if not os.path.exists(bstack11l111111l1_opy_):
    bstack111llll1ll1_opy_ = {
      bstack111l11_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥᲱ"): str(inipath),
      bstack111l11_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧᲲ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᲳ")), bstack111l11_opy_ (u"ࠬࡽࠧᲴ")) as bstack11l11111lll_opy_:
      bstack11l11111lll_opy_.write(json.dumps(bstack111llll1ll1_opy_))
def bstack11l11111111_opy_():
  try:
    bstack11l111111l1_opy_ = os.path.join(os.getcwd(), bstack111l11_opy_ (u"࠭࡬ࡰࡩࠪᲵ"), bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭Ჶ"))
    if os.path.exists(bstack11l111111l1_opy_):
      with open(bstack11l111111l1_opy_, bstack111l11_opy_ (u"ࠨࡴࠪᲷ")) as bstack11l11111lll_opy_:
        bstack111llllllll_opy_ = json.load(bstack11l11111lll_opy_)
      return bstack111llllllll_opy_.get(bstack111l11_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪᲸ"), bstack111l11_opy_ (u"ࠪࠫᲹ")), bstack111llllllll_opy_.get(bstack111l11_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭Ჺ"), bstack111l11_opy_ (u"ࠬ࠭᲻"))
  except:
    pass
  return None, None
def bstack111lllll111_opy_():
  try:
    bstack11l111111l1_opy_ = os.path.join(os.getcwd(), bstack111l11_opy_ (u"࠭࡬ࡰࡩࠪ᲼"), bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭Ჽ"))
    if os.path.exists(bstack11l111111l1_opy_):
      os.remove(bstack11l111111l1_opy_)
  except:
    pass
def bstack1ll1llll_opy_(config):
  from bstack_utils.helper import bstack111l111ll_opy_
  global bstack11l11111l1l_opy_
  try:
    if config.get(bstack111l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᲾ"), False):
      return
    uuid = os.getenv(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᲿ")) if os.getenv(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᳀")) else bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ᳁"))
    if not uuid or uuid == bstack111l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᳂"):
      return
    bstack111lllll1ll_opy_ = [bstack111l11_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩ᳃"), bstack111l11_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨ᳄"), bstack111l11_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩ᳅"), bstack11l11111l1l_opy_, bstack11l1111l111_opy_]
    bstack111llll11ll_opy_, root_path = bstack11l11111111_opy_()
    if bstack111llll11ll_opy_ != None:
      bstack111lllll1ll_opy_.append(bstack111llll11ll_opy_)
    if root_path != None:
      bstack111lllll1ll_opy_.append(os.path.join(root_path, bstack111l11_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧ᳆")))
    bstack1l1l1l1ll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩ᳇") + uuid + bstack111l11_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬ᳈"))
    with tarfile.open(output_file, bstack111l11_opy_ (u"ࠧࡽ࠺ࡨࡼࠥ᳉")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111lllll1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111llllll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111lllllll1_opy_ = data.encode()
        tarinfo.size = len(bstack111lllllll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111lllllll1_opy_))
    bstack11l1llll11_opy_ = MultipartEncoder(
      fields= {
        bstack111l11_opy_ (u"࠭ࡤࡢࡶࡤࠫ᳊"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111l11_opy_ (u"ࠧࡳࡤࠪ᳋")), bstack111l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭᳌")),
        bstack111l11_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᳍"): uuid
      }
    )
    response = requests.post(
      bstack111l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧ᳎"),
      data=bstack11l1llll11_opy_,
      headers={bstack111l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ᳏"): bstack11l1llll11_opy_.content_type},
      auth=(config[bstack111l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᳐")], config[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᳑")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭᳒") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧ᳓") + str(e))
  finally:
    try:
      bstack1l1lllll1ll_opy_()
      bstack111lllll111_opy_()
    except:
      pass