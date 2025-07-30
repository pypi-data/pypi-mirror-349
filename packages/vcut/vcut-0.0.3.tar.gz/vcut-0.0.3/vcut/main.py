from mcp.server.fastmcp import FastMCP
from .transitions import FadeTransition, BlindsTransition
from .processor import VideoTransitionProcessor
import os
from mcp.types import TextContent

mcp = FastMCP("VCut")


@mcp.tool(
    name="add_transitions",
    description="""Adds transition effects to two videos and generates a new video.
    
    Args:
        video1_path: Path to the first video.
        video2_path: Path to the second video.
        output_path: Path to the output video.
        transition_type: Type of transition effect, optional 'fade' or 'blinds'.
        duration_frames: Duration of the transition in frames, default is 30.
        num_blinds: Number of blinds, only valid for blinds transition, default is 10.
        direction: Direction of blinds, optional 'horizontal' or 'vertical', only valid for blinds transition, default is 'horizontal'.
        transition_start_frame: The frame number to start applying the transition effect. If None, the transition is applied at the end of the first video.
    
    Returns:
        Path to the output video.
    """
)
def add_transitions(video1_path: str, video2_path: str, output_path: str, 
                   transition_type: str = 'fade', duration_frames: int = 30,
                   num_blinds: int = 10, direction: str = 'horizontal',
                   transition_start_frame: int = None):
    # Check if input videos exist
    if not os.path.exists(video1_path):
        return TextContent(type="text", text=f"First video file does not exist: {video1_path}")
    
    if not os.path.exists(video2_path):
        return TextContent(type="text", text=f"Second video file does not exist: {video2_path}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create transition effect object based on transition type
    if transition_type.lower() == 'fade':
        transition = FadeTransition(duration_frames=duration_frames)
    elif transition_type.lower() == 'blinds':
        transition = BlindsTransition(duration_frames=duration_frames, 
                                     num_blinds=num_blinds, 
                                     direction=direction)
    else:
        return TextContent(type="text", text=f"Unsupported transition type: {transition_type}, please use 'fade' or 'blinds'")
    
    # Create video processor and process videos
    try:
        processor = VideoTransitionProcessor(transition)
        processor.process_videos(video1_path, video2_path, output_path, transition_start_frame)
        return {"success": True, "output_path": output_path}
    except Exception as e:
        return TextContent(type="text", text=f"Error processing video: {str(e)}")



def main():
    print("Start MCP server...")
    mcp.run()


if __name__ == "__main__":
    main()