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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11ll1ll1l11_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1111lll11ll_opy_ = urljoin(builder, bstack11l1lll_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬḙ"))
        if params:
            bstack1111lll11ll_opy_ += bstack11l1lll_opy_ (u"ࠨ࠿ࡼࡿࠥḚ").format(urlencode({bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧḛ"): params.get(bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨḜ"))}))
        return bstack11ll1ll1l11_opy_.bstack1111lll111l_opy_(bstack1111lll11ll_opy_)
    @staticmethod
    def bstack11ll1ll1lll_opy_(builder,params=None):
        bstack1111lll11ll_opy_ = urljoin(builder, bstack11l1lll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪḝ"))
        if params:
            bstack1111lll11ll_opy_ += bstack11l1lll_opy_ (u"ࠥࡃࢀࢃࠢḞ").format(urlencode({bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫḟ"): params.get(bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬḠ"))}))
        return bstack11ll1ll1l11_opy_.bstack1111lll111l_opy_(bstack1111lll11ll_opy_)
    @staticmethod
    def bstack1111lll111l_opy_(bstack1111lll11l1_opy_):
        bstack1111lll1l1l_opy_ = os.environ.get(bstack11l1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫḡ"), os.environ.get(bstack11l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫḢ"), bstack11l1lll_opy_ (u"ࠨࠩḣ")))
        headers = {bstack11l1lll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩḤ"): bstack11l1lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ḥ").format(bstack1111lll1l1l_opy_)}
        response = requests.get(bstack1111lll11l1_opy_, headers=headers)
        bstack1111lll1l11_opy_ = {}
        try:
            bstack1111lll1l11_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥḦ").format(e))
            pass
        if bstack1111lll1l11_opy_ is not None:
            bstack1111lll1l11_opy_[bstack11l1lll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ḧ")] = response.headers.get(bstack11l1lll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧḨ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1111lll1l11_opy_[bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧḩ")] = response.status_code
        return bstack1111lll1l11_opy_