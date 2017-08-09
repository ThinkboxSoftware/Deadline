set_slave_cpu_affinity.py
================================

This is an example of how to modify Slave settings using the REST API through
our Standalone Python API. The REST interface and object elements are different
than the internal API, so often it's worth investigating the dictionaries
with pprint and friends.

Here, we're setting the CPU affinity of MyMachine to a few different cores. Note
that the Deadline UI is mostly handling whether you pick more cores than the
machine has and if you select a specific number of cores.
