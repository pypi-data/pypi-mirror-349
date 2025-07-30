import cv2
import numpy as np
import os
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class Transition(ABC):
    """
    Abstract base class for transition effects. All transition effects should inherit from this class.
    """
    def __init__(self, duration_frames: int = 30):
        """
        Initializes the transition effect.
        
        Args:
            duration_frames: Duration of the transition in frames.
        """
        self.duration_frames = duration_frames
    
    @abstractmethod
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        """
        Applies the transition effect.
        
        Args:
            frame1: Frame from the first video.
            frame2: Frame from the second video.
            progress: Transition progress, ranging from 0 to 1.
            
        Returns:
            The frame after applying the transition effect.
        """
        pass

class BlindsTransition(Transition):
    """
    Blinds transition effect.
    """
    def __init__(self, duration_frames: int = 30, num_blinds: int = 10, direction: str = 'horizontal'):
        """
        Initializes the blinds transition effect.
        
        Args:
            duration_frames: Duration of the transition in frames.
            num_blinds: Number of blinds.
            direction: Direction of the blinds, 'horizontal' or 'vertical'.
        """
        super().__init__(duration_frames)
        self.num_blinds = num_blinds
        self.direction = direction
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        """
        Applies the blinds transition effect.
        
        Args:
            frame1: Frame from the first video.
            frame2: Frame from the second video.
            progress: Transition progress, ranging from 0 to 1.
            
        Returns:
            The frame after applying the blinds transition effect.
        """
        height, width = frame1.shape[:2]
        result = frame1.copy()
        
        if self.direction == 'horizontal':
            blind_height = height // self.num_blinds
            for i in range(self.num_blinds):
                y1 = i * blind_height
                y2 = (i + 1) * blind_height if i < self.num_blinds - 1 else height
                
                # Calculate the opening degree of the blinds
                blind_progress = min(1.0, progress * 2.0)
                
                # Determine the opening direction of the blinds based on the parity of the row number
                if i % 2 == 0:
                    # Even rows, open from left to right
                    cutoff = int(width * blind_progress)
                    result[y1:y2, :cutoff] = frame2[y1:y2, :cutoff]
                else:
                    # Odd rows, open from right to left
                    cutoff = int(width * (1 - blind_progress))
                    result[y1:y2, cutoff:] = frame2[y1:y2, cutoff:]
        else:  # vertical
            blind_width = width // self.num_blinds
            for i in range(self.num_blinds):
                x1 = i * blind_width
                x2 = (i + 1) * blind_width if i < self.num_blinds - 1 else width
                
                # Calculate the opening degree of the blinds
                blind_progress = min(1.0, progress * 2.0)
                
                # Determine the opening direction of the blinds based on the parity of the column number
                if i % 2 == 0:
                    # Even columns, open from top to bottom
                    cutoff = int(height * blind_progress)
                    result[:cutoff, x1:x2] = frame2[:cutoff, x1:x2]
                else:
                    # Odd columns, open from bottom to top
                    cutoff = int(height * (1 - blind_progress))
                    result[cutoff:, x1:x2] = frame2[cutoff:, x1:x2]
        
        return result

class FadeTransition(Transition):
    """
    Fade transition effect.
    """
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        """
        Applies the fade transition effect.
        
        Args:
            frame1: Frame from the first video.
            frame2: Frame from the second video.
            progress: Transition progress, ranging from 0 to 1.
            
        Returns:
            The frame after applying the fade transition effect.
        """
        return cv2.addWeighted(frame1, 1 - progress, frame2, progress, 0)