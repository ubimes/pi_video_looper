# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import glob

from .usb_drive_mounter import USBDriveMounter


class USBDriveReader:

    def __init__(self, config):
        """Create an instance of a file reader that uses the USB drive mounter
        service to keep track of attached USB drives and automatically mount
        them for reading videos.
        """
        self._load_config(config)
        self._mounter = USBDriveMounter(root=self._mount_path,
                                        readonly=self._readonly)
        self._mounter.start_monitor()
        self._previous_usb_count = 0


    def _load_config(self, config):
        self._mount_path = config.get('usb_drive', 'mount_path')
        self._readonly = config.getboolean('usb_drive', 'readonly')

    def search_paths(self):
        """Return a list of paths to search for files. Returns USB paths with priority:
        Secondary USB first (if present), then primary USB.
        """
        self._mounter.mount_all()
        return self._mounter.get_priority_paths()

    def is_changed(self):
        """Return true if the file search paths have changed, like when a new
        USB drive is inserted or removed.
        """
        return self._mounter.poll_changes()

    def get_usb_count(self):
        """Get current number of connected USB drives."""
        paths = self._mounter.get_priority_paths()
        return len(paths)

    def has_usb_count_changed(self):
        """Check if USB device count has changed since last check.
        
        Returns:
            bool: True if USB count increased or decreased
        """
        current_count = self.get_usb_count()
        changed = current_count != self._previous_usb_count
        if changed:
            self._previous_usb_count = current_count
        return changed

    def idle_message(self):
        """Return a message to display when idle and no files are found."""
        return 'Insert USB drive with compatible movies.'


def create_file_reader(config, screen):
    """Create new file reader based on mounting USB drives."""
    return USBDriveReader(config)
