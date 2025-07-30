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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11ll1ll1ll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1111lll1111_opy_ = urljoin(builder, bstack111l11_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩḤ"))
        if params:
            bstack1111lll1111_opy_ += bstack111l11_opy_ (u"ࠥࡃࢀࢃࠢḥ").format(urlencode({bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫḦ"): params.get(bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬḧ"))}))
        return bstack11ll1ll1ll1_opy_.bstack1111ll1ll1l_opy_(bstack1111lll1111_opy_)
    @staticmethod
    def bstack11ll1l1llll_opy_(builder,params=None):
        bstack1111lll1111_opy_ = urljoin(builder, bstack111l11_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧḨ"))
        if params:
            bstack1111lll1111_opy_ += bstack111l11_opy_ (u"ࠢࡀࡽࢀࠦḩ").format(urlencode({bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨḪ"): params.get(bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩḫ"))}))
        return bstack11ll1ll1ll1_opy_.bstack1111ll1ll1l_opy_(bstack1111lll1111_opy_)
    @staticmethod
    def bstack1111ll1ll1l_opy_(bstack1111lll111l_opy_):
        bstack1111ll1lll1_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨḬ"), os.environ.get(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨḭ"), bstack111l11_opy_ (u"ࠬ࠭Ḯ")))
        headers = {bstack111l11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ḯ"): bstack111l11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪḰ").format(bstack1111ll1lll1_opy_)}
        response = requests.get(bstack1111lll111l_opy_, headers=headers)
        bstack1111ll1llll_opy_ = {}
        try:
            bstack1111ll1llll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢḱ").format(e))
            pass
        if bstack1111ll1llll_opy_ is not None:
            bstack1111ll1llll_opy_[bstack111l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪḲ")] = response.headers.get(bstack111l11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫḳ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1111ll1llll_opy_[bstack111l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫḴ")] = response.status_code
        return bstack1111ll1llll_opy_