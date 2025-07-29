import sys 
import subprocess
import json
import boto3
import os
import configparser 

def get_home_directory():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Linux or MacOS
        cmd = 'echo $HOME'
    elif sys.platform.startswith('win'):
        # Windows
        cmd = 'echo %USERPROFILE%'
    else:
        print(f'Unsupported platform: {sys.platform}')
        exit(1)

    directory = subprocess.run(cmd, shell=True, capture_output=True)
    directory = directory.stdout.decode('utf-8').strip()
    return directory

def login_utility():
    directory = get_home_directory()

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
    with open(f'{directory}/.ck-sso-cli/config.json', 'r') as config_file_read:
        try:
            config = json.load(config_file_read)
        except:
            if profile!='default':
                print(f'Profile {profile} not found. To configure the profile, run ck-sso-cli configure --profile {profile}')
            else:
                print('No default profile configured. To configure a default profile, run ck-sso-cli configure')
            exit()
    update_aws_config(config=config,profile=profile,directory=directory)
    get_sso_creds(profile=profile)
    assume_role_using_sts(config=config,profile=profile,directory=directory)



def update_aws_config(config, profile, directory):
    config_path = os.path.join(directory, '.aws', 'config')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    parser = configparser.ConfigParser()
    parser.read(config_path)

    profile_key = f'profile {profile}' if profile != 'default' else profile
    sso_key = f'profile {profile}-sso'

    new_profile_data = {
        'region': config[profile]['region'],
        'output': 'json'
    }

    if parser.has_section(profile_key):
        for k, v in parser[profile_key].items():
            if k not in new_profile_data:
                new_profile_data[k] = v
        parser.remove_section(profile_key)

    new_sso_data = {
        'sso_start_url': config[profile]['sso_start_url'],
        'sso_region': config[profile]['sso_region'],
        'sso_account_id': config[profile]['sso_account_id'],
        'sso_role_name': config[profile]['sso_role_name'],
        'region': config[profile]['region'],
        'output': config[profile]['output']
    }

    if parser.has_section(sso_key):
        parser.remove_section(sso_key)

    parser[profile_key] = new_profile_data
    parser[sso_key] = new_sso_data

    with open(config_path, 'w') as configfile:
        parser.write(configfile)      
def get_sso_creds(profile):
    try:
        boto3.setup_default_session(profile_name=f'{profile}-sso')
        client = boto3.client('sts')
        client.get_caller_identity()
    except:
        subprocess.run(['aws','sso','login','--profile',f'{profile}-sso'])

def assume_role_using_sts(config, profile, directory):
    boto3.setup_default_session(profile_name=f'{profile}-sso')
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=config[profile]['destination_role_arn'],
        RoleSessionName=config[profile]['email_id']
    )

    aki = response['Credentials']['AccessKeyId']
    sak = response['Credentials']['SecretAccessKey']
    st = response['Credentials']['SessionToken']

    credentials_path = os.path.join(directory, '.aws', 'credentials')
    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)

    parser = configparser.ConfigParser()
    parser.read(credentials_path)

    new_creds = {
        'aws_access_key_id': aki,
        'aws_secret_access_key': sak,
        'aws_session_token': st
    }


    if parser.has_section(profile):
        for k, v in parser[profile].items():
            if k not in new_creds:
                new_creds[k] = v
        parser.remove_section(profile)


    parser[profile] = new_creds

    with open(credentials_path, 'w') as credfile:
        parser.write(credfile)

    print("Credentials written in ~/.aws/credentials file and are ready for use.")