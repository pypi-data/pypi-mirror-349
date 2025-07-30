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
from bstack_utils.helper import bstack1l1lll1ll_opy_, bstack11l1111l_opy_
from bstack_utils.measure import measure
class bstack1111111ll_opy_:
  working_dir = os.getcwd()
  bstack11lllll1l_opy_ = False
  config = {}
  bstack11l11l1l11l_opy_ = bstack111l11_opy_ (u"ࠪࠫᴩ")
  binary_path = bstack111l11_opy_ (u"ࠫࠬᴪ")
  bstack111lll11l11_opy_ = bstack111l11_opy_ (u"ࠬ࠭ᴫ")
  bstack111ll11l_opy_ = False
  bstack111l1llll1l_opy_ = None
  bstack111ll1l1l1l_opy_ = {}
  bstack111lll1111l_opy_ = 300
  bstack111ll1lll11_opy_ = False
  logger = None
  bstack111ll1ll11l_opy_ = False
  bstack1ll1l1ll_opy_ = False
  percy_build_id = None
  bstack111lll111ll_opy_ = bstack111l11_opy_ (u"࠭ࠧᴬ")
  bstack111l1ll11ll_opy_ = {
    bstack111l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᴭ") : 1,
    bstack111l11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩᴮ") : 2,
    bstack111l11_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᴯ") : 3,
    bstack111l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᴰ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll1111l1_opy_(self):
    bstack111l1l1ll11_opy_ = bstack111l11_opy_ (u"ࠫࠬᴱ")
    bstack111l1ll1111_opy_ = sys.platform
    bstack111ll1ll1ll_opy_ = bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᴲ")
    if re.match(bstack111l11_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨᴳ"), bstack111l1ll1111_opy_) != None:
      bstack111l1l1ll11_opy_ = bstack11ll111111l_opy_ + bstack111l11_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣᴴ")
      self.bstack111lll111ll_opy_ = bstack111l11_opy_ (u"ࠨ࡯ࡤࡧࠬᴵ")
    elif re.match(bstack111l11_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢᴶ"), bstack111l1ll1111_opy_) != None:
      bstack111l1l1ll11_opy_ = bstack11ll111111l_opy_ + bstack111l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦᴷ")
      bstack111ll1ll1ll_opy_ = bstack111l11_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢᴸ")
      self.bstack111lll111ll_opy_ = bstack111l11_opy_ (u"ࠬࡽࡩ࡯ࠩᴹ")
    else:
      bstack111l1l1ll11_opy_ = bstack11ll111111l_opy_ + bstack111l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤᴺ")
      self.bstack111lll111ll_opy_ = bstack111l11_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᴻ")
    return bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_
  def bstack111l1ll1l1l_opy_(self):
    try:
      bstack111ll111lll_opy_ = [os.path.join(expanduser(bstack111l11_opy_ (u"ࠣࢀࠥᴼ")), bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᴽ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111ll111lll_opy_:
        if(self.bstack111lll11111_opy_(path)):
          return path
      raise bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᴾ")
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨᴿ").format(e))
  def bstack111lll11111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll1ll111_opy_(self, bstack111l1llll11_opy_):
    return os.path.join(bstack111l1llll11_opy_, self.bstack11l11l1l11l_opy_ + bstack111l11_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦᵀ"))
  def bstack111l1l1lll1_opy_(self, bstack111l1llll11_opy_, bstack111l1ll1l11_opy_):
    if not bstack111l1ll1l11_opy_: return
    try:
      bstack111l1lll1ll_opy_ = self.bstack111ll1ll111_opy_(bstack111l1llll11_opy_)
      with open(bstack111l1lll1ll_opy_, bstack111l11_opy_ (u"ࠨࡷࠣᵁ")) as f:
        f.write(bstack111l1ll1l11_opy_)
        self.logger.debug(bstack111l11_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦᵂ"))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᵃ").format(e))
  def bstack111ll1l111l_opy_(self, bstack111l1llll11_opy_):
    try:
      bstack111l1lll1ll_opy_ = self.bstack111ll1ll111_opy_(bstack111l1llll11_opy_)
      if os.path.exists(bstack111l1lll1ll_opy_):
        with open(bstack111l1lll1ll_opy_, bstack111l11_opy_ (u"ࠤࡵࠦᵄ")) as f:
          bstack111l1ll1l11_opy_ = f.read().strip()
          return bstack111l1ll1l11_opy_ if bstack111l1ll1l11_opy_ else None
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᵅ").format(e))
  def bstack111ll11l1l1_opy_(self, bstack111l1llll11_opy_, bstack111l1l1ll11_opy_):
    bstack111l1lllll1_opy_ = self.bstack111ll1l111l_opy_(bstack111l1llll11_opy_)
    if bstack111l1lllll1_opy_:
      try:
        bstack111ll11111l_opy_ = self.bstack111l1l1l1ll_opy_(bstack111l1lllll1_opy_, bstack111l1l1ll11_opy_)
        if not bstack111ll11111l_opy_:
          self.logger.debug(bstack111l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨᵆ"))
          return True
        self.logger.debug(bstack111l11_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦᵇ"))
        return False
      except Exception as e:
        self.logger.warn(bstack111l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᵈ").format(e))
    return False
  def bstack111l1l1l1ll_opy_(self, bstack111l1lllll1_opy_, bstack111l1l1ll11_opy_):
    try:
      headers = {
        bstack111l11_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢᵉ"): bstack111l1lllll1_opy_
      }
      response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠨࡉࡈࡘࠬᵊ"), bstack111l1l1ll11_opy_, {}, {bstack111l11_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥᵋ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack111l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧᵌ").format(e))
  @measure(event_name=EVENTS.bstack11ll1111111_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
  def bstack111ll11lll1_opy_(self, bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_):
    try:
      bstack111ll1l1ll1_opy_ = self.bstack111l1ll1l1l_opy_()
      bstack111ll111l11_opy_ = os.path.join(bstack111ll1l1ll1_opy_, bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧᵍ"))
      bstack111ll1lllll_opy_ = os.path.join(bstack111ll1l1ll1_opy_, bstack111ll1ll1ll_opy_)
      if self.bstack111ll11l1l1_opy_(bstack111ll1l1ll1_opy_, bstack111l1l1ll11_opy_): # if bstack111ll111ll1_opy_, bstack1l1l1llll1l_opy_ bstack111l1ll1l11_opy_ is bstack111lll1l1l1_opy_ to bstack11l1llll11l_opy_ version available (response 304)
        if os.path.exists(bstack111ll1lllll_opy_):
          self.logger.info(bstack111l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᵎ").format(bstack111ll1lllll_opy_))
          return bstack111ll1lllll_opy_
        if os.path.exists(bstack111ll111l11_opy_):
          self.logger.info(bstack111l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦᵏ").format(bstack111ll111l11_opy_))
          return self.bstack111ll1ll1l1_opy_(bstack111ll111l11_opy_, bstack111ll1ll1ll_opy_)
      self.logger.info(bstack111l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧᵐ").format(bstack111l1l1ll11_opy_))
      response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠨࡉࡈࡘࠬᵑ"), bstack111l1l1ll11_opy_, {}, {})
      if response.status_code == 200:
        bstack111ll11llll_opy_ = response.headers.get(bstack111l11_opy_ (u"ࠤࡈࡘࡦ࡭ࠢᵒ"), bstack111l11_opy_ (u"ࠥࠦᵓ"))
        if bstack111ll11llll_opy_:
          self.bstack111l1l1lll1_opy_(bstack111ll1l1ll1_opy_, bstack111ll11llll_opy_)
        with open(bstack111ll111l11_opy_, bstack111l11_opy_ (u"ࠫࡼࡨࠧᵔ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᵕ").format(bstack111ll111l11_opy_))
        return self.bstack111ll1ll1l1_opy_(bstack111ll111l11_opy_, bstack111ll1ll1ll_opy_)
      else:
        raise(bstack111l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᵖ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᵗ").format(e))
  def bstack111ll1l1l11_opy_(self, bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_):
    try:
      retry = 2
      bstack111ll1lllll_opy_ = None
      bstack111l1lll1l1_opy_ = False
      while retry > 0:
        bstack111ll1lllll_opy_ = self.bstack111ll11lll1_opy_(bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_)
        bstack111l1lll1l1_opy_ = self.bstack111ll1l1111_opy_(bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_, bstack111ll1lllll_opy_)
        if bstack111l1lll1l1_opy_:
          break
        retry -= 1
      return bstack111ll1lllll_opy_, bstack111l1lll1l1_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᵘ").format(e))
    return bstack111ll1lllll_opy_, False
  def bstack111ll1l1111_opy_(self, bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_, bstack111ll1lllll_opy_, bstack111ll1l11ll_opy_ = 0):
    if bstack111ll1l11ll_opy_ > 1:
      return False
    if bstack111ll1lllll_opy_ == None or os.path.exists(bstack111ll1lllll_opy_) == False:
      self.logger.warn(bstack111l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᵙ"))
      return False
    bstack111ll111l1l_opy_ = bstack111l11_opy_ (u"ࡵࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬ࠤࡡࡪࠫ࡝࠰࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࠦᵚ")
    command = bstack111l11_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᵛ").format(bstack111ll1lllll_opy_)
    bstack111l1l1llll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111ll111l1l_opy_, bstack111l1l1llll_opy_) != None:
      return True
    else:
      self.logger.error(bstack111l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᵜ"))
      return False
  def bstack111ll1ll1l1_opy_(self, bstack111ll111l11_opy_, bstack111ll1ll1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll111l11_opy_)
      shutil.unpack_archive(bstack111ll111l11_opy_, working_dir)
      bstack111ll1lllll_opy_ = os.path.join(working_dir, bstack111ll1ll1ll_opy_)
      os.chmod(bstack111ll1lllll_opy_, 0o755)
      return bstack111ll1lllll_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᵝ"))
  def bstack111lll1l111_opy_(self):
    try:
      bstack111l1l1l1l1_opy_ = self.config.get(bstack111l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᵞ"))
      bstack111lll1l111_opy_ = bstack111l1l1l1l1_opy_ or (bstack111l1l1l1l1_opy_ is None and self.bstack11lllll1l_opy_)
      if not bstack111lll1l111_opy_ or self.config.get(bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᵟ"), None) not in bstack11ll11l11l1_opy_:
        return False
      self.bstack111ll11l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᵠ").format(e))
  def bstack111ll11l11l_opy_(self):
    try:
      bstack111ll11l11l_opy_ = self.percy_capture_mode
      return bstack111ll11l11l_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᵡ").format(e))
  def init(self, bstack11lllll1l_opy_, config, logger):
    self.bstack11lllll1l_opy_ = bstack11lllll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lll1l111_opy_():
      return
    self.bstack111ll1l1l1l_opy_ = config.get(bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᵢ"), {})
    self.percy_capture_mode = config.get(bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᵣ"))
    try:
      bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_ = self.bstack111ll1111l1_opy_()
      self.bstack11l11l1l11l_opy_ = bstack111ll1ll1ll_opy_
      bstack111ll1lllll_opy_, bstack111l1lll1l1_opy_ = self.bstack111ll1l1l11_opy_(bstack111l1l1ll11_opy_, bstack111ll1ll1ll_opy_)
      if bstack111l1lll1l1_opy_:
        self.binary_path = bstack111ll1lllll_opy_
        thread = Thread(target=self.bstack111lll11ll1_opy_)
        thread.start()
      else:
        self.bstack111ll1ll11l_opy_ = True
        self.logger.error(bstack111l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᵤ").format(bstack111ll1lllll_opy_))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᵥ").format(e))
  def bstack111l1lll111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᵦ"), bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᵧ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l11_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᵨ").format(logfile))
      self.bstack111lll11l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᵩ").format(e))
  @measure(event_name=EVENTS.bstack11ll11l11ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
  def bstack111lll11ll1_opy_(self):
    bstack111l1ll1ll1_opy_ = self.bstack111l1ll11l1_opy_()
    if bstack111l1ll1ll1_opy_ == None:
      self.bstack111ll1ll11l_opy_ = True
      self.logger.error(bstack111l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᵪ"))
      return False
    command_args = [bstack111l11_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᵫ") if self.bstack11lllll1l_opy_ else bstack111l11_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᵬ")]
    bstack11l111111l1_opy_ = self.bstack111ll11l111_opy_()
    if bstack11l111111l1_opy_ != None:
      command_args.append(bstack111l11_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᵭ").format(bstack11l111111l1_opy_))
    env = os.environ.copy()
    env[bstack111l11_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᵮ")] = bstack111l1ll1ll1_opy_
    env[bstack111l11_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᵯ")] = os.environ.get(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᵰ"), bstack111l11_opy_ (u"ࠬ࠭ᵱ"))
    bstack111lll11lll_opy_ = [self.binary_path]
    self.bstack111l1lll111_opy_()
    self.bstack111l1llll1l_opy_ = self.bstack111lll111l1_opy_(bstack111lll11lll_opy_ + command_args, env)
    self.logger.debug(bstack111l11_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᵲ"))
    bstack111ll1l11ll_opy_ = 0
    while self.bstack111l1llll1l_opy_.poll() == None:
      bstack111ll11ll1l_opy_ = self.bstack111ll111111_opy_()
      if bstack111ll11ll1l_opy_:
        self.logger.debug(bstack111l11_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᵳ"))
        self.bstack111ll1lll11_opy_ = True
        return True
      bstack111ll1l11ll_opy_ += 1
      self.logger.debug(bstack111l11_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᵴ").format(bstack111ll1l11ll_opy_))
      time.sleep(2)
    self.logger.error(bstack111l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᵵ").format(bstack111ll1l11ll_opy_))
    self.bstack111ll1ll11l_opy_ = True
    return False
  def bstack111ll111111_opy_(self, bstack111ll1l11ll_opy_ = 0):
    if bstack111ll1l11ll_opy_ > 10:
      return False
    try:
      bstack111l1llllll_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᵶ"), bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᵷ"))
      bstack111lll11l1l_opy_ = bstack111l1llllll_opy_ + bstack11ll11lll11_opy_
      response = requests.get(bstack111lll11l1l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᵸ"), {}).get(bstack111l11_opy_ (u"࠭ࡩࡥࠩᵹ"), None)
      return True
    except:
      self.logger.debug(bstack111l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᵺ"))
      return False
  def bstack111l1ll11l1_opy_(self):
    bstack111l1lll11l_opy_ = bstack111l11_opy_ (u"ࠨࡣࡳࡴࠬᵻ") if self.bstack11lllll1l_opy_ else bstack111l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᵼ")
    bstack111ll1l1lll_opy_ = bstack111l11_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᵽ") if self.config.get(bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᵾ")) is None else True
    bstack11l1ll11l11_opy_ = bstack111l11_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨᵿ").format(self.config[bstack111l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᶀ")], bstack111l1lll11l_opy_, bstack111ll1l1lll_opy_)
    if self.percy_capture_mode:
      bstack11l1ll11l11_opy_ += bstack111l11_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤᶁ").format(self.percy_capture_mode)
    uri = bstack1l1lll1ll_opy_(bstack11l1ll11l11_opy_)
    try:
      response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠨࡉࡈࡘࠬᶂ"), uri, {}, {bstack111l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᶃ"): (self.config[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᶄ")], self.config[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᶅ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack111ll11l_opy_ = data.get(bstack111l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᶆ"))
        self.percy_capture_mode = data.get(bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫᶇ"))
        os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᶈ")] = str(self.bstack111ll11l_opy_)
        os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᶉ")] = str(self.percy_capture_mode)
        if bstack111ll1l1lll_opy_ == bstack111l11_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᶊ") and str(self.bstack111ll11l_opy_).lower() == bstack111l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᶋ"):
          self.bstack1ll1l1ll_opy_ = True
        if bstack111l11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᶌ") in data:
          return data[bstack111l11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᶍ")]
        else:
          raise bstack111l11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ᶎ").format(data)
      else:
        raise bstack111l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢᶏ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤᶐ").format(e))
  def bstack111ll11l111_opy_(self):
    bstack111ll11ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᶑ"))
    try:
      if bstack111l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᶒ") not in self.bstack111ll1l1l1l_opy_:
        self.bstack111ll1l1l1l_opy_[bstack111l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᶓ")] = 2
      with open(bstack111ll11ll11_opy_, bstack111l11_opy_ (u"ࠬࡽࠧᶔ")) as fp:
        json.dump(self.bstack111ll1l1l1l_opy_, fp)
      return bstack111ll11ll11_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᶕ").format(e))
  def bstack111lll111l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll111ll_opy_ == bstack111l11_opy_ (u"ࠧࡸ࡫ࡱࠫᶖ"):
        bstack111l1l1l11l_opy_ = [bstack111l11_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᶗ"), bstack111l11_opy_ (u"ࠩ࠲ࡧࠬᶘ")]
        cmd = bstack111l1l1l11l_opy_ + cmd
      cmd = bstack111l11_opy_ (u"ࠪࠤࠬᶙ").join(cmd)
      self.logger.debug(bstack111l11_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᶚ").format(cmd))
      with open(self.bstack111lll11l11_opy_, bstack111l11_opy_ (u"ࠧࡧࠢᶛ")) as bstack111l1l1ll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l1l1ll1l_opy_, text=True, stderr=bstack111l1l1ll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1ll11l_opy_ = True
      self.logger.error(bstack111l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᶜ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1lll11_opy_:
        self.logger.info(bstack111l11_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᶝ"))
        cmd = [self.binary_path, bstack111l11_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᶞ")]
        self.bstack111lll111l1_opy_(cmd)
        self.bstack111ll1lll11_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᶟ").format(cmd, e))
  def bstack111l1111_opy_(self):
    if not self.bstack111ll11l_opy_:
      return
    try:
      bstack111lll1l11l_opy_ = 0
      while not self.bstack111ll1lll11_opy_ and bstack111lll1l11l_opy_ < self.bstack111lll1111l_opy_:
        if self.bstack111ll1ll11l_opy_:
          self.logger.info(bstack111l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᶠ"))
          return
        time.sleep(1)
        bstack111lll1l11l_opy_ += 1
      os.environ[bstack111l11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᶡ")] = str(self.bstack111l1ll111l_opy_())
      self.logger.info(bstack111l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᶢ"))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᶣ").format(e))
  def bstack111l1ll111l_opy_(self):
    if self.bstack11lllll1l_opy_:
      return
    try:
      bstack111ll1lll1l_opy_ = [platform[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᶤ")].lower() for platform in self.config.get(bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᶥ"), [])]
      bstack111ll1111ll_opy_ = sys.maxsize
      bstack111l1ll1lll_opy_ = bstack111l11_opy_ (u"ࠩࠪᶦ")
      for browser in bstack111ll1lll1l_opy_:
        if browser in self.bstack111l1ll11ll_opy_:
          bstack111ll1l11l1_opy_ = self.bstack111l1ll11ll_opy_[browser]
        if bstack111ll1l11l1_opy_ < bstack111ll1111ll_opy_:
          bstack111ll1111ll_opy_ = bstack111ll1l11l1_opy_
          bstack111l1ll1lll_opy_ = browser
      return bstack111l1ll1lll_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᶧ").format(e))
  @classmethod
  def bstack1111l1lll_opy_(self):
    return os.getenv(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᶨ"), bstack111l11_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫᶩ")).lower()
  @classmethod
  def bstack111ll1lll_opy_(self):
    return os.getenv(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᶪ"), bstack111l11_opy_ (u"ࠧࠨᶫ"))
  @classmethod
  def bstack1l1ll11l1ll_opy_(cls, value):
    cls.bstack1ll1l1ll_opy_ = value
  @classmethod
  def bstack111ll1llll1_opy_(cls):
    return cls.bstack1ll1l1ll_opy_
  @classmethod
  def bstack1l1ll11l1l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111ll11l1ll_opy_(cls):
    return cls.percy_build_id