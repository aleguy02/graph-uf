### Prerequisites
- Python 3.13.x

### Getting Started - Server
First
```
cd server
python -m venv .myenv
<activate virtual environment>
pip install -r requirements.txt
```

**Scraping UF SoC Data**
```
python ../scripts/scrape_soc.py
python ../scripts/clean_soc.py
```
Optionally, you can verify duplicates were removed with `./../scripts/verify_cleaned.sh`

**Running the Server**
First, make a new file called `.env` at the root directory, then copy the contents in `example.env` into this new file.
To start the develepment server do:
`flask run`