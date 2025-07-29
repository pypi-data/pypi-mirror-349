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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11l1l11l_opy_
from browserstack_sdk.bstack1ll1ll1l11_opy_ import bstack11ll1l111l_opy_
def _11l111l1111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111l1lll_opy_:
    def __init__(self, handler):
        self._11l1111llll_opy_ = {}
        self._11l111l111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11ll1l111l_opy_.version()
        if bstack11l11l1l11l_opy_(pytest_version, bstack11l1lll_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᱞ")) >= 0:
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱟ")] = Module._register_setup_function_fixture
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱠ")] = Module._register_setup_module_fixture
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱡ")] = Class._register_setup_class_fixture
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᱢ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱣ"))
            Module._register_setup_module_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᱤ"))
            Class._register_setup_class_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᱥ"))
            Class._register_setup_method_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᱦ"))
        else:
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᱧ")] = Module._inject_setup_function_fixture
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱨ")] = Module._inject_setup_module_fixture
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᱩ")] = Class._inject_setup_class_fixture
            self._11l1111llll_opy_[bstack11l1lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᱪ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᱫ"))
            Module._inject_setup_module_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱬ"))
            Class._inject_setup_class_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᱭ"))
            Class._inject_setup_method_fixture = self.bstack11l111l1l11_opy_(bstack11l1lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᱮ"))
    def bstack11l111l11l1_opy_(self, bstack11l111ll1l1_opy_, hook_type):
        bstack11l111ll111_opy_ = id(bstack11l111ll1l1_opy_.__class__)
        if (bstack11l111ll111_opy_, hook_type) in self._11l111l111l_opy_:
            return
        meth = getattr(bstack11l111ll1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l111l111l_opy_[(bstack11l111ll111_opy_, hook_type)] = meth
            setattr(bstack11l111ll1l1_opy_, hook_type, self.bstack11l111ll11l_opy_(hook_type, bstack11l111ll111_opy_))
    def bstack11l1111lll1_opy_(self, instance, bstack11l1111ll1l_opy_):
        if bstack11l1111ll1l_opy_ == bstack11l1lll_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᱯ"):
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᱰ"))
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᱱ"))
        if bstack11l1111ll1l_opy_ == bstack11l1lll_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᱲ"):
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᱳ"))
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᱴ"))
        if bstack11l1111ll1l_opy_ == bstack11l1lll_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᱵ"):
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᱶ"))
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᱷ"))
        if bstack11l1111ll1l_opy_ == bstack11l1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᱸ"):
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᱹ"))
            self.bstack11l111l11l1_opy_(instance.obj, bstack11l1lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᱺ"))
    @staticmethod
    def bstack11l111l1l1l_opy_(hook_type, func, args):
        if hook_type in [bstack11l1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᱻ"), bstack11l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᱼ")]:
            _11l111l1111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l111ll11l_opy_(self, hook_type, bstack11l111ll111_opy_):
        def bstack11l111l11ll_opy_(arg=None):
            self.handler(hook_type, bstack11l1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᱽ"))
            result = None
            try:
                bstack111111111l_opy_ = self._11l111l111l_opy_[(bstack11l111ll111_opy_, hook_type)]
                self.bstack11l111l1l1l_opy_(hook_type, bstack111111111l_opy_, (arg,))
                result = Result(result=bstack11l1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᱾"))
            except Exception as e:
                result = Result(result=bstack11l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᱿"), exception=e)
                self.handler(hook_type, bstack11l1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᲀ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᲁ"), result)
        def bstack11l1111ll11_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᲂ"))
            result = None
            exception = None
            try:
                self.bstack11l111l1l1l_opy_(hook_type, self._11l111l111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᲃ"))
            except Exception as e:
                result = Result(result=bstack11l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᲄ"), exception=e)
                self.handler(hook_type, bstack11l1lll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᲅ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᲆ"), result)
        if hook_type in [bstack11l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᲇ"), bstack11l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᲈ")]:
            return bstack11l1111ll11_opy_
        return bstack11l111l11ll_opy_
    def bstack11l111l1l11_opy_(self, bstack11l1111ll1l_opy_):
        def bstack11l111l1ll1_opy_(this, *args, **kwargs):
            self.bstack11l1111lll1_opy_(this, bstack11l1111ll1l_opy_)
            self._11l1111llll_opy_[bstack11l1111ll1l_opy_](this, *args, **kwargs)
        return bstack11l111l1ll1_opy_