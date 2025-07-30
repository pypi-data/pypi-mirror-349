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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111llll1l1_opy_ import bstack111lll1ll1_opy_, bstack111lll1l11_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1lllll1l1l_opy_
from bstack_utils.helper import bstack1l1lllll1l_opy_, bstack11l11ll11l_opy_, Result
from bstack_utils.bstack111lll11l1_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.capture import bstack111llllll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l111ll111_opy_:
    def __init__(self):
        self.bstack111lll1111_opy_ = bstack111llllll1_opy_(self.bstack11l1111111_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1111111_opy_(log):
        if not (log[bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧໟ")] and log[bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໠")].strip()):
            return
        active = bstack1lllll1l1l_opy_.bstack11l1111l11_opy_()
        log = {
            bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໡"): log[bstack111l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໢")],
            bstack111l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭໣"): bstack11l11ll11l_opy_(),
            bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໤"): log[bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥")],
        }
        if active:
            if active[bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ໦")] == bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ໧"):
                log[bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໨")] = active[bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໩")]
            elif active[bstack111l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ໪")] == bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ໫"):
                log[bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ໬")] = active[bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭໭")]
        bstack1l11l1l1ll_opy_.bstack1ll1llll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll1111_opy_.start()
        driver = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭໮"), None)
        bstack111llll1l1_opy_ = bstack111lll1l11_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11l11ll11l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111l11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ໯"),
            framework=bstack111l11_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩ໰"),
            scope=[attrs.feature.name],
            bstack111lll111l_opy_=bstack1l11l1l1ll_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໱")] = bstack111llll1l1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ໲"), bstack111llll1l1_opy_)
    def end_test(self, attrs):
        bstack111lll1l1l_opy_ = {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ໳"): attrs.feature.name,
            bstack111l11_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ໴"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111llll1l1_opy_ = self.tests[current_test_uuid][bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໵")]
        meta = {
            bstack111l11_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ໶"): bstack111lll1l1l_opy_,
            bstack111l11_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣ໷"): bstack111llll1l1_opy_.meta.get(bstack111l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ໸"), []),
            bstack111l11_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ໹"): {
                bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ໺"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111llll1l1_opy_.bstack111lllll1l_opy_(meta)
        bstack111llll1l1_opy_.bstack11l11111ll_opy_(bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ໻"), []))
        bstack11l11111l1_opy_, exception = self._111llll111_opy_(attrs)
        bstack111ll1lll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111llll1ll_opy_=[bstack11l11111l1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໼")].stop(time=bstack11l11ll11l_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll1lll1_opy_)
        bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ໽"), self.tests[threading.current_thread().current_test_uuid][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໾")])
    def bstack1l1lll1l1l_opy_(self, attrs):
        bstack111ll1llll_opy_ = {
            bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭໿"): uuid4().__str__(),
            bstack111l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬༀ"): attrs.keyword,
            bstack111l11_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ༁"): [],
            bstack111l11_opy_ (u"࠭ࡴࡦࡺࡷࠫ༂"): attrs.name,
            bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ༃"): bstack11l11ll11l_opy_(),
            bstack111l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ༄"): bstack111l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ༅"),
            bstack111l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ༆"): bstack111l11_opy_ (u"ࠫࠬ༇")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ༈")].add_step(bstack111ll1llll_opy_)
        threading.current_thread().current_step_uuid = bstack111ll1llll_opy_[bstack111l11_opy_ (u"࠭ࡩࡥࠩ༉")]
    def bstack11l11l111l_opy_(self, attrs):
        current_test_id = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ༊"), None)
        current_step_uuid = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ་"), None)
        bstack11l11111l1_opy_, exception = self._111llll111_opy_(attrs)
        bstack111ll1lll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111llll1ll_opy_=[bstack11l11111l1_opy_])
        self.tests[current_test_id][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༌")].bstack111lll1lll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll1lll1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1lll1l_opy_(self, name, attrs):
        try:
            bstack111lllll11_opy_ = uuid4().__str__()
            self.tests[bstack111lllll11_opy_] = {}
            self.bstack111lll1111_opy_.start()
            scopes = []
            driver = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ།"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ༎")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111lllll11_opy_)
            if name in [bstack111l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ༏"), bstack111l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༐")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ༑"), bstack111l11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ༒")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ༓")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111lll1ll1_opy_(
                name=name,
                uuid=bstack111lllll11_opy_,
                started_at=bstack11l11ll11l_opy_(),
                file_path=file_path,
                framework=bstack111l11_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ༔"),
                bstack111lll111l_opy_=bstack1l11l1l1ll_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ༕"),
                hook_type=name
            )
            self.tests[bstack111lllll11_opy_][bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ༖")] = hook_data
            current_test_id = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ༗"), None)
            if current_test_id:
                hook_data.bstack11l1111l1l_opy_(current_test_id)
            if name == bstack111l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯༘ࠦ"):
                threading.current_thread().before_all_hook_uuid = bstack111lllll11_opy_
            threading.current_thread().current_hook_uuid = bstack111lllll11_opy_
            bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ༙"), hook_data)
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ༚"), name, e)
    def bstack11l1lll1l1_opy_(self, attrs):
        bstack11l111111l_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༛"), None)
        hook_data = self.tests[bstack11l111111l_opy_][bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༜")]
        status = bstack111l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ༝")
        exception = None
        bstack11l11111l1_opy_ = None
        if hook_data.name == bstack111l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༞"):
            self.bstack111lll1111_opy_.reset()
            bstack111lll11ll_opy_ = self.tests[bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༟"), None)][bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༠")].result.result
            if bstack111lll11ll_opy_ == bstack111l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༡"):
                if attrs.hook_failures == 1:
                    status = bstack111l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ༢")
                elif attrs.hook_failures == 2:
                    status = bstack111l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༣")
            elif attrs.aborted:
                status = bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ༤")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ༥") and attrs.hook_failures == 1:
                status = bstack111l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ༦")
            elif hasattr(attrs, bstack111l11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ༧")) and attrs.error_message:
                status = bstack111l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༨")
            bstack11l11111l1_opy_, exception = self._111llll111_opy_(attrs)
        bstack111ll1lll1_opy_ = Result(result=status, exception=exception, bstack111llll1ll_opy_=[bstack11l11111l1_opy_])
        hook_data.stop(time=bstack11l11ll11l_opy_(), duration=0, result=bstack111ll1lll1_opy_)
        bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ༩"), self.tests[bstack11l111111l_opy_][bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༪")])
        threading.current_thread().current_hook_uuid = None
    def _111llll111_opy_(self, attrs):
        try:
            import traceback
            bstack1l1ll11ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l11111l1_opy_ = bstack1l1ll11ll_opy_[-1] if bstack1l1ll11ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ༫"))
            bstack11l11111l1_opy_ = None
            exception = None
        return bstack11l11111l1_opy_, exception