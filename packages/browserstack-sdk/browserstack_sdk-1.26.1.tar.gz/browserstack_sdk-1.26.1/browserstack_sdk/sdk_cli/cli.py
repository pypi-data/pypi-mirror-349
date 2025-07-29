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
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack11111llll1_opy_ import bstack1111l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l1ll_opy_ import bstack1llll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l111l_opy_ import bstack1llll1l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll11l_opy_ import bstack1lll11l1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import bstack1llll1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1ll_opy_ import bstack1llll1lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111lll_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1llll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l11l_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111111_opy_ import bstack1lll111111_opy_, bstack11lll11lll_opy_, bstack1llll1l111_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11l1_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1llllll111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1lll11l111l_opy_
from bstack_utils.helper import Notset, bstack1lllll111l1_opy_, get_cli_dir, bstack1lll11l1ll1_opy_, bstack1ll11lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1lllll_opy_ import bstack1l11ll11_opy_
from bstack_utils.helper import Notset, bstack1lllll111l1_opy_, get_cli_dir, bstack1lll11l1ll1_opy_, bstack1ll11lll_opy_, bstack11lll1lll_opy_, bstack1ll1ll11_opy_, bstack11l1l1l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11llll1_opy_, bstack1llll1111ll_opy_, bstack1ll1lll1111_opy_, bstack1lll1l11111_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1llllll11ll_opy_, bstack1llllll1l11_opy_, bstack11111ll1l1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l11l1lll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11111l1ll_opy_, bstack1l1lllll_opy_
logger = bstack1l11l1lll_opy_.get_logger(__name__, bstack1l11l1lll_opy_.bstack1lllll11ll1_opy_())
def bstack1lll1lll11l_opy_(bs_config):
    bstack1lll1111111_opy_ = None
    bstack1llll1llll1_opy_ = None
    try:
        bstack1llll1llll1_opy_ = get_cli_dir()
        bstack1lll1111111_opy_ = bstack1lll11l1ll1_opy_(bstack1llll1llll1_opy_)
        bstack1lll1l1l1l1_opy_ = bstack1lllll111l1_opy_(bstack1lll1111111_opy_, bstack1llll1llll1_opy_, bs_config)
        bstack1lll1111111_opy_ = bstack1lll1l1l1l1_opy_ if bstack1lll1l1l1l1_opy_ else bstack1lll1111111_opy_
        if not bstack1lll1111111_opy_:
            raise ValueError(bstack11l1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦှ"))
    except Exception as ex:
        logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦဿ").format(ex))
        bstack1lll1111111_opy_ = os.environ.get(bstack11l1lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧ၀"))
        if bstack1lll1111111_opy_:
            logger.debug(bstack11l1lll_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨ၁") + str(bstack1lll1111111_opy_) + bstack11l1lll_opy_ (u"ࠦࠧ၂"))
        else:
            logger.debug(bstack11l1lll_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣ၃"))
    return bstack1lll1111111_opy_, bstack1llll1llll1_opy_
bstack1llll11ll11_opy_ = bstack11l1lll_opy_ (u"ࠨ࠹࠺࠻࠼ࠦ၄")
bstack1ll1ll1llll_opy_ = bstack11l1lll_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨ၅")
bstack1lll1ll111l_opy_ = bstack11l1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧ၆")
bstack1llll1111l1_opy_ = bstack11l1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢ၇")
bstack1l1ll11ll_opy_ = bstack11l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨ၈")
bstack1ll1lll11l1_opy_ = re.compile(bstack11l1lll_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥ၉"))
bstack1llll11l111_opy_ = bstack11l1lll_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥ၊")
bstack1llll111l1l_opy_ = [
    bstack11lll11lll_opy_.bstack1ll11l1111_opy_,
    bstack11lll11lll_opy_.CONNECT,
    bstack11lll11lll_opy_.bstack1l1llll11l_opy_,
]
class SDKCLI:
    _1lllll11l11_opy_ = None
    process: Union[None, Any]
    bstack1lll111ll1l_opy_: bool
    bstack1lll1ll1111_opy_: bool
    bstack1lll1llll11_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1llll111lll_opy_: Union[None, grpc.Channel]
    bstack1llll11llll_opy_: str
    test_framework: TestFramework
    bstack1111111111_opy_: bstack1llllll111l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1lll11ll_opy_: bstack1llll11l11l_opy_
    accessibility: bstack1ll1ll1lll1_opy_
    bstack1l1l1lllll_opy_: bstack1l11ll11_opy_
    ai: bstack1llll1l1l1l_opy_
    bstack1lllll1l111_opy_: bstack1lll11l1111_opy_
    bstack1lll1l11ll1_opy_: List[bstack1llll1ll1l1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll11111l1_opy_: Any
    bstack1lll111l1ll_opy_: Dict[str, timedelta]
    bstack1lllll1ll11_opy_: str
    bstack11111llll1_opy_: bstack1111l111l1_opy_
    def __new__(cls):
        if not cls._1lllll11l11_opy_:
            cls._1lllll11l11_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lllll11l11_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll111ll1l_opy_ = False
        self.bstack1llll111lll_opy_ = None
        self.bstack1llll111ll1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1llll1111l1_opy_, None)
        self.bstack1lllll11lll_opy_ = os.environ.get(bstack1lll1ll111l_opy_, bstack11l1lll_opy_ (u"ࠨࠢ။")) == bstack11l1lll_opy_ (u"ࠢࠣ၌")
        self.bstack1lll1ll1111_opy_ = False
        self.bstack1lll1llll11_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll11111l1_opy_ = None
        self.test_framework = None
        self.bstack1111111111_opy_ = None
        self.bstack1llll11llll_opy_=bstack11l1lll_opy_ (u"ࠣࠤ၍")
        self.session_framework = None
        self.logger = bstack1l11l1lll_opy_.get_logger(self.__class__.__name__, bstack1l11l1lll_opy_.bstack1lllll11ll1_opy_())
        self.bstack1lll111l1ll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack11111llll1_opy_ = bstack1111l111l1_opy_()
        self.bstack1lll1l11lll_opy_ = None
        self.bstack1llll11111l_opy_ = None
        self.bstack1ll1lll11ll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll1l11ll1_opy_ = []
    def bstack1lll11l1l_opy_(self):
        return os.environ.get(bstack1l1ll11ll_opy_).lower().__eq__(bstack11l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ၎"))
    def is_enabled(self, config):
        if bstack11l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ၏") in config and str(config[bstack11l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨၐ")]).lower() != bstack11l1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫၑ"):
            return False
        bstack1lll111l1l1_opy_ = [bstack11l1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨၒ"), bstack11l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦၓ")]
        bstack1lll1l11l1l_opy_ = config.get(bstack11l1lll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦၔ")) in bstack1lll111l1l1_opy_ or os.environ.get(bstack11l1lll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪၕ")) in bstack1lll111l1l1_opy_
        os.environ[bstack11l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨၖ")] = str(bstack1lll1l11l1l_opy_) # bstack1lll11l11ll_opy_ bstack1llll1l1111_opy_ VAR to bstack1lllll1l11l_opy_ is binary running
        return bstack1lll1l11l1l_opy_
    def bstack11l1l111_opy_(self):
        for event in bstack1llll111l1l_opy_:
            bstack1lll111111_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1lll111111_opy_.logger.debug(bstack11l1lll_opy_ (u"ࠦࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠣࡁࡃࠦࡻࡢࡴࡪࡷࢂࠦࠢၗ") + str(kwargs) + bstack11l1lll_opy_ (u"ࠧࠨၘ"))
            )
        bstack1lll111111_opy_.register(bstack11lll11lll_opy_.bstack1ll11l1111_opy_, self.__1lll1111ll1_opy_)
        bstack1lll111111_opy_.register(bstack11lll11lll_opy_.CONNECT, self.__1lllll1l1ll_opy_)
        bstack1lll111111_opy_.register(bstack11lll11lll_opy_.bstack1l1llll11l_opy_, self.__1ll1llll1l1_opy_)
        bstack1lll111111_opy_.register(bstack11lll11lll_opy_.bstack1ll1ll1ll1_opy_, self.__1lll1l1ll1l_opy_)
    def bstack1l1l11lll_opy_(self):
        return not self.bstack1lllll11lll_opy_ and os.environ.get(bstack1lll1ll111l_opy_, bstack11l1lll_opy_ (u"ࠨࠢၙ")) != bstack11l1lll_opy_ (u"ࠢࠣၚ")
    def is_running(self):
        if self.bstack1lllll11lll_opy_:
            return self.bstack1lll111ll1l_opy_
        else:
            return bool(self.bstack1llll111lll_opy_)
    def bstack1lll1llll1l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll1l11ll1_opy_) and cli.is_running()
    def __1lll1l1llll_opy_(self, bstack1lllll1ll1l_opy_=10):
        if self.bstack1llll111ll1_opy_:
            return
        bstack11llll111l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1llll1111l1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11l1lll_opy_ (u"ࠣ࡝ࠥၛ") + str(id(self)) + bstack11l1lll_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣၜ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11l1lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧၝ"), 0), (bstack11l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢၞ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lllll1ll1l_opy_)
        self.bstack1llll111lll_opy_ = channel
        self.bstack1llll111ll1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1llll111lll_opy_)
        self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦၟ"), datetime.now() - bstack11llll111l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1llll1111l1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11l1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨၠ") + str(self.bstack1l1l11lll_opy_()) + bstack11l1lll_opy_ (u"ࠢࠣၡ"))
    def __1ll1llll1l1_opy_(self, event_name):
        if self.bstack1l1l11lll_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣၢ"))
        self.__1ll1ll1ll11_opy_()
    def __1lll1l1ll1l_opy_(self, event_name, bstack1lll1l1111l_opy_ = None, bstack1l11lllll_opy_=1):
        if bstack1l11lllll_opy_ == 1:
            self.logger.error(bstack11l1lll_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤၣ"))
        bstack1lll111l111_opy_ = Path(bstack1lll11ll111_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦၤ"))
        if self.bstack1llll1llll1_opy_ and bstack1lll111l111_opy_.exists():
            with open(bstack1lll111l111_opy_, bstack11l1lll_opy_ (u"ࠫࡷ࠭ၥ"), encoding=bstack11l1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫၦ")) as fp:
                data = json.load(fp)
                try:
                    bstack11lll1lll_opy_(bstack11l1lll_opy_ (u"࠭ࡐࡐࡕࡗࠫၧ"), bstack1ll1ll11_opy_(bstack1ll11ll11l_opy_), data, {
                        bstack11l1lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬၨ"): (self.config[bstack11l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪၩ")], self.config[bstack11l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬၪ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1lllll_opy_.format(str(e)))
            bstack1lll111l111_opy_.unlink()
        sys.exit(bstack1l11lllll_opy_)
    @measure(event_name=EVENTS.bstack1lll1ll11l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1lll1111ll1_opy_(self, event_name: str, data):
        from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1lll111_opy_
        self.bstack1llll11llll_opy_, self.bstack1llll1llll1_opy_ = bstack1lll1lll11l_opy_(data.bs_config)
        os.environ[bstack11l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨၫ")] = self.bstack1llll1llll1_opy_
        if not self.bstack1llll11llll_opy_ or not self.bstack1llll1llll1_opy_:
            raise ValueError(bstack11l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥၬ"))
        if self.bstack1l1l11lll_opy_():
            self.__1lllll1l1ll_opy_(event_name, bstack1llll1l111_opy_())
            return
        try:
            bstack1lll1lll111_opy_.end(EVENTS.bstack1111l11ll_opy_.value, EVENTS.bstack1111l11ll_opy_.value + bstack11l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧၭ"), EVENTS.bstack1111l11ll_opy_.value + bstack11l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦၮ"), status=True, failure=None, test_name=None)
            logger.debug(bstack11l1lll_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨၯ"))
        except Exception as e:
            logger.debug(bstack11l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧၰ").format(e))
        start = datetime.now()
        is_started = self.__1lll111ll11_opy_()
        self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨၱ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lll1l1llll_opy_()
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤၲ"), datetime.now() - start)
            start = datetime.now()
            self.__1llll111111_opy_(data)
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤၳ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll1llll1ll_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1lllll1l1ll_opy_(self, event_name: str, data: bstack1llll1l111_opy_):
        if not self.bstack1l1l11lll_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤၴ"))
            return
        bin_session_id = os.environ.get(bstack1lll1ll111l_opy_)
        start = datetime.now()
        self.__1lll1l1llll_opy_()
        self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧၵ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11l1lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨၶ") + str(bin_session_id) + bstack11l1lll_opy_ (u"ࠣࠤၷ"))
        start = datetime.now()
        self.__1llll1l1lll_opy_()
        self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢၸ"), datetime.now() - start)
    def __1lll1lllll1_opy_(self):
        if not self.bstack1llll111ll1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢၹ"))
            return
        bstack1ll1lllllll_opy_ = {
            bstack11l1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣၺ"): (bstack1lll11ll1l1_opy_, bstack1llll11l1l1_opy_, bstack1lll11l111l_opy_),
            bstack11l1lll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢၻ"): (bstack1llll1ll11l_opy_, bstack1llll1lll1l_opy_, bstack1lll111llll_opy_),
        }
        if not self.bstack1lll1l11lll_opy_ and self.session_framework in bstack1ll1lllllll_opy_:
            bstack1lll11111ll_opy_, bstack1ll1lll1l11_opy_, bstack1lll1l11l11_opy_ = bstack1ll1lllllll_opy_[self.session_framework]
            bstack1lll1l1l1ll_opy_ = bstack1ll1lll1l11_opy_()
            self.bstack1llll11111l_opy_ = bstack1lll1l1l1ll_opy_
            self.bstack1lll1l11lll_opy_ = bstack1lll1l11l11_opy_
            self.bstack1lll1l11ll1_opy_.append(bstack1lll1l1l1ll_opy_)
            self.bstack1lll1l11ll1_opy_.append(bstack1lll11111ll_opy_(self.bstack1llll11111l_opy_))
        if not self.bstack1ll1lll11ll_opy_ and self.config_observability and self.config_observability.success: # bstack1lll11l1l1l_opy_
            self.bstack1ll1lll11ll_opy_ = bstack1llll11l11l_opy_(self.bstack1lll1l11lll_opy_, self.bstack1llll11111l_opy_) # bstack1lll1l1l111_opy_
            self.bstack1lll1l11ll1_opy_.append(self.bstack1ll1lll11ll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1ll1lll1_opy_(self.bstack1lll1l11lll_opy_, self.bstack1llll11111l_opy_)
            self.bstack1lll1l11ll1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11l1lll_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣၼ"), False) == True:
            self.ai = bstack1llll1l1l1l_opy_()
            self.bstack1lll1l11ll1_opy_.append(self.ai)
        if not self.percy and self.bstack1lll11111l1_opy_ and self.bstack1lll11111l1_opy_.success:
            self.percy = bstack1lll11l1111_opy_(self.bstack1lll11111l1_opy_)
            self.bstack1lll1l11ll1_opy_.append(self.percy)
        for mod in self.bstack1lll1l11ll1_opy_:
            if not mod.bstack1lll1l1lll1_opy_():
                mod.configure(self.bstack1llll111ll1_opy_, self.config, self.cli_bin_session_id, self.bstack11111llll1_opy_)
    def __1llll1l1ll1_opy_(self):
        for mod in self.bstack1lll1l11ll1_opy_:
            if mod.bstack1lll1l1lll1_opy_():
                mod.configure(self.bstack1llll111ll1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1lll111l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1llll111111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll1ll1111_opy_:
            return
        self.__1ll1lllll11_opy_(data)
        bstack11llll111l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11l1lll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢၽ")
        req.sdk_language = bstack11l1lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣၾ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll1lll11l1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠤ࡞ࠦၿ") + str(id(self)) + bstack11l1lll_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႀ"))
            r = self.bstack1llll111ll1_opy_.StartBinSession(req)
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨႁ"), datetime.now() - bstack11llll111l_opy_)
            os.environ[bstack1lll1ll111l_opy_] = r.bin_session_id
            self.__1lll111lll1_opy_(r)
            self.__1lll1lllll1_opy_()
            self.bstack11111llll1_opy_.start()
            self.bstack1lll1ll1111_opy_ = True
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡡࠢႂ") + str(id(self)) + bstack11l1lll_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦႃ"))
        except grpc.bstack1lll1ll1l11_opy_ as bstack1lll1ll11ll_opy_:
            self.logger.error(bstack11l1lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤႄ") + str(bstack1lll1ll11ll_opy_) + bstack11l1lll_opy_ (u"ࠣࠤႅ"))
            traceback.print_exc()
            raise bstack1lll1ll11ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨႆ") + str(e) + bstack11l1lll_opy_ (u"ࠥࠦႇ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lllll1111l_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1llll1l1lll_opy_(self):
        if not self.bstack1l1l11lll_opy_() or not self.cli_bin_session_id or self.bstack1lll1llll11_opy_:
            return
        bstack11llll111l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫႈ"), bstack11l1lll_opy_ (u"ࠬ࠶ࠧႉ")))
        try:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨ࡛ࠣႊ") + str(id(self)) + bstack11l1lll_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႋ"))
            r = self.bstack1llll111ll1_opy_.ConnectBinSession(req)
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧႌ"), datetime.now() - bstack11llll111l_opy_)
            self.__1lll111lll1_opy_(r)
            self.__1lll1lllll1_opy_()
            self.bstack11111llll1_opy_.start()
            self.bstack1lll1llll11_opy_ = True
            self.logger.debug(bstack11l1lll_opy_ (u"ࠤ࡞ႍࠦ") + str(id(self)) + bstack11l1lll_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤႎ"))
        except grpc.bstack1lll1ll1l11_opy_ as bstack1lll1ll11ll_opy_:
            self.logger.error(bstack11l1lll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨႏ") + str(bstack1lll1ll11ll_opy_) + bstack11l1lll_opy_ (u"ࠧࠨ႐"))
            traceback.print_exc()
            raise bstack1lll1ll11ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ႑") + str(e) + bstack11l1lll_opy_ (u"ࠢࠣ႒"))
            traceback.print_exc()
            raise e
    def __1lll111lll1_opy_(self, r):
        self.bstack1lll11lll11_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11l1lll_opy_ (u"ࠣࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ႓") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11l1lll_opy_ (u"ࠤࡨࡱࡵࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡹࡳࡪࠢ႔"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11l1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡧࡵࡧࡾࠦࡩࡴࠢࡶࡩࡳࡺࠠࡰࡰ࡯ࡽࠥࡧࡳࠡࡲࡤࡶࡹࠦ࡯ࡧࠢࡷ࡬ࡪࠦࠢࡄࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠰ࠧࠦࡡ࡯ࡦࠣࡸ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡡ࡭ࡵࡲࠤࡺࡹࡥࡥࠢࡥࡽ࡙ࠥࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡪࡸࡥࡧࡱࡵࡩ࠱ࠦࡎࡰࡰࡨࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡩࡴࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ႕")
        self.bstack1lll11111l1_opy_ = getattr(r, bstack11l1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ႖"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ႗")] = self.config_testhub.jwt
        os.environ[bstack11l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ႘")] = self.config_testhub.build_hashed_id
    def bstack1llll1l11ll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll111ll1l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll1ll1l1l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll1ll1l1l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1llll1l11ll_opy_(event_name=EVENTS.bstack1lll1l111l1_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1lll111ll11_opy_(self, bstack1lllll1ll1l_opy_=10):
        if self.bstack1lll111ll1l_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤ႙"))
            return True
        self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢႚ"))
        if os.getenv(bstack11l1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤႛ")) == bstack1llll11l111_opy_:
            self.cli_bin_session_id = bstack1llll11l111_opy_
            self.cli_listen_addr = bstack11l1lll_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨႜ") % (self.cli_bin_session_id)
            self.bstack1lll111ll1l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1llll11llll_opy_, bstack11l1lll_opy_ (u"ࠦࡸࡪ࡫ࠣႝ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1llll1l1l11_opy_ compat for text=True in bstack1lll1l111ll_opy_ python
            encoding=bstack11l1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ႞"),
            bufsize=1,
            close_fds=True,
        )
        bstack1llll1ll1ll_opy_ = threading.Thread(target=self.__1lllll11l1l_opy_, args=(bstack1lllll1ll1l_opy_,))
        bstack1llll1ll1ll_opy_.start()
        bstack1llll1ll1ll_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥ႟") + str(self.process.stderr.read()) + bstack11l1lll_opy_ (u"ࠢࠣႠ"))
        if not self.bstack1lll111ll1l_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣ࡝ࠥႡ") + str(id(self)) + bstack11l1lll_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧႢ"))
            self.__1ll1ll1ll11_opy_()
        self.logger.debug(bstack11l1lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦႣ") + str(self.bstack1lll111ll1l_opy_) + bstack11l1lll_opy_ (u"ࠦࠧႤ"))
        return self.bstack1lll111ll1l_opy_
    def __1lllll11l1l_opy_(self, bstack1lllll1l1l1_opy_=10):
        bstack1lll11l11l1_opy_ = time.time()
        while self.process and time.time() - bstack1lll11l11l1_opy_ < bstack1lllll1l1l1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11l1lll_opy_ (u"ࠧ࡯ࡤ࠾ࠤႥ") in line:
                    self.cli_bin_session_id = line.split(bstack11l1lll_opy_ (u"ࠨࡩࡥ࠿ࠥႦ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨႧ") + str(self.cli_bin_session_id) + bstack11l1lll_opy_ (u"ࠣࠤႨ"))
                    continue
                if bstack11l1lll_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥႩ") in line:
                    self.cli_listen_addr = line.split(bstack11l1lll_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦႪ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢႫ") + str(self.cli_listen_addr) + bstack11l1lll_opy_ (u"ࠧࠨႬ"))
                    continue
                if bstack11l1lll_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧႭ") in line:
                    port = line.split(bstack11l1lll_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨႮ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢႯ") + str(port) + bstack11l1lll_opy_ (u"ࠤࠥႰ"))
                    continue
                if line.strip() == bstack1ll1ll1llll_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11l1lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧႱ"), bstack11l1lll_opy_ (u"ࠦ࠶ࠨႲ")) == bstack11l1lll_opy_ (u"ࠧ࠷ࠢႳ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll111ll1l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11l1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢႴ") + str(e) + bstack11l1lll_opy_ (u"ࠢࠣႵ"))
        return False
    @measure(event_name=EVENTS.bstack1lll1111l11_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def __1ll1ll1ll11_opy_(self):
        if self.bstack1llll111lll_opy_:
            self.bstack11111llll1_opy_.stop()
            start = datetime.now()
            if self.bstack1llll1lll11_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll1llll11_opy_:
                    self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧႶ"), datetime.now() - start)
                else:
                    self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨႷ"), datetime.now() - start)
            self.__1llll1l1ll1_opy_()
            start = datetime.now()
            self.bstack1llll111lll_opy_.close()
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧႸ"), datetime.now() - start)
            self.bstack1llll111lll_opy_ = None
        if self.process:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠦࡸࡺ࡯ࡱࠤႹ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣႺ"), datetime.now() - start)
            self.process = None
            if self.bstack1lllll11lll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11ll111ll_opy_()
                self.logger.info(
                    bstack11l1lll_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤႻ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11l1lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭Ⴜ")] = self.config_testhub.build_hashed_id
        self.bstack1lll111ll1l_opy_ = False
    def __1ll1lllll11_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11l1lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥႽ")] = selenium.__version__
            data.frameworks.append(bstack11l1lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦႾ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11l1lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢႿ")] = __version__
            data.frameworks.append(bstack11l1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣჀ"))
        except:
            pass
    def bstack1ll1llllll1_opy_(self, hub_url: str, platform_index: int, bstack1l1ll1ll1_opy_: Any):
        if self.bstack1111111111_opy_:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤჁ"))
            return
        try:
            bstack11llll111l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11l1lll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣჂ")
            self.bstack1111111111_opy_ = bstack1lll111llll_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1lllll1l_opy_={bstack11l1lll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦჃ"): bstack1l1ll1ll1_opy_}
            )
            def bstack1lll1ll1ll1_opy_(self):
                return
            if self.config.get(bstack11l1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥჄ"), True):
                Service.start = bstack1lll1ll1ll1_opy_
                Service.stop = bstack1lll1ll1ll1_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack1l11ll11_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll1lll1l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥჅ"), datetime.now() - bstack11llll111l_opy_)
        except Exception as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤ჆") + str(e) + bstack11l1lll_opy_ (u"ࠦࠧჇ"))
    def bstack1lllll111ll_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1lllll11ll_opy_
            self.bstack1111111111_opy_ = bstack1lll11l111l_opy_(
                platform_index,
                framework_name=bstack11l1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ჈"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࠢ჉") + str(e) + bstack11l1lll_opy_ (u"ࠢࠣ჊"))
            pass
    def bstack1ll1llll111_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥ჋"))
            return
        if bstack1ll11lll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11l1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤ჌"): pytest.__version__ }, [bstack11l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢჍ")], self.bstack11111llll1_opy_, self.bstack1llll111ll1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lll11l1lll_opy_({ bstack11l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦ჎"): pytest.__version__ }, [bstack11l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧ჏")], self.bstack11111llll1_opy_, self.bstack1llll111ll1_opy_)
        except Exception as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥა") + str(e) + bstack11l1lll_opy_ (u"ࠢࠣბ"))
        self.bstack1llll1ll111_opy_()
    def bstack1llll1ll111_opy_(self):
        if not self.bstack1lll11l1l_opy_():
            return
        bstack1l11l11lll_opy_ = None
        def bstack1ll1lll1l_opy_(config, startdir):
            return bstack11l1lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨგ").format(bstack11l1lll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣდ"))
        def bstack1ll1l1llll_opy_():
            return
        def bstack11l1l11l1_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11l1lll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪე"):
                return bstack11l1lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥვ")
            else:
                return bstack1l11l11lll_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l11l11lll_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1ll1lll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l1llll_opy_
            Config.getoption = bstack11l1l11l1_opy_
        except Exception as e:
            self.logger.error(bstack11l1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢზ") + str(e) + bstack11l1lll_opy_ (u"ࠨࠢთ"))
    def bstack1lll111l11l_opy_(self):
        bstack1lllll1ll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1lllll1ll_opy_, dict):
            if cli.config_observability:
                bstack1lllll1ll_opy_.update(
                    {bstack11l1lll_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢი"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11l1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦკ") in accessibility.get(bstack11l1lll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥლ"), {}):
                    bstack1ll1lll1ll1_opy_ = accessibility.get(bstack11l1lll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦმ"))
                    bstack1ll1lll1ll1_opy_.update({ bstack11l1lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧნ"): bstack1ll1lll1ll1_opy_.pop(bstack11l1lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣო")) })
                bstack1lllll1ll_opy_.update({bstack11l1lll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨპ"): accessibility })
        return bstack1lllll1ll_opy_
    @measure(event_name=EVENTS.bstack1lll11l1l11_opy_, stage=STAGE.bstack1l1l1lll1_opy_)
    def bstack1llll1lll11_opy_(self, bstack1lll1ll1lll_opy_: str = None, bstack1ll1ll1ll1l_opy_: str = None, bstack1l11lllll_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll111ll1_opy_:
            return
        bstack11llll111l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1l11lllll_opy_:
            req.bstack1l11lllll_opy_ = bstack1l11lllll_opy_
        if bstack1lll1ll1lll_opy_:
            req.bstack1lll1ll1lll_opy_ = bstack1lll1ll1lll_opy_
        if bstack1ll1ll1ll1l_opy_:
            req.bstack1ll1ll1ll1l_opy_ = bstack1ll1ll1ll1l_opy_
        try:
            r = self.bstack1llll111ll1_opy_.StopBinSession(req)
            SDKCLI.bstack1lll1llllll_opy_ = r.bstack1lll1llllll_opy_
            SDKCLI.bstack1l111l1l1l_opy_ = r.bstack1l111l1l1l_opy_
            self.bstack11ll1111_opy_(bstack11l1lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡰࡲࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣჟ"), datetime.now() - bstack11llll111l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11ll1111_opy_(self, key: str, value: timedelta):
        tag = bstack11l1lll_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣრ") if self.bstack1l1l11lll_opy_() else bstack11l1lll_opy_ (u"ࠤࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳࠣს")
        self.bstack1lll111l1ll_opy_[bstack11l1lll_opy_ (u"ࠥ࠾ࠧტ").join([tag + bstack11l1lll_opy_ (u"ࠦ࠲ࠨუ") + str(id(self)), key])] += value
    def bstack11ll111ll_opy_(self):
        if not os.getenv(bstack11l1lll_opy_ (u"ࠧࡊࡅࡃࡗࡊࡣࡕࡋࡒࡇࠤფ"), bstack11l1lll_opy_ (u"ࠨ࠰ࠣქ")) == bstack11l1lll_opy_ (u"ࠢ࠲ࠤღ"):
            return
        bstack1lllll11111_opy_ = dict()
        bstack1lllllll111_opy_ = []
        if self.test_framework:
            bstack1lllllll111_opy_.extend(list(self.test_framework.bstack1lllllll111_opy_.values()))
        if self.bstack1111111111_opy_:
            bstack1lllllll111_opy_.extend(list(self.bstack1111111111_opy_.bstack1lllllll111_opy_.values()))
        for instance in bstack1lllllll111_opy_:
            if not instance.platform_index in bstack1lllll11111_opy_:
                bstack1lllll11111_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lllll11111_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1lll1lll_opy_().items():
                report[k] += v
                report[k.split(bstack11l1lll_opy_ (u"ࠣ࠼ࠥყ"))[0]] += v
        bstack1llll11ll1l_opy_ = sorted([(k, v) for k, v in self.bstack1lll111l1ll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll11lll1l_opy_ = 0
        for r in bstack1llll11ll1l_opy_:
            bstack1ll1lll1l1l_opy_ = r[1].total_seconds()
            bstack1lll11lll1l_opy_ += bstack1ll1lll1l1l_opy_
            self.logger.debug(bstack11l1lll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡻࡳ࡝࠳ࡡࢂࡃࠢშ") + str(bstack1ll1lll1l1l_opy_) + bstack11l1lll_opy_ (u"ࠥࠦჩ"))
        self.logger.debug(bstack11l1lll_opy_ (u"ࠦ࠲࠳ࠢც"))
        bstack1llll1lllll_opy_ = []
        for platform_index, report in bstack1lllll11111_opy_.items():
            bstack1llll1lllll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1llll1lllll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11l1ll111l_opy_ = set()
        bstack1ll1llll11l_opy_ = 0
        for r in bstack1llll1lllll_opy_:
            bstack1ll1lll1l1l_opy_ = r[2].total_seconds()
            bstack1ll1llll11l_opy_ += bstack1ll1lll1l1l_opy_
            bstack11l1ll111l_opy_.add(r[0])
            self.logger.debug(bstack11l1lll_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࢁࡲ࡜࠲ࡠࢁ࠿ࢁࡲ࡜࠳ࡠࢁࡂࠨძ") + str(bstack1ll1lll1l1l_opy_) + bstack11l1lll_opy_ (u"ࠨࠢწ"))
        if self.bstack1l1l11lll_opy_():
            self.logger.debug(bstack11l1lll_opy_ (u"ࠢ࠮࠯ࠥჭ"))
            self.logger.debug(bstack11l1lll_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࢁࡴࡰࡶࡤࡰࡤࡩ࡬ࡪࡿࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠱ࢀࡹࡴࡳࠪࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠮ࢃ࠽ࠣხ") + str(bstack1ll1llll11l_opy_) + bstack11l1lll_opy_ (u"ࠤࠥჯ"))
        else:
            self.logger.debug(bstack11l1lll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࠢჰ") + str(bstack1lll11lll1l_opy_) + bstack11l1lll_opy_ (u"ࠦࠧჱ"))
        self.logger.debug(bstack11l1lll_opy_ (u"ࠧ࠳࠭ࠣჲ"))
    def bstack1lll11lll11_opy_(self, r):
        if r is not None and getattr(r, bstack11l1lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࠧჳ"), None) and getattr(r.testhub, bstack11l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧჴ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11l1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢჵ")))
            for bstack1llll11lll1_opy_, err in errors.items():
                if err[bstack11l1lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧჶ")] == bstack11l1lll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨჷ"):
                    self.logger.info(err[bstack11l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჸ")])
                else:
                    self.logger.error(err[bstack11l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ჹ")])
    def bstack11l11lll_opy_(self):
        return SDKCLI.bstack1lll1llllll_opy_, SDKCLI.bstack1l111l1l1l_opy_
cli = SDKCLI()