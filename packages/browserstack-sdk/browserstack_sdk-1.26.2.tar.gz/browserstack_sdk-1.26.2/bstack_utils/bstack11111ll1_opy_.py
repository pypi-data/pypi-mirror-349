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
from bstack_utils.bstack1lll111lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1ll1lll_opy_(object):
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠬࢄࠧᚷ")), bstack111l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᚸ"))
  bstack11ll1lll1l1_opy_ = os.path.join(bstack1l1l111l1_opy_, bstack111l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᚹ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1111l11ll_opy_ = None
  bstack1l1ll1l1l_opy_ = None
  bstack11llll11l11_opy_ = None
  bstack11lll11lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111l11_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᚺ")):
      cls.instance = super(bstack11ll1ll1lll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1lll111_opy_()
    return cls.instance
  def bstack11ll1lll111_opy_(self):
    try:
      with open(self.bstack11ll1lll1l1_opy_, bstack111l11_opy_ (u"ࠩࡵࠫᚻ")) as bstack11l11lll_opy_:
        bstack11ll1lll11l_opy_ = bstack11l11lll_opy_.read()
        data = json.loads(bstack11ll1lll11l_opy_)
        if bstack111l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᚼ") in data:
          self.bstack11lll1lll11_opy_(data[bstack111l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᚽ")])
        if bstack111l11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᚾ") in data:
          self.bstack1l11ll111l_opy_(data[bstack111l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᚿ")])
        if bstack111l11_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᛀ") in data:
          self.bstack11ll1lll1ll_opy_(data[bstack111l11_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛁ")])
    except:
      pass
  def bstack11ll1lll1ll_opy_(self, bstack11lll11lll1_opy_):
    if bstack11lll11lll1_opy_ != None:
      self.bstack11lll11lll1_opy_ = bstack11lll11lll1_opy_
  def bstack1l11ll111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack111l11_opy_ (u"ࠩࡶࡧࡦࡴࠧᛂ"),bstack111l11_opy_ (u"ࠪࠫᛃ"))
      self.bstack1111l11ll_opy_ = scripts.get(bstack111l11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨᛄ"),bstack111l11_opy_ (u"ࠬ࠭ᛅ"))
      self.bstack1l1ll1l1l_opy_ = scripts.get(bstack111l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᛆ"),bstack111l11_opy_ (u"ࠧࠨᛇ"))
      self.bstack11llll11l11_opy_ = scripts.get(bstack111l11_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᛈ"),bstack111l11_opy_ (u"ࠩࠪᛉ"))
  def bstack11lll1lll11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1lll1l1_opy_, bstack111l11_opy_ (u"ࠪࡻࠬᛊ")) as file:
        json.dump({
          bstack111l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨᛋ"): self.commands_to_wrap,
          bstack111l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸࠨᛌ"): {
            bstack111l11_opy_ (u"ࠨࡳࡤࡣࡱࠦᛍ"): self.perform_scan,
            bstack111l11_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᛎ"): self.bstack1111l11ll_opy_,
            bstack111l11_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᛏ"): self.bstack1l1ll1l1l_opy_,
            bstack111l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᛐ"): self.bstack11llll11l11_opy_
          },
          bstack111l11_opy_ (u"ࠥࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠢᛑ"): self.bstack11lll11lll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠿ࠦࡻࡾࠤᛒ").format(e))
      pass
  def bstack1ll11ll1l1_opy_(self, bstack1ll1l1ll1ll_opy_):
    try:
      return any(command.get(bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᛓ")) == bstack1ll1l1ll1ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11111ll1_opy_ = bstack11ll1ll1lll_opy_()