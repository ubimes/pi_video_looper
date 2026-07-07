# Copyright 2015 Adafruit Industries.
# License: GNU GPLv2, see LICENSE.txt
# Dual USB Priority Manager

class USBPriorityManager:
    """Manages USB device priority and switching for dual USB support."""

    def __init__(self):
        """Initialize USB priority manager."""
        self._previous_usb_count = 0
        self._current_usb_paths = []
        self._primary_usb = None
        self._secondary_usb = None

    def update_usb_status(self, paths):
        """
        Update USB status and detect changes.
        
        Args:
            paths: List of available USB mount paths
            
        Returns:
            dict with keys:
                - 'changed': bool, True if USB configuration changed
                - 'usb_count': int, current number of USB drives
                - 'primary': str, primary USB path
                - 'secondary': str, secondary USB path (if exists)
                - 'action': str, 'added', 'removed', or 'none'
        """
        current_count = len(paths)
        self._current_usb_paths = paths
        
        action = 'none'
        changed = False
        
        # Detect USB changes
        if current_count > self._previous_usb_count:
            action = 'added'
            changed = True
        elif current_count < self._previous_usb_count:
            action = 'removed'
            changed = True
        
        self._previous_usb_count = current_count
        
        # Set primary and secondary USB
        if len(paths) >= 2:
            # Secondary USB has priority (already sorted by get_priority_paths)
            self._secondary_usb = paths[0]  # 2nd USB (highest priority)
            self._primary_usb = paths[1]    # 1st USB
        elif len(paths) == 1:
            self._primary_usb = paths[0]
            self._secondary_usb = None
        else:
            self._primary_usb = None
            self._secondary_usb = None
        
        return {
            'changed': changed,
            'usb_count': current_count,
            'primary': self._primary_usb,
            'secondary': self._secondary_usb,
            'action': action,
            'paths': paths
        }

    def should_switch_usb(self):
        """
        Determine if playback should switch to a different USB.
        
        Returns:
            bool: True if secondary USB is available (switch to it)
        """
        return self._secondary_usb is not None

    def get_active_usb_path(self):
        """
        Get the currently active USB path.
        Secondary USB has priority when available.
        
        Returns:
            str: Active USB mount path
        """
        if self._secondary_usb is not None:
            return self._secondary_usb
        return self._primary_usb

    def get_usb_count(self):
        """Get current USB device count."""
        return self._previous_usb_count
