# EventScript.py

An event plugin that executes an external script.

The plugin gets the path to the external script from the jobs extra info, specifically if "EventScript" is specified as a key/value member.

```
ExtraInfoKeyValue1=EventScript=path/to/script.py
```

The event plugin also adds the direcotory of the script to ```sys.path```, so relative imports can be used.

The arguments passed that is normally passed to an event plugin are stored in ```sys.argv```. These arguments vary in length depending the event, but as a minimum will always have the name of the event and the job object.

Example of an external script printing all the arguments available.
```python
import sys


def main():

    event_name = sys.argv[0]
    print("Event Name: {0}".format(event_name))

    job = sys.argv[1]
    print("Job Object: {0}".format(job))

    print("Other arguments: {0}".format(sys.argv[1:]))

main()
```

Since event plugin execute the script in the same process, you import any Deadline related modules.

Lastly if anything fails a stracktrace will be printed and available in the job reports.
