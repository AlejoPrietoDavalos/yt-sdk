from typing import List
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
    def __init__(self, *, path_folder_output: Path):
        self.path_folder_output = path_folder_output

    def extract_info(self, *, ydl: YoutubeDL, youtube_id: str) -> dict:
        url = youtube_id_to_url(youtube_id=youtube_id)
        yt_info = ydl.extract_info(url, download=True)
        
        # Filtra los campos no serializables
        yt_info = serialize_yt_info(yt_info)
        
        for field_to_delete in self.info_fields_to_delete():
            yt_info.pop(field_to_delete)

        with open(self.paths.info, "w") as f:
            json.dump(yt_info, f, indent=INDENT)

    def audio(self, *, youtube_id: str) -> None:
        """Solo descarga el audio del video en formato `mp3`.
        - TODO: Ver como descargar el resto de formatos y posibilidades, abstraer.
        """
        """
        - Crea un folder en `path_out/<youtube_id>/<youtube_id>.mp3`.
        """
        logger.info(f"- Download audio - youtube_id={youtube_id}")
        yt_options = self.get_options_youtube_dl(youtube_id=youtube_id)
        with YoutubeDL(yt_options) as ydl:
            yt_info = self.extract_info(ydl=ydl)
            # --> TODO: Se puede seguir procesando el yt_info.

    def get_options_youtube_dl(self, *, youtube_id: str) -> dict:
        return {
            "format": "bestaudio/best",
            "outtmpl": str(self.path_folder_output / f"{youtube_id}.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",    # TODO: Ver que se puede tocar acá.
                    "preferredcodec": "mp3",        # TODO: Ver que se puede tocar acá.
                    "preferredquality": "192"       # TODO: Ver que se puede tocar acá.
                }
            ]
        }

    @staticmethod
    def info_fields_to_delete() -> List[str]:
        """ Campos para borrar del info, son pesados, ver si sirve el dato."""
        return [
            "formats",
            "thumbnails",
            "heatmap"       #TODO: heatmap -> Graficar esto. Creo que es la forma de las ondas.
        ]
