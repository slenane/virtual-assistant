import ollama
import subprocess

# Check if Ollama is running; if not, start it
def ensure_ollama_running():
    try:
        subprocess.run(["ollama", "list"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.Popen(["ollama", "serve"])

def ask_llm_local(prompt, history=[]):
    response = ollama.chat(
        model='llama3',
        messages=history + [{'role': "user", "content": prompt}]
    )
    answer = response['message']['content']
    return answer, history + [{"role": "assistant", "content": answer}]