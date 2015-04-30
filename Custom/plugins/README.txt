This is where to place custom render plugins

Render plugins handle the lifetime of a render task. They're loaded at
job dequeue time and handle things like detecting error and progress
text, setting up the render environment and a bunch of process related
things.

Note that for a new plugin type you'll need a custom submitter. Those
life in a completely different place for now, and as of Edwin writing
this, we don't have any examples in this Git repository.

See '[repo]/submission/[plugin]' for examples in your own Deadline
Repository!