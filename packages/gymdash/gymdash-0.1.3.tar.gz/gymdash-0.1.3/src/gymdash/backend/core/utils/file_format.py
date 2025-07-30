from typing import Dict, Iterable, Set, List, Union
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path

@dataclass
class FileFormat:
    """Class describing a file format with extension and MIME type."""
    extension:str = None
    mimetype:str = None

    @property
    def mime(self):
        return self.mimetype
    @property
    def ext(self):
        return self.extension
    @property
    def has_mimetype(self):
        return self.mimetype is not None
    @property
    def has_extension(self):
        return self.extension is not None

@dataclass
class SignatureBytes:
    data: bytes
    offset: int
    any_byte_idxs: Set[int] = field(default_factory=set)

    @property
    def length(self):
        """Total length of the signature including 'any'-bytes."""
        return len(self.data) + len(self.any_byte_idxs)
        
    def compare(self, other:bytes):
        """
        Compare an incoming byte sequence to see if it
        matches this signature. Compares byte-by-byte
        skipping any "any"-match indices, such as those
        in WAV: "52 49 46 46 ?? ?? ?? ?? 57 41 56 45".

        Args:
            other: Query bytes for guessing.
        Returns:
            match: True if query matches signature.
                False otherwise.
        """
        cut = other[self.offset:self.offset+self.length]
        comp_offset = 0
        for i in range(len(self.data)):
            while comp_offset + i in self.any_byte_idxs:
                comp_offset += 1
            if (self.data[i] != cut[comp_offset + i]):
                return False
        return True

    def __str__(self) -> str:
        """Hex string representation of signature."""
        any_byte = "?? "
        final = any_byte*self.offset
        comp_offset = 0
        # Loop all bytes, replacing "any" bytes
        # with "?? " substring
        for i in range(self.length):
            if i in self.any_byte_idxs:
                final += any_byte
                comp_offset += 1
            else:
                final += self.data[i - comp_offset].to_bytes(1, "big").hex() + " "
        
        return final.strip()

class Signature:
    """
    Representation of a file type signature, including the
    signature bytes and the file type extension and MIME type.
    """
    def __init__(self, sig_bytes: SignatureBytes, extension="<no_extension>", mime="<no_mime>") -> None:
        self.signature = sig_bytes
        self.format = FileFormat(extension, mime)

    @property
    def data(self):
        """Signature bytes."""
        return self.signature.data
    @property
    def length(self):
        """Signature length (including 'any'-bytes)."""
        return self.signature.length
    @property
    def offset(self):
        """Signature offset."""
        return self.signature.offset
    @property
    def extension(self):
        """Signature extension."""
        return self.format.extension
    @property
    def mimetype(self):
        """Signature MIME type"""
        return self.format.mimetype
    
    def compare(self, other:bytes):
        """
        Compare an incoming byte sequence to see if it
        matches this signature. Compares byte-by-byte
        skipping any "any"-match indices, such as those
        in WAV: "52 49 46 46 ?? ?? ?? ?? 57 41 56 45".

        Args:
            other: Query bytes for guessing.
        Returns:
            match: True if query matches signature.
                False otherwise.
        """
        return self.signature.compare(other)
    
    def __str__(self) -> str:
        """Signature string, including extension and MIME type."""
        return f"Signature(ext={self.extension}, mime={self.mimetype}, signature={self.signature.__str__()})"
    
