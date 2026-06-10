from pathlib import Path

from yt_dlp import YoutubeDL


DOWNLOAD_DIR = Path("media/audio")


def download_audio(video_url):
    """
    Download youtube audio file.
    """

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_template = str(
        DOWNLOAD_DIR / "%(id)s.%(ext)s"
    )

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
    }

    with YoutubeDL(options) as youtube:
        info = youtube.extract_info(
            video_url,
            download=True,
        )

    return DOWNLOAD_DIR / f"{info['id']}.{info['ext']}"