from sentence_transformers import SentenceTransformer
import requests, os

model = SentenceTransformer(os.getenv("EMBED_MODEL","sentence-transformers/all-MiniLM-L6-v2"))
OLLAMA=os.getenv("OLLAMA_URL","http://ollama:11434")

def embed_text(text:str):
    return model.encode([text])[0].tolist()

def explain_ioc(doc:dict):
    prompt=f"""You are a cybersecurity assistant.
IOC details:
Type: {doc.get('type')}
Value: {doc.get('value')}
Context: {doc.get('context','')}

Explain in simple terms why this IOC might be dangerous."""
    try:
        r=requests.post(f"{OLLAMA}/api/generate", json={"model":"llama3:8b-instruct","prompt":prompt})
        for line in r.iter_lines():
            if line:
                j=line.decode()
                if j.startswith("{") and "response" in j:
                    return j
    except Exception as e:
        return f"[AI Error] {e}"
    return "No explanation."