class SignatureMap:
    """
    Special signature map that does some easy preprocessing
    that separates each signature based on their first bytes.
    This helps increase speed by pruning a large subset of
    signatures that do not start with the query's first byte.
    Also separated by offset.
    """
    def __init__(self, signatures: Iterable[Signature]) -> None:
        # Separate the signatures based first on their offset values
        # Then separate them based on their first byte values.
        self.unique_offsets: List[int] = sorted(list(set((sig.offset for sig in signatures))))
        self.signatures: Dict[int, Dict[bytes, List[Signature]]] = {
            offset: defaultdict(list) for offset in self.unique_offsets
        }
        # Fill the signature map
        for sig in signatures:
            self.signatures[sig.offset][sig.data[0].to_bytes(1, "big")].append(sig)

    def guess_format(self, other: bytes) -> FileFormat:
        """
        Guesses the file format of given bytes using the available
        file signatures.

        Args:
            other: Query bytes for guessing.
        Returns:
            format: FileFormat describing the file type.
        """
        other_len = len(other)
        if other_len < 1: return None
        
        for offset in self.unique_offsets:
            # Ignore checking signatures where the offset 
            # is out of bounds of the input comparison data
            if offset >= other_len:
                continue
            first_byte = other[offset].to_bytes(1, "big")
            if first_byte not in self.signatures[offset]:
                continue
            for signature in self.signatures[offset][first_byte]:
                if (signature.compare(other)):
                    return signature.format

        return None
    

# https://en.wikipedia.org/wiki/List_of_file_signatures
# gif (GIF87a):     (offset 0), 47 49 46 38 37 61
# gif (GIF89a):     (offset 0), 47 49 46 38 39 61
# png:              (offset 0), 89 50 4E 47 0D 0A 1A 0A
# wav:              (offset 0), 52 49 46 46 ?? ?? ?? ?? 57 41 56 45
# mp4 (ftypMSNV):   (offset 4), 66 74 79 70 4D 53 4E 56
# mp4 (ftypisom):   (offset 4), 66 74 79 70 69 73 6F 6D
SIG_GIF1    = Signature(SignatureBytes(b'\x47\x49\x46\x38\x37\x61', 0), "gif", "image/gif")
SIG_GIF2    = Signature(SignatureBytes(b'\x47\x49\x46\x38\x39\x61', 0), "gif", "image/gif")
SIG_PNG     = Signature(SignatureBytes(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', 0), "png", "image/png")
SIG_WAV     = Signature(SignatureBytes(b'\x52\x49\x46\x46\x57\x41\x56\x45', 0, set((4, 5, 6, 7))), "wav", "audio/wav")
SIG_MP41    = Signature(SignatureBytes(b'\x66\x74\x79\x70\x4D\x53\x4E\x56', 4), "mp4", "video/mp4")
SIG_MP42    = Signature(SignatureBytes(b'\x66\x74\x79\x70\x69\x73\x6F\x6D', 4), "mp4", "video/mp4")

signatures = [
    SIG_GIF1,
    SIG_GIF2,
    SIG_PNG,
    SIG_WAV,
    SIG_MP41,
    SIG_MP42
]
signature_map = SignatureMap(signatures)

def format_from_file(file_path: Union[str, Path]) -> Union[FileFormat, None]:
    """
    Guesses the file format of given file using the available
    file signatures from the SignatureMap.

    Args:
        file_path: Query file path for guessing.
    Returns:
        format: FileFormat describing the file type.
    """
    chunk_size = 256
    try:
        with open(file_path, "rb") as f:
            data = f.read(chunk_size)
            return format_from_bytes(data)
    except:
        return None
def format_from_bytes(file_bytes: bytes) -> Union[FileFormat, None]:
    """
    Guesses the file format of given bytes using the available
    file signatures from the SignatureMap.

    Args:
        file_bytes: Query bytes for guessing.
    Returns:
        format: FileFormat describing the file type.
    """
    if not isinstance(file_bytes, bytes):
        return None
    return signature_map.guess_format(file_bytes)
def extension_from_bytes(file_bytes: bytes) -> Union[str, None]:
    """
    Guesses the file extension of given bytes using the available
    file signatures from the SignatureMap.

    Args:
        file_bytes: Query bytes for guessing.
    Returns:
        extension: File extension describing the file type.
    """
    fformat = format_from_bytes(file_bytes)
    if fformat is None:
        return None
    return fformat.ext
def mimetype_from_bytes(file_bytes: bytes) -> Union[str, None]:
    """
    Guesses the MIME type of given bytes using the available
    file signatures from the SignatureMap.

    Args:
        file_bytes: Query bytes for guessing.
    Returns:
        extension: MIME type describing the file type.
    """
    fformat = format_from_bytes(file_bytes)
    if fformat is None:
        return None
    return fformat.mime