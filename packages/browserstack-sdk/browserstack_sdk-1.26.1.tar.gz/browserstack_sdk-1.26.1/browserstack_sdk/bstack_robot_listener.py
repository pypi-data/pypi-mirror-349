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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111ll11lll_opy_ import RobotHandler
from bstack_utils.capture import bstack111llll11l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack111ll111l1_opy_, bstack111ll1llll_opy_, bstack111llllll1_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l111l11l_opy_
from bstack_utils.bstack11l1111111_opy_ import bstack1lll11111l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack111l11lll_opy_, bstack1lll11l11_opy_, Result, \
    bstack111l111111_opy_, bstack111l1lllll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ༬"): [],
        bstack11l1lll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭༭"): [],
        bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ༮"): []
    }
    bstack111l11l1l1_opy_ = []
    bstack111l11ll1l_opy_ = []
    @staticmethod
    def bstack111llll111_opy_(log):
        if not ((isinstance(log[bstack11l1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯")], list) or (isinstance(log[bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༰")], dict)) and len(log[bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༱")])>0) or (isinstance(log[bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༲")], str) and log[bstack11l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༳")].strip())):
            return
        active = bstack11l111l11l_opy_.bstack111lll1111_opy_()
        log = {
            bstack11l1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༴"): log[bstack11l1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲ༵ࠧ")],
            bstack11l1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༶"): bstack111l1lllll_opy_().isoformat() + bstack11l1lll_opy_ (u"ࠪ࡞༷ࠬ"),
            bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༸"): log[bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ༹࠭")],
        }
        if active:
            if active[bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ༺")] == bstack11l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ༻"):
                log[bstack11l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༼")] = active[bstack11l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ༽")]
            elif active[bstack11l1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ༾")] == bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ༿"):
                log[bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཀ")] = active[bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ཁ")]
        bstack1lll11111l_opy_.bstack1ll1l1lll_opy_([log])
    def __init__(self):
        self.messages = bstack111ll1ll11_opy_()
        self._111l1lll11_opy_ = None
        self._111l111ll1_opy_ = None
        self._1111llllll_opy_ = OrderedDict()
        self.bstack111lll111l_opy_ = bstack111llll11l_opy_(self.bstack111llll111_opy_)
    @bstack111l111111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1l11_opy_()
        if not self._1111llllll_opy_.get(attrs.get(bstack11l1lll_opy_ (u"ࠧࡪࡦࠪག")), None):
            self._1111llllll_opy_[attrs.get(bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫགྷ"))] = {}
        bstack111l11111l_opy_ = bstack111llllll1_opy_(
                bstack111l1l1l1l_opy_=attrs.get(bstack11l1lll_opy_ (u"ࠩ࡬ࡨࠬང")),
                name=name,
                started_at=bstack1lll11l11_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཅ")], start=os.getcwd()) if attrs.get(bstack11l1lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཆ")) != bstack11l1lll_opy_ (u"ࠬ࠭ཇ") else bstack11l1lll_opy_ (u"࠭ࠧ཈"),
                framework=bstack11l1lll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ཉ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫཊ"), None)
        self._1111llllll_opy_[attrs.get(bstack11l1lll_opy_ (u"ࠩ࡬ࡨࠬཋ"))][bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ཌ")] = bstack111l11111l_opy_
    @bstack111l111111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1l11ll_opy_()
        self._111l1111l1_opy_(messages)
        for bstack1111lllll1_opy_ in self.bstack111l11l1l1_opy_:
            bstack1111lllll1_opy_[bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ཌྷ")][bstack11l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫཎ")].extend(self.store[bstack11l1lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཏ")])
            bstack1lll11111l_opy_.bstack1ll1ll11l_opy_(bstack1111lllll1_opy_)
        self.bstack111l11l1l1_opy_ = []
        self.store[bstack11l1lll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ཐ")] = []
    @bstack111l111111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll111l_opy_.start()
        if not self._1111llllll_opy_.get(attrs.get(bstack11l1lll_opy_ (u"ࠨ࡫ࡧࠫད")), None):
            self._1111llllll_opy_[attrs.get(bstack11l1lll_opy_ (u"ࠩ࡬ࡨࠬདྷ"))] = {}
        driver = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩན"), None)
        bstack111lll11ll_opy_ = bstack111llllll1_opy_(
            bstack111l1l1l1l_opy_=attrs.get(bstack11l1lll_opy_ (u"ࠫ࡮ࡪࠧཔ")),
            name=name,
            started_at=bstack1lll11l11_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1lll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཕ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l1lll1l_opy_(attrs.get(bstack11l1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭བ"), None)),
            framework=bstack11l1lll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭བྷ"),
            tags=attrs[bstack11l1lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭མ")],
            hooks=self.store[bstack11l1lll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨཙ")],
            bstack111lllllll_opy_=bstack1lll11111l_opy_.bstack11l111111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1lll_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧཚ").format(bstack11l1lll_opy_ (u"ࠦࠥࠨཛ").join(attrs[bstack11l1lll_opy_ (u"ࠬࡺࡡࡨࡵࠪཛྷ")]), name) if attrs[bstack11l1lll_opy_ (u"࠭ࡴࡢࡩࡶࠫཝ")] else name
        )
        self._1111llllll_opy_[attrs.get(bstack11l1lll_opy_ (u"ࠧࡪࡦࠪཞ"))][bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫཟ")] = bstack111lll11ll_opy_
        threading.current_thread().current_test_uuid = bstack111lll11ll_opy_.bstack111l1l1111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1lll_opy_ (u"ࠩ࡬ࡨࠬའ"), None)
        self.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫཡ"), bstack111lll11ll_opy_)
    @bstack111l111111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll111l_opy_.reset()
        bstack111l11l11l_opy_ = bstack111l111lll_opy_.get(attrs.get(bstack11l1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫར")), bstack11l1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ལ"))
        self._1111llllll_opy_[attrs.get(bstack11l1lll_opy_ (u"࠭ࡩࡥࠩཤ"))][bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཥ")].stop(time=bstack1lll11l11_opy_(), duration=int(attrs.get(bstack11l1lll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ས"), bstack11l1lll_opy_ (u"ࠩ࠳ࠫཧ"))), result=Result(result=bstack111l11l11l_opy_, exception=attrs.get(bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཨ")), bstack111lll1l11_opy_=[attrs.get(bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཀྵ"))]))
        self.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧཪ"), self._1111llllll_opy_[attrs.get(bstack11l1lll_opy_ (u"࠭ࡩࡥࠩཫ"))][bstack11l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཬ")], True)
        self.store[bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ཭")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l111111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1l11_opy_()
        current_test_id = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ཮"), None)
        bstack111l1111ll_opy_ = current_test_id if bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ཯"), None) else bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ཰"), None)
        if attrs.get(bstack11l1lll_opy_ (u"ࠬࡺࡹࡱࡧཱࠪ"), bstack11l1lll_opy_ (u"ི࠭ࠧ")).lower() in [bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵཱི࠭"), bstack11l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰུࠪ")]:
            hook_type = bstack111ll11111_opy_(attrs.get(bstack11l1lll_opy_ (u"ࠩࡷࡽࡵ࡫ཱུࠧ")), bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧྲྀ"), None))
            hook_name = bstack11l1lll_opy_ (u"ࠫࢀࢃࠧཷ").format(attrs.get(bstack11l1lll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬླྀ"), bstack11l1lll_opy_ (u"࠭ࠧཹ")))
            if hook_type in [bstack11l1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏེࠫ"), bstack11l1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏཻࠫ")]:
                hook_name = bstack11l1lll_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿོࠪ").format(bstack111l11ll11_opy_.get(hook_type), attrs.get(bstack11l1lll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧཽࠪ"), bstack11l1lll_opy_ (u"ࠫࠬཾ")))
            bstack111l1llll1_opy_ = bstack111ll1llll_opy_(
                bstack111l1l1l1l_opy_=bstack111l1111ll_opy_ + bstack11l1lll_opy_ (u"ࠬ࠳ࠧཿ") + attrs.get(bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨྀࠫ"), bstack11l1lll_opy_ (u"ࠧࠨཱྀ")).lower(),
                name=hook_name,
                started_at=bstack1lll11l11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྂ")), start=os.getcwd()),
                framework=bstack11l1lll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨྃ"),
                tags=attrs[bstack11l1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ྄")],
                scope=RobotHandler.bstack111l1lll1l_opy_(attrs.get(bstack11l1lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ྅"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1llll1_opy_.bstack111l1l1111_opy_()
            threading.current_thread().current_hook_id = bstack111l1111ll_opy_ + bstack11l1lll_opy_ (u"ࠬ࠳ࠧ྆") + attrs.get(bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ྇"), bstack11l1lll_opy_ (u"ࠧࠨྈ")).lower()
            self.store[bstack11l1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬྉ")] = [bstack111l1llll1_opy_.bstack111l1l1111_opy_()]
            if bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ྊ"), None):
                self.store[bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྋ")].append(bstack111l1llll1_opy_.bstack111l1l1111_opy_())
            else:
                self.store[bstack11l1lll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪྌ")].append(bstack111l1llll1_opy_.bstack111l1l1111_opy_())
            if bstack111l1111ll_opy_:
                self._1111llllll_opy_[bstack111l1111ll_opy_ + bstack11l1lll_opy_ (u"ࠬ࠳ࠧྍ") + attrs.get(bstack11l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫྎ"), bstack11l1lll_opy_ (u"ࠧࠨྏ")).lower()] = { bstack11l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྐ"): bstack111l1llll1_opy_ }
            bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪྑ"), bstack111l1llll1_opy_)
        else:
            bstack111llll1l1_opy_ = {
                bstack11l1lll_opy_ (u"ࠪ࡭ࡩ࠭ྒ"): uuid4().__str__(),
                bstack11l1lll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩྒྷ"): bstack11l1lll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫྔ").format(attrs.get(bstack11l1lll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ྕ")), attrs.get(bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬྖ"), bstack11l1lll_opy_ (u"ࠨࠩྗ"))) if attrs.get(bstack11l1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ྘"), []) else attrs.get(bstack11l1lll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྙ")),
                bstack11l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫྚ"): attrs.get(bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪྛ"), []),
                bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪྜ"): bstack1lll11l11_opy_(),
                bstack11l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧྜྷ"): bstack11l1lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩྞ"),
                bstack11l1lll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧྟ"): attrs.get(bstack11l1lll_opy_ (u"ࠪࡨࡴࡩࠧྠ"), bstack11l1lll_opy_ (u"ࠫࠬྡ"))
            }
            if attrs.get(bstack11l1lll_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ྡྷ"), bstack11l1lll_opy_ (u"࠭ࠧྣ")) != bstack11l1lll_opy_ (u"ࠧࠨྤ"):
                bstack111llll1l1_opy_[bstack11l1lll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩྥ")] = attrs.get(bstack11l1lll_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪྦ"))
            if not self.bstack111l11ll1l_opy_:
                self._1111llllll_opy_[self._111l1ll1ll_opy_()][bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྦྷ")].add_step(bstack111llll1l1_opy_)
                threading.current_thread().current_step_uuid = bstack111llll1l1_opy_[bstack11l1lll_opy_ (u"ࠫ࡮ࡪࠧྨ")]
            self.bstack111l11ll1l_opy_.append(bstack111llll1l1_opy_)
    @bstack111l111111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1l11ll_opy_()
        self._111l1111l1_opy_(messages)
        current_test_id = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧྩ"), None)
        bstack111l1111ll_opy_ = current_test_id if current_test_id else bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩྪ"), None)
        bstack111ll1l11l_opy_ = bstack111l111lll_opy_.get(attrs.get(bstack11l1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྫ")), bstack11l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩྫྷ"))
        bstack111ll11l11_opy_ = attrs.get(bstack11l1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྭ"))
        if bstack111ll1l11l_opy_ != bstack11l1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫྮ") and not attrs.get(bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྯ")) and self._111l1lll11_opy_:
            bstack111ll11l11_opy_ = self._111l1lll11_opy_
        bstack111lllll1l_opy_ = Result(result=bstack111ll1l11l_opy_, exception=bstack111ll11l11_opy_, bstack111lll1l11_opy_=[bstack111ll11l11_opy_])
        if attrs.get(bstack11l1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪྰ"), bstack11l1lll_opy_ (u"࠭ࠧྱ")).lower() in [bstack11l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ྲ"), bstack11l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪླ")]:
            bstack111l1111ll_opy_ = current_test_id if current_test_id else bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬྴ"), None)
            if bstack111l1111ll_opy_:
                bstack11l11111l1_opy_ = bstack111l1111ll_opy_ + bstack11l1lll_opy_ (u"ࠥ࠱ࠧྵ") + attrs.get(bstack11l1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩྶ"), bstack11l1lll_opy_ (u"ࠬ࠭ྷ")).lower()
                self._1111llllll_opy_[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྸ")].stop(time=bstack1lll11l11_opy_(), duration=int(attrs.get(bstack11l1lll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬྐྵ"), bstack11l1lll_opy_ (u"ࠨ࠲ࠪྺ"))), result=bstack111lllll1l_opy_)
                bstack1lll11111l_opy_.bstack111llll1ll_opy_(bstack11l1lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫྻ"), self._1111llllll_opy_[bstack11l11111l1_opy_][bstack11l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྼ")])
        else:
            bstack111l1111ll_opy_ = current_test_id if current_test_id else bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭྽"), None)
            if bstack111l1111ll_opy_ and len(self.bstack111l11ll1l_opy_) == 1:
                current_step_uuid = bstack111l11lll_opy_(threading.current_thread(), bstack11l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ྾"), None)
                self._1111llllll_opy_[bstack111l1111ll_opy_][bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ྿")].bstack11l1111l11_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1lll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ࿀"), bstack11l1lll_opy_ (u"ࠨ࠲ࠪ࿁"))), result=bstack111lllll1l_opy_)
            else:
                self.bstack111l111l1l_opy_(attrs)
            self.bstack111l11ll1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l1lll_opy_ (u"ࠩ࡫ࡸࡲࡲࠧ࿂"), bstack11l1lll_opy_ (u"ࠪࡲࡴ࠭࿃")) == bstack11l1lll_opy_ (u"ࠫࡾ࡫ࡳࠨ࿄"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l111l11l_opy_.bstack111lll1111_opy_():
                logs.append({
                    bstack11l1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ࿅"): bstack1lll11l11_opy_(),
                    bstack11l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫࿆ࠧ"): message.get(bstack11l1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿇")),
                    bstack11l1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿈"): message.get(bstack11l1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿉")),
                    **bstack11l111l11l_opy_.bstack111lll1111_opy_()
                })
                if len(logs) > 0:
                    bstack1lll11111l_opy_.bstack1ll1l1lll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1lll11111l_opy_.bstack111ll11l1l_opy_()
    def bstack111l111l1l_opy_(self, bstack111ll1l111_opy_):
        if not bstack11l111l11l_opy_.bstack111lll1111_opy_():
            return
        kwname = bstack11l1lll_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩ࿊").format(bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ࿋")), bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿌"), bstack11l1lll_opy_ (u"࠭ࠧ࿍"))) if bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿎"), []) else bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿏"))
        error_message = bstack11l1lll_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣ࿐").format(kwname, bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿑")), str(bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿒"))))
        bstack111ll1l1l1_opy_ = bstack11l1lll_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ࿓").format(kwname, bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿔")))
        bstack111l1l111l_opy_ = error_message if bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿕")) else bstack111ll1l1l1_opy_
        bstack111l11llll_opy_ = {
            bstack11l1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ࿖"): self.bstack111l11ll1l_opy_[-1].get(bstack11l1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭࿗"), bstack1lll11l11_opy_()),
            bstack11l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿘"): bstack111l1l111l_opy_,
            bstack11l1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿙"): bstack11l1lll_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ࿚") if bstack111ll1l111_opy_.get(bstack11l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿛")) == bstack11l1lll_opy_ (u"ࠧࡇࡃࡌࡐࠬ࿜") else bstack11l1lll_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿝"),
            **bstack11l111l11l_opy_.bstack111lll1111_opy_()
        }
        bstack1lll11111l_opy_.bstack1ll1l1lll_opy_([bstack111l11llll_opy_])
    def _111l1ll1ll_opy_(self):
        for bstack111l1l1l1l_opy_ in reversed(self._1111llllll_opy_):
            bstack111l1ll11l_opy_ = bstack111l1l1l1l_opy_
            data = self._1111llllll_opy_[bstack111l1l1l1l_opy_][bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿞")]
            if isinstance(data, bstack111ll1llll_opy_):
                if not bstack11l1lll_opy_ (u"ࠪࡉࡆࡉࡈࠨ࿟") in data.bstack111ll111ll_opy_():
                    return bstack111l1ll11l_opy_
            else:
                return bstack111l1ll11l_opy_
    def _111l1111l1_opy_(self, messages):
        try:
            bstack111l1l1ll1_opy_ = BuiltIn().get_variable_value(bstack11l1lll_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ࿠")) in (bstack111ll1l1ll_opy_.DEBUG, bstack111ll1l1ll_opy_.TRACE)
            for message, bstack111ll11ll1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿡"))
                level = message.get(bstack11l1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ࿢"))
                if level == bstack111ll1l1ll_opy_.FAIL:
                    self._111l1lll11_opy_ = name or self._111l1lll11_opy_
                    self._111l111ll1_opy_ = bstack111ll11ll1_opy_.get(bstack11l1lll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ࿣")) if bstack111l1l1ll1_opy_ and bstack111ll11ll1_opy_ else self._111l111ll1_opy_
        except:
            pass
    @classmethod
    def bstack111llll1ll_opy_(self, event: str, bstack111l11l111_opy_: bstack111ll111l1_opy_, bstack111l11lll1_opy_=False):
        if event == bstack11l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿤"):
            bstack111l11l111_opy_.set(hooks=self.store[bstack11l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿥")])
        if event == bstack11l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ࿦"):
            event = bstack11l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭࿧")
        if bstack111l11lll1_opy_:
            bstack111l11l1ll_opy_ = {
                bstack11l1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ࿨"): event,
                bstack111l11l111_opy_.bstack111l1l1lll_opy_(): bstack111l11l111_opy_.bstack111l1ll1l1_opy_(event)
            }
            self.bstack111l11l1l1_opy_.append(bstack111l11l1ll_opy_)
        else:
            bstack1lll11111l_opy_.bstack111llll1ll_opy_(event, bstack111l11l111_opy_)
class bstack111ll1ll11_opy_:
    def __init__(self):
        self._111ll1111l_opy_ = []
    def bstack111l1l1l11_opy_(self):
        self._111ll1111l_opy_.append([])
    def bstack111l1l11ll_opy_(self):
        return self._111ll1111l_opy_.pop() if self._111ll1111l_opy_ else list()
    def push(self, message):
        self._111ll1111l_opy_[-1].append(message) if self._111ll1111l_opy_ else self._111ll1111l_opy_.append([message])
class bstack111ll1l1ll_opy_:
    FAIL = bstack11l1lll_opy_ (u"࠭ࡆࡂࡋࡏࠫ࿩")
    ERROR = bstack11l1lll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭࿪")
    WARNING = bstack11l1lll_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭࿫")
    bstack111l1l11l1_opy_ = bstack11l1lll_opy_ (u"ࠩࡌࡒࡋࡕࠧ࿬")
    DEBUG = bstack11l1lll_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩ࿭")
    TRACE = bstack11l1lll_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪ࿮")
    bstack111l1ll111_opy_ = [FAIL, ERROR]
def bstack111l111l11_opy_(bstack1111llll1l_opy_):
    if not bstack1111llll1l_opy_:
        return None
    if bstack1111llll1l_opy_.get(bstack11l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿯"), None):
        return getattr(bstack1111llll1l_opy_[bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿰")], bstack11l1lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ࿱"), None)
    return bstack1111llll1l_opy_.get(bstack11l1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭࿲"), None)
def bstack111ll11111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ࿳"), bstack11l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ࿴")]:
        return
    if hook_type.lower() == bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ࿵"):
        if current_test_uuid is None:
            return bstack11l1lll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ࿶")
        else:
            return bstack11l1lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ࿷")
    elif hook_type.lower() == bstack11l1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿸"):
        if current_test_uuid is None:
            return bstack11l1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ࿹")
        else:
            return bstack11l1lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭࿺")