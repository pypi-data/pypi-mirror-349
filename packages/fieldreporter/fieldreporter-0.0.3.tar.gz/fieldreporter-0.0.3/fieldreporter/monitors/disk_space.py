import shutil
from ..exceptions import ConditionFailedException

class FieldReporterDiskSpaceMonitor:
    def __init__(self, threshold, disks):
        self.threshold = threshold
        self.disks = disks

    def check(self):
        for disk in self.disks:
            usage = shutil.disk_usage(disk)
            free_gb = usage.free / (1024 ** 3)
            if free_gb >= self.threshold:
                print(" - Condition met (%s): %s GB free" % (disk, free_gb))
            else:
                raise ConditionFailedException(f"Disk {disk} has only {free_gb:.2f} GB free, below threshold of {self.threshold} GB.")