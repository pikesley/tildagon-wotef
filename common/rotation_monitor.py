from math import atan2

import imu


class RotationMonitor:
    """Monitor rotation."""

    def read(self):
        """Get rotation."""
        acc = imu.acc_read()
        weighting = min(1.0, int(abs(10 - acc[2])) / 9)
        return -(atan2(acc[1], acc[0])) * weighting
