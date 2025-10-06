This is a simple chatbot that run on ther


*_____________________After cloning this folder download reqired packages____________

python -m pip install --upgrade pip --user
pip install --user flask sentence-transformers torch groq

*_____________________Before Run Progrme________________________

$Env:GROQ_API_KEY="your_key"

*_____________________For Run Progrme____________________

python app.py

______________________________________________________________________________________________________________________________________

# SRP's Chatbot

An interactive AI-powered chatbot built using **Sentence Transformers** and **Groq LLM** for a fast Retrieval-Augmented Generation (RAG) pipeline. Users can ask questions about uploaded documents, and the chatbot retrieves the most relevant information to generate answers.

---

## 🌟 Features

- **RAG Pipeline**: Retrieve relevant document chunks using embeddings before generating answers.
- **Embeddings**: Powered by `SentenceTransformers` for semantic search.
- **LLM Integration**: Generates answers using Groq's `llama-3.3-70b-versatile`.
- **Interactive Web UI**: Modern, responsive chat interface built with Tailwind CSS.
- **Conversation History**: Keeps track of previous queries and answers.
- **Lightweight & Fast**: Uses MiniLM embeddings for efficient retrieval.

---

## 📁 Project Structure

```

project/
│
├─ data/                   # Folder containing .txt documents
├─ .venv/                  # Python virtual environment
├─ index.html              # Frontend HTML for the chatbot
├─ app.py                  # Flask backend to handle queries
├─ requirements.txt        # Python dependencies
└─ README.md

````

---

## ⚡ Requirements

- Python 3.10+
- Pip
- GPU recommended but not required
- Groq API key

Python packages:

```text
flask
sentence-transformers
torch
groq
````

---

## 🚀 Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd project
```

2. **Create a virtual environment**

```bash
python -m venv .venv
```

3. **Activate the virtual environment**

* Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

* macOS / Linux:

```bash
source .venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Set your Groq API key**

```powershell
setx GROQ_API_KEY "your_groq_api_key_here"
```

6. **Place your `.txt` documents** in the `data/` folder.

---

## 🖥️ Run the Chatbot

```bash
python app.py
```

* Open a browser and go to: `http://127.0.0.1:5000/`
* Type a query in the input box and press **Enter** or click **Ask**.
* The chatbot will retrieve relevant documents and generate an answer.

---

## 💡 How it Works

1. **Load documents** from the `data/` folder.
2. **Embed documents** using `SentenceTransformers`.
3. **User query** is embedded and compared to document embeddings.
4. **Top-K relevant documents** are sent to Groq LLM.
5. **LLM generates** a context-aware answer.
6. **Answer displayed** in an interactive chat interface.

---

## 🎨 Frontend Features

* Gradient background and modern UI with **Tailwind CSS**
* Animated chat bubbles for user and bot messages
* Smooth scroll and typing placeholders
* Responsive layout for mobile and desktop
* Footer credits

---

## ⚙️ Customization

* Change `TOP_K` in `app.py` to retrieve more or fewer document chunks.
* Switch embedding models by updating `EMBED_MODEL_NAME`.
* Update `index.html` to change UI colors, animations, or layout.

---

## 🛠️ Future Improvements

* Add **voice input/output**.
* Dark/light theme toggle.
* Persistent conversation history with **database support**.
* Support for **PDF and DOCX** files in addition to TXT.
* Loading animations and enhanced Lottie graphics.

---

## 📜 License

This project is **MIT License** — free to use, modify, and distribute.

---

## 🙏 Credits

* Built with **Python**, **Flask**, **Sentence Transformers**, **Groq LLM**, and **Tailwind CSS**
* Inspired by modern RAG pipelines for knowledge retrieval.
