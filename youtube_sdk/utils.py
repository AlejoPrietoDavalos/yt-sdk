from typing import Optional, List
from urllib.parse import urlparse
import re

from youtube_sdk.typings import T_YoutubeId


def youtube_id_from_url(*, url: str) -> Optional[T_YoutubeId]:
    # Validar que la URL es de YouTube (sin importar el esquema http/https)
    parsed_url = urlparse(url)
    if parsed_url.netloc not in ["www.youtube.com", "youtube.com"]:
        return None

    # Buscar el ID del video en la URL
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def youtube_ids_from_urls(*, urls: List[str]) -> List[tuple[Optional[T_YoutubeId], str]]:
    return [(youtube_id_from_url(url=url), url) for url in urls]
