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
            "I build things with Python — data pipelines, AI tools, automation scripts, and interactive web apps. "
            "My work spans the full stack of modern AI engineering: from training models and designing RAG pipelines "
            "to deploying production-grade Streamlit dashboards. I learn by building, and I ship what I learn."
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
            "title": "Python Network Port Scanner",
            "category": "Python/Automation",
            "description": "A multi-threaded network port scanner built with Python. Scans targets for open ports, identifies running services, and generates a clean report. Deployed as a live Streamlit app.",
            "tech": ["Python", "Streamlit", "Socket Programming", "Multi-threading"],
            "github": "https://github.com/Dinesh-raya/python-network-port-scanner",
            "demo": "https://drrnps.streamlit.app/",
            "image_slug": "port_scanner"
        },
        {
            "id": 2,
            "title": "Student Management System",
            "category": "Python/Automation",
            "description": "A full-featured student management system using Python and MySQL. Handles student records, attendance tracking, grade management, and search with an interactive dashboard.",
            "tech": ["Python", "MySQL", "Streamlit", "SQLAlchemy"],
            "github": "https://github.com/Dinesh-raya/Student-management-system-using-python-and-mysql",
            "demo": "https://drrsms.streamlit.app/",
            "image_slug": "student_management"
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
