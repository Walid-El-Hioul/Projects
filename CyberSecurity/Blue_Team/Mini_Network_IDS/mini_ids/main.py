import subprocess
import sys
import os


def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during {script_name} execution: {e}")
        sys.exit(1)


def main():
    # Define the script names
    scripts = ['config_setup.py', 'setup_db.py', 'mini_ids.py']

    # Check if the script files exist
    for script in scripts:
        if not os.path.isfile(script):
            print(f"Required file {script} is missing.")
            sys.exit(1)

    # Execute scripts in order
    run_script('config_setup.py')
    run_script('setup_db.py')
    run_script('mini_ids.py')


if __name__ == "__main__":
    main()
