from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict

def initialize_vertex_ai():
    """
    Initializes the Vertex AI SDK with the given project ID and location.
    
    Args:
        project_id (str): The Google Cloud project ID.
        location (str): The location for Vertex AI resources.
    """
    aiplatform.init(project=project_id, location="us-central1")
    

def call_vertex_ai_model(prompt):
    """
    Calls a Vertex AI model for predictions.
    
    Args:
        model_name (str): The name of the Vertex AI model to call.
        instances (list): A list of instances to send for prediction.
    
    Returns:
        The prediction response from the model.
    """
    model = aiplatform.Model(model_name="publishers/google/models/gemini-1.5-pro-001")
    response = model.predict([{
        "content": prompt,
        "role": "user"
    }])
    
    if response and response.text:
        return response.text
    else:
        return "❌ Failed to get AI response."
