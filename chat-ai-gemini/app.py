# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by Google's Gemini model.
# To run it, you'll need a Google API key.
# To get one, follow the instructions at https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python
# The previous method doesnt work so we default to our own credentials and a different library
# ------------------------------------------------------------------------------------
#from app_utils import load_dotenv
# import instructor
import google.auth
import google.auth.transport.requests
from openai import OpenAI
#from openai import AsyncOpenAI
from pydantic import BaseModel

#from google.generativeai import GenerativeModel

from shiny.express import ui

# Either explicitly set the GOOGLE_API_KEY environment variable before launching the
# app, or set them in a file named `.env`. The `python-dotenv` package will load `.env`
# as environment variables which can later be read by `os.getenv()`.
#load_dotenv()
creds, _ = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)
# Pass the Vertex endpoint and authentication to the OpenAI SDK
PROJECT = 'rax-enterprisebi'
LOCATION = (
    'us-central1'  # https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations
)
base_url = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/{LOCATION}/endpoints/openapi'
# llm = instructor.from_openai(
#     OpenAI(base_url=base_url, api_key=creds.token), mode=instructor.Mode.JSON
# )
#llm = AsyncOpenAI(base_url=base_url, api_key=creds.token)
llm = OpenAI(base_url=base_url, api_key=creds.token)


class QnA(BaseModel):
    question: str
    answer: int
#llm = GenerativeModel(token = creds.token)

def process_chat_contents(contents):
    """
    Processes a list of chat content (each containing 'role' and 'parts') and returns a list of messages.
    
    Args:
    - contents (list): List of dictionaries with keys 'role' and 'parts'.
    
    Returns:
    - list: List of processed message dictionaries with 'role' and 'content'.
    """
    messages = []

    for content in contents:
        # Ensure 'parts' is not empty and take the first item
        message = {
            "role": content['role'],
            "content": content['parts'][0] if content['parts'] else ''
        }
        messages.append(message)

    return messages


# Set some Shiny page options
ui.page_opts(
    title="Hello Google Gemini Chat",
    fillable=True,
    fillable_mobile=True,
)

# Create and display empty chat
chat = ui.Chat(id="chat")
chat.ui()


# Define a callback to run when the user submits a message
@chat.on_user_submit
async def _():
    # Get messages currently in the chat
    contents = chat.messages(format="google")

    # its a tuple
    #print(contents)
    processed_messages = process_chat_contents(contents)

    # Generate a response message stream
    response = llm.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        #response_model=QnA,
        messages=processed_messages,
        stream=True
        #response_model=User,
    )

    #print(response)

    # Append the response stream into the chat
    await chat.append_message_stream(response)
