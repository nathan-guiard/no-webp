import yaml
import os
import sys
from watchdog.events import *
from watchdog.observers import Observer

from parsing import *

BASIC_CONFIGURATION = 'config.yml'

config = {}

def on_create(event: FileCreatedEvent):
    global config
    if str(event.src_path).endswith('.webp') and not event.is_directory:

        base_file_name = os.path.basename(event.src_path)[:-5:]
        path = os.path.dirname(event.src_path)
        prefix = config["convertion"]["prefix"] if config["convertion"]["prefix"] else ''
        suffix = config["convertion"]["suffix"] if config["convertion"]["suffix"] else ''
        extention = config["convertion"]["extention"]

        new_file = path + '/' + prefix + base_file_name + suffix + extention

        print(f'{config["context"]["converter_package"]} ' \
              f'{event.src_path} {new_file}')
        
        os.system(f'{config["context"]["converter_package"]} ' \
                  f'{event.src_path} {new_file}')


def loop(config):
    handler = FileSystemEventHandler()
    handler.on_created = on_create

    watcher = Observer()
    for dir in config["context"]["directories"]:
        if not os.path.isdir(dir):
            print(f'WARINING: {dir} is not a directory. Skipping it.', file=sys.stderr)
            continue
        watcher.schedule(handler, dir, recursive=True)

    watcher.start()

    try:
        while 42:
            watcher.join()
    except KeyboardInterrupt:
        watcher.stop()


def main():
    config_path = BASIC_CONFIGURATION

    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    if not os.path.exists(config_path) and config_path != BASIC_CONFIGURATION:
        if not os.path.exists(config_path):
            print(f'Could not find configuration file {config_path}' \
                  f' nor {BASIC_CONFIGURATION}.\nAborting.', file=sys.stderr)
            exit(1)
        else:
            print(f'Could not find configuration file {config_path}. ' \
                  f'Using {BASIC_CONFIGURATION} instead.', file=sys.stderr)
            config_path = BASIC_CONFIGURATION
    elif not os.path.exists(config_path):
        print(f'Could not find configuartion file {BASIC_CONFIGURATION}.\n' \
              f'Aborting.', file=sys.stderr)
        exit(1)
    
    try:
        config_file = open(config_path, 'r')
    except Exception as e:
        print(f'{config_path} could not be opened: {e}', file=sys.stderr)
        exit(1)

    global config

    try:
        config = yaml.safe_load(config_file)
    except yaml.YAMLError as e:
        print(f'Counl not parse configuration file: {e}', file=sys.stderr)
        exit(1)

    print(config)

    config = verify_config(config)

    loop(config)
    
    

if __name__ == '__main__':
    main()