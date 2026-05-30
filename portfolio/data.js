/**
 * Portfolio content data.
 * Sourced from Sandesh Narendra Bagmare's resume.
 * Kept separate from rendering logic for easy updates.
 */
const PORTFOLIO_DATA = {
  roles: [
    "Associate Software Analyst",
    "Agentic AI Engineer",
    "Multi-Agent Systems Developer",
    "Cloud & DevOps Engineer",
  ],

  experience: [
    {
      company: "PTC",
      role: "Associate Software Analyst",
      period: "July 2025 – Present",
      location: "Pune, India",
      points: [
        "Developed the Twx AI Assistant agentic framework with a multi-agent PoC using LangGraph and Plan-and-Act methodology.",
        "Built an AI Agents Evaluation Framework integrating Azure AI Evaluation, DeepEval, and 4 custom evaluators with HTML/Allure reporting.",
        "Engineered a CLI-based Agent Development Kit (ADK) for automated agent creation with customization capabilities.",
        "Enhanced the Twx Copilot RAG system with Qdrant-based pipelines, optimized chunking, and hybrid reranking for improved retrieval.",
        "Contributed to development of agents and A2A (agent-to-agent) capabilities for the framework.",
      ],
    },
    {
      company: "PTC",
      role: "Software Engineering Intern",
      period: "July 2024 – June 2025",
      location: "Pune, India",
      points: [
        "Developed comprehensive unit tests for Helm charts across Solution Central repositories, ensuring deployment reliability.",
        "Resolved security vulnerabilities identified by Invicti, Prisma, and Black Duck for the Solution Central 3.1.2 release.",
        "Created Terraform scripts for Azure Flexible Server 16 deployment and PostgreSQL 11 migration validation scripts.",
        "Designed a LangGraph flow architecture for Twx Copilot ensuring data privacy and optimized token usage.",
        "Developed and presented a Twx Copilot RAG-based PoC demonstrating intelligent product assistance capabilities.",
      ],
    },
  ],

  projects: [
    {
      title: "AI-Powered Social Media Automation Platform",
      year: "2025",
      tags: ["Generative AI", "Python", "Analytics"],
      points: [
        "Automated AI-driven content creation, scheduling, and publishing across Instagram and YouTube accounts.",
        "Optimized SEO using LLM-generated hashtags, captions, and performance-based content pruning.",
        "Built an analytics pipeline for engagement tracking, reach prediction, and quality thresholding.",
        "Scaled the platform to manage 10+ accounts via API-based automation and influencer outreach.",
      ],
      icon: "🚀",
    },
    {
      title: "Vision-Based Humanoid Robotic Palm",
      year: "2024",
      tags: ["Deep Learning", "ResNet", "YOLOv5", "VGG16", "Arduino"],
      points: [
        "Developed a vision-based robotic palm to assist amputees in daily tasks, with Arduino Uno for precise gripping control.",
        "Achieved high object-detection accuracy: ResNet (98.92%), VGG16 (96.55%), YOLOv5 (84.90%).",
        "Integrated deep-learning classification with hardware control for real-time object recognition and adaptive gripping.",
      ],
      icon: "🦾",
    },
    {
      title: "Pressure-Sensor-Based Smart Bed",
      year: "2024",
      tags: ["Python", "FSR Sensors", "MySQL", "Data Visualization"],
      points: [
        "Developed a smart bed with a 20×10 FSR sensor matrix to monitor body-pressure distribution during sleep with real-time color-coded maps.",
        "Integrated a MySQL database for pressure-data storage with timestamps, enabling future analysis and research.",
        "Designed for bedsore prevention, sleep tracking, fall detection (elderly/infants), and sleep-disorder diagnosis.",
      ],
      icon: "🛏️",
    },
  ],

  skills: [
    { group: "Languages", items: ["Java", "Python", "HTML", "CSS", "JavaScript", "Bash"] },
    { group: "AI / ML", items: ["LangChain", "LangGraph", "RAG", "Qdrant", "Azure AI Evaluation", "DeepEval"] },
    { group: "Cloud & DevOps", items: ["Helm", "Terraform", "Azure", "Git", "Jenkins"] },
    { group: "Security", items: ["Burp Suite", "Invicti", "Prisma", "Black Duck"] },
    { group: "Databases", items: ["PostgreSQL", "Azure Flexible Server", "MySQL"] },
    { group: "Core Concepts", items: ["Agentic AI", "Multi-Agent Architectures", "DSA", "OOP", "DBMS", "OS", "Cybersecurity"] },
  ],

  awards: [
    "Product Spotlight Winner Q3'2025 — ThingWorx AI contributions",
    "Team PTC — AI contributions",
    "TCS Cybersecurity HackQuest 9 CTF — Digital Package secured",
    "Team PTC — Terraform and Security issues for SC 3.1.2",
    "Brain, Passion, and Fun — Helm contribution",
  ],

  certifications: [
    "AI & Cybersecurity 2025 — O'Reilly",
    "LinkedIn AI Academy — LinkedIn Learning",
    "Google Cybersecurity — Coursera",
    "Securing Generative AI — O'Reilly",
    "Agentic AI in Action — O'Reilly",
  ],

  education: [
    {
      institution: "Vishwakarma Institute of Technology, Pune",
      degree: "B.Tech — Electronics & Telecommunication",
      year: "2021 – 2025",
      score: "8.84 CGPA",
    },
    {
      institution: "Army Public School Kirkee, Pune",
      degree: "CBSE HSC (Class XII)",
      year: "2021",
      score: "90.80%",
    },
    {
      institution: "Army Public School Kirkee, Pune",
      degree: "CBSE SSC (Class X)",
      year: "2019",
      score: "91.83%",
    },
  ],
};
