from pprint import pprint

import Deadline.DeadlineConnect as Connect
conn = Connect.DeadlineCon('localhost', 8082)

SLAVE_NAME = 'MyMachine'

slave_settings = conn.Slaves.GetSlaveSettings(SLAVE_NAME)

pprint(slave_settings)

if len(slave_settings) < 1:
    print("No Slave was found")
    exit(1)

for setting in slave_settings:
    setting['Affin'] = [1, 3, 5]
    setting['AffinOvr'] = True
    print(conn.Slaves.SaveSlaveSettings(setting))