import requests
import urllib.robotparser
from webcrawler_project.config import USER_AGENT
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from webcrawler_project.utils.logger import get_logger

logger = get_logger("Fetcher")

robots_parsers = {}

def allowed_by_robots(url):
    parsed = urlparse(url)
    domain = f"{parsed.scheme}://{parsed.netloc}"
    if domain not in robots_parsers:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(urljoin(domain, "/robots.txt"))
        try:
            rp.read()
            robots_parsers[domain] = rp
        except Exception:
            robots_parsers[domain] = None
            return True
    rp = robots_parsers[domain]
    return rp is None or rp.can_fetch(USER_AGENT, url)

def fetch(url):
    logger.debug(f"Fetching: {url}")
    if not allowed_by_robots(url):
        logger.warning(f"Blocked by robots.txt: {url}")
        return None, []
    try:
        resp = requests.get(url, timeout=5, headers={"User-Agent": USER_AGENT})
        if resp.status_code != 200:
            return None, []
        soup = BeautifulSoup(resp.text, "html.parser")

        # meta robots check
        meta = soup.find("meta", attrs={"name": "robots"})
        robots_content = meta["content"].lower() if meta and "content" in meta.attrs else "all"
        if "noindex" in robots_content:
            return None, []
        
        return soup.get_text(), [
            urljoin(url, a["href"]) for a in soup.find_all("a", href=True)
            if urljoin(url, a["href"]).startswith("http")
        ] if "nofollow" not in robots_content else []
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None, []
