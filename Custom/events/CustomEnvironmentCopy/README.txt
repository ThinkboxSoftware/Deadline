CustomEnvrionmentCopy.py
========================================

This event plugin hooks into the "OnJobSubmitted" and allows a studio to duplicate the local environment variables except those chosen to the job's environment. 

For example you may want to pass a copy of the local environment variables but not the PATH, as that's specific to the submitter machine and of no use to the render machine. Typically you'd want to do this with "Include Environment=True" but that is only available after the job has been submitted. This allows you to achive similar functionality.

This will fire on every job that gets submitted, testing for job type will need to be added if that is not what you're looking for.

If you're looking for a good example event plugin to study, take a look at OverrideJobName.py.