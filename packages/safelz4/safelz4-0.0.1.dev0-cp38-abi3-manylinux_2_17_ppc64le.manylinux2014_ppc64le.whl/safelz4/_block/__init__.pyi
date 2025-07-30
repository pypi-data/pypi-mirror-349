def compress(input: bytes) -> bytes:
    """
    Compress the input bytes using LZ4.

    Args:
        input (`bytes`):
            fixed set of bytes to be compressed.

    Returns:
        (`bytes`): Compressed LZ4 block format.
    """
    ...

def compress_prepend_size(input: bytes) -> bytes:
    """
    Compress the input bytes using LZ4 and prepend the original size as
    a little-endian u32.

    This is compatible with `decompress_size_prepended`.

    Args:
        input (`bytes`):
            fixed set of bytes to be compressed.

    Returns:
        (`bytes`): Compressed LZ4 block data with the uncompressed size prepended.
    """
    ...

def compress_into(input: bytes, output: bytearray) -> int:
    """
    Compress the input bytes into the provided output buffer. The output buffer
    must be preallocated with a size obtained from `get_maximum_output_size`.

    Args:
        input (`bytes`):
            fixed set of bytes to be compressed.
        output (`bytearray`):
            Mutable buffer to hold combessed bytes.

    Returns:
        (`int`): Number of bytes written to the output buffer.
    """
    ...

def compress_with_dict(input: bytes, dictionary: bytes) -> bytes:
    """
    Compress the input bytes using a user-provided dictionary.

    Args:
        input (`bytes`):
            fixed set of bytes to be compressed.
        dictionary (`bytes`):
            Dictionary used for compression.

    Returns:
        (`bytes`): fixed set of bytes to be decompressed.
    """
    ...

def decompress(input: bytes, min_size: int) -> int:
    """
    Decompress the input block bytes.

    Args:
        input (`bytes`)
            fixed set of bytes to be decompressed
        min_size (`int`):
            minimum possible size of uncompressed bytes

    Returns:
        (`bytes`): decompressed repersentation of the compressed bytes.
    """
    ...

def decompress_into(input: bytes, output: bytearray) -> int:
    """
    Decompress input bytes into the provided output buffer.
    The output buffer must be preallocated with enough space
    for the uncompressed data.

    Args:
        input (`bytes`):
            Fixed set of bytes to be decompressed.
        output (`bytearray`):
            Mutable buffer to hold decompressed bytes.

    Returns:
        (`int`): Number of bytes written to the output buffer.
    """
    ...

def decompress_size_prepended(input: bytes) -> bytes:
    """
    Decompress input bytes that were compressed with the original
    size prepended. Compatible with `compress_prepend_size`.

    Args:
        input (`bytes`):
            fixed set of bytes to be decompressed

    Returns:
        (`bytes`): Decompressed data.
    """
    ...

def decompress_with_dict(input: bytes, ext_dict: bytes) -> bytes:
    """
    Decompress input bytes using a user-provided dictionary of
    bytes.

    Args:
        input (`bytes`):
            fixed set of bytes to be decompressed.
        ext_dict (`bytes`):
            Dictionary used for decompression.

    Returns:
        (`bytes`): Decompressed data.
    """
    ...

def get_maximum_output_size(input_len: int) -> int:
    """
    Obtain the maximum output size of the block

    Args:
        input_len (`int`):
            length of the bytes we need to allocate to compress
            into fixed buffer.
    Returns:
        (`int`):
            maximum possible size of the output buffer needs to be."""
    ...
