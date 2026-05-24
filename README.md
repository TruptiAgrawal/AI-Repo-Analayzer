# 🤖 AI GitHub Repo Summarizer

An AI-powered tool that analyzes any public GitHub repository and generates beginner-friendly summaries. Simply paste a repo URL and get instant insights about what the project does, its structure, and how the code works.

## Features

- 📝 Fetches README, file structure, and sample code from GitHub repos
- 🧠 Uses Groq AI (llama-3.1-8b-instant) to generate plain-English explanations
- 🎨 Clean Streamlit UI with visual file tree
- ⚡ Fast analysis with FastAPI backend

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Groq API key (free at [console.groq.com](https://console.groq.com))

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd AIRepoSummarizer
```

### 2. Install dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from [console.groq.com](https://console.groq.com).

## Usage

### Start the backend server

```bash
# Activate virtual environment if using pip
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Navigate to backend directory
cd backend

# Start FastAPI server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Start the frontend

In a new terminal:

```bash
# Activate virtual environment if using pip
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Navigate to frontend directory
cd frontend

# Start Streamlit app
streamlit run app.py
```

The web interface will open automatically at `http://localhost:8501`

### Analyze a repository

1. Open the Streamlit interface in your browser
2. Paste any public GitHub repository URL (e.g., `https://github.com/owner/repo`)
3. Click "Analyze Repo"
4. View the AI-generated summary and file structure

## Project Structure

```
AIRepoSummarizer/
├── backend/
│   ├── main.py              # FastAPI server with /analyze endpoint
│   ├── github_service.py    # GitHub API interactions
│   ├── grok_client.py       # Groq AI integration
│   ├── repo_reader.py       # Smart file selection logic
│   └── prompt_builder.py    # AI prompt construction
├── frontend/
│   └── app.py               # Streamlit web interface
├── .env                     # Environment variables (create this)
├── pyproject.toml           # Project dependencies
├── requirements.txt         # Pip requirements
└── README.md
```

## API Endpoints

### POST `/analyze`

Analyzes a GitHub repository and returns an AI summary.

**Request:**
```json
{
  "url": "https://github.com/owner/repo"
}
```

**Response:**
```json
{
  "summary": "AI-generated explanation...",
  "file_tree": ["file1.py", "file2.js", ...],
  "repo": "owner/repo"
}
```

## Limitations

- Only works with public repositories
- GitHub API rate limit: 60 requests/hour (unauthenticated)
- Analyzes only one sample code file per repo
- Always uses the default branch (HEAD)

## Troubleshooting

**"Cannot reach backend" error:**
- Ensure the backend server is running on `http://localhost:8000`
- Check that port 8000 is not in use by another application

**"GROQ_API_KEY is missing" error:**
- Verify `.env` file exists in the project root
- Check that `GROQ_API_KEY` is set correctly in `.env`

**GitHub rate limit errors:**
- Wait an hour for the rate limit to reset
- Consider adding GitHub token authentication (future enhancement)

## Future Enhancements

- [ ] GitHub token authentication for higher rate limits
- [ ] Support for private repositories
- [ ] Multi-file code analysis
- [ ] Branch selection
- [ ] Result caching
- [ ] Analysis history
- [ ] Docker deployment

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
