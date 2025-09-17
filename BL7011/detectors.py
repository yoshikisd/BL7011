import numpy as np


class Detector:
    """
    A class representing a detector.

    Attributes:
        name (str): The name of the detector.
    """

    def __init__(self):
        """
        Initializes the Detector instance.

        Args:
            name (str): The name of the detector.
        """
        self.dead_pixels = np.array([])  # Initialize dead pixels as an empty array
        self.pixel_shape = (2048, 2048)  # Default pixel shape
        self.dead_pixels_mask = np.array([])  # Initialize dead pixel mask as an empty array

    def update_dead_pixel_mask(self):
        """
        Updates the dead pixel mask based on the dead pixels. 0 indicates a dead pixel, 1 indicates a good pixel.
        """
        self.dead_pixel_mask = np.ones(self.pixel_shape, dtype=bool)
        for pixel in self.dead_pixels:
            x, y = pixel
            self.dead_pixel_mask[x, y] = 0


class MTE3(Detector):
    """
    A class representing a MTE3 detector.

    Inherits from the Detector class.
    """

    def __init__(self):
        """
        Initializes the MTE3 instance.

        Args:
            name (str): The name of the MTE3 detector.
        """
        super().__init__()
        self.name = "MTE3"
        self.pixel_shape = (2048, 2048)
        self.dead_pixels = np.array(
            [
                [213, 376],
                [229, 486],
                [228, 486],
                [249, 493],
                [397, 292],
                [328, 482],
                [328, 481],
                [327, 487],
                [327, 486],
                [372, 643],
                [373, 643],
                [372, 644],
                [373, 644],
                [181, 641],
                [181, 642],
                [182, 643],
                [442, 677],
                [443, 677],
                [402, 714],
                [402, 715],
                [402, 716],
                [402, 717],
                [403, 717],
                [403, 718],
                [407, 801],
                [406, 803],
                [405, 804],
                [405, 805],
                [404, 806],
                [404, 807],
                [403, 808],
                [332, 1080],
                [339, 1093],
            ]
        )
        self.dead_pixel_mask = np.zeros(
            (2048, 2048), dtype=bool
        )
        self.update_dead_pixel_mask()
