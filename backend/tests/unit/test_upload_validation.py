"""
Unit tests for upload_validation.py.

Covers looks_like_declared_type()'s real branches: each image format's
magic-byte signature, the extension-vs-content mismatch case the
function exists to catch, and the extensions (video) that deliberately
fall back to extension-only checking. File-size limits are enforced
separately by RequestSizeLimitMiddleware in main.py, not by this
module, so they aren't tested here.
"""

import pytest

from upload_validation import looks_like_declared_type

# Real magic-byte prefixes, not fabricated test doubles - the same bytes
# a real file of each format starts with.
JPEG_BYTES = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01"
PNG_BYTES = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
GIF87_BYTES = b"GIF87a\x01\x00\x01\x00"
GIF89_BYTES = b"GIF89a\x01\x00\x01\x00"
WEBP_BYTES = b"RIFF\x24\x00\x00\x00WEBPVP8 "


@pytest.mark.unit
class TestImageSignatureMatches:
    """A file's content matches what its extension claims."""

    def test_jpeg_with_jpg_extension(self) -> None:
        assert looks_like_declared_type(JPEG_BYTES, ".jpg") is True

    def test_jpeg_with_jpeg_extension(self) -> None:
        assert looks_like_declared_type(JPEG_BYTES, ".jpeg") is True

    def test_png(self) -> None:
        assert looks_like_declared_type(PNG_BYTES, ".png") is True

    def test_gif87a(self) -> None:
        assert looks_like_declared_type(GIF87_BYTES, ".gif") is True

    def test_gif89a(self) -> None:
        assert looks_like_declared_type(GIF89_BYTES, ".gif") is True

    def test_webp(self) -> None:
        assert looks_like_declared_type(WEBP_BYTES, ".webp") is True


@pytest.mark.unit
class TestImageSignatureMismatches:
    """A file's content does not match what its extension claims."""

    def test_png_bytes_with_jpg_extension(self) -> None:
        # The exact attack this function exists to catch: real bytes for
        # one format, a filename claiming another.
        assert looks_like_declared_type(PNG_BYTES, ".jpg") is False

    def test_jpeg_bytes_with_png_extension(self) -> None:
        assert looks_like_declared_type(JPEG_BYTES, ".png") is False

    def test_no_recognizable_signature(self) -> None:
        assert looks_like_declared_type(b"not an image at all", ".jpg") is False

    def test_empty_file(self) -> None:
        assert looks_like_declared_type(b"", ".jpg") is False

    def test_empty_file_png(self) -> None:
        assert looks_like_declared_type(b"", ".png") is False

    def test_webp_without_riff_header(self) -> None:
        assert looks_like_declared_type(b"not riff at all", ".webp") is False

    def test_webp_with_riff_header_but_wrong_format_tag(self) -> None:
        # A real RIFF container (e.g. a .wav or .avi renamed to .webp)
        # has the RIFF magic but a different 4-byte format tag at offset 8.
        riff_but_not_webp = b"RIFF\x24\x00\x00\x00WAVEfmt "
        assert looks_like_declared_type(riff_but_not_webp, ".webp") is False

    def test_webp_truncated_before_format_tag(self) -> None:
        # Shorter than the 12 bytes needed to read the format tag at all.
        assert looks_like_declared_type(b"RIFF\x24\x00\x00\x00", ".webp") is False


@pytest.mark.unit
class TestUnsignaturedExtensionsFallBackToExtensionOnly:
    """Extensions with no known signature here (video) are accepted as-is.

    See the module docstring: video container formats aren't uniformly
    signatured across variants, so this is a deliberate, documented gap,
    not an oversight.
    """

    @pytest.mark.parametrize("extension", [".mp4", ".mov", ".avi"])
    def test_video_extensions_always_pass(self, extension: str) -> None:
        assert looks_like_declared_type(b"anything at all", extension) is True

    def test_unknown_extension_passes(self) -> None:
        assert looks_like_declared_type(b"anything at all", ".xyz") is True
