from django.test import TestCase

from .utils import normalize_youtube_url


class YouTubeUrlNormalizationTests(TestCase):
    def test_normalizes_watch_url(self):
        self.assertEqual(
            normalize_youtube_url("https://www.youtube.com/watch?v=VIDEO_ID"),
            "https://www.youtube.com/watch?v=VIDEO_ID",
        )

    def test_normalizes_watch_url_without_www(self):
        self.assertEqual(
            normalize_youtube_url("https://youtube.com/watch?v=VIDEO_ID&t=30"),
            "https://www.youtube.com/watch?v=VIDEO_ID",
        )

    def test_normalizes_shared_youtu_be_url(self):
        self.assertEqual(
            normalize_youtube_url("https://youtu.be/VIDEO_ID?si=abc123"),
            "https://www.youtube.com/watch?v=VIDEO_ID",
        )

    def test_normalizes_shorts_url(self):
        self.assertEqual(
            normalize_youtube_url("https://www.youtube.com/shorts/VIDEO_ID"),
            "https://www.youtube.com/watch?v=VIDEO_ID",
        )

    def test_normalizes_embed_url(self):
        self.assertEqual(
            normalize_youtube_url("https://www.youtube.com/embed/VIDEO_ID"),
            "https://www.youtube.com/watch?v=VIDEO_ID",
        )

    def test_rejects_invalid_url(self):
        with self.assertRaisesMessage(ValueError, "Invalid YouTube URL."):
            normalize_youtube_url("https://example.com/watch?v=VIDEO_ID")
