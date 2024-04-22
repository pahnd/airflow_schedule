from jinja2 import Environment
import yaml

def generate_airflow_job(config, jinja2, dag_output, schedule: str):
    with open(config, 'r') as file:
        loaded = yaml.load(file)
    loaded['SCHEDULE'] = schedule

    with open(config, 'w') as file:
        yaml.dump(loaded, file)

    with open(jinja2, 'r') as file:
        jinja2_content = file.read()
    env = Environment()
    template = env.from_string(jinja2_content)

    with open(f"{config}", "r") as input_file:
        inputs = yaml.safe_load(input_file)                    
        with open(f"{dag_output}/{loaded['name']}.py", "w") as f:
            f.write(template.render(inputs))