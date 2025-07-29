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
from bstack_utils.bstack1l11l1lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1lll1ll_opy_(object):
  bstack1lll11l11l_opy_ = os.path.join(os.path.expanduser(bstack11l1lll_opy_ (u"ࠨࢀࠪᚬ")), bstack11l1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᚭ"))
  bstack11ll1lll11l_opy_ = os.path.join(bstack1lll11l11l_opy_, bstack11l1lll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪᚮ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l11ll1_opy_ = None
  bstack1ll1l1l1_opy_ = None
  bstack11lll1111ll_opy_ = None
  bstack11llll1l11l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1lll_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭ᚯ")):
      cls.instance = super(bstack11ll1lll1ll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1llll1l_opy_()
    return cls.instance
  def bstack11ll1llll1l_opy_(self):
    try:
      with open(self.bstack11ll1lll11l_opy_, bstack11l1lll_opy_ (u"ࠬࡸࠧᚰ")) as bstack1llllll1ll_opy_:
        bstack11ll1lll1l1_opy_ = bstack1llllll1ll_opy_.read()
        data = json.loads(bstack11ll1lll1l1_opy_)
        if bstack11l1lll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᚱ") in data:
          self.bstack11lll1ll1ll_opy_(data[bstack11l1lll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᚲ")])
        if bstack11l1lll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᚳ") in data:
          self.bstack11llll11_opy_(data[bstack11l1lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᚴ")])
        if bstack11l1lll_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚵ") in data:
          self.bstack11ll1llll11_opy_(data[bstack11l1lll_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚶ")])
    except:
      pass
  def bstack11ll1llll11_opy_(self, bstack11llll1l11l_opy_):
    if bstack11llll1l11l_opy_ != None:
      self.bstack11llll1l11l_opy_ = bstack11llll1l11l_opy_
  def bstack11llll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l1lll_opy_ (u"ࠬࡹࡣࡢࡰࠪᚷ"),bstack11l1lll_opy_ (u"࠭ࠧᚸ"))
      self.bstack11l11ll1_opy_ = scripts.get(bstack11l1lll_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫᚹ"),bstack11l1lll_opy_ (u"ࠨࠩᚺ"))
      self.bstack1ll1l1l1_opy_ = scripts.get(bstack11l1lll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᚻ"),bstack11l1lll_opy_ (u"ࠪࠫᚼ"))
      self.bstack11lll1111ll_opy_ = scripts.get(bstack11l1lll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᚽ"),bstack11l1lll_opy_ (u"ࠬ࠭ᚾ"))
  def bstack11lll1ll1ll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1lll11l_opy_, bstack11l1lll_opy_ (u"࠭ࡷࠨᚿ")) as file:
        json.dump({
          bstack11l1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤᛀ"): self.commands_to_wrap,
          bstack11l1lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤᛁ"): {
            bstack11l1lll_opy_ (u"ࠤࡶࡧࡦࡴࠢᛂ"): self.perform_scan,
            bstack11l1lll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᛃ"): self.bstack11l11ll1_opy_,
            bstack11l1lll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᛄ"): self.bstack1ll1l1l1_opy_,
            bstack11l1lll_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᛅ"): self.bstack11lll1111ll_opy_
          },
          bstack11l1lll_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥᛆ"): self.bstack11llll1l11l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11l1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᛇ").format(e))
      pass
  def bstack1l1ll1ll11_opy_(self, bstack1ll11llllll_opy_):
    try:
      return any(command.get(bstack11l1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᛈ")) == bstack1ll11llllll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1lll11ll11_opy_ = bstack11ll1lll1ll_opy_()