# -*- coding: utf-8 -*-
# Central data store for Dinesh Raya's Portfolio

PORTFOLIO_DATA = {
    "personal": {
        "name": "Dinesh Raya",
        "role": "AI Enthusiast • Developer • Problem Solver",
        "tagline": "Hi, I'm Dinesh Raya",
        "short_description": "I build intelligent, efficient, and impactful digital solutions using Python, AI/ML, and modern software engineering technologies.",
        "location": "Andhra Pradesh, India",
        "email": "dineshraya365@gmail.com",
        "github_username": "Dinesh-raya",
        "github": "https://github.com/Dinesh-raya",
        "linkedin": "https://www.linkedin.com/in/dinesh-raya/",
        "photo": "assets/profile.jpg",
        "resume_name": "Dinesh_Raya_Resume.pdf",
        "drives": [
            {"icon": "💡", "title": "Problem Solver"},
            {"icon": "📖", "title": "Continuous Learner"},
            {"icon": "🎯", "title": "Impact Focused"},
            {"icon": "🚀", "title": "Tech Explorer"},
        ],
    },
    
    "stats": [
        {"value": "15+", "label": "Projects Completed", "icon": "⚡"},
        {"value": "3+", "label": "Years Learning & Building", "icon": "🎓"},
        {"value": "6+", "label": "Tech Domains explored", "icon": "🌐"},
        {"value": "Infinite", "label": "Curiosity Level", "icon": "🔥"}
    ],
    
    "about": {
        "summary": (
            "I am a passionate AI Developer and Software Engineer focused on solving complex computational "
            "problems and building products that make a difference. With a solid foundation in Python, "
            "data structures, and AI/ML principles, I bridge the gap between advanced models and web user interfaces."
        ),
        "journey": (
            "My coding journey started out of pure curiosity—asking how software behaves under the hood. "
            "As I dove deeper, I fell in love with algorithm design and data structures. That quickly evolved "
            "into exploring artificial intelligence, machine learning, and automation. "
            "Today, I build web integrations, machine learning tools, automation scripts, and custom interactive dashboard platforms. "
            "I believe that engineering is not just about writing code; it's about engineering solutions to real-world problems."
        ),
        "education": [
            {
                "degree": "Master of Computer Applications",
                "institution": "Acharya Nagarjuna University",
                "year": "2021 - 2023"
            }
        ],
        "languages": ["Telugu (Native)", "English (Professional)", "Hindi (Conversational)"],
        "workspace_info": {
            "os": "Windows / Linux",
            "editor": "VS Code / Cursor",
            "terminal": "PowerShell / Zsh",
            "vibe": "Dark mode default, clean desk, coffee nearby."
        }
    },
    
    "projects": [
        {
            "id": 1,
            "title": "AI PDF Analyzer & Summarizer",
            "category": "AI/ML",
            "description": "An interactive utility that parses multi-page PDFs, extracts text layout structures, and builds vector index points for semantic question-answering and smart summarization.",
            "tech": ["Python", "Streamlit", "LangChain", "OpenAI API", "ChromaDB"],
            "github": "https://github.com/Dinesh-raya/ai-pdf-analyzer",
            "demo": "https://ai-pdf-analyzer.streamlit.app",
            "image_slug": "pdf_analyzer"
        },
        {
            "id": 2,
            "title": "Interactive Monopoly Game",
            "category": "Python/Automation",
            "description": "A fully functional Python implementation of the Monopoly board game featuring logical rules, simulated AI players with distinct buying strategies, and text/GUI interfaces.",
            "tech": ["Python", "Pygame", "Design Patterns", "Object-Oriented Programming"],
            "github": "https://github.com/Dinesh-raya/python-monopoly",
            "demo": "",
            "image_slug": "monopoly"
        },
        {
            "id": 3,
            "title": "Intelligent Resume Screener",
            "category": "AI/ML",
            "description": "An automated screening dashboard utilizing Natural Language Processing (NLP) to parse resumes, map experience descriptions to job requirements, and rank candidates using semantic similarity.",
            "tech": ["Python", "Streamlit", "NLTK", "scikit-learn", "Spacy"],
            "github": "https://github.com/Dinesh-raya/resume-screener",
            "demo": "https://resume-screener.streamlit.app",
            "image_slug": "resume_screener"
        },
        {
            "id": 4,
            "title": "DevOps Automation Dashboard",
            "category": "Python/Automation",
            "description": "A centralized engineering console monitoring API health checks, system performance metrics, and triggering container updates and backup cron scripts automatically.",
            "tech": ["Python", "Docker", "Bash", "Streamlit", "Prometheus Client"],
            "github": "https://github.com/Dinesh-raya/devops-dashboard",
            "demo": "",
            "image_slug": "devops_dashboard"
        },
        {
            "id": 5,
            "title": "Premium AI Engineer Portfolio",
            "category": "Full Stack",
            "description": "A modern glassmorphic dashboard showcasing professional achievements, skills, and interactive mini AI products built natively on top of Python and Streamlit.",
            "tech": ["Python", "Streamlit", "Custom CSS", "HTML5", "Plotly"],
            "github": "https://github.com/Dinesh-raya/portfolio",
            "demo": "",
            "image_slug": "portfolio"
        },
        {
            "id": 6,
            "title": "Advanced AI Chat Assistant",
            "category": "AI/ML",
            "description": "A premium chat panel incorporating system instruction overrides, conversation memory management, dynamic markdown streaming, and developer prompt templates.",
            "tech": ["Python", "Streamlit", "OpenAI", "Session State"],
            "github": "https://github.com/Dinesh-raya/ai-chat-assistant",
            "demo": "https://chat-assistant.streamlit.app",
            "image_slug": "chat_assistant"
        }
    ],
    
    "skills": {
        "radar": {
            "metrics": ["AI/ML", "Python Programming", "Web Development", "Data Structures", "Problem Solving", "Automation & Scripting"],
            "values": [90, 95, 85, 88, 92, 90]
        },
        "categories": [
            {
                "title": "Artificial Intelligence & ML",
                "items": ["Supervised/Unsupervised Learning", "Large Language Models (LLMs)", "RAG Architectures", "NLP & Semantic Search", "Vector Databases", "Prompt Engineering"]
            },
            {
                "title": "Software Engineering & Python",
                "items": ["Object-Oriented Programming", "Design Patterns", "Data Structures & Algorithms", "API Development (FastAPI, Flask)", "Unit Testing (pytest)", "Scripting & Automation"]
            },
            {
                "title": "Web & Deployment",
                "items": ["Streamlit", "HTML5 & CSS3 Variables", "Docker Containerization", "Git & GitHub Actions", "SQL (PostgreSQL/SQLite)", "Linux Administration"]
            }
        ]
    },
    
    "tech_stack": [
        {
            "category": "Languages",
            "items": [
                {"name": "Python", "icon_svg": "python"},
                {"name": "HTML5", "icon_svg": "html"},
                {"name": "CSS3", "icon_svg": "css"}
            ]
        },
        {
            "category": "Frameworks & Libraries",
            "items": [
                {"name": "Streamlit", "icon_svg": "streamlit"},
                {"name": "FastAPI", "icon_svg": "fastapi"},
                {"name": "PyTorch", "icon_svg": "pytorch"},
                {"name": "scikit-learn", "icon_svg": "scikitlearn"},
                {"name": "Pandas", "icon_svg": "pandas"}
            ]
        },
        {
            "category": "Tools & Infrastructure",
            "items": [
                {"name": "Docker", "icon_svg": "docker"},
                {"name": "Git & GitHub", "icon_svg": "git"},
                {"name": "Linux", "icon_svg": "linux"},
                {"name": "PostgreSQL", "icon_svg": "postgresql"},
                {"name": "VS Code", "icon_svg": "vscode"}
            ]
        }
    ],
    
    "highlights": [
        {"icon": "🛠️", "title": "Open Source", "desc": "Actively contributing to Python & AI repos"},
        {"icon": "📚", "title": "Self-Taught ML", "desc": "Mastered core ML concepts through hands-on building"},
        {"icon": "🚀", "title": "Shipped Products", "desc": "Deployed Streamlit apps to production"},
        {"icon": "🤝", "title": "Freelance Work", "desc": "Delivered real-world Python & AI solutions for clients"},
    ],

    "experience": [
        {
            "period": "2024 - Present",
            "title": "Independent AI/ML & Python Developer",
            "subtitle": "Freelancing & Personal Venture",
            "description": "Designing and deploying production-grade Streamlit dashboards, writing automation scripts in Python, integrating OpenAI APIs, and structuring semantic RAG applications for clients."
        },
        {
            "period": "2023 - 2024",
            "title": "Open Source Contributor & AI Researcher",
            "subtitle": "Tech Communities & Research",
            "description": "Collaborated on open source NLP repositories, researched LLM fine-tuning and agentic frameworks, and implemented data structures in competitive programming settings."
        },
        {
            "period": "2021 - 2023",
            "title": "Full Stack Learning & Foundations",
            "subtitle": "Computer Science Journey",
            "description": "Mastered fundamental concepts in Algorithms, Object-Oriented Design, Relational Databases, and built early projects utilizing JavaScript, Python, and CSS layouts."
        }
    ]
}
