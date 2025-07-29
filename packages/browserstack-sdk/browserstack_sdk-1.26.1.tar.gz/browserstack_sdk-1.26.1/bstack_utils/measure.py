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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l11l1lll_opy_ import get_logger
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
bstack11l1lll1l1_opy_ = bstack1lll1lll111_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l11ll1ll_opy_: Optional[str] = None):
    bstack11l1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ᳉")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l11llll_opy_: str = bstack11l1lll1l1_opy_.bstack11lll1l1111_opy_(label)
            start_mark: str = label + bstack11l1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᳊")
            end_mark: str = label + bstack11l1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᳋")
            result = None
            try:
                if stage.value == STAGE.bstack1l1l1l11_opy_.value:
                    bstack11l1lll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11l1lll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l11ll1ll_opy_)
                elif stage.value == STAGE.bstack1l1l1lll1_opy_.value:
                    start_mark: str = bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᳌")
                    end_mark: str = bstack1ll1l11llll_opy_ + bstack11l1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᳍")
                    bstack11l1lll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11l1lll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l11ll1ll_opy_)
            except Exception as e:
                bstack11l1lll1l1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l11ll1ll_opy_)
            return result
        return wrapper
    return decorator