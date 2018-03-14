# HostnameConfiguration #

Event listener which automatically assigns slaves into the groups or pools following mapping rules. The mapping can be set using regex.

```python
{
    "regex_slave_pattern" : {
        "Groups" : ["group_name","2nd_group_name"],
        "Pools" : ["pool_name", "2nd_pool_name"],
        "Override" : "False"},
    "2nd_regex_slave_pattern": {
        "Groups":["group_name","2nd_group_name"],
        "Pools":["pool_name", "2nd_pool_name"],
        "Override" : "True"}
}
```

For example if you would like to assign AWS machines into the group aws and pool maya.

```python
{
    "^ip-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}" : {
        "Groups" : ["aws"],
        "Pools" : ["maya"],
        "Override" : "True"}
}
```

This matches all slaves in the naming like ip-10-2-128-4 and assign them. If there is already assignment done on the slave and the override param is set to False then it will skip that slave.