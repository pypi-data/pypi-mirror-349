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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll11l111_opy_, bstack11lll111111_opy_, bstack11lll1lll_opy_, bstack111l111111_opy_, bstack11l1lll1l1l_opy_, bstack11l1ll111ll_opy_, bstack11l1l1lll11_opy_, bstack1lll11l11_opy_, bstack111l11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1111llll1ll_opy_ import bstack111l1111111_opy_
import bstack_utils.bstack11111l111_opy_ as bstack11lll1111_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l111l11l_opy_
import bstack_utils.accessibility as bstack1l11111lll_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack111ll111l1_opy_
bstack1111l1l111l_opy_ = bstack11l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ẟ")
logger = logging.getLogger(__name__)
class bstack1lll11111l_opy_:
    bstack1111llll1ll_opy_ = None
    bs_config = None
    bstack1lll1ll111_opy_ = None
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1111l1l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def launch(cls, bs_config, bstack1lll1ll111_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1ll111_opy_ = bstack1lll1ll111_opy_
        try:
            cls.bstack1111l1111l1_opy_()
            bstack11lll1l111l_opy_ = bstack11lll11l111_opy_(bs_config)
            bstack11ll1llllll_opy_ = bstack11lll111111_opy_(bs_config)
            data = bstack11lll1111_opy_.bstack11111llllll_opy_(bs_config, bstack1lll1ll111_opy_)
            config = {
                bstack11l1lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬẠ"): (bstack11lll1l111l_opy_, bstack11ll1llllll_opy_),
                bstack11l1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩạ"): cls.default_headers()
            }
            response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧẢ"), cls.request_url(bstack11l1lll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪả")), data, config)
            if response.status_code != 200:
                bstack1lllll1ll_opy_ = response.json()
                if bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬẤ")] == False:
                    cls.bstack1111l11lll1_opy_(bstack1lllll1ll_opy_)
                    return
                cls.bstack1111l111ll1_opy_(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬấ")])
                cls.bstack1111l11l1ll_opy_(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ầ")])
                return None
            bstack1111l1l1111_opy_ = cls.bstack1111l11l11l_opy_(response)
            return bstack1111l1l1111_opy_, response.json()
        except Exception as error:
            logger.error(bstack11l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧầ").format(str(error)))
            return None
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    def stop(cls, bstack1111l1l1l1l_opy_=None):
        if not bstack11l111l11l_opy_.on() and not bstack1l11111lll_opy_.on():
            return
        if os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬẨ")) == bstack11l1lll_opy_ (u"ࠤࡱࡹࡱࡲࠢẩ") or os.environ.get(bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨẪ")) == bstack11l1lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤẫ"):
            logger.error(bstack11l1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨẬ"))
            return {
                bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ậ"): bstack11l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ắ"),
                bstack11l1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩắ"): bstack11l1lll_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧẰ")
            }
        try:
            cls.bstack1111llll1ll_opy_.shutdown()
            data = {
                bstack11l1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨằ"): bstack1lll11l11_opy_()
            }
            if not bstack1111l1l1l1l_opy_ is None:
                data[bstack11l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨẲ")] = [{
                    bstack11l1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬẳ"): bstack11l1lll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫẴ"),
                    bstack11l1lll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧẵ"): bstack1111l1l1l1l_opy_
                }]
            config = {
                bstack11l1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩẶ"): cls.default_headers()
            }
            bstack11l1l1l1lll_opy_ = bstack11l1lll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪặ").format(os.environ[bstack11l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣẸ")])
            bstack1111l11llll_opy_ = cls.request_url(bstack11l1l1l1lll_opy_)
            response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠫࡕ࡛ࡔࠨẹ"), bstack1111l11llll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1lll_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦẺ"))
        except Exception as error:
            logger.error(bstack11l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥẻ") + str(error))
            return {
                bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧẼ"): bstack11l1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧẽ"),
                bstack11l1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪẾ"): str(error)
            }
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    def bstack1111l11l11l_opy_(cls, response):
        bstack1lllll1ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111l1l1111_opy_ = {}
        if bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠪ࡮ࡼࡺࠧế")) is None:
            os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨỀ")] = bstack11l1lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪề")
        else:
            os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỂ")] = bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠧ࡫ࡹࡷࠫể"), bstack11l1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ễ"))
        os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧễ")] = bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬỆ"), bstack11l1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩệ"))
        logger.info(bstack11l1lll_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪỈ") + os.getenv(bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫỉ")));
        if bstack11l111l11l_opy_.bstack1111l1l11ll_opy_(cls.bs_config, cls.bstack1lll1ll111_opy_.get(bstack11l1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨỊ"), bstack11l1lll_opy_ (u"ࠨࠩị"))) is True:
            bstack1111lll1l1l_opy_, build_hashed_id, bstack1111l111111_opy_ = cls.bstack1111l11l111_opy_(bstack1lllll1ll_opy_)
            if bstack1111lll1l1l_opy_ != None and build_hashed_id != None:
                bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩỌ")] = {
                    bstack11l1lll_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭ọ"): bstack1111lll1l1l_opy_,
                    bstack11l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ỏ"): build_hashed_id,
                    bstack11l1lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩỏ"): bstack1111l111111_opy_
                }
            else:
                bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ố")] = {}
        else:
            bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧố")] = {}
        bstack1111l11111l_opy_, build_hashed_id = cls.bstack1111l111l1l_opy_(bstack1lllll1ll_opy_)
        if bstack1111l11111l_opy_ != None and build_hashed_id != None:
            bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨỒ")] = {
                bstack11l1lll_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭ồ"): bstack1111l11111l_opy_,
                bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬỔ"): build_hashed_id,
            }
        else:
            bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫổ")] = {}
        if bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬỖ")].get(bstack11l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨỗ")) != None or bstack1111l1l1111_opy_[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧỘ")].get(bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪộ")) != None:
            cls.bstack1111l11ll1l_opy_(bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠩ࡭ࡻࡹ࠭Ớ")), bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬớ")))
        return bstack1111l1l1111_opy_
    @classmethod
    def bstack1111l11l111_opy_(cls, bstack1lllll1ll_opy_):
        if bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫỜ")) == None:
            cls.bstack1111l111ll1_opy_()
            return [None, None, None]
        if bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬờ")][bstack11l1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧỞ")] != True:
            cls.bstack1111l111ll1_opy_(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧở")])
            return [None, None, None]
        logger.debug(bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬỠ"))
        os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨỡ")] = bstack11l1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨỢ")
        if bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠫ࡯ࡽࡴࠨợ")):
            os.environ[bstack11l1lll_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩỤ")] = json.dumps({
                bstack11l1lll_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨụ"): bstack11lll11l111_opy_(cls.bs_config),
                bstack11l1lll_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩỦ"): bstack11lll111111_opy_(cls.bs_config)
            })
        if bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪủ")):
            os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨỨ")] = bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬứ")]
        if bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫỪ")].get(bstack11l1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ừ"), {}).get(bstack11l1lll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪỬ")):
            os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨử")] = str(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨỮ")][bstack11l1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪữ")][bstack11l1lll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧỰ")])
        else:
            os.environ[bstack11l1lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬự")] = bstack11l1lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥỲ")
        return [bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"࠭ࡪࡸࡶࠪỳ")], bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩỴ")], os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩỵ")]]
    @classmethod
    def bstack1111l111l1l_opy_(cls, bstack1lllll1ll_opy_):
        if bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩỶ")) == None:
            cls.bstack1111l11l1ll_opy_()
            return [None, None]
        if bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪỷ")][bstack11l1lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬỸ")] != True:
            cls.bstack1111l11l1ll_opy_(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬỹ")])
            return [None, None]
        if bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ỻ")].get(bstack11l1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨỻ")):
            logger.debug(bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬỼ"))
            parsed = json.loads(os.getenv(bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪỽ"), bstack11l1lll_opy_ (u"ࠪࡿࢂ࠭Ỿ")))
            capabilities = bstack11lll1111_opy_.bstack11111lllll1_opy_(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫỿ")][bstack11l1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ἀ")][bstack11l1lll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬἁ")], bstack11l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬἂ"), bstack11l1lll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧἃ"))
            bstack1111l11111l_opy_ = capabilities[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧἄ")]
            os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨἅ")] = bstack1111l11111l_opy_
            if bstack11l1lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨἆ") in bstack1lllll1ll_opy_ and bstack1lllll1ll_opy_.get(bstack11l1lll_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦἇ")) is None:
                parsed[bstack11l1lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧἈ")] = capabilities[bstack11l1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨἉ")]
            os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩἊ")] = json.dumps(parsed)
            scripts = bstack11lll1111_opy_.bstack11111lllll1_opy_(bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἋ")][bstack11l1lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫἌ")][bstack11l1lll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬἍ")], bstack11l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἎ"), bstack11l1lll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧἏ"))
            bstack1lll11ll11_opy_.bstack11llll11_opy_(scripts)
            commands = bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧἐ")][bstack11l1lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩἑ")][bstack11l1lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪἒ")].get(bstack11l1lll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬἓ"))
            bstack1lll11ll11_opy_.bstack11lll1ll1ll_opy_(commands)
            bstack11llll1l11l_opy_ = capabilities.get(bstack11l1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩἔ"))
            bstack1lll11ll11_opy_.bstack11ll1llll11_opy_(bstack11llll1l11l_opy_)
            bstack1lll11ll11_opy_.store()
        return [bstack1111l11111l_opy_, bstack1lllll1ll_opy_[bstack11l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧἕ")]]
    @classmethod
    def bstack1111l111ll1_opy_(cls, response=None):
        os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ἖")] = bstack11l1lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ἗")
        os.environ[bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬἘ")] = bstack11l1lll_opy_ (u"ࠩࡱࡹࡱࡲࠧἙ")
        os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩἚ")] = bstack11l1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪἛ")
        os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫἜ")] = bstack11l1lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦἝ")
        os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ἞")] = bstack11l1lll_opy_ (u"ࠣࡰࡸࡰࡱࠨ἟")
        cls.bstack1111l11lll1_opy_(response, bstack11l1lll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤἠ"))
        return [None, None, None]
    @classmethod
    def bstack1111l11l1ll_opy_(cls, response=None):
        os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨἡ")] = bstack11l1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩἢ")
        os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪἣ")] = bstack11l1lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫἤ")
        os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫἥ")] = bstack11l1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ἦ")
        cls.bstack1111l11lll1_opy_(response, bstack11l1lll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤἧ"))
        return [None, None, None]
    @classmethod
    def bstack1111l11ll1l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧἨ")] = jwt
        os.environ[bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩἩ")] = build_hashed_id
    @classmethod
    def bstack1111l11lll1_opy_(cls, response=None, product=bstack11l1lll_opy_ (u"ࠧࠨἪ")):
        if response == None or response.get(bstack11l1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭Ἣ")) == None:
            logger.error(product + bstack11l1lll_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤἬ"))
            return
        for error in response[bstack11l1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨἭ")]:
            bstack11l1llll1ll_opy_ = error[bstack11l1lll_opy_ (u"ࠩ࡮ࡩࡾ࠭Ἦ")]
            error_message = error[bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫἯ")]
            if error_message:
                if bstack11l1llll1ll_opy_ == bstack11l1lll_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥἰ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1lll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨἱ") + product + bstack11l1lll_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦἲ"))
    @classmethod
    def bstack1111l1111l1_opy_(cls):
        if cls.bstack1111llll1ll_opy_ is not None:
            return
        cls.bstack1111llll1ll_opy_ = bstack111l1111111_opy_(cls.bstack1111l111lll_opy_)
        cls.bstack1111llll1ll_opy_.start()
    @classmethod
    def bstack111ll11l1l_opy_(cls):
        if cls.bstack1111llll1ll_opy_ is None:
            return
        cls.bstack1111llll1ll_opy_.shutdown()
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    def bstack1111l111lll_opy_(cls, bstack111l11l111_opy_, event_url=bstack11l1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ἳ")):
        config = {
            bstack11l1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩἴ"): cls.default_headers()
        }
        logger.debug(bstack11l1lll_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤἵ").format(bstack11l1lll_opy_ (u"ࠪ࠰ࠥ࠭ἶ").join([event[bstack11l1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨἷ")] for event in bstack111l11l111_opy_])))
        response = bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"ࠬࡖࡏࡔࡖࠪἸ"), cls.request_url(event_url), bstack111l11l111_opy_, config)
        bstack11lll11ll1l_opy_ = response.json()
    @classmethod
    def bstack1ll1ll11l_opy_(cls, bstack111l11l111_opy_, event_url=bstack11l1lll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬἹ")):
        logger.debug(bstack11l1lll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢἺ").format(bstack111l11l111_opy_[bstack11l1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬἻ")]))
        if not bstack11lll1111_opy_.bstack11111llll11_opy_(bstack111l11l111_opy_[bstack11l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ἴ")]):
            logger.debug(bstack11l1lll_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣἽ").format(bstack111l11l111_opy_[bstack11l1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨἾ")]))
            return
        bstack1ll1111l11_opy_ = bstack11lll1111_opy_.bstack1111l1111ll_opy_(bstack111l11l111_opy_[bstack11l1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩἿ")], bstack111l11l111_opy_.get(bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨὀ")))
        if bstack1ll1111l11_opy_ != None:
            if bstack111l11l111_opy_.get(bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩὁ")) != None:
                bstack111l11l111_opy_[bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪὂ")][bstack11l1lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧὃ")] = bstack1ll1111l11_opy_
            else:
                bstack111l11l111_opy_[bstack11l1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨὄ")] = bstack1ll1111l11_opy_
        if event_url == bstack11l1lll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪὅ"):
            cls.bstack1111l1111l1_opy_()
            logger.debug(bstack11l1lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ὆").format(bstack111l11l111_opy_[bstack11l1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ὇")]))
            cls.bstack1111llll1ll_opy_.add(bstack111l11l111_opy_)
        elif event_url == bstack11l1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬὈ"):
            cls.bstack1111l111lll_opy_([bstack111l11l111_opy_], event_url)
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    def bstack1ll1l1lll_opy_(cls, logs):
        bstack1111l1l11l1_opy_ = []
        for log in logs:
            bstack1111l11ll11_opy_ = {
                bstack11l1lll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭Ὁ"): bstack11l1lll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫὊ"),
                bstack11l1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩὋ"): log[bstack11l1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪὌ")],
                bstack11l1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨὍ"): log[bstack11l1lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ὎")],
                bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ὏"): {},
                bstack11l1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩὐ"): log[bstack11l1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪὑ")],
            }
            if bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪὒ") in log:
                bstack1111l11ll11_opy_[bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫὓ")] = log[bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὔ")]
            elif bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ὕ") in log:
                bstack1111l11ll11_opy_[bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧὖ")] = log[bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨὗ")]
            bstack1111l1l11l1_opy_.append(bstack1111l11ll11_opy_)
        cls.bstack1ll1ll11l_opy_({
            bstack11l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭὘"): bstack11l1lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧὙ"),
            bstack11l1lll_opy_ (u"ࠫࡱࡵࡧࡴࠩ὚"): bstack1111l1l11l1_opy_
        })
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    def bstack1111l11l1l1_opy_(cls, steps):
        bstack1111l1l1l11_opy_ = []
        for step in steps:
            bstack1111l1l1ll1_opy_ = {
                bstack11l1lll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪὛ"): bstack11l1lll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ὜"),
                bstack11l1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ὕ"): step[bstack11l1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ὞")],
                bstack11l1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬὟ"): step[bstack11l1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ὠ")],
                bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬὡ"): step[bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ὢ")],
                bstack11l1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨὣ"): step[bstack11l1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩὤ")]
            }
            if bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨὥ") in step:
                bstack1111l1l1ll1_opy_[bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩὦ")] = step[bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪὧ")]
            elif bstack11l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫὨ") in step:
                bstack1111l1l1ll1_opy_[bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὩ")] = step[bstack11l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ὢ")]
            bstack1111l1l1l11_opy_.append(bstack1111l1l1ll1_opy_)
        cls.bstack1ll1ll11l_opy_({
            bstack11l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫὫ"): bstack11l1lll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬὬ"),
            bstack11l1lll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧὭ"): bstack1111l1l1l11_opy_
        })
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l11l1l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1111lll1_opy_(cls, screenshot):
        cls.bstack1ll1ll11l_opy_({
            bstack11l1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧὮ"): bstack11l1lll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨὯ"),
            bstack11l1lll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪὰ"): [{
                bstack11l1lll_opy_ (u"࠭࡫ࡪࡰࡧࠫά"): bstack11l1lll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩὲ"),
                bstack11l1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫέ"): datetime.datetime.utcnow().isoformat() + bstack11l1lll_opy_ (u"ࠩ࡝ࠫὴ"),
                bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫή"): screenshot[bstack11l1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪὶ")],
                bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬί"): screenshot[bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ὸ")]
            }]
        }, event_url=bstack11l1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬό"))
    @classmethod
    @bstack111l111111_opy_(class_method=True)
    def bstack111l1ll11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll1ll11l_opy_({
            bstack11l1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬὺ"): bstack11l1lll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ύ"),
            bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬὼ"): {
                bstack11l1lll_opy_ (u"ࠦࡺࡻࡩࡥࠤώ"): cls.current_test_uuid(),
                bstack11l1lll_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦ὾"): cls.bstack11l111111l_opy_(driver)
            }
        })
    @classmethod
    def bstack111llll1ll_opy_(cls, event: str, bstack111l11l111_opy_: bstack111ll111l1_opy_):
        bstack111l11l1ll_opy_ = {
            bstack11l1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ὿"): event,
            bstack111l11l111_opy_.bstack111l1l1lll_opy_(): bstack111l11l111_opy_.bstack111l1ll1l1_opy_(event)
        }
        cls.bstack1ll1ll11l_opy_(bstack111l11l1ll_opy_)
        result = getattr(bstack111l11l111_opy_, bstack11l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᾀ"), None)
        if event == bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᾁ"):
            threading.current_thread().bstackTestMeta = {bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᾂ"): bstack11l1lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᾃ")}
        elif event == bstack11l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᾄ"):
            threading.current_thread().bstackTestMeta = {bstack11l1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᾅ"): getattr(result, bstack11l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᾆ"), bstack11l1lll_opy_ (u"ࠧࠨᾇ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᾈ"), None) is None or os.environ[bstack11l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᾉ")] == bstack11l1lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᾊ")) and (os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᾋ"), None) is None or os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᾌ")] == bstack11l1lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᾍ")):
            return False
        return True
    @staticmethod
    def bstack11111llll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll11111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᾎ"): bstack11l1lll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᾏ"),
            bstack11l1lll_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᾐ"): bstack11l1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨᾑ")
        }
        if os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᾒ"), None):
            headers[bstack11l1lll_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᾓ")] = bstack11l1lll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᾔ").format(os.environ[bstack11l1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦᾕ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l1lll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᾖ").format(bstack1111l1l111l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᾗ"), None)
    @staticmethod
    def bstack11l111111l_opy_(driver):
        return {
            bstack11l1lll1l1l_opy_(): bstack11l1ll111ll_opy_(driver)
        }
    @staticmethod
    def bstack1111l111l11_opy_(exception_info, report):
        return [{bstack11l1lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᾘ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l111ll_opy_(typename):
        if bstack11l1lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᾙ") in typename:
            return bstack11l1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᾚ")
        return bstack11l1lll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᾛ")