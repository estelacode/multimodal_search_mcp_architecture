import gradio as gr
import soundfile as sf
from frontend.mcp_client import MultimodalSearchMCPClient
from frontend.stt import SpeechToTextProcessor
from frontend.metrics import Metrics
from frontend.utils import image_to_base64
import logging

logger = logging.getLogger(__name__)

def process_audio_query(audio_query_file_path: str, top_k: int) -> tuple[list, str, float, float, float, float]:
    """
    Process an audio query using the SpeechToTextProcessor and
    MultimodalSearchMCPClient and retrieve the gallery items.

    Args:
        audio_query_file_path (str): The path to the audio query file.
        top_k (int): The number of top results to retrieve.

    Returns:
        tuple[list, str, float, float, float, float]: A tuple containing
        the gallery items, the text query, the transcription latency,
        the MCP tool latency, the post-processing latency, and the total latency.
    """
    logger.info("Processing audio query from file: %s", audio_query_file_path)

   
    metrics = Metrics() 
       
    start_time = metrics.start_timer()  
    try:
        text_query= SpeechToTextProcessor().transcribe(audio_query_file_path)
        metrics.trascription_latency = metrics.end_timer(start_time)
    except Exception as ge:
        logger.error("Error during speech-to-text transcription: %s", ge)
        raise gr.Error(f"{ge}")
    
    try:  
        client = MultimodalSearchMCPClient()
        with client.mcp_client:
            start_time = metrics.start_timer()  
            tool_result = client.invoke_tool(tool_name="text_to_image_search_tool", arguments={"text_query": text_query, "top_k": top_k})
            metrics.mcp_tool_latency = metrics.end_timer(start_time)

            start_time = metrics.start_timer()
            gallery_items = client.get_items_gallery(tool_result)
            metrics.post_processing_latency = metrics.end_timer(start_time)
        return gallery_items, text_query, metrics.trascription_latency, metrics.mcp_tool_latency, metrics.post_processing_latency, metrics.get_total_latency()
    except Exception as e:
        logger.error(f"Error processing audio query: {e}")
        return [], "", 0.0, 0.0, 0.0, 0.0


def process_text_query(text_query: str, top_k: int)-> tuple[list, str, float, float, float, float]:
    """
    Process a text query using the MultimodalSearchMCPClient and
    retrieve the gallery items.

    Args:
        text_query (str): The text query to process.
        top_k (int): The number of top results to retrieve.
    Returns:
        tuple[list, str, float, float, float, float]: A tuple containing
        the gallery items, the text query, the transcription latency,
        the MCP tool latency, the post-processing latency, and the total latency.
    """
    logger.info("Processing text query: %s", text_query)
    try:
        metrics = Metrics()  # Creamos la instancia de la clase Metrics

        
        client = MultimodalSearchMCPClient()
        with client.mcp_client:
            start_time = metrics.start_timer()  
            tool_result = client.invoke_tool(tool_name="text_to_image_search_tool", arguments={"text_query": text_query, "top_k": top_k})
            metrics.mcp_tool_latency = metrics.end_timer(start_time)

            start_time = metrics.start_timer()  
            gallery_items = client.get_items_gallery(tool_result)
            metrics.post_processing_latency = metrics.end_timer(start_time)

            return gallery_items,"", metrics.trascription_latency, metrics.mcp_tool_latency, metrics.post_processing_latency, metrics.get_total_latency()
    except Exception as e:
        logger.error(f"Error processing text query: {e}")
        return [], "", 0.0, 0.0, 0.0, 0.0

