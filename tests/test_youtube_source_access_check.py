import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import youtube_source_access_check as checker


class YouTubeSourceAccessTests(unittest.TestCase):
    def test_watch_url_with_playlist_parameters(self):
        video_id, canonical = checker.parse_video_url(
            "https://www.youtube.com/watch?v=r30Rs_NuExc&list=PLe-C8xNnzJX8&index=2")
        self.assertEqual(video_id, "r30Rs_NuExc")
        self.assertEqual(canonical, "https://www.youtube.com/watch?v=r30Rs_NuExc")

    def test_short_url(self):
        video_id, _ = checker.parse_video_url("https://youtu.be/r30Rs_NuExc?t=12")
        self.assertEqual(video_id, "r30Rs_NuExc")

    def test_embed_url(self):
        video_id, _ = checker.parse_video_url(
            "https://www.youtube-nocookie.com/embed/r30Rs_NuExc")
        self.assertEqual(video_id, "r30Rs_NuExc")

    def test_rejects_non_youtube_host(self):
        with self.assertRaises(checker.InputError):
            checker.parse_video_url("https://example.com/watch?v=r30Rs_NuExc")

    def test_rejects_playlist_without_video_id(self):
        with self.assertRaises(checker.InputError):
            checker.parse_video_url("https://www.youtube.com/playlist?list=PLe-C8xNnzJX8")

    def test_rejects_malformed_video_id(self):
        with self.assertRaises(checker.InputError):
            checker.parse_video_url("https://www.youtube.com/watch?v=short")

    def test_oembed_success_means_metadata_only(self):
        result = checker.classify_oembed(
            200, {"title": "Example title", "author_name": "Example channel"})
        self.assertEqual(result["access_state"], "METADATA_ONLY")
        self.assertEqual(result["title"], "Example title")
        self.assertEqual(result["channel"], "Example channel")

    def test_http_denial_does_not_claim_video_unavailable(self):
        result = checker.classify_oembed(403, None)
        self.assertEqual(result["access_state"], "METADATA_ENDPOINT_BLOCKED")
        self.assertIsNone(result["title"])

    def test_report_disclaims_playback(self):
        result = checker.classify_oembed(
            200, {"title": "A title", "author_name": "A channel"})
        report = checker.build_report(
            "r30Rs_NuExc",
            "https://www.youtube.com/watch?v=r30Rs_NuExc", result)
        self.assertIn("Official player playback: NOT_TESTED", report)
        self.assertIn("Frame/audio inspection: NOT_STARTED", report)
        self.assertIn("does NOT prove that the video player can play", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
