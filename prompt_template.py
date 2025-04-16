from openai import OpenAI
from .pdf2list import pdf2list


  # class NumberOrNone(BaseModel):
  #   page: Optional[int]

def prompt_template(client, model, role, prompt, seed = None, image = None, response_format = None):
  """
  A template for calling the ChatGPT API that can be called directly.

  Parameters
  ----------
  client: openai.OpenAI
    Client invoked from the openai python package.
  model: str
    OpenAI model to use, see also <https://platform.openai.com/docs/models>.
  role: str
    Text string to use as system role. To be used as persona and to provide background information, e.g., "You are graduate student working as a research assistant..."
  seed: int
    Number to use for seed to control randomness and make API call (somewhat) reproducible.
  image: str
    base64 encoded image for vision model to inspect.
  response_format:
    json schema or native SDK structured output, see also <https://openai.com/index/introducing-structured-outputs-in-the-api/>.
  """
  system_role = {"role": "system", "content": role}
  
  # Get image json set up.
  if image is not None:
    image_json = {
      "type": "image_url", 
      "imague_url": {
        "url": f"data:image/jpeg;base64,{image}"
      }
    }
  else:
    image_json = None

  # Combine image with text prompt.
  prompt_json = {
    "role": "user", 
    "content": [
      {
        "type": "text", 
        "text": prompt
      },
      {
        image_json
      }
    ]
  }

  messages = [
    system_role, 
    prompt_json
  ]
  respons = client.beta.chat.completions.parse(
    model = model, 
    messages = messages,
    seed = seed,
    response_format = json_schema # This line should not be here if no response_format.
  )
