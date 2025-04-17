from openai import OpenAI
from .pdf2list import pdf2list


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
  
  # Set up text prompt.
  prompt_json = {
    "role": "user", 
    "content": [
      {
        "type": "text", 
        "text": prompt
      }
    ]
  }

  # Add image json
  if image is not None:
    image_json = {
      "type": "image_url", 
      "image_url": {
        "url": f"data:image/jpeg;base64,{image}"
      }
    }
    prompt_json['content'].append(image_json)

  messages = [
    system_role, 
    prompt_json
  ]

  if response_format is not None:
    response = client.beta.chat.completions.parse(
      model = model, 
      messages = messages,
      seed = seed,
      response_format = "json_schema", 
      tools = [response_format]
    )
  else:
    response = client.beta.chat.completions.parse(
      model = model, 
      messages = messages,
      seed = seed
    )
  return response
