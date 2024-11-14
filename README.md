<h1 align="center">🚨 EMSUGI 🚨</h1>

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Running with Docker](#running-with-docker)
  - [Folder Structure](#folder-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [MIT License](#mit-license)

## Project Overview

The **EMSUGI** is a sophisticated application designed to gather and analyze emergency alerts from various sources. It leverages generative AI to predict future incidents based on historical data and current trends. This system aims to enhance the efficiency of emergency responses by providing insightful reports and visual analytics.

> This Project is Still in Active Development!

## Key Features:
- **Real-Time Alert Monitoring**: Fetches and stores emergency alerts across different countries.
- **Generative AI**: Implements AI to analyze and generate future predictions of emergency incidents.
- **Graphical Representation**: Displays data using charts and graphs, allowing users to visualize key metrics.
- **Interactive Date/Time Range Selection**: Enables users to set custom date and time ranges for report generation.
- **Keyword and Topic Analysis**: Identifies popular keywords and topics by country and region.
- **Responsive Design**: Supports a mobile-friendly and responsive layout for viewing reports.


> **NOTE:** These features are based project's future intention so the actual performance and feature may vary due to active development phases

## Screenshots

Below are some screenshots showing the features and layout of the system:

![Screenshot 2024-11-14 220005](https://github.com/user-attachments/assets/0021a145-ca8d-44c3-a333-0d51e949b346)
![Screenshot 2024-10-09 215759](https://github.com/user-attachments/assets/b740eb1b-edd2-44e3-9abb-f655637beaf4)
![Screenshot 2024-10-09 215822](https://github.com/user-attachments/assets/05ee531e-9fdd-4ff5-93e5-88b7b78fed2e)
![Screenshot 2024-10-09 215844](https://github.com/user-attachments/assets/1954ee0b-6b50-4599-874e-c754e476eb17)
![Screenshot 2024-10-09 215909](https://github.com/user-attachments/assets/50e2f263-b909-41ee-a3ef-faba59613287)
![Screenshot 2024-10-09 215937](https://github.com/user-attachments/assets/249d9f8f-7c31-49be-9c75-f0367880280f)
![Screenshot 2024-10-09 220003](https://github.com/user-attachments/assets/63dc28e6-f028-4e82-8ec9-b393c19d59fe)
![Screenshot 2024-11-14 220006](https://github.com/user-attachments/assets/1381e445-8603-48c4-b7e1-9276fa89965d)
![Screenshot 2024-11-14 220007](https://github.com/user-attachments/assets/6b17ecbd-3603-45dc-8340-b1c7d8c0b45f)


> **NOTE:** These screenshots reflect the current state of the project's development and may change in the future as features evolve and improvements are made.

## Getting Started

### Tech Stack:

- **Python** (Version 3.x or higher): A powerful, high-level programming language used for backend development.  
- **Flask**: A lightweight web framework for building web applications in Python.  
- **pandas**: A data manipulation library that provides powerful data structures for data analysis.  
- **matplotlib**: A popular plotting library used for creating static, animated, and interactive visualizations.  
- **gemini**: An AI-powered tool for generative report generation, used for creating emergency and disaster reports.  
- **torch**: A deep learning framework that provides flexible and efficient tools for training and deploying machine learning models, particularly for local model inference.  
- **transformers**: A library by Hugging Face for working with pre-trained transformers and other state-of-the-art machine learning models.  
- **logly**: A logging and monitoring tool used to track and manage logs within applications.  
- **python-dotenv**: A tool to manage environment variables, allowing the configuration of sensitive information (API keys, tokens, etc.) in a `.env` file.  
- **SQLite**: A lightweight, disk-based database to store and retrieve data for the application.  
- **Tailwind CSS**: A utility-first CSS framework for quickly designing responsive, modern web interfaces.
- **Font Awesome** - Icon library used for adding scalable vector icons in the UI.
- **Chart.js** - JavaScript library for creating interactive and customizable charts for data visualization.

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/muhammad-fiaz/EMSUGI.git
   cd EMSUGI
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```


3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
### Running with Docker

If you'd like to run this project using Docker, check out the [docker_readme.md](DOCKER_README.md) file for a step-by-step guide on building, 
running, and managing the EMSUGI application in a Docker container.

### Folder Structure:
```bash
.
├── app.py                  # Main Flask application
├── fetch_alerts.py         # Fetch report from online
├── generate.py             # Return a generated AI report based on data
├── report_general.py       # Return a generated summary and keywords and tags from fetched articles
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
│   ├── styles.css          # Global styles
├── database.py             # Used to create DB
├── database_alerts.db      # Stored Database
├── Dockerfile              # Docker configuration file
├── CODE_OF_CONDUCT.md      # Code of conduct for contributors
├── LICENSE                 # Open-source license for the project
├── pyproject.toml          # Python project configuration file
├── docker_readme.md        # Instructions for using Docker
└── README.md               # Project documentation
```

## Usage

- Open the application in your browser.
- Enter a range of dates and times to generate reports.
- Visualize the results in various graphical formats.

## Contributing

We welcome contributions! Feel free to submit issues and pull requests to improve the project. 
When contributing, please make sure to follow our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a respectful and collaborative environment for all contributors.

## MIT License
```text
Copyright (c) 2024 Muhammad Fiaz

Permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the condition that the copyright notice and this permission notice are included in all copies.

The software is provided "as is", without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors be liable for any claims or damages.

```
For more details, please refer to the full [LICENSE](LICENSE).

