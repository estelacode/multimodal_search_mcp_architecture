import time
import logging

logger = logging.getLogger(__name__)

class Metrics:
    
    def __init__(self):
        self.trascription_latency = 0.0
        self.mcp_tool_latency = 0.0
        self.post_processing_latency = 0.0
    
    
    def get_total_latency(self) -> float:
        """
        Returns the total latency of the system in seconds, rounded to 3 decimal places.

        This is the sum of the transcription latency, the MCP tool latency, and the post-processing latency.

        Returns:
            float: The total latency in seconds, rounded to 3 decimal places.
        """
        total_latency = round(self.trascription_latency + self.mcp_tool_latency + self.post_processing_latency, 3)
        logger.info(f"Total Latency: {total_latency} seconds")
        return total_latency

    def start_timer(self)-> float:
        """
        Starts a timer by returning the current time in seconds.

        Returns:
            float: The current time in seconds.
        """
        return time.time()

    def end_timer(self,start_time: float) -> float:
        """
        Ends a timer by subtracting the start time from the current time and rounding to 3 decimal places.

        Args:
            start_time (float): The start time of the timer in seconds.

        Returns:
            float: The elapsed time in seconds, rounded to 3 decimal places.
        """
        return round(time.time() - start_time, 3)    