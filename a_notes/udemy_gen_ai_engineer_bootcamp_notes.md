# Udemy Course:
https://www.udemy.com/course/ai-developer-bootcamp/

# Tutorial Notes:
* modulo langchain permite hablar con LLMs
* Open AI y Google tienen su propio modulo además de los langchain

# LLM.invoke y agent.invoke
* see code `a_basic_LLM_call.py`
* see code `a_basic_agnt_call.py`

# LLM API
## Gemini
https://aistudio.google.com/api-keys

### Required PIP install
pip install google-genai
https://googleapis.github.io/python-genai/

### Code sample image upload:
see lrn_pdf_parser/src/image_parse_genai.py

### python code:
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

# Read the raw binary data
with open("procurement_bypass_form.pdf", "rb") as f:
    pdf_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents=[
        types.Part.from_bytes(
            data=pdf_bytes,
            mime_type='application/pdf',
        ),
        "Analyze this procurement exception form."
    ],
    config=types.GenerateContentConfig(
        system_instruction="...[Your System Prompt]...",
        response_mime_type="application/json",
        response_schema=ProcurementAuditSchema,
        temperature=0.0
    ),
)

print(response.text)
```

### code sample chat text generation
see lrn_ai_prod/src/inst_loc.py

```python
@app.get("/", response_class=HTMLResponse)
def instant():
    client = genai.Client(api_key=GEMINI_API_KEY)
    # messages = [{"role": "user", "content": user_message}]
    # chat = client.chats.create(model="gemini-2.5-flash")
    chat = client.chats.create(model="gemini-2.5-flash")
    response = chat.send_message(user_message)
    reply = response.text.replace("\n", "<br/>")

    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"

    # return "Live from production!"
    return html
  ```


# memory db
## modules
* import InMemorySaver permite al agente crear la 'memoria'
* modulo langraph.checkpoint.memory 
* see code `agent_memory_db.py`
* sql memory see `sec5_main_sqlite.py`

## code
* agent.invoke {"configurable":{"thread_id":"n"}} es lo que identifica el thread para la memoria
* thread_id gets associated with each user in your app to have a memory for each conversation

## Supabase - Postgre SQL
* langchain uses connection string to DBs (Disable DATA API)
* define hosting region: Choose the same as the hosting region for the app

### Connection -> Connect button in settings (Top part of screen)
* Direct
* Type: URI
* Copy the connection string -> ".env" file SUPABASE_DB_URI = postgresql://postgres:[YOUR-PASSWORD]@db.....

# Self Hostable Models
## Good por laptop
### Meta 3 Series
* Llama 3.2
* Llama 3.3 70B

### Gemini
* Gemma 3

## Good for Coding
* Qwen3 Series -> Coding
* DeepSeek Series -> reasoning
* Mistral 7B -> Balanced

## ollama python setup

* ollama api: localhost:11434
* bash: ollama serve
* library: langchain + langchain-ollama
