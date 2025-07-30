import cv2
import numpy as np
import os
from typing import Optional
from .transitions import Transition

class VideoTransitionProcessor:
    """
    Video transition processor for stitching two videos and applying transition effects.
    """
    def __init__(self, transition: Transition):
        """
        Initializes the video transition processor.
        
        Args:
            transition: The transition effect to apply.
        """
        self.transition = transition
    
    def process_videos(self, video1_path: str, video2_path: str, output_path: str, 
                       transition_start_frame: Optional[int] = None):
        """
        Processes two videos, applies transition effects, and saves the result.
        
        Args:
            video1_path: Path to the first video.
            video2_path: Path to the second video.
            output_path: Path to the output video.
            transition_start_frame: The frame number to start applying the transition effect. If None, the transition is applied at the end of the first video.
        """
        # Open video files
        cap1 = cv2.VideoCapture(video1_path)
        cap2 = cv2.VideoCapture(video2_path)
        
        # Get video properties
        width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap1.get(cv2.CAP_PROP_FPS)
        total_frames1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Determine the starting frame of the transition
        if transition_start_frame is None:
            transition_start_frame = total_frames1 - self.transition.duration_frames
        
        # Create video writer
        # Use a more common codec to ensure compatibility
        try:
            # Try to use H.264 encoder
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Check if the video writer was initialized successfully
            if not out.isOpened():
                # If H.264 is not available, try using MPEG-4
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
            # Check again
            if not out.isOpened():
                # Finally, try using the MJPG encoder
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                out = cv2.VideoWriter(output_path + ".avi", fourcc, fps, (width, height))
                print(f"Warning: Using MJPG encoder, output file changed to {output_path}.avi")
                
            if not out.isOpened():
                raise Exception("Failed to create video writer, please check codec support.")
                
        except Exception as e:
            print(f"Error creating video writer: {str(e)}")
            raise
        
        # Process the first video until the transition starts
        frame_count = 0
        while frame_count < transition_start_frame:
            ret, frame = cap1.read()
            if not ret:
                print(f"Warning: First video ended prematurely at frame {frame_count}, total frames: {total_frames1}")
                break
            try:
                out.write(frame)
                frame_count += 1
            except Exception as e:
                print(f"Error writing frame {frame_count}: {str(e)}")
                raise
        
        # Apply transition effect
        print(f"Starting to apply transition effect, duration {self.transition.duration_frames} frames")
        for i in range(self.transition.duration_frames):
            ret1, frame1 = cap1.read()
            if not ret1:
                # If the first video has ended, use the last frame
                print(f"First video has ended, using the last frame to continue transition")
                cap1.set(cv2.CAP_PROP_POS_FRAMES, transition_start_frame - 1)
                ret1, frame1 = cap1.read()
                if not ret1:
                    print(f"Error: Cannot read the last frame of the first video")
                    break
            
            # Set the position of the second video
            cap2.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret2, frame2 = cap2.read()
            if not ret2:
                print(f"Error: Cannot read frame {i} from the second video")
                break
            
            # Ensure both frames have the same dimensions
            if frame1.shape != frame2.shape:
                print(f"Warning: Video frame dimensions do not match. First video: {frame1.shape}, Second video: {frame2.shape}")
                # Resize the second frame to match the first
                frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
            
            # Calculate transition progress
            progress = i / self.transition.duration_frames
            
            # Apply transition effect
            try:
                result_frame = self.transition.apply(frame1, frame2, progress)
                
                # Write the result frame
                out.write(result_frame)
                frame_count += 1
            except Exception as e:
                print(f"Error applying transition effect or writing frame: {str(e)}")
                raise
        
        # Process the remaining part of the second video
        print(f"Processing the remaining part of the second video")
        cap2.set(cv2.CAP_PROP_POS_FRAMES, self.transition.duration_frames)
        second_video_frame_count = 0
        while True:
            ret, frame = cap2.read()
            if not ret:
                break
            try:
                out.write(frame)
                second_video_frame_count += 1
            except Exception as e:
                print(f"Error writing frame {second_video_frame_count} of the second video: {str(e)}")
                raise
        
        # Release resources
        cap1.release()
        cap2.release()
        out.release()
        
        # Check if the output file exists and its size is greater than 0
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video successfully saved to {output_path}")
            print(f"Total processed frames: {frame_count + second_video_frame_count}, file size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        else:
            # Check if an .avi file was generated (if MJPG encoder was used)
            avi_path = output_path + ".avi"
            if os.path.exists(avi_path) and os.path.getsize(avi_path) > 0:
                print(f"Video successfully saved to {avi_path}")
                print(f"Total processed frames: {frame_count + second_video_frame_count}, file size: {os.path.getsize(avi_path) / (1024*1024):.2f} MB")
            else:
                print(f"Warning: Output file {output_path} does not exist or is empty, video processing may have failed.")
                print(f"Please check codec support and output path permissions.")