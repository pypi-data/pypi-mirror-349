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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l11111l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l111111_opy_, bstack1ll1lll1ll_opy_, update, bstack11l1lll1ll_opy_,
                                       bstack11l111l1l_opy_, bstack11l1ll1ll_opy_, bstack1l111111l_opy_, bstack1l1lll1ll1_opy_,
                                       bstack11111lll1_opy_, bstack1lll1ll1l1_opy_, bstack1111111l1_opy_, bstack1ll111l1ll_opy_,
                                       bstack11l1l11l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1ll1l1ll_opy_)
from browserstack_sdk.bstack111lll1l_opy_ import bstack11l1lll11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1lll111lll_opy_
from bstack_utils.capture import bstack111llllll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11llllll_opy_, bstack11l1ll111_opy_, bstack1ll11ll11l_opy_, \
    bstack11lll1lll_opy_
from bstack_utils.helper import bstack1l1lllll1l_opy_, bstack11l1l1l1111_opy_, bstack111l1l1111_opy_, bstack11l11ll11_opy_, bstack1ll1111llll_opy_, bstack11l11ll11l_opy_, \
    bstack11l1lll111l_opy_, \
    bstack11l1ll1111l_opy_, bstack11l1lll1l_opy_, bstack1l1ll11l11_opy_, bstack11l1llll1l1_opy_, bstack11l11l11_opy_, Notset, \
    bstack1l1l1llll1_opy_, bstack11l11l1ll1l_opy_, bstack11l111llll1_opy_, Result, bstack11l1ll1l111_opy_, bstack11l111ll1l1_opy_, bstack111l11111l_opy_, \
    bstack1lll11l11l_opy_, bstack11111llll_opy_, bstack1l1llll1_opy_, bstack11l1l1l1ll1_opy_
from bstack_utils.bstack11l1111l1l1_opy_ import bstack11l111l11l1_opy_
from bstack_utils.messages import bstack1l1l1lll11_opy_, bstack1l1ll11l_opy_, bstack1lll1llll_opy_, bstack111l11ll1_opy_, bstack11l11ll1l1_opy_, \
    bstack11llll11l_opy_, bstack11l11l1ll1_opy_, bstack11llllll11_opy_, bstack111lll1l1_opy_, bstack1l11111l1l_opy_, \
    bstack11l1lllll1_opy_, bstack111l11l11_opy_
from bstack_utils.proxy import bstack11lllllll_opy_, bstack1ll1l1l111_opy_
from bstack_utils.bstack1l1l1111ll_opy_ import bstack111l1111lll_opy_, bstack111l1111l11_opy_, bstack111l11111l1_opy_, bstack1111llllll1_opy_, \
    bstack111l111l1l1_opy_, bstack111l11111ll_opy_, bstack111l1111l1l_opy_, bstack1l1ll1111l_opy_, bstack111l111l11l_opy_
from bstack_utils.bstack1lll11ll1l_opy_ import bstack1ll1l1l11_opy_
from bstack_utils.bstack1l11lll11l_opy_ import bstack1l11l111ll_opy_, bstack11111ll1l_opy_, bstack1l1ll1l111_opy_, \
    bstack11ll11l11_opy_, bstack11ll11ll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack111lll1l11_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack1lllll1l1l_opy_
