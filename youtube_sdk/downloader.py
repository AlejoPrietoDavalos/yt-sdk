from pathlib import Path
import logging
import json

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)
INDENT = 4


def serialize_yt_info(yt_info: dict) -> dict:
    yt_info_cleaned = {}

    for key, value in yt_info.items():
        try:
            # Intenta serializar el valor para ver si es serializable
            json.dumps(value)
            yt_info_cleaned[key] = value
        except (TypeError, ValueError):
            # Si el valor no es serializable, lo omite
            continue

    return yt_info_cleaned


def youtube_id_to_url(*, youtube_id: str) -> str:
    return f"https://www.youtube.com/watch?v={youtube_id}"


class YoutubeDownloader:
    def __init__(self):
        ...

    def extract_info(self, *, ydl: YoutubeDL, youtube_id: str) -> dict:
        yt_info = ydl.extract_info(youtube_id_to_url(youtube_id=youtube_id), download=True)
        
        # Filtra los campos no serializables
        yt_info = serialize_yt_info(yt_info)
        
        for field_to_delete in self.info_fields_to_delete():
            yt_info.pop(field_to_delete)
        
        # Path donde descarga el audio dentro de la maquina.
        #path_audio = Path(yt_info["requested_downloads"][0]["filepath"])

        with open(self.paths.info, "w") as f:
            json.dump(yt_info, f, indent=INDENT)

    def audio(self) -> None:
        """Solo descarga el audio del video en formato `mp3`.
        - TODO: Ver como descargar el resto de formatos y posibilidades, abstraer.
        """
        """
        - Crea un folder en `path_out/<youtube_id>/<youtube_id>.mp3`.
        """
        logger.info(f"- Download audio - youtube_id={self.youtube_id}")
        with YoutubeDL(self.get_options_youtube_dl()) as ydl:
            yt_info = self.extract_info(ydl=ydl)
            # --> TODO: Se puede seguir procesando el yt_info.

    def get_options_youtube_dl(self, *, path_folder: Path) -> dict:
        return {
            "format": "bestaudio/best",
            "outtmpl": str(path_folder / f"{self.youtube_id}.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ]
        }