# AI Language Translator

A small full-stack translation application that lets users enter text, choose a target language, and receive an AI-generated translation. The project uses a Streamlit web interface, a FastAPI/LangServe API, LangChain, and Groq.

## What the project does

1. Shows a web form where the user selects a target language.
2. Accepts the text the user wants to translate.
3. Checks that the text is not empty.
4. Sends the text and selected language to the backend API.
5. Builds a LangChain prompt requesting translation into that language.
6. Sends the prompt to Groq's `openai/gpt-oss-20b` chat model.
7. Converts the model response into plain text.
8. Returns the translation to the web interface and displays it to the user.

## Supported target languages

- Telugu
- Hindi
- French
- Spanish
- German
- Japanese
- English

## Tech stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend | Streamlit | Interactive browser-based translation form and result display. |
| HTTP client | Requests | Sends translation requests from Streamlit to the backend. |
| Backend | FastAPI | Hosts the API server on port `8000`. |
| API routing | LangServe | Exposes the LangChain chain at `/chain`. |
| AI orchestration | LangChain | Combines the prompt, model, and output parser into one chain. |
| LLM provider | Groq / `langchain-groq` | Runs the `openai/gpt-oss-20b` model. |
| Configuration | python-dotenv | Loads `GROQ_API_KEY` from `.env`. |
| Server | Uvicorn | Runs the FastAPI application. |

## Project structure

```text
AI_Language_Translator/
├── app.py              # Streamlit frontend
├── serve.py            # FastAPI, LangServe, and LangChain backend
├── main.py             # Minimal Python entry point
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project metadata
├── .env                # Local Groq API key (create locally; do not commit)
└── README.md           # Project documentation
```

## How it works

```text
User
  │ enters text + selects language
  ▼
Streamlit UI (app.py)
  │ POST http://localhost:8000/chain/invoke
  │ { "input": { "language": "...", "text": "..." } }
  ▼
FastAPI + LangServe (serve.py)
  ▼
LangChain prompt → Groq model → string output parser
  ▼
Translation response
  ▼
Streamlit displays translated text
```

### Detailed request flow

1. The user opens the Streamlit application and chooses a language from the dropdown.
2. The user enters source text and clicks **Translate**.
3. `app.py` trims the input. If it is empty, the app shows a warning and does not call the backend.
4. For valid input, the frontend sends this JSON payload to `http://localhost:8000/chain/invoke`:

   ```json
   {
     "input": {
       "language": "French",
       "text": "I love programming."
     }
   }
   ```

5. LangServe passes `language` and `text` into the chain defined in `serve.py`.
6. `ChatPromptTemplate` creates a conversation with the instruction `Translate the following into {language}:` and the user's text.
7. `ChatGroq` sends that prompt to the configured Groq model, `openai/gpt-oss-20b`.
8. `StrOutputParser` extracts the text response from the model output.
9. LangServe returns the result in its JSON response; the frontend reads `result["output"]` and shows it under **Translated Text**.

## Setup

### Prerequisites

- Python 3.14 or later (as specified in `pyproject.toml`)
- A Groq API key
- Internet access for the Groq API request

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI_Language_Translator
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Keep this file private and never commit it with a real key. Add `.env` to `.gitignore` before publishing the repository.

## Run the application

The backend must be running before the frontend can translate text.

### Terminal 1: start the backend

```bash
python serve.py
```

The API starts at `http://localhost:8000`. LangServe exposes the translation chain at:

```text
POST http://localhost:8000/chain/invoke
```

### Terminal 2: start the frontend

```bash
streamlit run app.py
```

Open the local URL Streamlit prints in the terminal, usually `http://localhost:8501`.

## API usage

You can invoke the backend directly without the Streamlit interface.

```bash
curl -X POST http://localhost:8000/chain/invoke \
  -H "Content-Type: application/json" \
  -d '{"input":{"language":"Spanish","text":"Good morning"}}'
```

The response contains the generated translation in its `output` field.

## Built-in user feedback and error handling

- Empty input: shows **Please enter some text to translate.**
- Request in progress: shows a **Translating...** spinner.
- Successful request: shows a success message and the translation.
- Backend error response: shows the HTTP status code and response body.
- Backend unavailable: shows guidance to start FastAPI on port `8000`.

## Configuration notes

- The frontend currently expects the backend at `http://localhost:8000`; update the `url` in `app.py` if the backend is deployed elsewhere.
- The backend currently binds to `localhost`, so it is intended for local use.
- The model is set in `serve.py` as `openai/gpt-oss-20b`. You can change it there to another Groq-supported model if needed.
- The application does not store submitted text or translations in a database.

## Common issues

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| “Cannot connect to the backend” | `serve.py` is not running or is not listening on port `8000`. | Start `python serve.py` and keep that terminal open. |
| Authentication/model error | `GROQ_API_KEY` is missing, invalid, or lacks access to the configured model. | Check the `.env` file and restart the backend. |
| `ModuleNotFoundError` | Dependencies are not installed in the active environment. | Activate `.venv` and run `pip install -r requirements.txt`. |
| No result or server error | The Groq service or network connection is unavailable. | Check internet connectivity, backend logs, and your Groq account status. |

## Future improvements

- Add source-language detection.
- Let users enter any target language instead of selecting only from a fixed list.
- Add translation history and copy-to-clipboard support.
- Add automated tests for the API and frontend request handling.
- Add deployment configuration and environment-specific backend URLs.
