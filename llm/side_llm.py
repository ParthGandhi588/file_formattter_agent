from RAW.RAW import GroqLLM, OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()

side_llm = GroqLLM(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.3-70b-versatile", temperature=0.3) 
# side_llm = OllamaLLM(host="http://192.168.1.19:11434", model="llama3.1:70b", num_ctx=32768)
# side_llm = OllamaLLM(host="http://192.168.1.19:11434", model="gemma3:27b", num_ctx=32768, temperature=0.5)