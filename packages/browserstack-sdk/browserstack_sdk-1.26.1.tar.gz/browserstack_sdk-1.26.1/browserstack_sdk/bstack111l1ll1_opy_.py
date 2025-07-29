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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111lll11ll_opy_ import bstack111ll1llll_opy_, bstack111llllll1_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l111l11l_opy_
from bstack_utils.helper import bstack111l11lll_opy_, bstack1lll11l11_opy_, Result
from bstack_utils.bstack11l1111111_opy_ import bstack1lll11111l_opy_
from bstack_utils.capture import bstack111llll11l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack111l1ll1_opy_:
    def __init__(self):
        self.bstack111lll111l_opy_ = bstack111llll11l_opy_(self.bstack111llll111_opy_)
        self.tests = {}
    @staticmethod
    def bstack111llll111_opy_(log):
        if not (log[bstack11l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧໟ")] and log[bstack11l1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໠")].strip()):
            return
        active = bstack11l111l11l_opy_.bstack111lll1111_opy_()
        log = {
            bstack11l1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໡"): log[bstack11l1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໢")],
            bstack11l1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭໣"): bstack1lll11l11_opy_(),
            bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໤"): log[bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥")],
        }
        if active:
            if active[bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ໦")] == bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ໧"):
                log[bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໨")] = active[bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໩")]
            elif active[bstack11l1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ໪")] == bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ໫"):
                log[bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ໬")] = active[bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭໭")]
        bstack1lll11111l_opy_.bstack1ll1l1lll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll111l_opy_.start()
        driver = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭໮"), None)
        bstack111lll11ll_opy_ = bstack111llllll1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1lll11l11_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11l1lll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ໯"),
            framework=bstack11l1lll_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩ໰"),
            scope=[attrs.feature.name],
            bstack111lllllll_opy_=bstack1lll11111l_opy_.bstack11l111111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໱")] = bstack111lll11ll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ໲"), bstack111lll11ll_opy_)
    def end_test(self, attrs):
        bstack111lllll11_opy_ = {
            bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ໳"): attrs.feature.name,
            bstack11l1lll_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ໴"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111lll11ll_opy_ = self.tests[current_test_uuid][bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໵")]
        meta = {
            bstack11l1lll_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ໶"): bstack111lllll11_opy_,
            bstack11l1lll_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣ໷"): bstack111lll11ll_opy_.meta.get(bstack11l1lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ໸"), []),
            bstack11l1lll_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ໹"): {
                bstack11l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ໺"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111lll11ll_opy_.bstack111ll1ll1l_opy_(meta)
        bstack111lll11ll_opy_.bstack111lll1ll1_opy_(bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ໻"), []))
        bstack111lll1lll_opy_, exception = self._11l1111l1l_opy_(attrs)
        bstack111lllll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack111lll1l11_opy_=[bstack111lll1lll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໼")].stop(time=bstack1lll11l11_opy_(), duration=int(attrs.duration)*1000, result=bstack111lllll1l_opy_)
        bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ໽"), self.tests[threading.current_thread().current_test_uuid][bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໾")])
    def bstack1111ll1l1_opy_(self, attrs):
        bstack111llll1l1_opy_ = {
            bstack11l1lll_opy_ (u"ࠪ࡭ࡩ࠭໿"): uuid4().__str__(),
            bstack11l1lll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬༀ"): attrs.keyword,
            bstack11l1lll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ༁"): [],
            bstack11l1lll_opy_ (u"࠭ࡴࡦࡺࡷࠫ༂"): attrs.name,
            bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ༃"): bstack1lll11l11_opy_(),
            bstack11l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ༄"): bstack11l1lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ༅"),
            bstack11l1lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ༆"): bstack11l1lll_opy_ (u"ࠫࠬ༇")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ༈")].add_step(bstack111llll1l1_opy_)
        threading.current_thread().current_step_uuid = bstack111llll1l1_opy_[bstack11l1lll_opy_ (u"࠭ࡩࡥࠩ༉")]
    def bstack11111l11_opy_(self, attrs):
        current_test_id = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ༊"), None)
        current_step_uuid = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ་"), None)
        bstack111lll1lll_opy_, exception = self._11l1111l1l_opy_(attrs)
        bstack111lllll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack111lll1l11_opy_=[bstack111lll1lll_opy_])
        self.tests[current_test_id][bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༌")].bstack11l1111l11_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111lllll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11lll1111l_opy_(self, name, attrs):
        try:
            bstack111ll1lll1_opy_ = uuid4().__str__()
            self.tests[bstack111ll1lll1_opy_] = {}
            self.bstack111lll111l_opy_.start()
            scopes = []
            driver = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ།"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ༎")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111ll1lll1_opy_)
            if name in [bstack11l1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ༏"), bstack11l1lll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༐")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ༑"), bstack11l1lll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ༒")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11l1lll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ༓")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111ll1llll_opy_(
                name=name,
                uuid=bstack111ll1lll1_opy_,
                started_at=bstack1lll11l11_opy_(),
                file_path=file_path,
                framework=bstack11l1lll_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ༔"),
                bstack111lllllll_opy_=bstack1lll11111l_opy_.bstack11l111111l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11l1lll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ༕"),
                hook_type=name
            )
            self.tests[bstack111ll1lll1_opy_][bstack11l1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ༖")] = hook_data
            current_test_id = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ༗"), None)
            if current_test_id:
                hook_data.bstack111lll1l1l_opy_(current_test_id)
            if name == bstack11l1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯༘ࠦ"):
                threading.current_thread().before_all_hook_uuid = bstack111ll1lll1_opy_
            threading.current_thread().current_hook_uuid = bstack111ll1lll1_opy_
            bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ༙"), hook_data)
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ༚"), name, e)
    def bstack111ll11l1_opy_(self, attrs):
        bstack11l11111l1_opy_ = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༛"), None)
        hook_data = self.tests[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༜")]
        status = bstack11l1lll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ༝")
        exception = None
        bstack111lll1lll_opy_ = None
        if hook_data.name == bstack11l1lll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༞"):
            self.bstack111lll111l_opy_.reset()
            bstack111lll11l1_opy_ = self.tests[bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༟"), None)][bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༠")].result.result
            if bstack111lll11l1_opy_ == bstack11l1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༡"):
                if attrs.hook_failures == 1:
                    status = bstack11l1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ༢")
                elif attrs.hook_failures == 2:
                    status = bstack11l1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༣")
            elif attrs.aborted:
                status = bstack11l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ༤")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11l1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ༥") and attrs.hook_failures == 1:
                status = bstack11l1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ༦")
            elif hasattr(attrs, bstack11l1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ༧")) and attrs.error_message:
                status = bstack11l1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༨")
            bstack111lll1lll_opy_, exception = self._11l1111l1l_opy_(attrs)
        bstack111lllll1l_opy_ = Result(result=status, exception=exception, bstack111lll1l11_opy_=[bstack111lll1lll_opy_])
        hook_data.stop(time=bstack1lll11l11_opy_(), duration=0, result=bstack111lllll1l_opy_)
        bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ༩"), self.tests[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༪")])
        threading.current_thread().current_hook_uuid = None
    def _11l1111l1l_opy_(self, attrs):
        try:
            import traceback
            bstack1ll111llll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111lll1lll_opy_ = bstack1ll111llll_opy_[-1] if bstack1ll111llll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ༫"))
            bstack111lll1lll_opy_ = None
            exception = None
        return bstack111lll1lll_opy_, exception