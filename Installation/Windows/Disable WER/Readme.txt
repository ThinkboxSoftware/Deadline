Windows Error Reporting Registry fix:
------------------------------------

When apps crash on Windows, the system holds the application open in
memory and displays a helpful box asking if you want to submit the error
report.

While that's super handy for all sorts of reasons, if there's no
one there to click the dialog, Deadline will assume application du
jour is still running and wait indefinitely by default (It's actually
pretty tricky to detect that stupid dialog).

So, this registry fix should stop that from popping up on render nodes
that don't have baby sitters. Meaning when the application crashes,
it actually exits like we know it should.

For more information about the possible settings, look here:
http://msdn.microsoft.com/en-us/library/bb513638.aspx

It's possible to just default to sending them if you like, or to
store the crash dumps in a safe place if you're a developer. Pretty
cool.