import bstack_utils.accessibility as bstack11lll1ll1_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.bstack11111ll1_opy_ import bstack11111ll1_opy_
from browserstack_sdk.__init__ import bstack1ll111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l_opy_ import bstack1ll11l11l_opy_, bstack1l1111l1ll_opy_, bstack11l1l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111l111l1_opy_, bstack1lll1l111ll_opy_, bstack1llll1lll1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll11l11l_opy_ import bstack1ll11l11l_opy_, bstack1l1111l1ll_opy_, bstack11l1l1l1ll_opy_
bstack11ll11lll1_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack1111ll11l_opy_ = None
bstack1l1l11ll_opy_ = None
bstack111111ll_opy_ = None
bstack1l1111llll_opy_ = None
bstack111l1lll1_opy_ = None
bstack1l11ll11l1_opy_ = None
bstack1lll11l1l_opy_ = None
bstack11llll1ll1_opy_ = None
bstack1llll11ll1_opy_ = None
bstack1lllll1lll_opy_ = None
bstack1ll11l1l11_opy_ = None
bstack11llllllll_opy_ = bstack111l11_opy_ (u"࠭ࠧ‒")
CONFIG = {}
bstack1ll11ll11_opy_ = False
bstack1ll11l1l_opy_ = bstack111l11_opy_ (u"ࠧࠨ–")
bstack1l11l11111_opy_ = bstack111l11_opy_ (u"ࠨࠩ—")
bstack11lll1l11_opy_ = False
bstack11111l1l_opy_ = []
bstack1lll1l1l11_opy_ = bstack11llllll_opy_
bstack111111l1111_opy_ = bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ―")
bstack1l1llll111_opy_ = {}
bstack11lll11lll_opy_ = None
bstack1l1111111_opy_ = False
logger = bstack1lll111lll_opy_.get_logger(__name__, bstack1lll1l1l11_opy_)
store = {
    bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ‖"): []
}
bstack11111l111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111ll1l1ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111l111l1_opy_(
    test_framework_name=bstack1ll1l11lll_opy_[bstack111l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨ‗")] if bstack11l11l11_opy_() else bstack1ll1l11lll_opy_[bstack111l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬ‘")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack111l1l11_opy_(page, bstack11111l11l_opy_):
    try:
        page.evaluate(bstack111l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ’"),
                      bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ‚") + json.dumps(
                          bstack11111l11l_opy_) + bstack111l11_opy_ (u"ࠣࡿࢀࠦ‛"))
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ“"), e)
def bstack1lllll1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack111l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ”"), bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ„") + json.dumps(
            message) + bstack111l11_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ‟") + json.dumps(level) + bstack111l11_opy_ (u"࠭ࡽࡾࠩ†"))
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ‡"), e)
def pytest_configure(config):
    global bstack1ll11l1l_opy_
    global CONFIG
    bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
    config.args = bstack1lllll1l1l_opy_.bstack11111l11ll1_opy_(config.args)
    bstack111l111ll_opy_.bstack11ll11ll11_opy_(bstack1l1llll1_opy_(config.getoption(bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ•"))))
    try:
        bstack1lll111lll_opy_.bstack11l11111ll1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.CONNECT, bstack11l1l1l1ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ‣"), bstack111l11_opy_ (u"ࠪ࠴ࠬ․")))
        config = json.loads(os.environ.get(bstack111l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ‥"), bstack111l11_opy_ (u"ࠧࢁࡽࠣ…")))
        cli.bstack1lllll11111_opy_(bstack1l1ll11l11_opy_(bstack1ll11l1l_opy_, CONFIG), cli_context.platform_index, bstack11l1lll1ll_opy_)
    if cli.bstack1llll1111ll_opy_(bstack1lll1l111l1_opy_):
        cli.bstack1lllll11l11_opy_()
        logger.debug(bstack111l11_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ‧") + str(cli_context.platform_index) + bstack111l11_opy_ (u"ࠢࠣ "))
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.BEFORE_ALL, bstack1llll1lll1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack111l11_opy_ (u"ࠣࡹ࡫ࡩࡳࠨ "), None)
    if cli.is_running() and when == bstack111l11_opy_ (u"ࠤࡦࡥࡱࡲࠢ‪"):
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.LOG_REPORT, bstack1llll1lll1l_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack111l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ‫"):
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.POST, item, call, outcome)
        elif when == bstack111l11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ‬"):
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.LOG_REPORT, bstack1llll1lll1l_opy_.POST, item, call, outcome)
        elif when == bstack111l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ‭"):
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.AFTER_EACH, bstack1llll1lll1l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111111l1ll_opy_
    skipSessionName = item.config.getoption(bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ‮"))
    plugins = item.config.getoption(bstack111l11_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣ "))
    report = outcome.get_result()
    bstack111111llll1_opy_(item, call, report)
    if bstack111l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨ‰") not in plugins or bstack11l11l11_opy_():
        return
    summary = []
    driver = getattr(item, bstack111l11_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥ‱"), None)
    page = getattr(item, bstack111l11_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤ′"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack111111l11l1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack111111ll111_opy_(item, report, summary, skipSessionName)
def bstack111111l11l1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ″") and report.skipped:
        bstack111l111l11l_opy_(report)
    if report.when in [bstack111l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ‴"), bstack111l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ‵")]:
        return
    if not bstack1ll1111llll_opy_():
        return
    try:
        if (str(skipSessionName).lower() != bstack111l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ‶") and not cli.is_running()):
            item._driver.execute_script(
                bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭‷") + json.dumps(
                    report.nodeid) + bstack111l11_opy_ (u"ࠩࢀࢁࠬ‸"))
        os.environ[bstack111l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭‹")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦ›").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ※")))
    bstack1l111111ll_opy_ = bstack111l11_opy_ (u"ࠨࠢ‼")
    bstack111l111l11l_opy_(report)
    if not passed:
        try:
            bstack1l111111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ‽").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l111111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ‾")))
        bstack1l111111ll_opy_ = bstack111l11_opy_ (u"ࠤࠥ‿")
        if not passed:
            try:
                bstack1l111111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⁀").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l111111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⁁")
                    + json.dumps(bstack111l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨ⁂"))
                    + bstack111l11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ⁃")
                )
            else:
                item._driver.execute_script(
                    bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ⁄")
                    + json.dumps(str(bstack1l111111ll_opy_))
                    + bstack111l11_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ⁅")
                )
        except Exception as e:
            summary.append(bstack111l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢ⁆").format(e))
def bstack111111ll11l_opy_(test_name, error_message):
    try:
        bstack111111l1lll_opy_ = []
        bstack1lll11lll1_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⁇"), bstack111l11_opy_ (u"ࠫ࠵࠭⁈"))
        bstack11lll1l1_opy_ = {bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁉"): test_name, bstack111l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⁊"): error_message, bstack111l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⁋"): bstack1lll11lll1_opy_}
        bstack111111ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⁌"))
        if os.path.exists(bstack111111ll1l1_opy_):
            with open(bstack111111ll1l1_opy_) as f:
                bstack111111l1lll_opy_ = json.load(f)
        bstack111111l1lll_opy_.append(bstack11lll1l1_opy_)
        with open(bstack111111ll1l1_opy_, bstack111l11_opy_ (u"ࠩࡺࠫ⁍")) as f:
            json.dump(bstack111111l1lll_opy_, f)
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨ⁎") + str(e))
def bstack111111ll111_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack111l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⁏"), bstack111l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⁐")]:
        return
    if (str(skipSessionName).lower() != bstack111l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ⁑")):
        bstack111l1l11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⁒")))
    bstack1l111111ll_opy_ = bstack111l11_opy_ (u"ࠣࠤ⁓")
    bstack111l111l11l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l111111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⁔").format(e)
                )
        try:
            if passed:
                bstack11ll11ll_opy_(getattr(item, bstack111l11_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⁕"), None), bstack111l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ⁖"))
            else:
                error_message = bstack111l11_opy_ (u"ࠬ࠭⁗")
                if bstack1l111111ll_opy_:
                    bstack1lllll1l1_opy_(item._page, str(bstack1l111111ll_opy_), bstack111l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ⁘"))
                    bstack11ll11ll_opy_(getattr(item, bstack111l11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭⁙"), None), bstack111l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ⁚"), str(bstack1l111111ll_opy_))
                    error_message = str(bstack1l111111ll_opy_)
                else:
                    bstack11ll11ll_opy_(getattr(item, bstack111l11_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⁛"), None), bstack111l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ⁜"))
                bstack111111ll11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣ⁝").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack111l11_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ⁞"), default=bstack111l11_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ "), help=bstack111l11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ⁠"))
    parser.addoption(bstack111l11_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ⁡"), default=bstack111l11_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⁢"), help=bstack111l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⁣"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111l11_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨ⁤"), action=bstack111l11_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦ⁥"), default=bstack111l11_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨ⁦"),
                         help=bstack111l11_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨ⁧"))
def bstack11l1111111_opy_(log):
    if not (log[bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⁨")] and log[bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⁩")].strip()):
        return
    active = bstack11l1111l11_opy_()
    log = {
        bstack111l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⁪"): log[bstack111l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⁫")],
        bstack111l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⁬"): bstack111l1l1111_opy_().isoformat() + bstack111l11_opy_ (u"࡚࠭ࠨ⁭"),
        bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⁮"): log[bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⁯")],
    }
    if active:
        if active[bstack111l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⁰")] == bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨⁱ"):
            log[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁲")] = active[bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁳")]
        elif active[bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⁴")] == bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࠬ⁵"):
            log[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁶")] = active[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁷")]
    bstack1l11l1l1ll_opy_.bstack1ll1llll_opy_([log])
