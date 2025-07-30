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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1lllll1_opy_, bstack11lll11l1l1_opy_, bstack11l1111l_opy_, bstack111l11111l_opy_, bstack11l1lll1lll_opy_, bstack11l11l1l1ll_opy_, bstack11l11l1l111_opy_, bstack11l11ll11l_opy_, bstack1l1lllll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1111lll11ll_opy_ import bstack1111llll1ll_opy_
import bstack_utils.bstack1l11ll1111_opy_ as bstack11ll1ll1ll_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1lllll1l1l_opy_
import bstack_utils.accessibility as bstack11lll1ll1_opy_
from bstack_utils.bstack11111ll1_opy_ import bstack11111ll1_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1111llllll_opy_
bstack1111l111lll_opy_ = bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪẪ")
logger = logging.getLogger(__name__)
class bstack1l11l1l1ll_opy_:
    bstack1111lll11ll_opy_ = None
    bs_config = None
    bstack1llllll1l1_opy_ = None
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1l111ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def launch(cls, bs_config, bstack1llllll1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1llllll1l1_opy_ = bstack1llllll1l1_opy_
        try:
            cls.bstack1111l11l1ll_opy_()
            bstack11lll1l1111_opy_ = bstack11ll1lllll1_opy_(bs_config)
            bstack11lll1111ll_opy_ = bstack11lll11l1l1_opy_(bs_config)
            data = bstack11ll1ll1ll_opy_.bstack1111l11ll1l_opy_(bs_config, bstack1llllll1l1_opy_)
            config = {
                bstack111l11_opy_ (u"ࠫࡦࡻࡴࡩࠩẫ"): (bstack11lll1l1111_opy_, bstack11lll1111ll_opy_),
                bstack111l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭Ậ"): cls.default_headers()
            }
            response = bstack11l1111l_opy_(bstack111l11_opy_ (u"࠭ࡐࡐࡕࡗࠫậ"), cls.request_url(bstack111l11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧẮ")), data, config)
            if response.status_code != 200:
                bstack1llll1lll1_opy_ = response.json()
                if bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩắ")] == False:
                    cls.bstack11111lll1ll_opy_(bstack1llll1lll1_opy_)
                    return
                cls.bstack1111l11l11l_opy_(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩẰ")])
                cls.bstack1111l11ll11_opy_(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪằ")])
                return None
            bstack1111l111ll1_opy_ = cls.bstack1111l1111l1_opy_(response)
            return bstack1111l111ll1_opy_, response.json()
        except Exception as error:
            logger.error(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤẲ").format(str(error)))
            return None
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    def stop(cls, bstack1111l1111ll_opy_=None):
        if not bstack1lllll1l1l_opy_.on() and not bstack11lll1ll1_opy_.on():
            return
        if os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩẳ")) == bstack111l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦẴ") or os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬẵ")) == bstack111l11_opy_ (u"ࠣࡰࡸࡰࡱࠨẶ"):
            logger.error(bstack111l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬặ"))
            return {
                bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪẸ"): bstack111l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪẹ"),
                bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ẻ"): bstack111l11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫẻ")
            }
        try:
            cls.bstack1111lll11ll_opy_.shutdown()
            data = {
                bstack111l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬẼ"): bstack11l11ll11l_opy_()
            }
            if not bstack1111l1111ll_opy_ is None:
                data[bstack111l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬẽ")] = [{
                    bstack111l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩẾ"): bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨế"),
                    bstack111l11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫỀ"): bstack1111l1111ll_opy_
                }]
            config = {
                bstack111l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ề"): cls.default_headers()
            }
            bstack11l1ll11l11_opy_ = bstack111l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧỂ").format(os.environ[bstack111l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧể")])
            bstack1111l11l111_opy_ = cls.request_url(bstack11l1ll11l11_opy_)
            response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠨࡒࡘࡘࠬỄ"), bstack1111l11l111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111l11_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣễ"))
        except Exception as error:
            logger.error(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢỆ") + str(error))
            return {
                bstack111l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫệ"): bstack111l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫỈ"),
                bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧỉ"): str(error)
            }
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    def bstack1111l1111l1_opy_(cls, response):
        bstack1llll1lll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111l111ll1_opy_ = {}
        if bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠧ࡫ࡹࡷࠫỊ")) is None:
            os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬị")] = bstack111l11_opy_ (u"ࠩࡱࡹࡱࡲࠧỌ")
        else:
            os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧọ")] = bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠫ࡯ࡽࡴࠨỎ"), bstack111l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪỏ"))
        os.environ[bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫỐ")] = bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩố"), bstack111l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ồ"))
        logger.info(bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧồ") + os.getenv(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨỔ")));
        if bstack1lllll1l1l_opy_.bstack1111l1l111l_opy_(cls.bs_config, cls.bstack1llllll1l1_opy_.get(bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬổ"), bstack111l11_opy_ (u"ࠬ࠭Ỗ"))) is True:
            bstack1111ll1lll1_opy_, build_hashed_id, bstack11111llll11_opy_ = cls.bstack1111l11llll_opy_(bstack1llll1lll1_opy_)
            if bstack1111ll1lll1_opy_ != None and build_hashed_id != None:
                bstack1111l111ll1_opy_[bstack111l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ỗ")] = {
                    bstack111l11_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪỘ"): bstack1111ll1lll1_opy_,
                    bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪộ"): build_hashed_id,
                    bstack111l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ớ"): bstack11111llll11_opy_
                }
            else:
                bstack1111l111ll1_opy_[bstack111l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪớ")] = {}
        else:
            bstack1111l111ll1_opy_[bstack111l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫỜ")] = {}
        bstack11111lll1l1_opy_, build_hashed_id = cls.bstack1111l111111_opy_(bstack1llll1lll1_opy_)
        if bstack11111lll1l1_opy_ != None and build_hashed_id != None:
            bstack1111l111ll1_opy_[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬờ")] = {
                bstack111l11_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪỞ"): bstack11111lll1l1_opy_,
                bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩở"): build_hashed_id,
            }
        else:
            bstack1111l111ll1_opy_[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨỠ")] = {}
        if bstack1111l111ll1_opy_[bstack111l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩỡ")].get(bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬỢ")) != None or bstack1111l111ll1_opy_[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫợ")].get(bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧỤ")) != None:
            cls.bstack1111l11111l_opy_(bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"࠭ࡪࡸࡶࠪụ")), bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩỦ")))
        return bstack1111l111ll1_opy_
    @classmethod
    def bstack1111l11llll_opy_(cls, bstack1llll1lll1_opy_):
        if bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨủ")) == None:
            cls.bstack1111l11l11l_opy_()
            return [None, None, None]
        if bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩỨ")][bstack111l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫứ")] != True:
            cls.bstack1111l11l11l_opy_(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫỪ")])
            return [None, None, None]
        logger.debug(bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩừ"))
        os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬỬ")] = bstack111l11_opy_ (u"ࠧࡵࡴࡸࡩࠬử")
        if bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠨ࡬ࡺࡸࠬỮ")):
            os.environ[bstack111l11_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ữ")] = json.dumps({
                bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬỰ"): bstack11ll1lllll1_opy_(cls.bs_config),
                bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ự"): bstack11lll11l1l1_opy_(cls.bs_config)
            })
        if bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧỲ")):
            os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬỳ")] = bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩỴ")]
        if bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨỵ")].get(bstack111l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪỶ"), {}).get(bstack111l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧỷ")):
            os.environ[bstack111l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬỸ")] = str(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬỹ")][bstack111l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧỺ")][bstack111l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫỻ")])
        else:
            os.environ[bstack111l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩỼ")] = bstack111l11_opy_ (u"ࠤࡱࡹࡱࡲࠢỽ")
        return [bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠪ࡮ࡼࡺࠧỾ")], bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ỿ")], os.environ[bstack111l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ἀ")]]
    @classmethod
    def bstack1111l111111_opy_(cls, bstack1llll1lll1_opy_):
        if bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ἁ")) == None:
            cls.bstack1111l11ll11_opy_()
            return [None, None]
        if bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧἂ")][bstack111l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩἃ")] != True:
            cls.bstack1111l11ll11_opy_(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἄ")])
            return [None, None]
        if bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἅ")].get(bstack111l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬἆ")):
            logger.debug(bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩἇ"))
            parsed = json.loads(os.getenv(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧἈ"), bstack111l11_opy_ (u"ࠧࡼࡿࠪἉ")))
            capabilities = bstack11ll1ll1ll_opy_.bstack1111l111l1l_opy_(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨἊ")][bstack111l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪἋ")][bstack111l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩἌ")], bstack111l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩἍ"), bstack111l11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫἎ"))
            bstack11111lll1l1_opy_ = capabilities[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫἏ")]
            os.environ[bstack111l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬἐ")] = bstack11111lll1l1_opy_
            if bstack111l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥἑ") in bstack1llll1lll1_opy_ and bstack1llll1lll1_opy_.get(bstack111l11_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣἒ")) is None:
                parsed[bstack111l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫἓ")] = capabilities[bstack111l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬἔ")]
            os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ἕ")] = json.dumps(parsed)
            scripts = bstack11ll1ll1ll_opy_.bstack1111l111l1l_opy_(bstack1llll1lll1_opy_[bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭἖")][bstack111l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ἗")][bstack111l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩἘ")], bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧἙ"), bstack111l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫἚ"))
            bstack11111ll1_opy_.bstack1l11ll111l_opy_(scripts)
            commands = bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫἛ")][bstack111l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ἔ")][bstack111l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧἝ")].get(bstack111l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ἞"))
            bstack11111ll1_opy_.bstack11lll1lll11_opy_(commands)
            bstack11lll11lll1_opy_ = capabilities.get(bstack111l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭἟"))
            bstack11111ll1_opy_.bstack11ll1lll1ll_opy_(bstack11lll11lll1_opy_)
            bstack11111ll1_opy_.store()
        return [bstack11111lll1l1_opy_, bstack1llll1lll1_opy_[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫἠ")]]
    @classmethod
    def bstack1111l11l11l_opy_(cls, response=None):
        os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨἡ")] = bstack111l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩἢ")
        os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩἣ")] = bstack111l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫἤ")
        os.environ[bstack111l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ἥ")] = bstack111l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧἦ")
        os.environ[bstack111l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨἧ")] = bstack111l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣἨ")
        os.environ[bstack111l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬἩ")] = bstack111l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥἪ")
        cls.bstack11111lll1ll_opy_(response, bstack111l11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨἫ"))
        return [None, None, None]
    @classmethod
    def bstack1111l11ll11_opy_(cls, response=None):
        os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬἬ")] = bstack111l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ἥ")
        os.environ[bstack111l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧἮ")] = bstack111l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨἯ")
        os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨἰ")] = bstack111l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪἱ")
        cls.bstack11111lll1ll_opy_(response, bstack111l11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨἲ"))
        return [None, None, None]
    @classmethod
    def bstack1111l11111l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫἳ")] = jwt
        os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ἴ")] = build_hashed_id
    @classmethod
    def bstack11111lll1ll_opy_(cls, response=None, product=bstack111l11_opy_ (u"ࠤࠥἵ")):
        if response == None or response.get(bstack111l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪἶ")) == None:
            logger.error(product + bstack111l11_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨἷ"))
            return
        for error in response[bstack111l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬἸ")]:
            bstack11l1l1l111l_opy_ = error[bstack111l11_opy_ (u"࠭࡫ࡦࡻࠪἹ")]
            error_message = error[bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨἺ")]
            if error_message:
                if bstack11l1l1l111l_opy_ == bstack111l11_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢἻ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111l11_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥἼ") + product + bstack111l11_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣἽ"))
    @classmethod
    def bstack1111l11l1ll_opy_(cls):
        if cls.bstack1111lll11ll_opy_ is not None:
            return
        cls.bstack1111lll11ll_opy_ = bstack1111llll1ll_opy_(cls.bstack11111lll11l_opy_)
        cls.bstack1111lll11ll_opy_.start()
    @classmethod
    def bstack111ll111ll_opy_(cls):
        if cls.bstack1111lll11ll_opy_ is None:
            return
        cls.bstack1111lll11ll_opy_.shutdown()
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    def bstack11111lll11l_opy_(cls, bstack111l11ll11_opy_, event_url=bstack111l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪἾ")):
        config = {
            bstack111l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭Ἷ"): cls.default_headers()
        }
        logger.debug(bstack111l11_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨὀ").format(bstack111l11_opy_ (u"ࠧ࠭ࠢࠪὁ").join([event[bstack111l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬὂ")] for event in bstack111l11ll11_opy_])))
        response = bstack11l1111l_opy_(bstack111l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧὃ"), cls.request_url(event_url), bstack111l11ll11_opy_, config)
        bstack11ll1llll11_opy_ = response.json()
    @classmethod
    def bstack111l1l1ll_opy_(cls, bstack111l11ll11_opy_, event_url=bstack111l11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩὄ")):
        logger.debug(bstack111l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦὅ").format(bstack111l11ll11_opy_[bstack111l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ὆")]))
        if not bstack11ll1ll1ll_opy_.bstack1111l11lll1_opy_(bstack111l11ll11_opy_[bstack111l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ὇")]):
            logger.debug(bstack111l11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧὈ").format(bstack111l11ll11_opy_[bstack111l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬὉ")]))
            return
        bstack1l1ll111l_opy_ = bstack11ll1ll1ll_opy_.bstack11111lllll1_opy_(bstack111l11ll11_opy_[bstack111l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ὂ")], bstack111l11ll11_opy_.get(bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬὋ")))
        if bstack1l1ll111l_opy_ != None:
            if bstack111l11ll11_opy_.get(bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ὄ")) != None:
                bstack111l11ll11_opy_[bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧὍ")][bstack111l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ὎")] = bstack1l1ll111l_opy_
            else:
                bstack111l11ll11_opy_[bstack111l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ὏")] = bstack1l1ll111l_opy_
        if event_url == bstack111l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧὐ"):
            cls.bstack1111l11l1ll_opy_()
            logger.debug(bstack111l11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧὑ").format(bstack111l11ll11_opy_[bstack111l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧὒ")]))
            cls.bstack1111lll11ll_opy_.add(bstack111l11ll11_opy_)
        elif event_url == bstack111l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩὓ"):
            cls.bstack11111lll11l_opy_([bstack111l11ll11_opy_], event_url)
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    def bstack1ll1llll_opy_(cls, logs):
        bstack1111l11l1l1_opy_ = []
        for log in logs:
            bstack1111l111l11_opy_ = {
                bstack111l11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪὔ"): bstack111l11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨὕ"),
                bstack111l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ὖ"): log[bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧὗ")],
                bstack111l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ὘"): log[bstack111l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ὑ")],
                bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫ὚"): {},
                bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ὓ"): log[bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ὜")],
            }
            if bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧὝ") in log:
                bstack1111l111l11_opy_[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ὞")] = log[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩὟ")]
            elif bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪὠ") in log:
                bstack1111l111l11_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫὡ")] = log[bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὢ")]
            bstack1111l11l1l1_opy_.append(bstack1111l111l11_opy_)
        cls.bstack111l1l1ll_opy_({
            bstack111l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪὣ"): bstack111l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫὤ"),
            bstack111l11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ὥ"): bstack1111l11l1l1_opy_
        })
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    def bstack1111l1l1111_opy_(cls, steps):
        bstack11111llll1l_opy_ = []
        for step in steps:
            bstack11111llllll_opy_ = {
                bstack111l11_opy_ (u"ࠩ࡮࡭ࡳࡪࠧὦ"): bstack111l11_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ὧ"),
                bstack111l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪὨ"): step[bstack111l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫὩ")],
                bstack111l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩὪ"): step[bstack111l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪὫ")],
                bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩὬ"): step[bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪὭ")],
                bstack111l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬὮ"): step[bstack111l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭Ὧ")]
            }
            if bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὰ") in step:
                bstack11111llllll_opy_[bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ά")] = step[bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧὲ")]
            elif bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨέ") in step:
                bstack11111llllll_opy_[bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩὴ")] = step[bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪή")]
            bstack11111llll1l_opy_.append(bstack11111llllll_opy_)
        cls.bstack111l1l1ll_opy_({
            bstack111l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨὶ"): bstack111l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩί"),
            bstack111l11_opy_ (u"࠭࡬ࡰࡩࡶࠫὸ"): bstack11111llll1l_opy_
        })
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1lll111111_opy_, stage=STAGE.bstack1l1l11ll1_opy_)
    def bstack11lllll1l1_opy_(cls, screenshot):
        cls.bstack111l1l1ll_opy_({
            bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫό"): bstack111l11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬὺ"),
            bstack111l11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧύ"): [{
                bstack111l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨὼ"): bstack111l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ώ"),
                bstack111l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ὾"): datetime.datetime.utcnow().isoformat() + bstack111l11_opy_ (u"࡚࠭ࠨ὿"),
                bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᾀ"): screenshot[bstack111l11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᾁ")],
                bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾂ"): screenshot[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾃ")]
            }]
        }, event_url=bstack111l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᾄ"))
    @classmethod
    @bstack111l11111l_opy_(class_method=True)
    def bstack1lll1ll11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111l1l1ll_opy_({
            bstack111l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᾅ"): bstack111l11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᾆ"),
            bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᾇ"): {
                bstack111l11_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᾈ"): cls.current_test_uuid(),
                bstack111l11_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᾉ"): cls.bstack111ll1ll1l_opy_(driver)
            }
        })
    @classmethod
    def bstack111llll11l_opy_(cls, event: str, bstack111l11ll11_opy_: bstack1111llllll_opy_):
        bstack111ll1l1l1_opy_ = {
            bstack111l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᾊ"): event,
            bstack111l11ll11_opy_.bstack1111lllll1_opy_(): bstack111l11ll11_opy_.bstack111l11lll1_opy_(event)
        }
        cls.bstack111l1l1ll_opy_(bstack111ll1l1l1_opy_)
        result = getattr(bstack111l11ll11_opy_, bstack111l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᾋ"), None)
        if event == bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᾌ"):
            threading.current_thread().bstackTestMeta = {bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᾍ"): bstack111l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᾎ")}
        elif event == bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᾏ"):
            threading.current_thread().bstackTestMeta = {bstack111l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᾐ"): getattr(result, bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᾑ"), bstack111l11_opy_ (u"ࠫࠬᾒ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᾓ"), None) is None or os.environ[bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᾔ")] == bstack111l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᾕ")) and (os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᾖ"), None) is None or os.environ[bstack111l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᾗ")] == bstack111l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᾘ")):
            return False
        return True
    @staticmethod
    def bstack11111lll111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l1l1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᾙ"): bstack111l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᾚ"),
            bstack111l11_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᾛ"): bstack111l11_opy_ (u"ࠧࡵࡴࡸࡩࠬᾜ")
        }
        if os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᾝ"), None):
            headers[bstack111l11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᾞ")] = bstack111l11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᾟ").format(os.environ[bstack111l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣᾠ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111l11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᾡ").format(bstack1111l111lll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᾢ"), None)
    @staticmethod
    def bstack111ll1ll1l_opy_(driver):
        return {
            bstack11l1lll1lll_opy_(): bstack11l11l1l1ll_opy_(driver)
        }
    @staticmethod
    def bstack1111l1l11l1_opy_(exception_info, report):
        return [{bstack111l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᾣ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l11ll1_opy_(typename):
        if bstack111l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᾤ") in typename:
            return bstack111l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᾥ")
        return bstack111l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᾦ")