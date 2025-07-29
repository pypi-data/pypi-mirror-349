"""A utility to automatically quicksave in Starfield on a specified interval."""

from __future__ import annotations

import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

from polykit.core import platform_check
from polykit.files import PolyFile
from polykit.formatters import TZ
from polykit.log import PolyLog
from pynput.keyboard import Key, KeyCode, Listener

try:
    from pynput.keyboard import Controller, Key
except ImportError:
    if platform_check("Windows"):
        print("pynput is not installed. Please install it using 'pip install pynput'.")
    sys.exit(1)

from starfieldsaver.config_loader import ConfigLoader, get_config_file
from starfieldsaver.process_monitor import ProcessMonitor
from starfieldsaver.save_cleaner import SaveCleaner
from starfieldsaver.sound_player import SoundPlayer
from starfieldsaver.types import SaveType

if TYPE_CHECKING:
    from logging import Logger

    from starfieldsaver.config_loader import QuicksaveConfig


class StarfieldQuicksaver:
    """Quicksaver for Starfield."""

    def __init__(self):
        self.config: QuicksaveConfig = ConfigLoader.load()
        self.logger: Logger = PolyLog.get_logger(
            "quicksave", level="debug" if self.config.enable_debug else "info"
        )

        self.logger.info("Using config file: %s", get_config_file().absolute())

        self.keyboard = Controller()
        self.sound = SoundPlayer(self.logger)
        self.save_cleaner: SaveCleaner = SaveCleaner(self.config, self.logger)

        # Validate save directory
        save_dir = Path(self.config.save_dir)
        if not save_dir.exists():
            self.logger.error("Save directory does not exist: %s", save_dir)
            self.logger.warning("Please update the configuration with a valid save directory.")
            sys.exit(1)

        self.last_save_time: datetime | None = None
        self.last_copied_save_name: str | None = None
        self.is_scheduled_save: bool = False

        self.monitor = ProcessMonitor(self)
        self._log_current_config()

        # Set up keyboard listener for quit functionality
        self.keyboard_listener = Listener(on_press=self._on_key_press)
        self.keyboard_listener.start()
        self.logger.info("Press 'Q' to quit the application.")

    def run(self) -> None:
        """Run the quicksave utility."""
        self.logger.info("Started quicksave utility for %s.", self.config.game_exe)

        # Perform initial save cleanup (if enabled)
        self.save_cleaner.cleanup_old_saves()

        try:
            self._main_loop()
        except KeyboardInterrupt:
            self.logger.info("Exiting quicksave utility.")
            sys.exit(0)
        except Exception as e:
            self.logger.error("An error occurred: %s", str(e))
            self.sound.play_error()
        finally:
            self.monitor.config_observer.stop()
            self.monitor.config_observer.join()
            self.monitor.save_observer.stop()
            self.monitor.save_observer.join()
            self._cleanup_and_exit()

    def _main_loop(self) -> None:
        while True:
            try:
                time.sleep(self.config.check_interval)
                self.monitor.check_logging_status()

                if not self.monitor.is_game_running():
                    continue

                if not self.monitor.is_game_in_foreground():
                    continue

                if self.config.enable_quicksave:
                    self.save_on_interval()

                self.save_cleaner.cleanup_saves_if_scheduled()

            except Exception as e:
                self.logger.error("An error occurred during the main loop: %s", str(e))
                self.sound.play_error()
                time.sleep(2)  # Prevent rapid error loop

    def save_on_interval(self) -> None:
        """Create a new quicksave by sending F5 to the game."""
        current_time = datetime.now(tz=TZ)
        if self.last_save_time is None or (current_time - self.last_save_time) >= timedelta(
            seconds=self.config.quicksave_every
        ):
            self.is_scheduled_save = True
            self.keyboard.press(Key.f5)
            time.sleep(0.2)
            self.keyboard.release(Key.f5)
            self.logger.info("Quicksaved on schedule.")
            self.last_save_time = current_time

    @staticmethod
    def identify_save_type(save_path: str) -> SaveType:
        """Identify the type of save based on the file name."""
        if "Quicksave0" in save_path:
            return SaveType.QUICKSAVE
        return SaveType.AUTOSAVE if "Autosave" in save_path else SaveType.MANUAL

    def new_game_save_detected(self, save_path: str) -> None:
        """Handle a manual quicksave event or an autosave event."""
        self.logger.debug("New save detected: %s", Path(save_path).name)
        save_type = self.identify_save_type(save_path)

        if save_type == SaveType.MANUAL:
            self.logger.debug("Skipping manual save: %s", Path(save_path).name)
            return

        # If this was a scheduled interval save, treat it as automatic
        if save_type == SaveType.QUICKSAVE and self.is_scheduled_save:
            self.logger.info(
                "Copying new scheduled quicksave to regular save: %s", Path(save_path).name
            )
            self.copy_save_to_new_file(save_path, auto=True, scheduled=True)
            self.is_scheduled_save = False
            return

        save_time = datetime.fromtimestamp(Path(save_path).stat().st_mtime, tz=TZ)

        if self.last_save_time is None or save_time > self.last_save_time:
            if save_type == SaveType.QUICKSAVE:
                self.copy_save_to_new_file(save_path, auto=False)
            elif save_type == SaveType.AUTOSAVE:
                self.logger.debug("New autosave: %s", Path(save_path).name)
                self.copy_save_to_new_file(save_path, auto=True)

    def copy_save_to_new_file(self, source: str, auto: bool, scheduled: bool = False) -> bool:
        """Copy the save to a new file with a name matching the game's format."""
        if source == self.last_copied_save_name:
            self.logger.debug("Skipping save already copied: %s", Path(source).name)
            return False

        save_files = PolyFile.list(Path(self.config.save_dir), extensions=["sfs"])
        source_filename = Path(source).name

        highest_save_id, next_save_id = self._get_next_save_id([str(f) for f in save_files])
        self.logger.debug(
            "Found %s saves. Highest ID is %s. Next ID is %s.",
            len(save_files),
            highest_save_id,
            next_save_id,
        )

        new_filename = re.sub(r"^(Quicksave0|Autosave\d+)", f"Save{next_save_id}", source_filename)
        destination = Path(self.config.save_dir) / new_filename

        try:
            return self._perform_file_copy(source, str(destination), scheduled, auto)
        except Exception as e:
            self.logger.error("Failed to copy file: %s", str(e))
            self.sound.play_error()
            return False

    def _perform_file_copy(
        self, source: str, destination: str, scheduled: bool, auto: bool
    ) -> bool:
        PolyFile.copy(Path(source), Path(destination))
        self.logger.info(
            "Copied most recent %s%s to %s.",
            "scheduled " if scheduled else "",
            self.identify_save_type(source),
            Path(destination).name,
        )
        if auto:
            self.sound.play_success()
        else:
            self.sound.play_notification()

        save_time = datetime.fromtimestamp(Path(source).stat().st_mtime, tz=TZ)
        self.last_copied_save_name = source
        self.last_save_time = save_time
        self.logger.debug(
            "Reset interval timer due to %s save: %s",
            "automatic" if auto else "manual",
            Path(source).name,
        )
        return True

    def _get_next_save_id(self, save_files: list[str]) -> tuple[int, int]:
        """Get the next available save ID. Returns highest existing and next IDs."""
        save_ids = []

        for f in save_files:
            if match := re.match(r"Save(\d+)_[A-F0-9]{8}", Path(f).name):
                try:
                    save_id = int(match[1])
                    save_ids.append(save_id)
                except ValueError:
                    self.logger.error("Failed to parse save ID for file: %s", f)

        if not save_ids:
            self.logger.warning("No valid save IDs found, starting from 1.")
            return 0, 1

        highest_save_id = max(save_ids)
        next_save_id = highest_save_id + 1

        # Protect against unexpected digit count increases
        expected_digits = len(str(highest_save_id))
        if (
            len(str(next_save_id)) > expected_digits
            and str(highest_save_id) != "9" * expected_digits
        ):
            self.logger.warning("Unexpected digit increase. Adjusting save ID.")
            next_save_id = int("1" + "0" * (expected_digits - 1))

        return highest_save_id, next_save_id

    def _on_key_press(self, key: Key | KeyCode | None) -> None:
        """Handle keyboard input to allow quitting with 'Q'."""
        try:
            if key == KeyCode.from_char("q") or key == KeyCode.from_char("Q"):
                self.logger.info("Quit key pressed. Exiting application...")
                self._cleanup_and_exit()
        except AttributeError:
            pass  # Special keys like function keys don't have a char attribute

    def _cleanup_and_exit(self):
        """Clean up resources and exit the application."""
        try:
            # Stop all observers and listeners
            if hasattr(self, "monitor"):
                if hasattr(self.monitor, "config_observer"):
                    self.monitor.config_observer.stop()
                    self.monitor.config_observer.join(timeout=1.0)
                if hasattr(self.monitor, "save_observer"):
                    self.monitor.save_observer.stop()
                    self.monitor.save_observer.join(timeout=1.0)

            # Stop the keyboard listener
            if hasattr(self, "keyboard_listener"):
                self.keyboard_listener.stop()
        except Exception as e:
            self.logger.error("Error during cleanup: %s", str(e))

        import os

        os._exit(0)

    def reload_config(self) -> None:
        """Reload the configuration from the JSON file."""
        self.config = ConfigLoader.reload(self.config, self.logger)
        self._log_current_config()
        self.save_cleaner.cleanup_old_saves()

    def _log_current_config(self) -> None:
        self.logger.debug(
            "Loaded config: check every %ss, %s%s, sounds %s",
            round(self.config.check_interval),
            f"save every {round(self.config.quicksave_every)}s"
            if self.config.enable_quicksave
            else "save disabled",
            "" if self.config.copy_to_regular_save else ", copy disabled",
            "enabled" if self.config.enable_success_sounds else "disabled",
        )
