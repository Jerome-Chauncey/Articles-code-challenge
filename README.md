# Magazine Author Article Manager 📚✍️

A Python + SQLAlchemy project for managing authors, magazines, and their published articles. Supports both ORM and raw SQL queries, with focus on many-to-many and one-to-many relationships, data integrity, and transaction safety.

---

## 🔧 Features

- Add and retrieve authors, magazines, and articles
- Associate articles with specific magazines
- View topic areas and contributor lists
- Perform queries using both SQLAlchemy ORM and raw SQL
- Use data validation and transaction handling

---

## 🗂 Project Structure

lib/  
└── models/  
&emsp; ├── __init__.py &nbsp;&nbsp;&nbsp;&nbsp;# Initializes DB (SQLAlchemy instance)  
&emsp; ├── base.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Base class for declarative models  
&emsp; ├── author.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Author model + custom methods  
&emsp; ├── magazine.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Magazine model + queries  
&emsp; ├── article.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Article model  
&emsp; └── association.py &nbsp;&nbsp;# Association table for many-to-many  

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jerome-Chauncey/Articles-code-challenge.git
   cd Articles-code-challenge
