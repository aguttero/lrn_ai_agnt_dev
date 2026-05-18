# Udemy Course:
https://www.udemy.com/course/ai-developer-bootcamp/

# Tutorial Notes:
* modulo langchain permite hablar con LLMs

# LLM.invoke y agent.invoke
* see code `a_basic_LLM_call.py`
* see code `a_basic_agnt_call.py`

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

### Connection
* Direct
* Type: URI
* Copy the connection string -> ".env" file SUPABASE_DB_URI = postgresql://postgres:[YOUR-PASSWORD]@db.....

