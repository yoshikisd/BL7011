from BL7011.detectors import MTE3
import numpy as np


def test_mte3_init():
    """
    Test the initialization of the MTE3 detector.
    """
    mte3 = MTE3()
    assert mte3.name == "MTE3"
    assert isinstance(mte3.dead_pixels, np.ndarray)
    assert mte3.dead_pixels.size > 0
    assert isinstance(mte3.dead_pixel_mask, np.ndarray)
    assert mte3.dead_pixel_mask.shape == (2048, 2048)
