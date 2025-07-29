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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111llll1l11_opy_
bstack11ll1llll1_opy_ = Config.bstack1ll1l1l1l1_opy_()
def bstack111l11l1l1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l11l11l1_opy_(bstack111l111llll_opy_, bstack111l11l11ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l111llll_opy_):
        with open(bstack111l111llll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l11l1l1l_opy_(bstack111l111llll_opy_):
        pac = get_pac(url=bstack111l111llll_opy_)
    else:
        raise Exception(bstack11l1lll_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᶻ").format(bstack111l111llll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1lll_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦᶼ"), 80))
        bstack111l11l111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l11l111l_opy_ = bstack11l1lll_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬᶽ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l11l11ll_opy_, bstack111l11l111l_opy_)
    return proxy_url
def bstack1l1ll1lll1_opy_(config):
    return bstack11l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᶾ") in config or bstack11l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᶿ") in config
def bstack111ll1lll_opy_(config):
    if not bstack1l1ll1lll1_opy_(config):
        return
    if config.get(bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᷀")):
        return config.get(bstack11l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᷁"))
    if config.get(bstack11l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ᷂࠭")):
        return config.get(bstack11l1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᷃"))
def bstack1ll111l1_opy_(config, bstack111l11l11ll_opy_):
    proxy = bstack111ll1lll_opy_(config)
    proxies = {}
    if config.get(bstack11l1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᷄")) or config.get(bstack11l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᷅")):
        if proxy.endswith(bstack11l1lll_opy_ (u"࠭࠮ࡱࡣࡦࠫ᷆")):
            proxies = bstack11l111l1_opy_(proxy, bstack111l11l11ll_opy_)
        else:
            proxies = {
                bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᷇"): proxy
            }
    bstack11ll1llll1_opy_.bstack11l1l11lll_opy_(bstack11l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ᷈"), proxies)
    return proxies
def bstack11l111l1_opy_(bstack111l111llll_opy_, bstack111l11l11ll_opy_):
    proxies = {}
    global bstack111l11l1111_opy_
    if bstack11l1lll_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬ᷉") in globals():
        return bstack111l11l1111_opy_
    try:
        proxy = bstack111l11l11l1_opy_(bstack111l111llll_opy_, bstack111l11l11ll_opy_)
        if bstack11l1lll_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖ᷊ࠥ") in proxy:
            proxies = {}
        elif bstack11l1lll_opy_ (u"ࠦࡍ࡚ࡔࡑࠤ᷋") in proxy or bstack11l1lll_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦ᷌") in proxy or bstack11l1lll_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ᷍") in proxy:
            bstack111l11l1l11_opy_ = proxy.split(bstack11l1lll_opy_ (u"ࠢࠡࠤ᷎"))
            if bstack11l1lll_opy_ (u"ࠣ࠼࠲࠳᷏ࠧ") in bstack11l1lll_opy_ (u"ࠤ᷐ࠥ").join(bstack111l11l1l11_opy_[1:]):
                proxies = {
                    bstack11l1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ᷑"): bstack11l1lll_opy_ (u"ࠦࠧ᷒").join(bstack111l11l1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᷓ"): str(bstack111l11l1l11_opy_[0]).lower() + bstack11l1lll_opy_ (u"ࠨ࠺࠰࠱ࠥᷔ") + bstack11l1lll_opy_ (u"ࠢࠣᷕ").join(bstack111l11l1l11_opy_[1:])
                }
        elif bstack11l1lll_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᷖ") in proxy:
            bstack111l11l1l11_opy_ = proxy.split(bstack11l1lll_opy_ (u"ࠤࠣࠦᷗ"))
            if bstack11l1lll_opy_ (u"ࠥ࠾࠴࠵ࠢᷘ") in bstack11l1lll_opy_ (u"ࠦࠧᷙ").join(bstack111l11l1l11_opy_[1:]):
                proxies = {
                    bstack11l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᷚ"): bstack11l1lll_opy_ (u"ࠨࠢᷛ").join(bstack111l11l1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᷜ"): bstack11l1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᷝ") + bstack11l1lll_opy_ (u"ࠤࠥᷞ").join(bstack111l11l1l11_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᷟ"): proxy
            }
    except Exception as e:
        print(bstack11l1lll_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᷠ"), bstack111llll1l11_opy_.format(bstack111l111llll_opy_, str(e)))
    bstack111l11l1111_opy_ = proxies
    return proxies