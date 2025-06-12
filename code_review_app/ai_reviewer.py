from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import google.generativeai as genai

def initialize_vertex_ai():
    """
    Initializes the Vertex AI SDK with the given project ID and location.
    
    Args:
        project_id (str): The Google Cloud project ID.
        location (str): The location for Vertex AI resources.
    """
    aiplatform.init(project="agent-development-461516", location="us-central1")
    

def call_vertex_ai_model(prompt):
    """
    Calls a Vertex AI model for predictions.
    
    Args:
        model_name (str): The name of the Vertex AI model to call.
        instances (list): A list of instances to send for prediction.
    
    Returns:
        The prediction response from the model.
    """
    # model = aiplatform.Model(model_name="gemini-1.5-pro-001")
    # response = model.predict([{
    #     "content": prompt,
    #     "role": "user"
    # }])
    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"] 
    credentials, _ = default()
    scoped_credentials = credentials.with_scopes(SCOPES)

    # Configure generative AI client with scoped credentials
    genai.configure(credentials=scoped_credentials)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-001")
    response = model.generate_content(prompt)
    
    
    if response and response.text:
        return response.text
    else:
        return "❌ Failed to get AI response."