def process_image_query(image_query_file_path: str, top_k: int) -> tuple[list, str, float, float, float, float]:
    """
    Process an image query using the MultimodalSearchMCPClient and
    retrieve the gallery items.

    Args:
        image_query (str): The path to the image query file.
        top_k (int): The number of top results to retrieve.

    Returns:
        tuple[list, str, float, float, float, float]: A tuple containing
        the gallery items, the text query, the transcription latency,
        the MCP tool latency, the post-processing latency, and the total latency.
    """
    logger.info("Processing image query.")
    try:
        
        # Convert image to base64
        image_query = image_to_base64(image_query_file_path)

        metrics = Metrics()  
         
        client = MultimodalSearchMCPClient()
        with client.mcp_client:
            start_time = metrics.start_timer()  
            tool_result = client.invoke_tool(tool_name="image_to_image_search_tool", arguments={"image_query": image_query, "top_k": top_k})
            metrics.mcp_tool_latency = metrics.end_timer(start_time)

            start_time = metrics.start_timer()
            gallery_items = client.get_items_gallery(tool_result)
            metrics.post_processing_latency = metrics.end_timer(start_time)
            return gallery_items,"", metrics.trascription_latency, metrics.mcp_tool_latency, metrics.post_processing_latency, metrics.get_total_latency()
    except Exception as e:
        logger.error(f"Error processing image query: {e}")
        return [], "", 0.0, 0.0, 0.0, 0.0


def get_audio_duration(audio_query_file_path: str) -> float:
    """ Get the duration of the audio file.
    
    Args:
        audio_query_file_path (str): The path to the audio file.
    
    Returns:
        float: The duration of the audio file in seconds.
    
    Raises:
        gr.Error: If the audio file is invalid.

    """
    if not audio_query_file_path:
        raise gr.Error("❌ Error: Invalid audio file.")

    data, samplerate = sf.read(audio_query_file_path)
    duration = len(data) / samplerate
    return duration


def validate_audio_duration(duration: float, min_seconds: float = 1.0) -> None:
    """ 
    Validate the duration of the audio file.
    
    Args:
        duration (float): The duration of the audio file in seconds.
        min_seconds (float): The minimum duration of the audio file in seconds. Default is 1 second.

    Raises:
        gr.Error: If the duration of the audio file is less than the minimum duration.
    """
    if duration < min_seconds:
        raise gr.Error(f"❌ Error: - Audio too short ({duration:.2f}s). Please speak for at least {min_seconds:.2f}s.")
    

def validate_single_query(*queries) -> None:
    """
    Validate that the user has provided only one query (text, image, or audio).
    - If all files are empty, raise an Error.    
    - If more than one file is filled, raise an Error.

    Args:
        *queries: The queries to validate.

    Raises:
        gr.Error: If the user has not provided any query.
        gr.Error: If the user has provided more than one query.

    """
    count = sum(bool(q) for q in queries)

    if count == 0:
        raise gr.Error("❌ Error: Please provide at least one query (text, image, or audio).")

    if count > 1:
        raise gr.Error("❌ Error: Please provide only one query (text, image, or audio). Do not fill more than one field.")


def update_ui(audio_query_file_path: str, text_query: str, image_query_file_path: str, top_k: int) -> tuple[list, str, float, float, float, float]:
    """
    Processes an audio/text/image query and returns the gallery items.

    Args:
        audio_query_file_path (str): The path to the audio query file.
        text_query (str): The text query.
        image_query_file_path (str): The path to the image query file.
        top_k (int): The number of top results to retrieve.

    Returns:
        tuple[list, str, float, float, float, float]: A tuple containing
        the gallery items, the text query, the transcription latency,
        the MCP tool latency, the post-processing latency, and the total latency.
    """

    validate_single_query(audio_query_file_path, text_query, image_query_file_path)

    if audio_query_file_path:
        duration = get_audio_duration(audio_query_file_path)
        validate_audio_duration(duration, min_seconds=1.0)
        logger.info("Processing audio query...")
        return process_audio_query(audio_query_file_path, top_k)
        
    elif text_query:
        logger.info("Processing text query...")
        return process_text_query(text_query, top_k)
    else:
        logger.info("Processing image query...")
        return process_image_query(image_query_file_path, top_k)

