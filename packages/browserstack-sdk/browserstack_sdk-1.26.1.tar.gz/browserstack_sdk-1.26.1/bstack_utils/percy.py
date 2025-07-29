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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll1ll11_opy_, bstack11lll1lll_opy_
from bstack_utils.measure import measure
class bstack1l11l1ll11_opy_:
  working_dir = os.getcwd()
  bstack11ll1l11ll_opy_ = False
  config = {}
  bstack11l1ll1l1ll_opy_ = bstack11l1lll_opy_ (u"࠭ࠧᴞ")
  binary_path = bstack11l1lll_opy_ (u"ࠧࠨᴟ")
  bstack111lll11111_opy_ = bstack11l1lll_opy_ (u"ࠨࠩᴠ")
  bstack1l11l1111l_opy_ = False
  bstack111l1llll1l_opy_ = None
  bstack111l1llll11_opy_ = {}
  bstack111l1ll1l11_opy_ = 300
  bstack111ll111lll_opy_ = False
  logger = None
  bstack111l1ll1lll_opy_ = False
  bstack1lll1l1lll_opy_ = False
  percy_build_id = None
  bstack111ll1l11ll_opy_ = bstack11l1lll_opy_ (u"ࠩࠪᴡ")
  bstack111lll1l111_opy_ = {
    bstack11l1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᴢ") : 1,
    bstack11l1lll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᴣ") : 2,
    bstack11l1lll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᴤ") : 3,
    bstack11l1lll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ᴥ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll111111_opy_(self):
    bstack111ll1l1ll1_opy_ = bstack11l1lll_opy_ (u"ࠧࠨᴦ")
    bstack111ll11l1ll_opy_ = sys.platform
    bstack111l1lll1ll_opy_ = bstack11l1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᴧ")
    if re.match(bstack11l1lll_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤᴨ"), bstack111ll11l1ll_opy_) != None:
      bstack111ll1l1ll1_opy_ = bstack11ll11l1l1l_opy_ + bstack11l1lll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦᴩ")
      self.bstack111ll1l11ll_opy_ = bstack11l1lll_opy_ (u"ࠫࡲࡧࡣࠨᴪ")
    elif re.match(bstack11l1lll_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥᴫ"), bstack111ll11l1ll_opy_) != None:
      bstack111ll1l1ll1_opy_ = bstack11ll11l1l1l_opy_ + bstack11l1lll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢᴬ")
      bstack111l1lll1ll_opy_ = bstack11l1lll_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥᴭ")
      self.bstack111ll1l11ll_opy_ = bstack11l1lll_opy_ (u"ࠨࡹ࡬ࡲࠬᴮ")
    else:
      bstack111ll1l1ll1_opy_ = bstack11ll11l1l1l_opy_ + bstack11l1lll_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧᴯ")
      self.bstack111ll1l11ll_opy_ = bstack11l1lll_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᴰ")
    return bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_
  def bstack111l1ll1ll1_opy_(self):
    try:
      bstack111ll1111ll_opy_ = [os.path.join(expanduser(bstack11l1lll_opy_ (u"ࠦࢃࠨᴱ")), bstack11l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᴲ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111ll1111ll_opy_:
        if(self.bstack111l1l1lll1_opy_(path)):
          return path
      raise bstack11l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᴳ")
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤᴴ").format(e))
  def bstack111l1l1lll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll11llll_opy_(self, bstack111lll11lll_opy_):
    return os.path.join(bstack111lll11lll_opy_, self.bstack11l1ll1l1ll_opy_ + bstack11l1lll_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢᴵ"))
  def bstack111ll1lll11_opy_(self, bstack111lll11lll_opy_, bstack111ll111l1l_opy_):
    if not bstack111ll111l1l_opy_: return
    try:
      bstack111ll1ll11l_opy_ = self.bstack111ll11llll_opy_(bstack111lll11lll_opy_)
      with open(bstack111ll1ll11l_opy_, bstack11l1lll_opy_ (u"ࠤࡺࠦᴶ")) as f:
        f.write(bstack111ll111l1l_opy_)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢᴷ"))
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᴸ").format(e))
  def bstack111ll11l111_opy_(self, bstack111lll11lll_opy_):
    try:
      bstack111ll1ll11l_opy_ = self.bstack111ll11llll_opy_(bstack111lll11lll_opy_)
      if os.path.exists(bstack111ll1ll11l_opy_):
        with open(bstack111ll1ll11l_opy_, bstack11l1lll_opy_ (u"ࠧࡸࠢᴹ")) as f:
          bstack111ll111l1l_opy_ = f.read().strip()
          return bstack111ll111l1l_opy_ if bstack111ll111l1l_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᴺ").format(e))
  def bstack111ll1111l1_opy_(self, bstack111lll11lll_opy_, bstack111ll1l1ll1_opy_):
    bstack111ll11ll1l_opy_ = self.bstack111ll11l111_opy_(bstack111lll11lll_opy_)
    if bstack111ll11ll1l_opy_:
      try:
        bstack111l1l1llll_opy_ = self.bstack111l1ll111l_opy_(bstack111ll11ll1l_opy_, bstack111ll1l1ll1_opy_)
        if not bstack111l1l1llll_opy_:
          self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤᴻ"))
          return True
        self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢᴼ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᴽ").format(e))
    return False
  def bstack111l1ll111l_opy_(self, bstack111ll11ll1l_opy_, bstack111ll1l1ll1_opy_):
    try:
      headers = {
        bstack11l1lll_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥᴾ"): bstack111ll11ll1l_opy_
      }
      response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠫࡌࡋࡔࠨᴿ"), bstack111ll1l1ll1_opy_, {}, {bstack11l1lll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨᵀ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣᵁ").format(e))
  @measure(event_name=EVENTS.bstack11ll11l11l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
  def bstack111lll11l11_opy_(self, bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_):
    try:
      bstack111ll111ll1_opy_ = self.bstack111l1ll1ll1_opy_()
      bstack111l1ll1l1l_opy_ = os.path.join(bstack111ll111ll1_opy_, bstack11l1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪᵂ"))
      bstack111ll11lll1_opy_ = os.path.join(bstack111ll111ll1_opy_, bstack111l1lll1ll_opy_)
      if self.bstack111ll1111l1_opy_(bstack111ll111ll1_opy_, bstack111ll1l1ll1_opy_):
        if os.path.exists(bstack111ll11lll1_opy_):
          self.logger.info(bstack11l1lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᵃ").format(bstack111ll11lll1_opy_))
          return bstack111ll11lll1_opy_
        if os.path.exists(bstack111l1ll1l1l_opy_):
          self.logger.info(bstack11l1lll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢᵄ").format(bstack111l1ll1l1l_opy_))
          return self.bstack111lll111l1_opy_(bstack111l1ll1l1l_opy_, bstack111l1lll1ll_opy_)
      self.logger.info(bstack11l1lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣᵅ").format(bstack111ll1l1ll1_opy_))
      response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠫࡌࡋࡔࠨᵆ"), bstack111ll1l1ll1_opy_, {}, {})
      if response.status_code == 200:
        bstack111lll111ll_opy_ = response.headers.get(bstack11l1lll_opy_ (u"ࠧࡋࡔࡢࡩࠥᵇ"), bstack11l1lll_opy_ (u"ࠨࠢᵈ"))
        if bstack111lll111ll_opy_:
          self.bstack111ll1lll11_opy_(bstack111ll111ll1_opy_, bstack111lll111ll_opy_)
        with open(bstack111l1ll1l1l_opy_, bstack11l1lll_opy_ (u"ࠧࡸࡤࠪᵉ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1lll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᵊ").format(bstack111l1ll1l1l_opy_))
        return self.bstack111lll111l1_opy_(bstack111l1ll1l1l_opy_, bstack111l1lll1ll_opy_)
      else:
        raise(bstack11l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᵋ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᵌ").format(e))
  def bstack111ll1ll111_opy_(self, bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_):
    try:
      retry = 2
      bstack111ll11lll1_opy_ = None
      bstack111l1ll11ll_opy_ = False
      while retry > 0:
        bstack111ll11lll1_opy_ = self.bstack111lll11l11_opy_(bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_)
        bstack111l1ll11ll_opy_ = self.bstack111ll1l11l1_opy_(bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_, bstack111ll11lll1_opy_)
        if bstack111l1ll11ll_opy_:
          break
        retry -= 1
      return bstack111ll11lll1_opy_, bstack111l1ll11ll_opy_
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᵍ").format(e))
    return bstack111ll11lll1_opy_, False
  def bstack111ll1l11l1_opy_(self, bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_, bstack111ll11lll1_opy_, bstack111ll1llll1_opy_ = 0):
    if bstack111ll1llll1_opy_ > 1:
      return False
    if bstack111ll11lll1_opy_ == None or os.path.exists(bstack111ll11lll1_opy_) == False:
      self.logger.warn(bstack11l1lll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᵎ"))
      return False
    bstack111l1lllll1_opy_ = bstack11l1lll_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᵏ")
    command = bstack11l1lll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵐ").format(bstack111ll11lll1_opy_)
    bstack111l1l1ll1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l1lllll1_opy_, bstack111l1l1ll1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᵑ"))
      return False
  def bstack111lll111l1_opy_(self, bstack111l1ll1l1l_opy_, bstack111l1lll1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack111l1ll1l1l_opy_)
      shutil.unpack_archive(bstack111l1ll1l1l_opy_, working_dir)
      bstack111ll11lll1_opy_ = os.path.join(working_dir, bstack111l1lll1ll_opy_)
      os.chmod(bstack111ll11lll1_opy_, 0o755)
      return bstack111ll11lll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᵒ"))
  def bstack111ll11ll11_opy_(self):
    try:
      bstack111ll1l1l1l_opy_ = self.config.get(bstack11l1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᵓ"))
      bstack111ll11ll11_opy_ = bstack111ll1l1l1l_opy_ or (bstack111ll1l1l1l_opy_ is None and self.bstack11ll1l11ll_opy_)
      if not bstack111ll11ll11_opy_ or self.config.get(bstack11l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᵔ"), None) not in bstack11ll11llll1_opy_:
        return False
      self.bstack1l11l1111l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᵕ").format(e))
  def bstack111ll1l1lll_opy_(self):
    try:
      bstack111ll1l1lll_opy_ = self.percy_capture_mode
      return bstack111ll1l1lll_opy_
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᵖ").format(e))
  def init(self, bstack11ll1l11ll_opy_, config, logger):
    self.bstack11ll1l11ll_opy_ = bstack11ll1l11ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll11ll11_opy_():
      return
    self.bstack111l1llll11_opy_ = config.get(bstack11l1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵗ"), {})
    self.percy_capture_mode = config.get(bstack11l1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᵘ"))
    try:
      bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_ = self.bstack111ll111111_opy_()
      self.bstack11l1ll1l1ll_opy_ = bstack111l1lll1ll_opy_
      bstack111ll11lll1_opy_, bstack111l1ll11ll_opy_ = self.bstack111ll1ll111_opy_(bstack111ll1l1ll1_opy_, bstack111l1lll1ll_opy_)
      if bstack111l1ll11ll_opy_:
        self.binary_path = bstack111ll11lll1_opy_
        thread = Thread(target=self.bstack111ll1l111l_opy_)
        thread.start()
      else:
        self.bstack111l1ll1lll_opy_ = True
        self.logger.error(bstack11l1lll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᵙ").format(bstack111ll11lll1_opy_))
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᵚ").format(e))
  def bstack111lll1ll11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1lll_opy_ (u"ࠫࡱࡵࡧࠨᵛ"), bstack11l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᵜ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᵝ").format(logfile))
      self.bstack111lll11111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᵞ").format(e))
  @measure(event_name=EVENTS.bstack11ll1l111ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
  def bstack111ll1l111l_opy_(self):
    bstack111lll1l1ll_opy_ = self.bstack111ll1l1l11_opy_()
    if bstack111lll1l1ll_opy_ == None:
      self.bstack111l1ll1lll_opy_ = True
      self.logger.error(bstack11l1lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᵟ"))
      return False
    command_args = [bstack11l1lll_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᵠ") if self.bstack11ll1l11ll_opy_ else bstack11l1lll_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᵡ")]
    bstack11l1111l11l_opy_ = self.bstack111l1lll11l_opy_()
    if bstack11l1111l11l_opy_ != None:
      command_args.append(bstack11l1lll_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᵢ").format(bstack11l1111l11l_opy_))
    env = os.environ.copy()
    env[bstack11l1lll_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᵣ")] = bstack111lll1l1ll_opy_
    env[bstack11l1lll_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᵤ")] = os.environ.get(bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᵥ"), bstack11l1lll_opy_ (u"ࠨࠩᵦ"))
    bstack111ll1ll1l1_opy_ = [self.binary_path]
    self.bstack111lll1ll11_opy_()
    self.bstack111l1llll1l_opy_ = self.bstack111ll111l11_opy_(bstack111ll1ll1l1_opy_ + command_args, env)
    self.logger.debug(bstack11l1lll_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᵧ"))
    bstack111ll1llll1_opy_ = 0
    while self.bstack111l1llll1l_opy_.poll() == None:
      bstack111ll1l1111_opy_ = self.bstack111ll11l1l1_opy_()
      if bstack111ll1l1111_opy_:
        self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᵨ"))
        self.bstack111ll111lll_opy_ = True
        return True
      bstack111ll1llll1_opy_ += 1
      self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᵩ").format(bstack111ll1llll1_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᵪ").format(bstack111ll1llll1_opy_))
    self.bstack111l1ll1lll_opy_ = True
    return False
  def bstack111ll11l1l1_opy_(self, bstack111ll1llll1_opy_ = 0):
    if bstack111ll1llll1_opy_ > 10:
      return False
    try:
      bstack111lll11l1l_opy_ = os.environ.get(bstack11l1lll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ᵫ"), bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᵬ"))
      bstack111l1llllll_opy_ = bstack111lll11l1l_opy_ + bstack11ll11l1111_opy_
      response = requests.get(bstack111l1llllll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᵭ"), {}).get(bstack11l1lll_opy_ (u"ࠩ࡬ࡨࠬᵮ"), None)
      return True
    except:
      self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᵯ"))
      return False
  def bstack111ll1l1l11_opy_(self):
    bstack111lll1l1l1_opy_ = bstack11l1lll_opy_ (u"ࠫࡦࡶࡰࠨᵰ") if self.bstack11ll1l11ll_opy_ else bstack11l1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᵱ")
    bstack111ll11111l_opy_ = bstack11l1lll_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᵲ") if self.config.get(bstack11l1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᵳ")) is None else True
    bstack11l1l1l1lll_opy_ = bstack11l1lll_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᵴ").format(self.config[bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᵵ")], bstack111lll1l1l1_opy_, bstack111ll11111l_opy_)
    if self.percy_capture_mode:
      bstack11l1l1l1lll_opy_ += bstack11l1lll_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧᵶ").format(self.percy_capture_mode)
    uri = bstack1ll1ll11_opy_(bstack11l1l1l1lll_opy_)
    try:
      response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠫࡌࡋࡔࠨᵷ"), uri, {}, {bstack11l1lll_opy_ (u"ࠬࡧࡵࡵࡪࠪᵸ"): (self.config[bstack11l1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᵹ")], self.config[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᵺ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l11l1111l_opy_ = data.get(bstack11l1lll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᵻ"))
        self.percy_capture_mode = data.get(bstack11l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᵼ"))
        os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᵽ")] = str(self.bstack1l11l1111l_opy_)
        os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᵾ")] = str(self.percy_capture_mode)
        if bstack111ll11111l_opy_ == bstack11l1lll_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᵿ") and str(self.bstack1l11l1111l_opy_).lower() == bstack11l1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᶀ"):
          self.bstack1lll1l1lll_opy_ = True
        if bstack11l1lll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᶁ") in data:
          return data[bstack11l1lll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᶂ")]
        else:
          raise bstack11l1lll_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᶃ").format(data)
      else:
        raise bstack11l1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᶄ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᶅ").format(e))
  def bstack111l1lll11l_opy_(self):
    bstack111ll1lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1lll_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᶆ"))
    try:
      if bstack11l1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᶇ") not in self.bstack111l1llll11_opy_:
        self.bstack111l1llll11_opy_[bstack11l1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᶈ")] = 2
      with open(bstack111ll1lllll_opy_, bstack11l1lll_opy_ (u"ࠨࡹࠪᶉ")) as fp:
        json.dump(self.bstack111l1llll11_opy_, fp)
      return bstack111ll1lllll_opy_
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᶊ").format(e))
  def bstack111ll111l11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1l11ll_opy_ == bstack11l1lll_opy_ (u"ࠪࡻ࡮ࡴࠧᶋ"):
        bstack111l1lll1l1_opy_ = [bstack11l1lll_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᶌ"), bstack11l1lll_opy_ (u"ࠬ࠵ࡣࠨᶍ")]
        cmd = bstack111l1lll1l1_opy_ + cmd
      cmd = bstack11l1lll_opy_ (u"࠭ࠠࠨᶎ").join(cmd)
      self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᶏ").format(cmd))
      with open(self.bstack111lll11111_opy_, bstack11l1lll_opy_ (u"ࠣࡣࠥᶐ")) as bstack111l1ll1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l1ll1111_opy_, text=True, stderr=bstack111l1ll1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l1ll1lll_opy_ = True
      self.logger.error(bstack11l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᶑ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll111lll_opy_:
        self.logger.info(bstack11l1lll_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᶒ"))
        cmd = [self.binary_path, bstack11l1lll_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᶓ")]
        self.bstack111ll111l11_opy_(cmd)
        self.bstack111ll111lll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᶔ").format(cmd, e))
  def bstack1111l1l11_opy_(self):
    if not self.bstack1l11l1111l_opy_:
      return
    try:
      bstack111ll11l11l_opy_ = 0
      while not self.bstack111ll111lll_opy_ and bstack111ll11l11l_opy_ < self.bstack111l1ll1l11_opy_:
        if self.bstack111l1ll1lll_opy_:
          self.logger.info(bstack11l1lll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᶕ"))
          return
        time.sleep(1)
        bstack111ll11l11l_opy_ += 1
      os.environ[bstack11l1lll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᶖ")] = str(self.bstack111ll1ll1ll_opy_())
      self.logger.info(bstack11l1lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᶗ"))
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᶘ").format(e))
  def bstack111ll1ll1ll_opy_(self):
    if self.bstack11ll1l11ll_opy_:
      return
    try:
      bstack111lll1111l_opy_ = [platform[bstack11l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᶙ")].lower() for platform in self.config.get(bstack11l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᶚ"), [])]
      bstack111lll1l11l_opy_ = sys.maxsize
      bstack111ll1lll1l_opy_ = bstack11l1lll_opy_ (u"ࠬ࠭ᶛ")
      for browser in bstack111lll1111l_opy_:
        if browser in self.bstack111lll1l111_opy_:
          bstack111l1ll11l1_opy_ = self.bstack111lll1l111_opy_[browser]
        if bstack111l1ll11l1_opy_ < bstack111lll1l11l_opy_:
          bstack111lll1l11l_opy_ = bstack111l1ll11l1_opy_
          bstack111ll1lll1l_opy_ = browser
      return bstack111ll1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack11l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᶜ").format(e))
  @classmethod
  def bstack1lll1l11ll_opy_(self):
    return os.getenv(bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᶝ"), bstack11l1lll_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᶞ")).lower()
  @classmethod
  def bstack1l1lll1ll_opy_(self):
    return os.getenv(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᶟ"), bstack11l1lll_opy_ (u"ࠪࠫᶠ"))
  @classmethod
  def bstack1l1ll11ll11_opy_(cls, value):
    cls.bstack1lll1l1lll_opy_ = value
  @classmethod
  def bstack111lll11ll1_opy_(cls):
    return cls.bstack1lll1l1lll_opy_
  @classmethod
  def bstack1l1ll111lll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111l1lll111_opy_(cls):
    return cls.percy_build_id