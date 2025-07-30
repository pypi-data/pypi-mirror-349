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
from browserstack_sdk.bstack111lll1l_opy_ import bstack11l1lll11_opy_
from browserstack_sdk.bstack111l111l11_opy_ import RobotHandler
def bstack1ll1l11ll1_opy_(framework):
    if framework.lower() == bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᨧ"):
        return bstack11l1lll11_opy_.version()
    elif framework.lower() == bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᨨ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᨩ"):
        import behave
        return behave.__version__
    else:
        return bstack111l11_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᨪ")
def bstack1111l1ll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack111l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᨫ"))
        framework_version.append(importlib.metadata.version(bstack111l11_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᨬ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᨭ"))
        framework_version.append(importlib.metadata.version(bstack111l11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᨮ")))
    except:
        pass
    return {
        bstack111l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᨯ"): bstack111l11_opy_ (u"ࠬࡥࠧᨰ").join(framework_name),
        bstack111l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᨱ"): bstack111l11_opy_ (u"ࠧࡠࠩᨲ").join(framework_version)
    }