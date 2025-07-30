import os
from typing import Optional, Union, Any
from typing_extensions import Self

from enum import IntEnum, Enum

class BlockMode(Enum):
    """
    Block mode for frame compression.

    Attributes:
        Independent: Independent block mode.
        Linked: Linked block mode.
    """

    Independent = "Independent"
    Linked = "Linked"

class BlockSize(IntEnum):
    """
    Block size for frame compression.

    Attributes:
        Auto: Will detect optimal frame size based on the size of the first
        write call.
        Max64KB: The default block size (64KB).
        Max256KB: 256KB block size.
        Max1MB: 1MB block size.
        Max4MB: 4MB block size.
        Max8MB: 8MB block size.
    """

    Auto = 0
    Max64KB = 4
    Max256KB = 5
    Max1MB = 6
    Max4MB = 7
    Max8MB = 8

class FrameInfo:
    """
    Information about a compression frame.

    Attributes:
        content_size: If set, includes the total uncompressed size of data in
                      the frame.
        block_size: The maximum uncompressed size of each data block.
        block_mode: The block mode.
        block_checksums: If set, includes a checksum for each data block in the
        frame.
        content_checksum: If set, includes a content checksum to verify that the
          full frame contents have been decoded correctly.
        legacy_frame: If set, use the legacy frame format.
    """

    content_size: Optional[int]
    block_size: BlockSize
    block_mode: BlockMode
    block_checksums: bool
    dict_id: Optional[int]
    content_checksum: bool
    legacy_frame: bool

    def __new__(
        self,
        block_size: BlockSize,
        block_mode: BlockMode,
        block_checksums: Optional[bool] = None,
        dict_id: Optional[int] = None,
        content_checksum: Optional[bool] = None,
        content_size: Optional[int] = None,
        legacy_frame: Optional[bool] = None,
    ) -> Self: ...
    @staticmethod
    def default() -> Self:
        """
        build a default `FrameInfo` class.

        Returns:
            (`FrameInfo`): default object.
        """
        ...
    @staticmethod
    def read_header_info(input: bytes) -> Self:
        """Read header info to construct header."""
        ...
    def read_header_size(input: bytes) -> Self:
        """Read the size of the header info"""
        ...
    @property
    def block_checksums(self) -> bool: ...
    @block_checksums.setter
    def block_checksums(self, value: bool) -> None: ...
    @property
    def block_size(self) -> BlockSize: ...
    @block_size.setter
    def block_size(self, value: BlockSize) -> None: ...
    @property
    def block_mode(self) -> BlockMode: ...
    @property
    def content_size(self) -> Optional[int]: ...
    @content_size.setter
    def content_size(self, value: int) -> None: ...
    @property
    def content_sum(self) -> bool: ...
    @property
    def content_checksum(self) -> bool: ...
    @content_checksum.setter
    def content_checksum(self, value: bool) -> None: ...
    @property
    def legacy_frame(self) -> bool: ...
    @legacy_frame.setter
    def legacy_frame(self, value: bool) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class open_frame:
    """
    Context manager that allows us to decompresses a buffer of bytes using thex
    LZ4 frame format.

    Example:
    ```
    output = None
    with open_frame("datafile") as f:
        output = f.decompress()

    print(output)
    ```
    """

    def __new__(self, filename: Union[str, os.PathLike]) -> "open_frame":
        """Initialize the open_frame context manager with a filename."""
        ...
    def info(self) -> FrameInfo:
        """
        Return the frameinfo of the compression file.
        Returns:
            `FrameInfo`:
                The freeform FrameInfo.
        """
        ...
    def decompress(self) -> bytes:
        """
        Decompress the whole frame file.
        Returns:
            (`bytes`):
                The decompressed (original) representation of the bytes
                within the file.
        """
        ...
    def content_size(self) -> Optional[int]:
        """Return the content size if available in the frame header."""
        ...
    def __enter__(self) -> "open_frame":
        """Enter the context manager and return self."""
        ...
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        """Exit the context manager and clean up resources."""
        ...

def decompress(input: bytes) -> bytes:
    """
    Decompresses a buffer of bytes using thex LZ4 frame format.

    Args:
        input (`bytes`):
            A byte containing LZ4-compressed data (in frame format).
            Typically obtained from a prior call to an `compress` or read from
            a compressed file `compress_file`.

    Returns:
        (`bytes`):
            The decompressed (original) representation of the input bytes.
    """
    ...

def decompress_file(filename: Union[os.PathLike, str]) -> bytes:
    """
    Decompresses a buffer of bytes into a file using thex LZ4 frame format.

    Args:
        filename (`str` or `os.PathLike`):
            The filename we are loading from.

    Returns:
        (`bytes`):
            The decompressed (original) representation of the input bytes.
    """
    ...

def compress(input: bytes) -> bytes:
    """
    Compresses a buffer of LZ4-compressed bytes using the LZ4 frame format.

    Args:
        input (`bytes`):
            An arbitrary byte buffer to be compressed.
    Returns:
        `bytes`:
             The LZ4 frame-compressed representation of the input bytes.
    """
    ...

def compress_file(filename: Union[os.PathLike, str], input: bytes) -> None:
    """
    Compresses a buffer of bytes into a file using using the LZ4 frame format.

    Args:
        filename (`str` or `os.PathLike`):
            The filename we are saving into.
        input (`bytes`):
            un-compressed representation of the input bytes.

    Returns:
        (`None`)
    """
    ...

def compress_file_with_info(
    filename: Union[os.PathLike, str],
    input: bytes,
    info: Optional[FrameInfo] = None,
) -> None:
    """
    Compresses a buffer of bytes into a file using using the LZ4 frame format,
    with more control on Frame.

    Args:
        filename (`str`, or `os.PathLike`):
            The filename we are saving into.
        input (`bytes`):
            fixed set of bytes to be compressed.
        info (`FrameInfo, *optional*, defaults to `None``):
            The metadata for de/compressing with lz4 frame format.

    Returns:
        (`None`)
    """
    ...

def compress_with_info(
    input: bytes,
    info: Optional[FrameInfo] = None,
) -> None:
    """
    Compresses a buffer of bytes into byte buffer using using the LZ4 frame
    format, with more control on Frame.

    Args:
        input (`bytes`):
            fixed set of bytes to be compressed.
        info (`FrameInfo, *optional*, defaults to `None``):
            The metadata for de/compressing with lz4 frame format.

    Returns:
        (`bytes`):
            The LZ4 frame-compressed representation of the input bytes.
    """
    ...
