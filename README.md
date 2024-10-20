# Emergency Management System Using Generative AI

> This Project is Still in Active Development!

## Project Overview

The **Emergency Management System Using Generative AI** is a sophisticated application designed to gather and analyze emergency alerts from various sources. It leverages generative AI to predict future incidents based on historical data and current trends. This system aims to enhance the efficiency of emergency responses by providing insightful reports and visual analytics.

### Key Features:
- **Real-Time Alert Monitoring**: Fetches and stores emergency alerts across different countries.
- **Generative AI**: Implements AI to analyze and generate future predictions of emergency incidents.
- **Graphical Representation**: Displays data using charts and graphs, allowing users to visualize key metrics.
- **Interactive Date/Time Range Selection**: Enables users to set custom date and time ranges for report generation.
- **Keyword and Topic Analysis**: Identifies popular keywords and topics by country and region.
- **Responsive Design**: Supports a mobile-friendly and responsive layout for viewing reports.

## Screenshots

Below are some screenshots showing the features and layout of the system:

![Screenshot 2024-10-09 215727](https://github.com/user-attachments/assets/7e4f2a78-6bd3-49ee-860e-acfa1897b862)
![Screenshot 2024-10-09 215759](https://github.com/user-attachments/assets/b740eb1b-edd2-44e3-9abb-f655637beaf4)
![Screenshot 2024-10-09 215822](https://github.com/user-attachments/assets/05ee531e-9fdd-4ff5-93e5-88b7b78fed2e)
![Screenshot 2024-10-09 215844](https://github.com/user-attachments/assets/1954ee0b-6b50-4599-874e-c754e476eb17)
![Screenshot 2024-10-09 215909](https://github.com/user-attachments/assets/50e2f263-b909-41ee-a3ef-faba59613287)
![Screenshot 2024-10-09 215937](https://github.com/user-attachments/assets/249d9f8f-7c31-49be-9c75-f0367880280f)
![Screenshot 2024-10-09 220003](https://github.com/user-attachments/assets/63dc28e6-f028-4e82-8ec9-b393c19d59fe)

## Getting Started

### Prerequisites:
- **Python** (Version 3.x or higher)
- **Flask** (Web framework)
- **pandas** (For data manipulation)
- **matplotlib** (For data visualization)

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/muhammad-fiaz/Emergency-Management-System-using-Generative-AI.git
   cd Emergency-Management-System-using-Generative-AI
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

### Folder Structure:
```bash
.
├── app.py                  # Main Flask application
├── fetch_alerts.py            # Fetch report from online
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
│   ├── styles.css
├── database_alerts.db         # stored Database
└── README.md               # Project documentation
```

## Usage

- Open the application in your browser.
- Enter a range of dates and times to generate reports.
- Visualize the results in various graphical formats.

## Contributing

We welcome contributions! Feel free to submit issues and pull requests to improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

