from urllib.parse import parse_qs, urlparse


YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={video_id}"


def normalize_youtube_url(url):
    """
    Return a clean YouTube watch URL for supported YouTube URL formats.
    """

    if not url:
        raise ValueError("Invalid YouTube URL.")

    parsed_url = urlparse(url)
    host = (parsed_url.hostname or "").lower()
    path_parts = [
        part for part in parsed_url.path.split("/")
        if part
    ]

    video_id = None

    if host in {"www.youtube.com", "youtube.com"}:
        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        elif len(path_parts) >= 2 and path_parts[0] in {"shorts", "embed"}:
            video_id = path_parts[1]
    elif host == "youtu.be" and path_parts:
        video_id = path_parts[0]

    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    return YOUTUBE_WATCH_URL.format(video_id=video_id)


def create_dummy_questions():
    """
    Return 10 dummy questions.
    """

    questions = []

    for number in range(1, 11):
        questions.append(
            {
                "question_title": f"Question {number}",
                "question_options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D",
                ],
                "answer": "Option A",
            }
        )

    return questions
