# Project: ScribbleData - YouTube Video Analysis

## Description

ScribbleData - YouTube Video Analysis is a Python-based project that aims to provide insights into YouTube video data through data analysis techniques. This project caters to data scientists, project managers, and analysts within a media company, enabling them to prepare, process, and analyze event data from YouTube in various meaningful ways.


YouTube Video Analysis is a data-driven project designed to uncover patterns and trends within YouTube video data. By utilizing advanced data analysis techniques, this project offers valuable insights that can benefit content creators, marketers, and other stakeholders.
 Project Structure

The project is structured into various components:

- **Operations:** 
- **Database:**
- **Outliers:** 
- **Workflows:** 
- **Models:**

## 3. Usage Instructions

Follow these steps to set up and run the project:

1. Clone the repository:

`git clone https://github.com/sagrawal486/ScribbleDataAssignment.git`


2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate
```

3. Install required dependencies from `requirements.txt`:
`pip install -r requirements.txt`

4. Configure the `config.ini` file with your settings. A sample config file is provided.

5. Run `main.py` to save data into SQLite and identify outliers:
`python main.py`

6. Run the server using [Uvicorn](https://www.uvicorn.org/):
`uvicorn app:app --port 8000`

7. Access API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)
