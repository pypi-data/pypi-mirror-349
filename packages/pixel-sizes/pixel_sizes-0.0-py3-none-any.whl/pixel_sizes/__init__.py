from dataclasses import dataclass
import math

# https://packaging-guide.openastronomy.org/en/latest/advanced/versioning.html
from ._version import __version__


@dataclass(frozen=True)
class Size:
    """A class to represent a size in pixels.
    Attributes:
        width (int): The width of the size in pixels.
        height (int): The height of the size in pixels.
    """

    width: int
    height: int

    def aspect_ratio(self) -> float:
        """Returns the aspect ratio as a float.
        Example: 1920x1080 => 16/9 => 1.7777777777777777
        """
        return self.width / self.height

    def aspect_ratio_two(self) -> tuple[int, int]:
        """Returns the aspect ratio as a tuple of integers.
        Example: 1920x1080 => (16, 9)
        """
        gcd = math.gcd(self.width, self.height)
        return self.width // gcd, self.height // gcd

    def rotate(self) -> "Size":
        """Returns a new Size object with the width and height swapped.
        Example: 1920x1080 => 1080x1920
        """
        return Size(self.height, self.width)

    def scale(self, factor: int) -> "Size":
        """Returns a new Size object with the width and height scaled by the given factor.
        Example: 1920x1080, factor=2 => 3840x2160
        """
        return Size(self.width * factor, self.height * factor)


SIZES = {
    "480p": Size(854, 480),
    "360p": Size(640, 360),
    "240p": Size(426, 240),
    "144p": Size(256, 144),
    "720p": Size(1280, 720),
    "Full HD": Size(1920, 1080),
    "HD 1080p": Size(1920, 1080),
    "1080p": Size(1920, 1080),
    "1080i": Size(1920, 1080),
    "HD": Size(1280, 720),
    "QCIF": Size(176, 144),
    "QVGA": Size(320, 240),
    "HVGA": Size(480, 320),
    "DCGA": Size(640, 400),
    "VGA": Size(640, 480),
    "SVGA": Size(800, 600),
    "WSVGA": Size(1024, 600),  # 2 versions
    "DoubleVGA": Size(960, 640),
    "XGA": Size(1024, 768),
    "HD 720p": Size(1280, 720),
    "WXGA": Size(1280, 800),
    "FWXGA": Size(1366, 768),
    "WXGA+": Size(1440, 900),
    "HD+": Size(1600, 900),
    "WXGA++": Size(1600, 900),
    "SXGA+": Size(1400, 1050),
    "WSXGA+": Size(1680, 1050),
    "UXGA": Size(1600, 1200),
    "WQHD": Size(2560, 1440),
    # https://en.wikipedia.org/wiki/2K_resolution
    "DCI 2K": Size(2048, 1080),
    "DCI 2K (flat cropped)": Size(1998, 1080),
    "DCI 2K (CinemaScope cropped)": Size(2048, 858),
    "QXGA": Size(2048, 1536),
    "WQXGA": Size(2560, 1600),
    "WUXGA": Size(1920, 1200),
    "QWXGA": Size(2048, 1152),
    "QUXGA": Size(3200, 2400),
    "QUXGA Wide": Size(3840, 2400),
    # https://en.wikipedia.org/wiki/4K_resolution
    "DCI 4K": Size(4096, 2160),
    "DCI 4K (flat cropped)": Size(3996, 2160),
    "DCI 4K (CinemaScope cropped)": Size(4096, 1716),
    "4K UHD": Size(3840, 2160),
    "4K UHDTV": Size(3840, 2160),
    "UHDTV1": Size(3840, 2160),
    "2160p": Size(3840, 2160),
    # https://en.wikipedia.org/wiki/5K_resolution
    "5K": Size(5120, 2880),
    "5K2K": Size(5120, 2160),
    # https://en.wikipedia.org/wiki/8K_resolution
    "8K UHD": Size(7680, 4320),
    "UHDTV2": Size(7680, 4320),
}

__all__ = ["Size", "SIZES", "__version__"]
