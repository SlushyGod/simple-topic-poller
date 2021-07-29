Very simple architecture to pass data from an "execution engine" over to an "analysis engine"

Setup:

Install virtual environment
```
apt install python3-venv
python3.8 -m venv venv
```
Start the virtual environment
```
source venv/bin/activate
```
Install dependencies
```
python3.8 -m pip install -r requirements.txt
```

After that you should be able to run the broker > analysis_engine > execution engine