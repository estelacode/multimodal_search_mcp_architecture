from faster_whisper import WhisperModel
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)

load_dotenv()

class SpeechToTextProcessor:
    def __init__(self):
        
        """
        Initializes the SpeechToTextProcessor class with the Whisper model from Faster Whisper.
        
        """
        self.model = WhisperModel(os.getenv("WHISPER_MODEL_NAME"), device=os.getenv("WHISPER_DEVICE_TYPE"), compute_type=os.getenv("WHISPER_COMPUTE_TYPE"))
        logger.info("Whisper model from Faster Whisper loaded")


    def transcribe(self, audio_query_file_path:str) -> str:
        """
        Transcribes the audio query using faster whisper.

        Args:
            audio_query_file_path (str): The audio query file path to transcribe.

        Returns:
            str: The transcribed text.
        """
        try:
            logger.info(f"Starting transcription for audio file: {audio_query_file_path}")

            segments, _ = self.model.transcribe(audio_query_file_path, task="transcribe")
            segments = list(segments)
            # Check if any segments were returned
            if not segments:
                logger.error(f"No speech detected in the audio file: {audio_query_file_path}")
                raise Exception("❌ Error: No speech detected.")
            
            transcribed_text = segments[0].text.strip()
            # Check if the transcribed text is empty or audio with only noise/silence. If so, the model could transcribe the audio as " .", ".", "...", " ", "\n", "\t"
            if transcribed_text in [" .", ".","...", " ", "\n", "\t"]:
                logger.error(f"Invalid transcription detected for audio file {audio_query_file_path}: {transcribed_text}")
                raise Exception("❌ Error: Please provide a valid audio query. No empty audio or audio with only silence.")                
            
            logger.info(f"Successful transcription for audio file {audio_query_file_path}, text: {transcribed_text}")
            return transcribed_text

        except Exception as e:
            logger.error(f"Error during transcription for audio file {audio_query_file_path}: {e}")
            raise Exception(f"{e}")

