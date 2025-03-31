def parse_command(command_string):
    command_parts = command_string.split()
    command_name = command_parts[0]
    command_args = command_parts[1:]

    return command_name, command_args

def validate_command(command_name):
    # List of valid Django management commands
    valid_commands = [
        'makemigrations',
        'migrate',
        'createsuperuser',
        'runserver',
        'shell',
        'startapp',
        'startproject',
        'collectstatic',
        'test',
        'flush',
        'loaddata',
        'dumpdata',
        'check',
        'migrate',
        'createsuperuser',
        'changepassword',
        'dbshell',
        'sendtestemail',
        'makemigrations',
        'migrate',
        'runserver',
        'shell',
        'startapp',
        'startproject',
        'collectstatic',
        'test',
        'flush',
        'loaddata',
        'dumpdata',
        'check',
        'migrate',
        'createsuperuser',
        'changepassword',
        'dbshell',
        'sendtestemail',
    ]

    return command_name in valid_commands

def format_command_response(success, message, logs=None, errors=None):
    response = {
        'success': success,
        'message': message,
    }
    if logs:
        response['logs'] = logs
    if errors:
        response['errors'] = errors

    return response