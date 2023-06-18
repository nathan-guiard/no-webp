import sys

def print_missing_option(opt: str):
    print(f'CONFIG: {opt} not found on configuration file.' \
              f' This configuration option is mendatory', file=sys.stderr)
    return True

def print_empty_option(opt: str):
    print(f'CONFIG: {opt} cannot be empty.', file=sys.stderr)
    return True

def print_wrong_type_option(opt: str, type: str):
    print(f'CONFIG: {opt} is of wrong type, should be {type}.', file=sys.stderr)
    return True


def verify_config(config):
    pb = False

    if "convertion" in config:
        convertion = config["convertion"]
        if convertion is None:
            pb = print_empty_option('convertion')
        elif "extention" not in convertion or convertion["extention"] is None:
            pb = print_missing_option("convertion.extention")
        elif not isinstance(convertion["extention"], str):
            pb = print_wrong_type_option('convertion.extention', 'string')
        
        if not "suffix" in convertion:
            config["convertion"]["suffix"] = None
        elif not isinstance(convertion["suffix"], str):
            pb = print_wrong_type_option('convertion.suffix', str)
        
        if not "prefix" in convertion:
            config["convertion"]["prefix"] = None
        elif not isinstance(convertion["prefix"], str):
            pb = print_wrong_type_option('convertion.prefix', str)
    else:
        pb = print_missing_option("convertion")

    if "context" in config:
        context = config["context"]

        if context is None:
            pb = print_empty_option('context')
        elif "directories" not in context or context["directories"] is None:
            pb = print_missing_option("context.directories")
        elif not (isinstance(context["directories"], list) and all(isinstance(dir, str) for dir in context["directories"])):
            pb = print_wrong_type_option('context.directories', 'list of strings')

        if context is None:
            pb = print_empty_option('context')
        elif "converter_package" not in context or context["converter_package"] is None:
            pb = print_missing_option("context.converter_package")
        elif not isinstance(context["converter_package"], str):
            pb = print_wrong_type_option('context.converter_package', 'string')
    else:
        pb = print_missing_option("context")
    
    if pb:
        exit(1)
    return config