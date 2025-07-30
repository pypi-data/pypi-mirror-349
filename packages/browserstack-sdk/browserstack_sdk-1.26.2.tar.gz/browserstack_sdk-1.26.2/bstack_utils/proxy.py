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
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111llll11l1_opy_
bstack111l111ll_opy_ = Config.bstack11l11lll1l_opy_()
def bstack111l11l111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l111l1ll_opy_(bstack111l111ll1l_opy_, bstack111l111lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l111ll1l_opy_):
        with open(bstack111l111ll1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l11l111l_opy_(bstack111l111ll1l_opy_):
        pac = get_pac(url=bstack111l111ll1l_opy_)
    else:
        raise Exception(bstack111l11_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭᷆").format(bstack111l111ll1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l11_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣ᷇"), 80))
        bstack111l111ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l111ll11_opy_ = bstack111l11_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩ᷈")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l111lll1_opy_, bstack111l111ll11_opy_)
    return proxy_url
def bstack1l1l1l1ll1_opy_(config):
    return bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᷉") in config or bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿ᷊ࠧ") in config
def bstack11lllllll_opy_(config):
    if not bstack1l1l1l1ll1_opy_(config):
        return
    if config.get(bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᷋")):
        return config.get(bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᷌"))
    if config.get(bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ᷍")):
        return config.get(bstack111l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ᷎ࠫ"))
def bstack1l1l11ll1l_opy_(config, bstack111l111lll1_opy_):
    proxy = bstack11lllllll_opy_(config)
    proxies = {}
    if config.get(bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼ᷏ࠫ")) or config.get(bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ᷐࠭")):
        if proxy.endswith(bstack111l11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ᷑")):
            proxies = bstack1ll1l1l111_opy_(proxy, bstack111l111lll1_opy_)
        else:
            proxies = {
                bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ᷒"): proxy
            }
    bstack111l111ll_opy_.bstack111l1llll_opy_(bstack111l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬᷓ"), proxies)
    return proxies
def bstack1ll1l1l111_opy_(bstack111l111ll1l_opy_, bstack111l111lll1_opy_):
    proxies = {}
    global bstack111l11l1111_opy_
    if bstack111l11_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᷔ") in globals():
        return bstack111l11l1111_opy_
    try:
        proxy = bstack111l111l1ll_opy_(bstack111l111ll1l_opy_, bstack111l111lll1_opy_)
        if bstack111l11_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᷕ") in proxy:
            proxies = {}
        elif bstack111l11_opy_ (u"ࠣࡊࡗࡘࡕࠨᷖ") in proxy or bstack111l11_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᷗ") in proxy or bstack111l11_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᷘ") in proxy:
            bstack111l111llll_opy_ = proxy.split(bstack111l11_opy_ (u"ࠦࠥࠨᷙ"))
            if bstack111l11_opy_ (u"ࠧࡀ࠯࠰ࠤᷚ") in bstack111l11_opy_ (u"ࠨࠢᷛ").join(bstack111l111llll_opy_[1:]):
                proxies = {
                    bstack111l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᷜ"): bstack111l11_opy_ (u"ࠣࠤᷝ").join(bstack111l111llll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᷞ"): str(bstack111l111llll_opy_[0]).lower() + bstack111l11_opy_ (u"ࠥ࠾࠴࠵ࠢᷟ") + bstack111l11_opy_ (u"ࠦࠧᷠ").join(bstack111l111llll_opy_[1:])
                }
        elif bstack111l11_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᷡ") in proxy:
            bstack111l111llll_opy_ = proxy.split(bstack111l11_opy_ (u"ࠨࠠࠣᷢ"))
            if bstack111l11_opy_ (u"ࠢ࠻࠱࠲ࠦᷣ") in bstack111l11_opy_ (u"ࠣࠤᷤ").join(bstack111l111llll_opy_[1:]):
                proxies = {
                    bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᷥ"): bstack111l11_opy_ (u"ࠥࠦᷦ").join(bstack111l111llll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᷧ"): bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᷨ") + bstack111l11_opy_ (u"ࠨࠢᷩ").join(bstack111l111llll_opy_[1:])
                }
        else:
            proxies = {
                bstack111l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᷪ"): proxy
            }
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᷫ"), bstack111llll11l1_opy_.format(bstack111l111ll1l_opy_, str(e)))
    bstack111l11l1111_opy_ = proxies
    return proxies