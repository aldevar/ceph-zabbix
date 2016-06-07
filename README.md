ceph-zabbix
===========

Zabbix plugin for Ceph monitoring

Installation
===========
Edit the *zabbix_agent_ceph_plugin.conf* to set the path to the python scripts (default is /opt/ceph*.py) then add it to your zabbix agent config

Add the xml template and link them to your node.

Link the ceph templates to your hosts

What's next
==============

Actually zabbix agent pull data from script.
One option is to send directly from the script to zabbix trough zabbix-trapper
