from pathlib import Path

from yt_dlp import YoutubeDL


DOWNLOAD_DIR = Path("media/audio")


def get_download_options(output_template):
    """
    Return yt-dlp download options.
    """

    return {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
    }


def get_output_template():
    """
    Return yt-dlp output template.
    """

    return str(DOWNLOAD_DIR / "%(id)s.%(ext)s")


def ensure_download_dir():
    """
    Create audio download directory.
    """

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def download_audio(video_url):
    """
    Download youtube audio file.
    """

    ensure_download_dir()
    output_template = get_output_template()
    options = get_download_options(output_template)

    with YoutubeDL(options) as youtube:
        info = youtube.extract_info(video_url, download=True)

    return DOWNLOAD_DIR / f"{info['id']}.{info['ext']}"