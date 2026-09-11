"""Server-side validation for uploaded files.

Extension checking alone only rejects a file based on its name, which the
client fully controls - a malicious upload can claim any extension it
wants. This adds a real check on top: reading the first few bytes of the
actual file content and comparing against the known magic-byte signature
for the image formats this app accepts, so a mislabeled or fabricated file
is rejected regardless of what its filename claims.

Deliberately not checking UploadFile.content_type as an alternative: that
field comes straight from the client's multipart Content-Type header,
which is exactly as attacker-controlled as the filename is. Checking it
would look like a real validation step without actually being one.

Video formats (mp4/mov/avi) are not magic-byte-checked here - their
container formats are more complex and less uniformly signatured across
variants, and this app doesn't do anything with uploaded video beyond
storing and serving it back unmodified. Documented as a known, accepted
gap in docs/reference/SECURITY_NOTES.md rather than left unexplained.
"""

_IMAGE_SIGNATURES: dict[str, tuple[bytes, ...]] = {
    ".jpg": (b"\xff\xd8\xff",),
    ".jpeg": (b"\xff\xd8\xff",),
    ".png": (b"\x89PNG\r\n\x1a\n",),
    ".gif": (b"GIF87a", b"GIF89a"),
}


def looks_like_declared_type(contents: bytes, extension: str) -> bool:
    """Check that a file's actual bytes match what its extension claims.

    Returns True for extensions with no known signature here (the video
    extensions) - those fall back to extension-only checking, see the
    module docstring for why.
    """
    if extension == ".webp":
        # RIFF containers store a 4-byte format tag at offset 8, after the
        # 4-byte "RIFF" magic and a 4-byte chunk size field.
        return contents[:4] == b"RIFF" and contents[8:12] == b"WEBP"

    signature = _IMAGE_SIGNATURES.get(extension)
    if signature is None:
        return True
    return contents.startswith(signature)
