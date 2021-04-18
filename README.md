# Track Job Opening

> Track 'Work on Campus' Job Opportunities in Langara College for Summer 2021

## Usage

1. Run ```pip install -r requirements.txt``` to install required packages.
2. Configure *send_mail* function in *functions.py* according to your email account.
3. Run ```track_job.py```

## Notes

* Intended to be used with Windows Task Scheduler to fully automate the process.
* Alerts are sent via email only when a relevant role is found or when an error is encountered. Nothing is done otherwise. However, all actions and results are logged in the *log.txt* file.