def ui()-> gr.Blocks:

    """
    This function creates a Gradio interface that allows users to input audio, text, and image queries and get a list of results.
    Returns:
        gr.Blocks: A Gradio interface for the Multimodal Search demo.
    """
    with gr.Blocks() as demo:
                
        with gr.Row():

            # -------- Left column --------
            with gr.Column(scale=55):

                with gr.Row():
                    
                    with gr.Column():

                        gr.Markdown( 
                            """
                            <div style="text-align:center; margin-top:0px; margin-bottom:0px; border:1px solid #E4E4E7; padding-top: 25px; padding-bottom: 25px;">
                                <h2 style="margin:3px 0; font-family:Arial, sans-serif; color:#ED7400; display:inline;">
                                    Multimodal Search
                                </h2> 
                                <h3 style="margin:0px 0; font-family:Arial, sans-serif; color:#9E9E9E;"> 
                                    Text2Img · Img2Img · Audio2Img
                                </h3>
                                <p style="margin:3px 0; font-size:12px; font-family:Arial, sans-serif; color:#555;">
                                    Direct Tool Invocation | MCP Protocol | MCP Architecture
                                </p>
                            </div>
                            """
                        )


                        # -------- Text query --------
                        text_query = gr.Textbox(label="Text Query", placeholder="Add your text query...", lines=2)

                        # -------- Top K Results --------
                        top_k = gr.Slider(1, 4, value=1, step=1, label="Top K Results")
 
                        # -------- Audio query --------
                        audio_query = gr.Audio(label="Audio Query", sources=["microphone"], type="filepath")

                        #  Transcribed text
                        transcribed_text = gr.Textbox(label="Transcribed_text", placeholder="Transcribed text...", lines=2)
    

                    # -------- Image query -------- 
                    with gr.Column(scale=1):

                        # -------- Image query --------

                        image_query = gr.Image(
                            label="Image Query",
                            type="filepath",
                            height="auto",
                            show_label=True, 
                            
                        )

                        
                        # -------- Button Search --------
                        btn_search = gr.Button("Search", variant="primary")
                        # -------- Button Clear --------
                        btn_clear = gr.Button(value="Clear", variant="secondary")
            
            
            # -------- Right column --------
            with gr.Column(scale=45):
            # --------  Gallery ----------  

                gallery = gr.Gallery(
                    label="Results",
                    columns=2,
                    height="500px",
                    show_label=True,
                    allow_preview=True,
                    object_fit="scale-down",
                    
                )

                
                    
            with gr.Row():
                
                with gr.Column(scale=1):

                    gr.Markdown(
                        """
                        <div style="text-align:center; margin-top:0px; margin-bottom:0px; border:1px solid #E4E4E7; padding-top:25px; padding-bottom:25px;">
                            <h2 style="margin:0; font-family:Arial, sans-serif; color:#ED7400;">Latency</h2>
                            <h3 style="margin:0; font-family:Arial, sans-serif; color:#9E9E9E;">Metrics</h3>
                        </div>
                        """
                    )


                    # -------- Metrics Latency ----------

                    transcribe_latency = gr.Number(value=0.0,label="Transcribe Latency (s)",precision=3)
                    result_invoke_tool_latency = gr.Number(value=0.0,label= "Invoke Tool Latency (s)", precision=3)
                    postprocess_latency = gr.Number(value=0.0,label="Postprocess Latency (s)", precision=3)
                    total_latency = gr.Number(value=0.0,label="Total Latency (s)", precision=3)
        

           
            
        btn_search.click(
            fn=update_ui,
            inputs=[audio_query,text_query,image_query, top_k],
            outputs=[gallery, transcribed_text, transcribe_latency, result_invoke_tool_latency, postprocess_latency, total_latency]
            
        )

        btn_clear.click(

            fn=lambda:(None,"", None, 1, [], "", 0.0, 0.0, 0.0, 0.0),
            outputs=[audio_query,text_query,image_query, top_k, gallery, transcribed_text, transcribe_latency, result_invoke_tool_latency, postprocess_latency, total_latency]
            
        )  
           
    return demo
    
    
                