def bstack11l1111l11_opy_():
    if len(store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⁸")]) > 0 and store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⁹")][-1]:
        return {
            bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⁺"): bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⁻"),
            bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⁼"): store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⁽")][-1]
        }
    if store.get(bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⁾"), None):
        return {
            bstack111l11_opy_ (u"ࠪࡸࡾࡶࡥࠨⁿ"): bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ₀"),
            bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ₁"): store[bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ₂")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.INIT_TEST, bstack1llll1lll1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.INIT_TEST, bstack1llll1lll1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1111111l1l1_opy_ = True
        bstack1llll1111_opy_ = bstack11lll1ll1_opy_.bstack1lllll1111_opy_(bstack11l1ll1111l_opy_(item.own_markers))
        if not cli.bstack1llll1111ll_opy_(bstack1lll1l111l1_opy_):
            item._a11y_test_case = bstack1llll1111_opy_
            if bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭₃"), None):
                driver = getattr(item, bstack111l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ₄"), None)
                item._a11y_started = bstack11lll1ll1_opy_.bstack1111ll1l_opy_(driver, bstack1llll1111_opy_)
        if not bstack1l11l1l1ll_opy_.on() or bstack111111l1111_opy_ != bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ₅"):
            return
        global current_test_uuid #, bstack111lll1111_opy_
        bstack111l1111l1_opy_ = {
            bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ₆"): uuid4().__str__(),
            bstack111l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₇"): bstack111l1l1111_opy_().isoformat() + bstack111l11_opy_ (u"ࠬࡠࠧ₈")
        }
        current_test_uuid = bstack111l1111l1_opy_[bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ₉")]
        store[bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ₊")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭₋")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111ll1l1ll_opy_[item.nodeid] = {**_111ll1l1ll_opy_[item.nodeid], **bstack111l1111l1_opy_}
        bstack11111l11111_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ₌"))
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬ₍"), str(err))
def pytest_runtest_setup(item):
    store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ₎")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.PRE, item, bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ₏"))
        return # skip all existing bstack1111111l1ll_opy_
    global bstack11111l111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1llll1l1_opy_():
        atexit.register(bstack1l11l11l_opy_)
        if not bstack11111l111ll_opy_:
            try:
                bstack1111111lll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1l1ll1_opy_():
                    bstack1111111lll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1111111lll1_opy_:
                    signal.signal(s, bstack111111l111l_opy_)
                bstack11111l111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢₐ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1111lll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧₑ")
    try:
        if not bstack1l11l1l1ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1111l1_opy_ = {
            bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ₒ"): uuid,
            bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ₓ"): bstack111l1l1111_opy_().isoformat() + bstack111l11_opy_ (u"ࠪ࡞ࠬₔ"),
            bstack111l11_opy_ (u"ࠫࡹࡿࡰࡦࠩₕ"): bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪₖ"),
            bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩₗ"): bstack111l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬₘ"),
            bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫₙ"): bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨₚ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧₛ")] = item
        store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨₜ")] = [uuid]
        if not _111ll1l1ll_opy_.get(item.nodeid, None):
            _111ll1l1ll_opy_[item.nodeid] = {bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ₝"): [], bstack111l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ₞"): []}
        _111ll1l1ll_opy_[item.nodeid][bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭₟")].append(bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭₠")])
        _111ll1l1ll_opy_[item.nodeid + bstack111l11_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩ₡")] = bstack111l1111l1_opy_
        bstack111111l1l11_opy_(item, bstack111l1111l1_opy_, bstack111l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ₢"))
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ₣"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.AFTER_EACH, bstack1llll1lll1l_opy_.PRE, item, bstack111l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ₤"))
        return # skip all existing bstack1111111l1ll_opy_
    try:
        global bstack1l1llll111_opy_
        bstack1lll11lll1_opy_ = 0
        if bstack11lll1l11_opy_ is True:
            bstack1lll11lll1_opy_ = int(os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭₥")))
        if bstack1111111ll_opy_.bstack1111l1lll_opy_() == bstack111l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ₦"):
            if bstack1111111ll_opy_.bstack111ll1lll_opy_() == bstack111l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ₧"):
                bstack1111111ll11_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ₨"), None)
                bstack11l1l1lll_opy_ = bstack1111111ll11_opy_ + bstack111l11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ₩")
                driver = getattr(item, bstack111l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ₪"), None)
                bstack11ll111lll_opy_ = getattr(item, bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₫"), None)
                bstack1ll1111l_opy_ = getattr(item, bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ€"), None)
                PercySDK.screenshot(driver, bstack11l1l1lll_opy_, bstack11ll111lll_opy_=bstack11ll111lll_opy_, bstack1ll1111l_opy_=bstack1ll1111l_opy_, bstack1l1l1111l1_opy_=bstack1lll11lll1_opy_)
        if not cli.bstack1llll1111ll_opy_(bstack1lll1l111l1_opy_):
            if getattr(item, bstack111l11_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ₭"), False):
                bstack11l1lll11_opy_.bstack1l11l1l111_opy_(getattr(item, bstack111l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ₮"), None), bstack1l1llll111_opy_, logger, item)
        if not bstack1l11l1l1ll_opy_.on():
            return
        bstack111l1111l1_opy_ = {
            bstack111l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ₯"): uuid4().__str__(),
            bstack111l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ₰"): bstack111l1l1111_opy_().isoformat() + bstack111l11_opy_ (u"ࠫ࡟࠭₱"),
            bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ₲"): bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ₳"),
            bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ₴"): bstack111l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ₵"),
            bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ₶"): bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ₷")
        }
        _111ll1l1ll_opy_[item.nodeid + bstack111l11_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧ₸")] = bstack111l1111l1_opy_
        bstack111111l1l11_opy_(item, bstack111l1111l1_opy_, bstack111l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭₹"))
    except Exception as err:
        print(bstack111l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬ₺"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1111llllll1_opy_(fixturedef.argname):
        store[bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭₻")] = request.node
    elif bstack111l111l1l1_opy_(fixturedef.argname):
        store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭₼")] = request.node
    if not bstack1l11l1l1ll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111111l1ll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111111l1ll_opy_
    try:
        fixture = {
            bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ₽"): fixturedef.argname,
            bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₾"): bstack11l1lll111l_opy_(outcome),
            bstack111l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭₿"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⃀")]
        if not _111ll1l1ll_opy_.get(current_test_item.nodeid, None):
            _111ll1l1ll_opy_[current_test_item.nodeid] = {bstack111l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⃁"): []}
        _111ll1l1ll_opy_[current_test_item.nodeid][bstack111l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⃂")].append(fixture)
    except Exception as err:
        logger.debug(bstack111l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ⃃"), str(err))
if bstack11l11l11_opy_() and bstack1l11l1l1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.STEP, bstack1llll1lll1l_opy_.PRE, request, step)
            return
        try:
            _111ll1l1ll_opy_[request.node.nodeid][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⃄")].bstack1l1lll1l1l_opy_(id(step))
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ⃅"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.STEP, bstack1llll1lll1l_opy_.POST, request, step, exception)
            return
        try:
            _111ll1l1ll_opy_[request.node.nodeid][bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⃆")].bstack111lll1lll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ⃇"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.STEP, bstack1llll1lll1l_opy_.POST, request, step)
            return
        try:
            bstack111llll1l1_opy_: bstack111lll1l11_opy_ = _111ll1l1ll_opy_[request.node.nodeid][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⃈")]
            bstack111llll1l1_opy_.bstack111lll1lll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ⃉"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111111l1111_opy_
        try:
            if not bstack1l11l1l1ll_opy_.on() or bstack111111l1111_opy_ != bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⃊"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.TEST, bstack1llll1lll1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ⃋"), None)
            if not _111ll1l1ll_opy_.get(request.node.nodeid, None):
                _111ll1l1ll_opy_[request.node.nodeid] = {}
            bstack111llll1l1_opy_ = bstack111lll1l11_opy_.bstack1111ll1111l_opy_(
                scenario, feature, request.node,
                name=bstack111l11111ll_opy_(request.node, scenario),
                started_at=bstack11l11ll11l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ⃌"),
                tags=bstack111l1111l1l_opy_(feature, scenario),
                bstack111lll111l_opy_=bstack1l11l1l1ll_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {}
            )
            _111ll1l1ll_opy_[request.node.nodeid][bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⃍")] = bstack111llll1l1_opy_
            bstack1111111l11l_opy_(bstack111llll1l1_opy_.uuid)
            bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⃎"), bstack111llll1l1_opy_)
        except Exception as err:
            print(bstack111l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ⃏"), str(err))
def bstack111111lll1l_opy_(bstack111lllll11_opy_):
    if bstack111lllll11_opy_ in store[bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⃐")]:
        store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⃑")].remove(bstack111lllll11_opy_)
def bstack1111111l11l_opy_(test_uuid):
    store[bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ⃒࠭")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l11l1l1ll_opy_.bstack11111lll111_opy_
def bstack111111llll1_opy_(item, call, report):
    logger.debug(bstack111l11_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡵࡸ⃓ࠬ"))
    global bstack111111l1111_opy_
    bstack1l1l111lll_opy_ = bstack11l11ll11l_opy_()
    if hasattr(report, bstack111l11_opy_ (u"ࠫࡸࡺ࡯ࡱࠩ⃔")):
        bstack1l1l111lll_opy_ = bstack11l1ll1l111_opy_(report.stop)
    elif hasattr(report, bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫ⃕")):
        bstack1l1l111lll_opy_ = bstack11l1ll1l111_opy_(report.start)
    try:
        if getattr(report, bstack111l11_opy_ (u"࠭ࡷࡩࡧࡱࠫ⃖"), bstack111l11_opy_ (u"ࠧࠨ⃗")) == bstack111l11_opy_ (u"ࠨࡥࡤࡰࡱ⃘࠭"):
            logger.debug(bstack111l11_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀ⃙ࠫ").format(getattr(report, bstack111l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⃚"), bstack111l11_opy_ (u"ࠫࠬ⃛")).__str__(), bstack111111l1111_opy_))
            if bstack111111l1111_opy_ == bstack111l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⃜"):
                _111ll1l1ll_opy_[item.nodeid][bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃝")] = bstack1l1l111lll_opy_
                bstack11111l11111_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⃞"), report, call)
                store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⃟")] = None
            elif bstack111111l1111_opy_ == bstack111l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ⃠"):
                bstack111llll1l1_opy_ = _111ll1l1ll_opy_[item.nodeid][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⃡")]
                bstack111llll1l1_opy_.set(hooks=_111ll1l1ll_opy_[item.nodeid].get(bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⃢"), []))
                exception, bstack111llll1ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111llll1ll_opy_ = [call.excinfo.exconly(), getattr(report, bstack111l11_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫ⃣"), bstack111l11_opy_ (u"࠭ࠧ⃤"))]
                bstack111llll1l1_opy_.stop(time=bstack1l1l111lll_opy_, result=Result(result=getattr(report, bstack111l11_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⃥"), bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⃦")), exception=exception, bstack111llll1ll_opy_=bstack111llll1ll_opy_))
                bstack1l11l1l1ll_opy_.bstack111llll11l_opy_(bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⃧"), _111ll1l1ll_opy_[item.nodeid][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ⃨࠭")])
        elif getattr(report, bstack111l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⃩"), bstack111l11_opy_ (u"⃪ࠬ࠭")) in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ⃫ࠬ"), bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯⃬ࠩ")]:
            logger.debug(bstack111l11_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿ⃭ࠪ").format(getattr(report, bstack111l11_opy_ (u"ࠩࡺ࡬ࡪࡴ⃮ࠧ"), bstack111l11_opy_ (u"⃯ࠪࠫ")).__str__(), bstack111111l1111_opy_))
            bstack11l111111l_opy_ = item.nodeid + bstack111l11_opy_ (u"ࠫ࠲࠭⃰") + getattr(report, bstack111l11_opy_ (u"ࠬࡽࡨࡦࡰࠪ⃱"), bstack111l11_opy_ (u"࠭ࠧ⃲"))
            if getattr(report, bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⃳"), False):
                hook_type = bstack111l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⃴") if getattr(report, bstack111l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⃵"), bstack111l11_opy_ (u"ࠪࠫ⃶")) == bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⃷") else bstack111l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⃸")
                _111ll1l1ll_opy_[bstack11l111111l_opy_] = {
                    bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⃹"): uuid4().__str__(),
                    bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⃺"): bstack1l1l111lll_opy_,
                    bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⃻"): hook_type
                }
            _111ll1l1ll_opy_[bstack11l111111l_opy_][bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⃼")] = bstack1l1l111lll_opy_
            bstack111111lll1l_opy_(_111ll1l1ll_opy_[bstack11l111111l_opy_][bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⃽")])
            bstack111111l1l11_opy_(item, _111ll1l1ll_opy_[bstack11l111111l_opy_], bstack111l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⃾"), report, call)
            if getattr(report, bstack111l11_opy_ (u"ࠬࡽࡨࡦࡰࠪ⃿"), bstack111l11_opy_ (u"࠭ࠧ℀")) == bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭℁"):
                if getattr(report, bstack111l11_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩℂ"), bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ℃")) == bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ℄"):
                    bstack111l1111l1_opy_ = {
                        bstack111l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ℅"): uuid4().__str__(),
                        bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ℆"): bstack11l11ll11l_opy_(),
                        bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫℇ"): bstack11l11ll11l_opy_()
                    }
                    _111ll1l1ll_opy_[item.nodeid] = {**_111ll1l1ll_opy_[item.nodeid], **bstack111l1111l1_opy_}
                    bstack11111l11111_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ℈"))
                    bstack11111l11111_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ℉"), report, call)
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧℊ"), str(err))
def bstack111111ll1ll_opy_(test, bstack111l1111l1_opy_, result=None, call=None, bstack1111l1l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111llll1l1_opy_ = {
        bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨℋ"): bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠫࡺࡻࡩࡥࠩℌ")],
        bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪℍ"): bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࠫℎ"),
        bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬℏ"): test.name,
        bstack111l11_opy_ (u"ࠨࡤࡲࡨࡾ࠭ℐ"): {
            bstack111l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧℑ"): bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪℒ"),
            bstack111l11_opy_ (u"ࠫࡨࡵࡤࡦࠩℓ"): inspect.getsource(test.obj)
        },
        bstack111l11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ℔"): test.name,
        bstack111l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬℕ"): test.name,
        bstack111l11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ№"): bstack1lllll1l1l_opy_.bstack111l11llll_opy_(test),
        bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ℗"): file_path,
        bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ℘"): file_path,
        bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪℙ"): bstack111l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬℚ"),
        bstack111l11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪℛ"): file_path,
        bstack111l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪℜ"): bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫℝ")],
        bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ℞"): bstack111l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ℟"),
        bstack111l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭℠"): {
            bstack111l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ℡"): test.nodeid
        },
        bstack111l11_opy_ (u"ࠬࡺࡡࡨࡵࠪ™"): bstack11l1ll1111l_opy_(test.own_markers)
    }
    if bstack1111l1l1_opy_ in [bstack111l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ℣"), bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩℤ")]:
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭℥")] = {
            bstack111l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫΩ"): bstack111l1111l1_opy_.get(bstack111l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ℧"), [])
        }
    if bstack1111l1l1_opy_ == bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬℨ"):
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ℩")] = bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧK")
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Å")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧℬ")]
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧℭ")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ℮")]
    if result:
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫℯ")] = result.outcome
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ℰ")] = result.duration * 1000
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫℱ")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬℲ")]
        if result.failed:
            bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧℳ")] = bstack1l11l1l1ll_opy_.bstack1111l11ll1_opy_(call.excinfo.typename)
            bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪℴ")] = bstack1l11l1l1ll_opy_.bstack1111l1l11l1_opy_(call.excinfo, result)
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩℵ")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪℶ")]
    if outcome:
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬℷ")] = bstack11l1lll111l_opy_(outcome)
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧℸ")] = 0
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬℹ")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭℺")]
        if bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ℻")] == bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪℼ"):
            bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪℽ")] = bstack111l11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ℾ")  # bstack11111l111l1_opy_
            bstack111llll1l1_opy_[bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧℿ")] = [{bstack111l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⅀"): [bstack111l11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⅁")]}]
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⅂")] = bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⅃")]
    return bstack111llll1l1_opy_
