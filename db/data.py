import yaml
import sys
import os
from storage.storage import NewJobDict

#with open("config/job.yaml", "r") as f:
#    data = yaml.safe_load(f)
data1 = {
  "job": [
    {
      "config_schedule_file": "./job2.yaml",
      "jinja2_path": "/root/duypa/test.jinja",
      "name": "Backup1",
      "dag_output_locate": "/opt/dag/"
    },
    {
      "config_schedule_file": "./job2.yaml",
      "jinja2_path": "/root/duypa/test.jinja",
      "name": "Backup2",
      "dag_output_locate": "/opt/dag/"
    }
  ]
}

data = NewJobDict(data1)

# print(data)

# # for job in data.job:
# #      print(job.name)
