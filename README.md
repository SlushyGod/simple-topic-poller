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
Install pyzmq
```
python3.8 -m pip install pyzmq
```

After that you should be able to run the broker > analysis_engine > execution engine