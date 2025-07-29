import sys
import json
import subprocess
import os

def configure_utility():
    # Retrieving the directory where .ck-sso-cli/ folder is present

    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Linux or MacOS
        cmd = 'echo $HOME'
    elif sys.platform.startswith('win'):
        # Windows
        cmd = 'echo %USERPROFILE%'

    directory = subprocess.run(cmd, shell=True, capture_output=True)
    directory = directory.stdout.decode('utf-8').strip()

    # Setting the profile
    profile = 'default'
    if len(sys.argv) == 2:
        print('Using default profile')
    elif len(sys.argv) == 4:
        if sys.argv[2] == '--profile':
            profile = sys.argv[3]
            print(f'Using {profile} profile')
        else:
            print(f'Invalid flag {sys.argv[2]}. Acceptable flag is --profile.')
            exit()

    config = {}

    # Reading existing data from ~/.ck-sso-cli/config.json
    try:
        config_file_read = open(os.path.join(directory, '.ck-sso-cli', 'config.json'), 'r')
        config_file_read.close()
    except FileNotFoundError:
        os.makedirs(os.path.join(directory, '.ck-sso-cli'), exist_ok=True)
        with open(os.path.join(directory, '.ck-sso-cli', 'config.json'), 'w') as f:
            f.write("{}")

    with open(os.path.join(directory, '.ck-sso-cli', 'config.json'), 'r') as config_file_read:
        try:
            config = json.load(config_file_read)
        except json.JSONDecodeError:
            pass

    # Writing data to ~/.ck-sso-cli/config.json
    with open(os.path.join(directory, '.ck-sso-cli', 'config.json'), 'w') as config_file_write:
        email_id = input('Enter your Email ID: ')
        sso_start_url = input('Enter the start URL of your SSO:')
        sso_region = input('Enter the region where SSO is provisioned: ')
        sso_account_id = input("Enter the SSO Account ID: ")
        sso_role_name = input("Enter the SSO Assume_Role Name: ")
        destination_role_arn = input("Enter the Role ARN of the destination account which you wish to assume: ")
        region = 'us-east-1'
        output = 'json'
        config[profile] = {}
        config[profile]['sso_start_url'] = sso_start_url
        config[profile]['sso_region'] = sso_region
        config[profile]['sso_account_id'] = sso_account_id
        config[profile]['sso_role_name'] = sso_role_name
        config[profile]['region'] = region
        config[profile]['output'] = output
        config[profile]['destination_role_arn'] = destination_role_arn
        config[profile]['email_id'] = email_id
        json.dump(config, config_file_write)