# Descirption
Multitasking bot for local or backend deployment.

# Installation
Steps listed below.
1. Create and activate environment.
```
python -m venv env
source env/bin/activate 
```

2. Requirements
```
pip install -r requirements.txt
```

# Deployment
Pipeline for reboot and first run.
1. Activate environment
```
source env/bin/activate 
```

2. Run
```
python app.py
```

# Exit codes reference.
```
0 - finished successfully, or by command
1 - unknown error, needs restart
2 - config error, shutdown
```

# Credits
Private owned by Nikita Alpatiev, all rights reserved.