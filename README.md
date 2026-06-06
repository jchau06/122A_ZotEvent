## 1. Clone the Repository
- git clone https://github.com/jchau06/122A_ZotEvent.git
- cd 122A_ZotEvent

## 2. Install dependencies
- brew install mysql
- pip3 install mysql-connector-python

## 3. Run Setup and Test Connection
- python3 -c "from database import setup_schema; setup_schema()"
- python3 project.py import sample_data
