job_submission.py
================================

This is an example of how to submit jobs via the REST API through the 
standalone Python API. The bare minimum number of options are shown here for
the job info collection, but you pull from the options found on [this page](https://docs.thinkboxsoftware.com/products/deadline/9.0/1_User%20Manual/manual/manual-submission.html#job-info-file-options).

Different plugins will have different requirements for the plugin info
collection, and you should refer to some existing jobs in your queue for ideas
on what those feilds can be. Check the 'Submission Params' section of the
'Modify Job Properties' dialog.