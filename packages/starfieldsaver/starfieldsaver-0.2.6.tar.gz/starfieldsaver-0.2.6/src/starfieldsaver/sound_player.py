from __future__ import annotations

import sys
import time
from typing import TYPE_CHECKING

if sys.platform == "win32":
    import winsound

if TYPE_CHECKING:
    import logging

try:
    import numpy as np
    import pygame

    pygame_available = True
except ImportError:
    pygame_available = False


class SoundPlayer:
    """Class for handling playback of notification sounds."""

    def __init__(self, logger: logging.Logger, enable_success_sounds: bool = True) -> None:
        self.logger = logger
        self.enable_success_sounds = enable_success_sounds
        self.setup_sound_system()

    def __del__(self):
        """Cleanup pygame resources if used."""
        if pygame_available:
            pygame.mixer.quit()

    def setup_sound_system(self) -> None:
        """Set up the sound system based on available libraries."""
        if pygame_available:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            self.play_beep = self.pygame_beep
            self.logger.debug("Using pygame for sound playback.")
        else:
            self.play_beep = self.winsound_beep_wrapper
            self.logger.debug("Pygame not available. Using winsound for sound playback.")

    def winsound_beep_wrapper(
        self,
        freq: int,
        duration: float,
        pause: float = 0.0,
        vol: float = 0.5,  # noqa: ARG002 (not used by winsound)
    ) -> None:
        """Wrapper for winsound_beep that matches the play_beep signature."""
        self.winsound_beep(freq, duration)
        if pause > 0:
            time.sleep(pause)

    def play_success(self) -> None:
        """Play a success sound to indicate a save action."""
        if not self.enable_success_sounds:
            return

        self.logger.debug(
            "Playing success sound%s.", " (muted)" if not self.enable_success_sounds else ""
        )
        self.play_beep(440, 0.05, pause=0, vol=0.1)

    def play_notification(self) -> None:
        """Play an info sound to update the user."""
        if not self.enable_success_sounds:
            return

        self.logger.debug(
            "Playing info sound%s.", " (muted)" if not self.enable_success_sounds else ""
        )
        self.play_beep(400, 0.1, pause=0, vol=0.1)
        self.play_beep(800, 0.1, pause=0, vol=0.1)

    def play_error(self) -> None:
        """Play an error sound to alert the user."""
        self.logger.debug(
            "Playing error sound%s.", " (muted)" if not self.enable_success_sounds else ""
        )
        for _ in range(2):
            self.play_beep(500, 0.2, pause=0.1, vol=0.5)
            self.play_beep(300, 0.3, pause=0.2, vol=0.5)

    def play_beep(self, freq: int, duration: float, pause: float = 0.0, vol: float = 0.5) -> None:
        """Play a beep with a specific frequency, duration, and pause."""
        if pygame_available:
            self.pygame_beep(freq, duration, pause, vol)
        else:
            self.winsound_beep(freq, duration)
            if pause > 0:
                time.sleep(pause)

    def pygame_beep(self, freq: int, duration: float, pause: float = 0.0, vol: float = 0.5) -> None:
        """Play a beep using pygame."""
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, num_samples, False)
        tone = np.sin(freq * t * 2 * np.pi)
        stereo_tone = np.column_stack((tone, tone))
        stereo_tone = (stereo_tone * vol * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(stereo_tone)
        sound.play()
        pygame.time.wait(int(duration * 1000))
        pygame.time.wait(int(pause * 1000))

    @staticmethod
    def winsound_beep(freq: int, duration: float) -> None:
        """Play a beep using winsound."""
        if sys.platform != "win32":
            return
        winsound.Beep(freq, int(duration * 1000))
