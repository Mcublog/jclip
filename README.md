# jclip

Script for the attaching file to Jira issue

## Using

```bash
usage: JClip [-h] -u USERNAME -i ISSUE -f FILE [-t TOKEN]

JClip v0.1.0

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Email address of the user
  -i ISSUE, --issue ISSUE
                        Number of issue or task (KKT-some_number)
  -f FILE, --file FILE  Path to attachment file
  -t TOKEN, --token TOKEN
                        JIRA token or use system environment variable JIRA_TOKEN
```
