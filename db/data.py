import yaml
from storage.storage import NewJobDict

with open("config/job.yaml", "r") as f:
   data_config = yaml.safe_load(f)

data = NewJobDict(data_config)
