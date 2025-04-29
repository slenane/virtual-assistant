import ollama
import subprocess
import markdown

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
    answer = markdown.markdown(response['message']['content'])
    return answer, history + [{"role": "assistant", "content": answer}]