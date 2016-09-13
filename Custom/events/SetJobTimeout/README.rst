SetJobTimeout.py
==================================

This guy is useful for when you want to make sure Jobs on the farm cannot run for too long, or want to make sure a task is considered failed if it didn't render long enough. These can be set on individual jobs, but this event will ensure those settings are applied to any newly submitted jobs.

Timeouts are particularly useful in shared farms such as schools where a student may accidentally submit a job that would occupy the farm for days. You could set a maximum of one hour for example and the task will be requeued after that timeout.