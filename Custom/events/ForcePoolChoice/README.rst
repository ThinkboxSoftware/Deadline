ForcePoolChoice
==================================

When submitting a job, in some cases it would be useful to prevent certain
users from submitting to pools they aren't supposed to. An example might be
a studio which has pooled different departments together into the same farm
where each of the distinct departments have their own segment defined by
pools.

This plugin relies on user groups existing with the same name as the available
pools. If a user is in one or more of these groups they are able to submit to
the pool of the same name.

If they are not in a definied group, the job will be submitted without a pool.

There is also an option to assign a secondary pool to any job submitted. This
will take effect on all jobs which are submitted regardless of user group or
pool configuration.
