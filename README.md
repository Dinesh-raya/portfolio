<div align="center">

# Dinesh Raya — AI Engineer Portfolio

A clean, fast portfolio site. Static HTML/CSS served via GitHub Pages — no frameworks, no server, no build step.

**Live:** [https://dinesh-raya.github.io/portfolio/](https://dinesh-raya.github.io/portfolio/)

## Projects

| Project | Stack | Demo |
|---------|-------|------|
| [RAG Chatbot](projects/rag-chatbot/) | Python, Streamlit, Gemini API, RAG | [Live](https://drrragai.streamlit.app/) |
| [AI Code Review API](projects/code-review-api/) | FastAPI, Gemini AI, Docker, CI/CD | [Live](https://code-review-api.streamlit.app/) |
| [Data Pipeline](projects/data-pipeline/) | Python, pandas, SQLite, GitHub API, CI/CD | [Live](https://data-pipeline.streamlit.app/) |
| [Network Port Scanner](https://github.com/Dinesh-raya/python-network-port-scanner) | Python, Streamlit, Socket Programming | [Live](https://drrnps.streamlit.app/) |
| [Student Management System](https://github.com/Dinesh-raya/Student-management-system-using-python-and-mysql) | Python, MySQL, Streamlit | [Live](https://drrsms.streamlit.app/) |

</div>

---

## Features

- **Hero Dashboard** — Profile, stats, skills radar chart, and quick actions
- **Projects Showcase** — Filterable project cards with tech stacks and links
- **Skills Matrix** — Interactive skill categories with progress indicators
- **Experience Timeline** — Professional journey with visual timeline
- **Playground** — AI chatbot, PDF analyzer, code analyzer, and prompt optimizer
- **Contact Form** — Formspree integration with local fallback
- **Theme Toggle** — Dark and light mode with CSS variables
- **Responsive Design** — Optimized for desktop, tablet, and mobile
- **GitHub Integration** — Live stats pulled from GitHub API

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Dinesh-raya/portfolio.git
cd portfolio

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Troubleshooting

If the app looks stale or the port is busy:

```bash
# Windows (PowerShell)
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process

# Then restart
streamlit run app.py
```

> Only run one `streamlit run app.py` at a time during development.

---

## Project Structure

```
portfolio/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── assets/
│   ├── profile.jpg           # Profile picture
│   └── dinesh_raya.pdf       # Resume PDF
├── components/
│   ├── hero.py               # Hero dashboard section
│   ├── projects.py           # Projects showcase
│   ├── skills.py             # Skills matrix
│   ├── experience.py         # Experience timeline
│   ├── playground.py         # Interactive tools
│   └── contact.py            # Contact form
├── data/
│   └── portfolio_data.py     # Central data store
├── styles/
│   └── main.css              # Custom CSS (glassmorphic UI)
├── utils/
│   ├── __init__.py           # Utility exports
│   └── helpers.py            # Theme, API, form utilities
└── scripts/
    ├── verify.py             # Project verification
    └── check_live.py         # Live deployment checks
```

---

## Assets

Place these optional files in `assets/`:

| File | Purpose | Required |
|------|---------|----------|
| `profile.jpg` | Headshot on Hero section | No (falls back to monogram) |
| `dinesh_raya.pdf` | Resume download button | No (shows "Request Resume" link) |

---

## Configuration

### Environment Variables

No environment variables required for basic functionality.

### Formspree (Contact Form)

For production email delivery:

1. Create a form at [Formspree.io](https://formspree.io/)
2. Copy your form ID
3. Add to Streamlit secrets:

**Local development** — Create `.streamlit/secrets.toml`:
```toml
[formspree]
form_id = "your_formspree_form_id"
```

**Streamlit Cloud** — Go to App Settings → Secrets and add the same TOML structure.

> Without Formspree, local submissions save to `assets/messages.json`. On Cloud without secrets, users see a configuration message.

---

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → Select this repo → `app.py` → `main` branch
4. (Optional) Add Formspree secrets under **Advanced settings → Secrets**
5. Click **Deploy**

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Framework** | Streamlit |
| **Language** | Python 3.9+ |
| **Visualization** | Plotly |
| **Styling** | Custom CSS (Glassmorphic) |
| **APIs** | GitHub API, Formspree |
| **PDF Processing** | PyMuPDF |
| **Testing** | Pytest |

---

## Verification

Run the verification script to check project health:

```bash
python scripts/verify.py
```

With the app running, perform live checks:

```bash
python scripts/check_live.py
```

---

## License

This project is licensed under the MIT License.

---

<div align="center">

**Built by [Dinesh Raya](https://github.com/Dinesh-raya)**

[![GitHub](https://img.shields.io/badge/GitHub-Dinesh--raya-181717?logo=github)](https://github.com/Dinesh-raya)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Dinesh--raya-0A66C2?logo=linkedin)](https://www.linkedin.com/in/dinesh-raya/)

</div>