def bstack111111lll11_opy_(test, bstack111l1l1ll1_opy_, bstack1111l1l1_opy_, result, call, outcome, bstack11111l11l11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⅄")]
    hook_name = bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨⅅ")]
    hook_data = {
        bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫⅆ"): bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬⅇ")],
        bstack111l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ⅈ"): bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧⅉ"),
        bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⅊"): bstack111l11_opy_ (u"ࠫࢀࢃࠧ⅋").format(bstack111l1111l11_opy_(hook_name)),
        bstack111l11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⅌"): {
            bstack111l11_opy_ (u"࠭࡬ࡢࡰࡪࠫ⅍"): bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧⅎ"),
            bstack111l11_opy_ (u"ࠨࡥࡲࡨࡪ࠭⅏"): None
        },
        bstack111l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ⅐"): test.name,
        bstack111l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⅑"): bstack1lllll1l1l_opy_.bstack111l11llll_opy_(test, hook_name),
        bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⅒"): file_path,
        bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⅓"): file_path,
        bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⅔"): bstack111l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⅕"),
        bstack111l11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⅖"): file_path,
        bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⅗"): bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⅘")],
        bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⅙"): bstack111l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ⅚") if bstack111111l1111_opy_ == bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⅛") else bstack111l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⅜"),
        bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⅝"): hook_type
    }
    bstack1111l1lllll_opy_ = bstack111l1l1l1l_opy_(_111ll1l1ll_opy_.get(test.nodeid, None))
    if bstack1111l1lllll_opy_:
        hook_data[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ⅞")] = bstack1111l1lllll_opy_
    if result:
        hook_data[bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⅟")] = result.outcome
        hook_data[bstack111l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬⅠ")] = result.duration * 1000
        hook_data[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪⅡ")] = bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫⅢ")]
        if result.failed:
            hook_data[bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭Ⅳ")] = bstack1l11l1l1ll_opy_.bstack1111l11ll1_opy_(call.excinfo.typename)
            hook_data[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩⅤ")] = bstack1l11l1l1ll_opy_.bstack1111l1l11l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩⅥ")] = bstack11l1lll111l_opy_(outcome)
        hook_data[bstack111l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫⅦ")] = 100
        hook_data[bstack111l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⅧ")] = bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪⅨ")]
        if hook_data[bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Ⅹ")] == bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧⅪ"):
            hook_data[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧⅫ")] = bstack111l11_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪⅬ")  # bstack11111l111l1_opy_
            hook_data[bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫⅭ")] = [{bstack111l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧⅮ"): [bstack111l11_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩⅯ")]}]
    if bstack11111l11l11_opy_:
        hook_data[bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ⅰ")] = bstack11111l11l11_opy_.result
        hook_data[bstack111l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨⅱ")] = bstack11l11l1ll1l_opy_(bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬⅲ")], bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧⅳ")])
        hook_data[bstack111l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨⅴ")] = bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⅵ")]
        if hook_data[bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬⅶ")] == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ⅷ"):
            hook_data[bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ⅸ")] = bstack1l11l1l1ll_opy_.bstack1111l11ll1_opy_(bstack11111l11l11_opy_.exception_type)
            hook_data[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩⅹ")] = [{bstack111l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬⅺ"): bstack11l111llll1_opy_(bstack11111l11l11_opy_.exception)}]
    return hook_data
def bstack11111l11111_opy_(test, bstack111l1111l1_opy_, bstack1111l1l1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack111l11_opy_ (u"ࠪࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠢ࠰ࠤࢀࢃࠧⅻ").format(bstack1111l1l1_opy_))
    bstack111llll1l1_opy_ = bstack111111ll1ll_opy_(test, bstack111l1111l1_opy_, result, call, bstack1111l1l1_opy_, outcome)
    driver = getattr(test, bstack111l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬⅼ"), None)
    if bstack1111l1l1_opy_ == bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ⅽ") and driver:
        bstack111llll1l1_opy_[bstack111l11_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬⅾ")] = bstack1l11l1l1ll_opy_.bstack111ll1ll1l_opy_(driver)
    if bstack1111l1l1_opy_ == bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨⅿ"):
        bstack1111l1l1_opy_ = bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪↀ")
    bstack111ll1l1l1_opy_ = {
        bstack111l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ↁ"): bstack1111l1l1_opy_,
        bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬↂ"): bstack111llll1l1_opy_
    }
    bstack1l11l1l1ll_opy_.bstack111l1l1ll_opy_(bstack111ll1l1l1_opy_)
    if bstack1111l1l1_opy_ == bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬↃ"):
        threading.current_thread().bstackTestMeta = {bstack111l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬↄ"): bstack111l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧↅ")}
    elif bstack1111l1l1_opy_ == bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩↆ"):
        threading.current_thread().bstackTestMeta = {bstack111l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨↇ"): getattr(result, bstack111l11_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪↈ"), bstack111l11_opy_ (u"ࠪࠫ↉"))}
