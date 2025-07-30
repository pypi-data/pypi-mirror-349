import yaml
import click
def read_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            doc = yaml.safe_load(f)
            return doc if doc is not None else {}
    except FileNotFoundError:
        click.echo(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        click.echo(f"Error reading YAML file: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
    return {}
    
def write_yaml(file_path, data):
    if not data:
        return
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False)
    except Exception as e:
        click.echo(f"Error writing YAML file: {e}", err=True)


def read_file_to_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError:
        # if read by utf-8 failed, try the binary format
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                return content.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"read file failed: {str(e)}")
            return None
    except Exception as e:
        print(f"read file failed: {str(e)}")
        return None

    
    