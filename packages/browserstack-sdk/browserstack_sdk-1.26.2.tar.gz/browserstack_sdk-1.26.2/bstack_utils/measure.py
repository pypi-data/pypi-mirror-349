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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1lll111lll_opy_ import get_logger
from bstack_utils.bstack11l11111l_opy_ import bstack1ll1ll1ll11_opy_
bstack11l11111l_opy_ = bstack1ll1ll1ll11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1llll1111l_opy_: Optional[str] = None):
    bstack111l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤ᳔ࠥࠦ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l11ll1l_opy_: str = bstack11l11111l_opy_.bstack11llll11111_opy_(label)
            start_mark: str = label + bstack111l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶ᳕ࠥ")
            end_mark: str = label + bstack111l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᳖")
            result = None
            try:
                if stage.value == STAGE.bstack1lll11l1l1_opy_.value:
                    bstack11l11111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11l11111l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1llll1111l_opy_)
                elif stage.value == STAGE.bstack1l1l11ll1_opy_.value:
                    start_mark: str = bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸ᳗ࠧ")
                    end_mark: str = bstack1ll1l11ll1l_opy_ + bstack111l11_opy_ (u"ࠨ࠺ࡦࡰࡧ᳘ࠦ")
                    bstack11l11111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11l11111l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1llll1111l_opy_)
            except Exception as e:
                bstack11l11111l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1llll1111l_opy_)
            return result
        return wrapper
    return decorator