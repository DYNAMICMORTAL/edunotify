# EduNotify — Cloud-Based Notification System for Colleges

EduNotify is an open-source web application that enables colleges and universities to manage and broadcast academic notices digitally. Built with Python (Flask) and deployed using AWS services like Elastic Beanstalk, S3, and DynamoDB, it offers a scalable solution for connecting professors and students through a centralized, cloud-native platform.

---

## ✨ Features

- 🔐 **Secure Role-Based Login** — Separate interfaces for professors and students
- 📢 **Admin Dashboard** — Post notices with optional attachments
- 🎯 **Student Filters** — View notices by department and academic year
- ☁️ **AWS Integration** — Uploads stored in S3, notices stored in DynamoDB
- 🚀 **Cloud Deployment** — Ready-to-deploy via Elastic Beanstalk

---

## 📦 Tech Stack

| Layer           | Technology                     |
|----------------|---------------------------------|
| Frontend       | HTML, Tailwind CSS, Jinja2     |
| Backend        | Python (Flask)                 |
| Storage        | Amazon S3, DynamoDB            |
| Hosting        | AWS Elastic Beanstalk (EC2)    |
| Permissions    | IAM Roles + Policies           |

---

## 🗂️ Directory Structure

```
edunotify/
├── application.py              # Main Flask app
├── requirements.txt            # Python dependencies
├── templates/                  # Jinja2 HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── post_notice.html
│   ├── view_notices.html
│   ├── student_management.html
│   └── partials/
│       ├── sidebar.html
│       └── navbar.html
```

---

## ☁️ AWS Architecture

### 🔹 Elastic Beanstalk (EC2)
- Hosts the Flask application
- Handles auto-scaling and environment management

### 🔹 Amazon S3
- Stores uploaded notice attachments
- Files served securely via S3 URLs

### 🔹 Amazon DynamoDB
- NoSQL database for notices
- Schema-less, fast, highly available

### 🔹 IAM
- Manages role-based access control for EC2 + services

### 🔹 VPC (Optional)
- Secure networking configuration for EC2 environment

---

## 🚀 Deployment Guide

### 1. Prepare ZIP Package
Ensure the following are included:

- `application.py`
- `templates/` folder with all HTML files
- `requirements.txt`

### 2. Elastic Beanstalk Setup
- Platform: **Python 3.8**
- Tier: **Web Server Environment**
- Upload ZIP and deploy

### 3. AWS Configuration
- ✅ S3 Bucket: `edunotify-attachments`
- ✅ DynamoDB Table: `EduNotify-Notices` (Primary key: `id`)
- ✅ IAM Role with policies:
  - `AmazonS3FullAccess`
  - `AmazonDynamoDBFullAccess`

---

## 🧪 Requirements

```bash
Flask
boto3
Werkzeug
```

Install dependencies locally:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and open pull requests to add features, fix bugs, or improve the documentation.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