def bstack111111l1l11_opy_(test, bstack111l1111l1_opy_, bstack1111l1l1_opy_, result=None, call=None, outcome=None, bstack11111l11l11_opy_=None):
    logger.debug(bstack111l11_opy_ (u"ࠫࡸ࡫࡮ࡥࡡ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡨࡰࡱ࡮ࠤࡩࡧࡴࡢ࠮ࠣࡩࡻ࡫࡮ࡵࡖࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ↊").format(bstack1111l1l1_opy_))
    hook_data = bstack111111lll11_opy_(test, bstack111l1111l1_opy_, bstack1111l1l1_opy_, result, call, outcome, bstack11111l11l11_opy_)
    bstack111ll1l1l1_opy_ = {
        bstack111l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ↋"): bstack1111l1l1_opy_,
        bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ↌"): hook_data
    }
    bstack1l11l1l1ll_opy_.bstack111l1l1ll_opy_(bstack111ll1l1l1_opy_)
def bstack111l1l1l1l_opy_(bstack111l1111l1_opy_):
    if not bstack111l1111l1_opy_:
        return None
    if bstack111l1111l1_opy_.get(bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ↍"), None):
        return getattr(bstack111l1111l1_opy_[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ↎")], bstack111l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ↏"), None)
    return bstack111l1111l1_opy_.get(bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ←"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.LOG, bstack1llll1lll1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_.LOG, bstack1llll1lll1l_opy_.POST, request, caplog)
        return # skip all existing bstack1111111l1ll_opy_
    try:
        if not bstack1l11l1l1ll_opy_.on():
            return
        places = [bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ↑"), bstack111l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ→"), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ↓")]
        logs = []
        for bstack1111111l111_opy_ in places:
            records = caplog.get_records(bstack1111111l111_opy_)
            bstack11111l11l1l_opy_ = bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ↔") if bstack1111111l111_opy_ == bstack111l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭↕") else bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ↖")
            bstack111111lllll_opy_ = request.node.nodeid + (bstack111l11_opy_ (u"ࠪࠫ↗") if bstack1111111l111_opy_ == bstack111l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ↘") else bstack111l11_opy_ (u"ࠬ࠳ࠧ↙") + bstack1111111l111_opy_)
            test_uuid = bstack111l1l1l1l_opy_(_111ll1l1ll_opy_.get(bstack111111lllll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l111ll1l1_opy_(record.message):
                    continue
                logs.append({
                    bstack111l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ↚"): bstack11l1l1l1111_opy_(record.created).isoformat() + bstack111l11_opy_ (u"࡛ࠧࠩ↛"),
                    bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ↜"): record.levelname,
                    bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ↝"): record.message,
                    bstack11111l11l1l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l11l1l1ll_opy_.bstack1ll1llll_opy_(logs)
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ↞"), str(err))
def bstack1lll1lll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1111111_opy_
    bstack11ll1llll_opy_ = bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ↟"), None) and bstack1l1lllll1l_opy_(
            threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ↠"), None)
    bstack1l1l11lll1_opy_ = getattr(driver, bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭↡"), None) != None and getattr(driver, bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ↢"), None) == True
    if sequence == bstack111l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ↣") and driver != None:
      if not bstack1l1111111_opy_ and bstack1ll1111llll_opy_() and bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↤") in CONFIG and CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ↥")] == True and bstack11111ll1_opy_.bstack1ll11ll1l1_opy_(driver_command) and (bstack1l1l11lll1_opy_ or bstack11ll1llll_opy_) and not bstack1l1ll1l1ll_opy_(args):
        try:
          bstack1l1111111_opy_ = True
          logger.debug(bstack111l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭↦").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ↧").format(str(err)))
        bstack1l1111111_opy_ = False
    if sequence == bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ↨"):
        if driver_command == bstack111l11_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ↩"):
            bstack1l11l1l1ll_opy_.bstack11lllll1l1_opy_({
                bstack111l11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ↪"): response[bstack111l11_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ↫")],
                bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ↬"): store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ↭")]
            })
