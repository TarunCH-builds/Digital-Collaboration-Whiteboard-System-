# Digital-Collaboration-Whiteboard-System
# 🎨 CollabBoard – Digital Collaborative Whiteboard System

CollabBoard is a modern, real-time Digital Collaborative Whiteboard platform designed to enhance teamwork, brainstorming, project planning, and remote collaboration. The application allows multiple users to work together on a shared virtual canvas while communicating through an integrated live chat system. Built using Flask, Socket.IO, SQLite, HTML, CSS, and JavaScript, CollabBoard provides a secure, responsive, and interactive workspace for teams, students, educators, and professionals.

---

## 🚀 Project Features

### 🔐 User Authentication
- User Registration
- Secure Login System
- Password Hashing using Werkzeug
- Session Management
- Logout Functionality

### 🖌️ Real-Time Collaborative Whiteboard
- Multi-User Drawing Synchronization
- Pencil Tool
- Brush Tool
- Eraser Tool
- Line Tool
- Rectangle Tool
- Circle Tool
- Text Tool
- Real-Time Updates using WebSockets

### 💬 Live Communication
- Integrated Team Chat
- Instant Message Broadcasting
- Join/Leave Notifications
- Persistent Chat History

### ⚡ Advanced Workspace Features
- Undo & Redo Operations
- Real-Time Cursor Tracking
- Zoom In & Zoom Out
- Canvas Auto-Save
- Shared Workspace Synchronization
- Multiple Board Support

### 📁 Export Capabilities
- Export Whiteboard as PNG
- Export Whiteboard as PDF

### 🎨 Modern User Interface
- Glassmorphism Design
- Responsive Layout
- Interactive Dashboard
- Professional Workspace Environment

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-SocketIO

### Database
- SQLite3

### Libraries & Tools
- Socket.IO
- Werkzeug Security
- jsPDF
- html2canvas

---

## 📂 Project Structure

```text
CollabBoard/
│
├── app.py
│
├── database/
│   └── collabboard.db
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── whiteboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── README.md
```

---

## ⚙️ Installation Guide

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/CollabBoard.git
cd CollabBoard
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask flask-socketio eventlet werkzeug
```

### 5. Run Application

```bash
python app.py
```

Application URL:

```text
http://localhost:5000
```

---

## 🗄️ Database Design

### Users Table

| Field | Type |
|---------|---------|
| id | Integer |
| username | Text |
| email | Text |
| password | Text |

### Whiteboards Table

| Field | Type |
|---------|---------|
| id | Integer |
| board_name | Text |
| created_by | Text |
| created_date | Text |
| canvas_data | Text |

### Messages Table

| Field | Type |
|---------|---------|
| id | Integer |
| board_id | Integer |
| username | Text |
| message | Text |
| timestamp | Text |

---

## 🔄 System Workflow

1. User registers and logs into the platform.
2. User creates or joins an existing whiteboard.
3. Drawing actions are synchronized in real time using Socket.IO.
4. Team members collaborate simultaneously on the same board.
5. Users communicate through the integrated chat module.
6. Canvas state is automatically saved periodically.
7. Boards can be exported as PNG or PDF files.

---

## 🎯 Applications

- Online Education
- Team Brainstorming
- Project Planning
- Agile Sprint Meetings
- Research Collaboration
- Software Architecture Design
- Business Discussions
- Remote Team Collaboration
- Virtual Workshops

---

## 🔒 Security Features

- Password Hashing
- Session-Based Authentication
- Protected User Routes
- Secure Login and Registration
- Database Integrity Management

---

## 🌟 Future Enhancements

- Voice Chat Integration
- Video Conferencing
- File Sharing Support
- Cloud Database Integration
- Board Sharing via Links
- User Roles & Permissions
- AI-Powered Whiteboard Assistant
- Mobile Application Version
- Dark/Light Theme Switcher
- Activity Logs and Analytics

---

## 📈 Project Highlights

✔ Real-Time Collaboration  
✔ Multi-User Drawing Environment  
✔ Live Team Communication  
✔ Auto-Save Functionality  
✔ Undo/Redo Support  
✔ Cursor Tracking  
✔ PNG & PDF Export  
✔ Secure Authentication  
✔ Modern Glassmorphism UI  
✔ Lightweight SQLite Database  

---

## 👨‍💻 Developer 

Tarun C H

### Project Title
**CollabBoard – Digital Collaborative Whiteboard System**

A professional real-time collaboration platform developed using Flask, Socket.IO, SQLite, HTML, CSS, and JavaScript to enable seamless teamwork, communication, and visual collaboration in a shared digital workspace.

---

## 📜 License

This project is developed for educational, academic, and learning purposes. Feel free to modify and extend it for personal or institutional use.
