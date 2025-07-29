from pixel_sizes import Size, SIZES


def test_sizes() -> None:
    assert SIZES["Full HD"].rotate() == Size(1080, 1920)
    assert SIZES["HD"].rotate() == Size(720, 1280)
    assert SIZES["480p"].rotate() == Size(480, 854)
    assert SIZES["360p"].rotate() == Size(360, 640)
    assert SIZES["240p"].rotate() == Size(240, 426)
    assert SIZES["144p"].rotate() == Size(144, 256)


def test_size_rotate() -> None:
    size = Size(1920, 1080)
    assert size.rotate().rotate() == size


def test_size_aspect_ratio() -> None:
    size = Size(1920, 1080)
    assert size.aspect_ratio() == 16 / 9
    assert size.aspect_ratio_two() == (16, 9)

    size = Size(1280, 720)
    assert size.aspect_ratio() == 16 / 9
    assert size.aspect_ratio_two() == (16, 9)
    assert SIZES["Full HD"].aspect_ratio_two() == (16, 9)
    assert SIZES["HD"].aspect_ratio_two() == (16, 9)
    assert SIZES["QCIF"].aspect_ratio_two() == (11, 9)
    assert SIZES["QVGA"].aspect_ratio_two() == (4, 3)
    assert SIZES["HVGA"].aspect_ratio_two() == (3, 2)
    assert SIZES["DCGA"].aspect_ratio_two() == (8, 5)
    assert SIZES["VGA"].aspect_ratio_two() == (4, 3)
    assert SIZES["SVGA"].aspect_ratio_two() == (4, 3)
    assert SIZES["DoubleVGA"].aspect_ratio_two() == (3, 2)
    assert SIZES["XGA"].aspect_ratio_two() == (4, 3)
    assert SIZES["WXGA"].aspect_ratio_two() == (8, 5)
    assert SIZES["FWXGA"].aspect_ratio_two() == (683, 384)
    assert SIZES["WXGA+"].aspect_ratio_two() == (8, 5)
    assert SIZES["HD+"].aspect_ratio_two() == (16, 9)
    assert SIZES["HD+"] == SIZES["WXGA++"]
    assert SIZES["WXGA++"].aspect_ratio_two() == (16, 9)


def test_size_scale() -> None:
    size = Size(1920, 1080)
    assert size.scale(2) == Size(3840, 2160)
    assert size.scale(3) == Size(5760, 3240)
    assert size.scale(4) == Size(7680, 4320)
    assert size.scale(5) == Size(9600, 5400)
    assert size.scale(6) == Size(11520, 6480)
    assert size.scale(7) == Size(13440, 7560)
    assert size.scale(8) == Size(15360, 8640)
    assert SIZES["Full HD"].scale(2) == SIZES["4K UHD"]
    assert SIZES["4K UHD"].scale(2) == SIZES["8K UHD"]