def bstack1l11l11l_opy_():
    global bstack11111l1l_opy_
    bstack1lll111lll_opy_.bstack1l1l1l1ll_opy_()
    logging.shutdown()
    bstack1l11l1l1ll_opy_.bstack111ll111ll_opy_()
    for driver in bstack11111l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111111l111l_opy_(*args):
    global bstack11111l1l_opy_
    bstack1l11l1l1ll_opy_.bstack111ll111ll_opy_()
    for driver in bstack11111l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11llll111_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1l1lllll11_opy_(self, *args, **kwargs):
    bstack1l111l111l_opy_ = bstack11ll11lll1_opy_(self, *args, **kwargs)
    bstack11llllll1_opy_ = getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭↮"), None)
    if bstack11llllll1_opy_ and bstack11llllll1_opy_.get(bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭↯"), bstack111l11_opy_ (u"ࠧࠨ↰")) == bstack111l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ↱"):
        bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(self)
    return bstack1l111l111l_opy_
@measure(event_name=EVENTS.bstack11l111lll_opy_, stage=STAGE.bstack1lll11l1l1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1l11111111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
    if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭↲")):
        return
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ↳"), True)
    global bstack11llllllll_opy_
    global bstack111ll11ll_opy_
    bstack11llllllll_opy_ = framework_name
    logger.info(bstack111l11l11_opy_.format(bstack11llllllll_opy_.split(bstack111l11_opy_ (u"ࠫ࠲࠭↴"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111llll_opy_():
            Service.start = bstack1l111111l_opy_
            Service.stop = bstack1l1lll1ll1_opy_
            webdriver.Remote.get = bstack1ll11l1l1_opy_
            webdriver.Remote.__init__ = bstack11l1l1l11_opy_
            if not isinstance(os.getenv(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭↵")), str):
                return
            WebDriver.close = bstack11111lll1_opy_
            WebDriver.quit = bstack1lll11111l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l11l1l1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1l1lllll11_opy_
        bstack111ll11ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack111l11_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ↶")):
        bstack111ll11ll_opy_ = eval(os.environ.get(bstack111l11_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ↷")))
    if not bstack111ll11ll_opy_:
        bstack1111111l1_opy_(bstack111l11_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ↸"), bstack11l1lllll1_opy_)
    if bstack11lll11l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l1ll11111_opy_ = bstack1ll1l1ll1l_opy_
        except Exception as e:
            logger.error(bstack11llll11l_opy_.format(str(e)))
    if bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ↹") in str(framework_name).lower():
        if not bstack1ll1111llll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l111l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1ll1ll_opy_
            Config.getoption = bstack1lllll11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11ll11l1ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1lll11l_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1lll11111l_opy_(self):
    global bstack11llllllll_opy_
    global bstack1lll11l1ll_opy_
    global bstack1ll1l111ll_opy_
    try:
        if bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ↺") in bstack11llllllll_opy_ and self.session_id != None and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ↻"), bstack111l11_opy_ (u"ࠬ࠭↼")) != bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ↽"):
            bstack111llll1l_opy_ = bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ↾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ↿")
            bstack11111llll_opy_(logger, True)
            if self != None:
                bstack11ll11l11_opy_(self, bstack111llll1l_opy_, bstack111l11_opy_ (u"ࠩ࠯ࠤࠬ⇀").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll1111ll_opy_(bstack1lll1l111l1_opy_):
            item = store.get(bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⇁"), None)
            if item is not None and bstack1l1lllll1l_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⇂"), None):
                bstack11l1lll11_opy_.bstack1l11l1l111_opy_(self, bstack1l1llll111_opy_, logger, item)
        threading.current_thread().testStatus = bstack111l11_opy_ (u"ࠬ࠭⇃")
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢ⇄") + str(e))
    bstack1ll1l111ll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11lll111ll_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack11l1l1l11_opy_(self, command_executor,
             desired_capabilities=None, bstack11l1l1l11l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll11l1ll_opy_
    global bstack11lll11lll_opy_
    global bstack11lll1l11_opy_
    global bstack11llllllll_opy_
    global bstack11ll11lll1_opy_
    global bstack11111l1l_opy_
    global bstack1ll11l1l_opy_
    global bstack1l11l11111_opy_
    global bstack1l1llll111_opy_
    CONFIG[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⇅")] = str(bstack11llllllll_opy_) + str(__version__)
    command_executor = bstack1l1ll11l11_opy_(bstack1ll11l1l_opy_, CONFIG)
    logger.debug(bstack111l11ll1_opy_.format(command_executor))
    proxy = bstack11l1l11l1_opy_(CONFIG, proxy)
    bstack1lll11lll1_opy_ = 0
    try:
        if bstack11lll1l11_opy_ is True:
            bstack1lll11lll1_opy_ = int(os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⇆")))
    except:
        bstack1lll11lll1_opy_ = 0
    bstack11l1lll111_opy_ = bstack1l111111_opy_(CONFIG, bstack1lll11lll1_opy_)
    logger.debug(bstack11llllll11_opy_.format(str(bstack11l1lll111_opy_)))
    bstack1l1llll111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⇇"))[bstack1lll11lll1_opy_]
    if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⇈") in CONFIG and CONFIG[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⇉")]:
        bstack1l1ll1l111_opy_(bstack11l1lll111_opy_, bstack1l11l11111_opy_)
    if bstack11lll1ll1_opy_.bstack1l11l1ll1l_opy_(CONFIG, bstack1lll11lll1_opy_) and bstack11lll1ll1_opy_.bstack1l1111lll1_opy_(bstack11l1lll111_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll1111ll_opy_(bstack1lll1l111l1_opy_):
            bstack11lll1ll1_opy_.set_capabilities(bstack11l1lll111_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll1ll11_opy_ = bstack1ll1lll1ll_opy_(desired_capabilities)
        bstack11ll1ll11_opy_[bstack111l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ⇊")] = bstack1l1l1llll1_opy_(CONFIG)
        bstack111l1l1l1_opy_ = bstack1l111111_opy_(bstack11ll1ll11_opy_)
        if bstack111l1l1l1_opy_:
            bstack11l1lll111_opy_ = update(bstack111l1l1l1_opy_, bstack11l1lll111_opy_)
        desired_capabilities = None
    if options:
        bstack1lll1ll1l1_opy_(options, bstack11l1lll111_opy_)
    if not options:
        options = bstack11l1lll1ll_opy_(bstack11l1lll111_opy_)
    if proxy and bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⇋")):
        options.proxy(proxy)
    if options and bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⇌")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1lll1l_opy_() < version.parse(bstack111l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⇍")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l1lll111_opy_)
    logger.info(bstack1lll1llll_opy_)
    bstack11l11111l_opy_.end(EVENTS.bstack11l111lll_opy_.value, EVENTS.bstack11l111lll_opy_.value + bstack111l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⇎"),
                               EVENTS.bstack11l111lll_opy_.value + bstack111l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⇏"), True, None)
    if bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⇐")):
        bstack11ll11lll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⇑")):
        bstack11ll11lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11l1l1l11l_opy_=bstack11l1l1l11l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭⇒")):
        bstack11ll11lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11l1l1l11l_opy_=bstack11l1l1l11l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11ll11lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11l1l1l11l_opy_=bstack11l1l1l11l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l1lll11l1_opy_ = bstack111l11_opy_ (u"ࠧࠨ⇓")
        if bstack11l1lll1l_opy_() >= version.parse(bstack111l11_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ⇔")):
            bstack1l1lll11l1_opy_ = self.caps.get(bstack111l11_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ⇕"))
        else:
            bstack1l1lll11l1_opy_ = self.capabilities.get(bstack111l11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⇖"))
        if bstack1l1lll11l1_opy_:
            bstack1lll11l11l_opy_(bstack1l1lll11l1_opy_)
            if bstack11l1lll1l_opy_() <= version.parse(bstack111l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ⇗")):
                self.command_executor._url = bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⇘") + bstack1ll11l1l_opy_ + bstack111l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ⇙")
            else:
                self.command_executor._url = bstack111l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ⇚") + bstack1l1lll11l1_opy_ + bstack111l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ⇛")
            logger.debug(bstack1l1ll11l_opy_.format(bstack1l1lll11l1_opy_))
        else:
            logger.debug(bstack1l1l1lll11_opy_.format(bstack111l11_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ⇜")))
    except Exception as e:
        logger.debug(bstack1l1l1lll11_opy_.format(e))
    bstack1lll11l1ll_opy_ = self.session_id
    if bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⇝") in bstack11llllllll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⇞"), None)
        if item:
            bstack1111111ll1l_opy_ = getattr(item, bstack111l11_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪ⇟"), False)
            if not getattr(item, bstack111l11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⇠"), None) and bstack1111111ll1l_opy_:
                setattr(store[bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⇡")], bstack111l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⇢"), self)
        bstack11llllll1_opy_ = getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⇣"), None)
        if bstack11llllll1_opy_ and bstack11llllll1_opy_.get(bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⇤"), bstack111l11_opy_ (u"ࠫࠬ⇥")) == bstack111l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⇦"):
            bstack1l11l1l1ll_opy_.bstack1lll1ll11l_opy_(self)
    bstack11111l1l_opy_.append(self)
    if bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⇧") in CONFIG and bstack111l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⇨") in CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⇩")][bstack1lll11lll1_opy_]:
        bstack11lll11lll_opy_ = CONFIG[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⇪")][bstack1lll11lll1_opy_][bstack111l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⇫")]
    logger.debug(bstack1l11111l1l_opy_.format(bstack1lll11l1ll_opy_))
@measure(event_name=EVENTS.bstack1l1l1ll1l1_opy_, stage=STAGE.bstack1l1l11ll1_opy_, bstack1llll1111l_opy_=bstack11lll11lll_opy_)
def bstack1ll11l1l1_opy_(self, url):
    global bstack1lll11l1l_opy_
    global CONFIG
    try:
        bstack11111ll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111lll1l1_opy_.format(str(err)))
    try:
        bstack1lll11l1l_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1111ll1l_opy_ = str(e)
            if any(err_msg in bstack1l1111ll1l_opy_ for err_msg in bstack1ll11ll11l_opy_):
                bstack11111ll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111lll1l1_opy_.format(str(err)))
        raise e
def bstack11l1llll_opy_(item, when):
    global bstack1lllll1lll_opy_
    try:
        bstack1lllll1lll_opy_(item, when)
    except Exception as e:
        pass
def bstack11ll11l1ll_opy_(item, call, rep):
    global bstack1ll11l1l11_opy_
    global bstack11111l1l_opy_
    name = bstack111l11_opy_ (u"ࠫࠬ⇬")
    try:
        if rep.when == bstack111l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⇭"):
            bstack1lll11l1ll_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⇮"))
            try:
                if (str(skipSessionName).lower() != bstack111l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ⇯")):
                    name = str(rep.nodeid)
                    bstack111l11l1_opy_ = bstack1l11l111ll_opy_(bstack111l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⇰"), name, bstack111l11_opy_ (u"ࠩࠪ⇱"), bstack111l11_opy_ (u"ࠪࠫ⇲"), bstack111l11_opy_ (u"ࠫࠬ⇳"), bstack111l11_opy_ (u"ࠬ࠭⇴"))
                    os.environ[bstack111l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⇵")] = name
                    for driver in bstack11111l1l_opy_:
                        if bstack1lll11l1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack111l11l1_opy_)
            except Exception as e:
                logger.debug(bstack111l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ⇶").format(str(e)))
            try:
                bstack1l1ll1111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⇷"):
                    status = bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⇸") if rep.outcome.lower() == bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⇹") else bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⇺")
                    reason = bstack111l11_opy_ (u"ࠬ࠭⇻")
                    if status == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⇼"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111l11_opy_ (u"ࠧࡪࡰࡩࡳࠬ⇽") if status == bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⇾") else bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⇿")
                    data = name + bstack111l11_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ∀") if status == bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ∁") else name + bstack111l11_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ∂") + reason
                    bstack11l1l111l1_opy_ = bstack1l11l111ll_opy_(bstack111l11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ∃"), bstack111l11_opy_ (u"ࠧࠨ∄"), bstack111l11_opy_ (u"ࠨࠩ∅"), bstack111l11_opy_ (u"ࠩࠪ∆"), level, data)
                    for driver in bstack11111l1l_opy_:
                        if bstack1lll11l1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1l111l1_opy_)
            except Exception as e:
                logger.debug(bstack111l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ∇").format(str(e)))
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ∈").format(str(e)))
    bstack1ll11l1l11_opy_(item, call, rep)
notset = Notset()
def bstack1lllll11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll11ll1_opy_
    if str(name).lower() == bstack111l11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ∉"):
        return bstack111l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ∊")
    else:
        return bstack1llll11ll1_opy_(self, name, default, skip)
def bstack1ll1l1ll1l_opy_(self):
    global CONFIG
    global bstack111l1lll1_opy_
    try:
        proxy = bstack11lllllll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ∋")):
                proxies = bstack1ll1l1l111_opy_(proxy, bstack1l1ll11l11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lllllll1_opy_ = proxies.popitem()
                    if bstack111l11_opy_ (u"ࠣ࠼࠲࠳ࠧ∌") in bstack1lllllll1_opy_:
                        return bstack1lllllll1_opy_
                    else:
                        return bstack111l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ∍") + bstack1lllllll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ∎").format(str(e)))
    return bstack111l1lll1_opy_(self)
def bstack11lll11l1l_opy_():
    return (bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ∏") in CONFIG or bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ∐") in CONFIG) and bstack11l11ll11_opy_() and bstack11l1lll1l_opy_() >= version.parse(
        bstack11l1ll111_opy_)
def bstack1l11l1ll11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11lll11lll_opy_
    global bstack11lll1l11_opy_
    global bstack11llllllll_opy_
    CONFIG[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ∑")] = str(bstack11llllllll_opy_) + str(__version__)
    bstack1lll11lll1_opy_ = 0
    try:
        if bstack11lll1l11_opy_ is True:
            bstack1lll11lll1_opy_ = int(os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ−")))
    except:
        bstack1lll11lll1_opy_ = 0
    CONFIG[bstack111l11_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ∓")] = True
    bstack11l1lll111_opy_ = bstack1l111111_opy_(CONFIG, bstack1lll11lll1_opy_)
    logger.debug(bstack11llllll11_opy_.format(str(bstack11l1lll111_opy_)))
    if CONFIG.get(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭∔")):
        bstack1l1ll1l111_opy_(bstack11l1lll111_opy_, bstack1l11l11111_opy_)
    if bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭∕") in CONFIG and bstack111l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ∖") in CONFIG[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ∗")][bstack1lll11lll1_opy_]:
        bstack11lll11lll_opy_ = CONFIG[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ∘")][bstack1lll11lll1_opy_][bstack111l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ∙")]
    import urllib
    import json
    if bstack111l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ√") in CONFIG and str(CONFIG[bstack111l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭∛")]).lower() != bstack111l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ∜"):
        bstack1l11lll1_opy_ = bstack1ll111ll1_opy_()
        bstack11l11l1ll_opy_ = bstack1l11lll1_opy_ + urllib.parse.quote(json.dumps(bstack11l1lll111_opy_))
    else:
        bstack11l11l1ll_opy_ = bstack111l11_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭∝") + urllib.parse.quote(json.dumps(bstack11l1lll111_opy_))
    browser = self.connect(bstack11l11l1ll_opy_)
    return browser
def bstack11l1lll11l_opy_():
    global bstack111ll11ll_opy_
    global bstack11llllllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11ll11llll_opy_
        if not bstack1ll1111llll_opy_():
            global bstack11ll11l1_opy_
            if not bstack11ll11l1_opy_:
                from bstack_utils.helper import bstack1l11l1lll1_opy_, bstack1l1llllll_opy_
                bstack11ll11l1_opy_ = bstack1l11l1lll1_opy_()
                bstack1l1llllll_opy_(bstack11llllllll_opy_)
            BrowserType.connect = bstack11ll11llll_opy_
            return
        BrowserType.launch = bstack1l11l1ll11_opy_
        bstack111ll11ll_opy_ = True
    except Exception as e:
        pass
def bstack11111l1111l_opy_():
    global CONFIG
    global bstack1ll11ll11_opy_
    global bstack1ll11l1l_opy_
    global bstack1l11l11111_opy_
    global bstack11lll1l11_opy_
    global bstack1lll1l1l11_opy_
    CONFIG = json.loads(os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ∞")))
    bstack1ll11ll11_opy_ = eval(os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ∟")))
    bstack1ll11l1l_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ∠"))
    bstack1ll111l1ll_opy_(CONFIG, bstack1ll11ll11_opy_)
    bstack1lll1l1l11_opy_ = bstack1lll111lll_opy_.bstack111ll1l1l_opy_(CONFIG, bstack1lll1l1l11_opy_)
    if cli.bstack11llll1l_opy_():
        bstack1ll11l11l_opy_.invoke(bstack1l1111l1ll_opy_.CONNECT, bstack11l1l1l1ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ∡"), bstack111l11_opy_ (u"ࠩ࠳ࠫ∢")))
        cli.bstack1ll1lll1l1l_opy_(cli_context.platform_index)
        cli.bstack1lllll11111_opy_(bstack1l1ll11l11_opy_(bstack1ll11l1l_opy_, CONFIG), cli_context.platform_index, bstack11l1lll1ll_opy_)
        cli.bstack1lllll11l11_opy_()
        logger.debug(bstack111l11_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ∣") + str(cli_context.platform_index) + bstack111l11_opy_ (u"ࠦࠧ∤"))
        return # skip all existing bstack1111111l1ll_opy_
    global bstack11ll11lll1_opy_
    global bstack1ll1l111ll_opy_
    global bstack1111ll11l_opy_
    global bstack1l1l11ll_opy_
    global bstack111111ll_opy_
    global bstack1l1111llll_opy_
    global bstack1l11ll11l1_opy_
    global bstack1lll11l1l_opy_
    global bstack111l1lll1_opy_
    global bstack1llll11ll1_opy_
    global bstack1lllll1lll_opy_
    global bstack1ll11l1l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11ll11lll1_opy_ = webdriver.Remote.__init__
        bstack1ll1l111ll_opy_ = WebDriver.quit
        bstack1l11ll11l1_opy_ = WebDriver.close
        bstack1lll11l1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ∥") in CONFIG or bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ∦") in CONFIG) and bstack11l11ll11_opy_():
        if bstack11l1lll1l_opy_() < version.parse(bstack11l1ll111_opy_):
            logger.error(bstack11l11l1ll1_opy_.format(bstack11l1lll1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack111l1lll1_opy_ = RemoteConnection._1l1ll11111_opy_
            except Exception as e:
                logger.error(bstack11llll11l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll11ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1lllll1lll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11l11ll1l1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll11l1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ∧"))
    bstack1l11l11111_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ∨"), {}).get(bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ∩"))
    bstack11lll1l11_opy_ = True
    bstack1l11111111_opy_(bstack11lll1lll_opy_)
if (bstack11l1llll1l1_opy_()):
    bstack11111l1111l_opy_()
@bstack111l11111l_opy_(class_method=False)
def bstack1111111llll_opy_(hook_name, event, bstack1l11l111111_opy_=None):
    if hook_name not in [bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ∪"), bstack111l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ∫"), bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ∬"), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ∭"), bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ∮"), bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ∯"), bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ∰"), bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ∱")]:
        return
    node = store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ∲")]
    if hook_name in [bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ∳"), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ∴")]:
        node = store[bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭∵")]
    elif hook_name in [bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭∶"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ∷")]:
        node = store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ∸")]
    hook_type = bstack111l11111l1_opy_(hook_name)
    if event == bstack111l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ∹"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_[hook_type], bstack1llll1lll1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l1ll1_opy_ = {
            bstack111l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ∺"): uuid,
            bstack111l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ∻"): bstack11l11ll11l_opy_(),
            bstack111l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ∼"): bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭∽"),
            bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ∾"): hook_type,
            bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭∿"): hook_name
        }
        store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ≀")].append(uuid)
        bstack111111l1ll1_opy_ = node.nodeid
        if hook_type == bstack111l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ≁"):
            if not _111ll1l1ll_opy_.get(bstack111111l1ll1_opy_, None):
                _111ll1l1ll_opy_[bstack111111l1ll1_opy_] = {bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≂"): []}
            _111ll1l1ll_opy_[bstack111111l1ll1_opy_][bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭≃")].append(bstack111l1l1ll1_opy_[bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭≄")])
        _111ll1l1ll_opy_[bstack111111l1ll1_opy_ + bstack111l11_opy_ (u"ࠩ࠰ࠫ≅") + hook_name] = bstack111l1l1ll1_opy_
        bstack111111l1l11_opy_(node, bstack111l1l1ll1_opy_, bstack111l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ≆"))
    elif event == bstack111l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ≇"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l111ll_opy_[hook_type], bstack1llll1lll1l_opy_.POST, node, None, bstack1l11l111111_opy_)
            return
        bstack11l111111l_opy_ = node.nodeid + bstack111l11_opy_ (u"ࠬ࠳ࠧ≈") + hook_name
        _111ll1l1ll_opy_[bstack11l111111l_opy_][bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≉")] = bstack11l11ll11l_opy_()
        bstack111111lll1l_opy_(_111ll1l1ll_opy_[bstack11l111111l_opy_][bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ≊")])
        bstack111111l1l11_opy_(node, _111ll1l1ll_opy_[bstack11l111111l_opy_], bstack111l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ≋"), bstack11111l11l11_opy_=bstack1l11l111111_opy_)
def bstack111111l1l1l_opy_():
    global bstack111111l1111_opy_
    if bstack11l11l11_opy_():
        bstack111111l1111_opy_ = bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭≌")
    else:
        bstack111111l1111_opy_ = bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ≍")
@bstack1l11l1l1ll_opy_.bstack11111lll111_opy_
def bstack111111l11ll_opy_():
    bstack111111l1l1l_opy_()
    if cli.is_running():
        try:
            bstack11l111l11l1_opy_(bstack1111111llll_opy_)
        except Exception as e:
            logger.debug(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ≎").format(e))
        return
    if bstack11l11ll11_opy_():
        bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
        bstack111l11_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ≏")
        if bstack111l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ≐")):
            if CONFIG.get(bstack111l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ≑")) is not None and int(CONFIG[bstack111l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ≒")]) > 1:
                bstack1ll1l1l11_opy_(bstack1lll1lll_opy_)
            return
        bstack1ll1l1l11_opy_(bstack1lll1lll_opy_)
    try:
        bstack11l111l11l1_opy_(bstack1111111llll_opy_)
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ≓").format(e))
bstack111111l11ll_opy_()