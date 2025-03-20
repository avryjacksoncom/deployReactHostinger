
"""
     - I had an issue with updating my portfolio website automatically.
     Hostinger's platform to host domains had an deploy feature or
     auto deploy feature that did not work for me becuase I was
     using react. It said it needed like console.something, which
     was php related.
    
     Key things:
     - Summary: It connects your terminal and and with the
       hosting terminal dir. via SSH

     - Only runs with pw. Will make one with ssh keys.
     - Works for updating react projects that have a build folder.
     - Don't know if it works with other framewroks, hosting sites
       and or tech stacks. Only works for front end react with
       Hostinger.
    
     - So this program runs npm install, (if you need it don't have
     to do it everytime)runs npm run build, grabs those files, and 
     uses paramiko (SSH library), connects to the hostinger and uploads
      all the files in the Build folder to hosingers dir public HTML.

     - You Have to like set env varialbles for your path. For example below.

     - If you dont know how to do that ill give a little tutorial on how.
       and maybe i can make an add on so you can just make them automatically.

     - Can edit out some of the listing commands if you want. I had them 
     there to see if commands were working code works or not.

"""

import subprocess
import os
from dotenv import load_dotenv
import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError
import time
pathToEnv = os.path.expanduser("~/.find_env")  # Automatically find your env file.
load_dotenv(pathToEnv)

# Paths to directorys
path_to_website_dir = os.getenv("PATHTOMAIN")
path_to_build_dir = os.getenv("PATHTOBUILD")
path_to_hostinger_public_dir = os.getenv("PATHTOHOSTINGERPUBLIC")
path_to_git_dir = os.getenv("GITDIRECTORY")

#Your env variables, usin gsystme callx with os.getenv to grab your file.env
ssh_username_env = os.getenv("SSH_USERNAME")
ssh_password_env = os.getenv("SSH_PASSWORD")
ssh_port_env = os.getenv("SSH_PORT")
ssh_ip_env = os.getenv("SSH_IP")
command_env = os.getenv("COMMAND_FOR_HOSTINGER")
# example of command cd /home/username123123912499123/domains/domain.com/public_html && ls && rm -rf * && ls

""" 
    This section of code makes it so you don't have to type in git commands
    to push a change. Automatically done.
"""
subprocess.run(["git", "add","."], cwd=path_to_git_dir, check=True)
commit_message = 'routine website commit'
command = ["git", "commit", "-m", commit_message]
subprocess.run(command, cwd=path_to_website_dir, check=True)
subprocess.run(["git", "push", "origin", "main"], cwd=path_to_git_dir, check=True)


""" 
    Start of paramiko client code.
"""

client = paramiko.SSHClient()
# Automatically add the host key
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

"""
    Connects to your terminal, and domain's ssh to delete the files 
     within public_html with a command.
"""
try:
   
    client.connect(ssh_ip_env,port=ssh_port_env, username=ssh_username_env, password=ssh_password_env)

    # Run the command
    stdin, stdout, stderr = client.exec_command(command_env)

    # Get the output
    output = stdout.read().decode()
    print(output)

    # Get any error output
    error = stderr.read().decode()
    if error:
        print(f"Error: {error}")

except SSHException as e:
    print(f"SSH error: {e}")
except NoValidConnectionsError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()


"""
    This section of code refresees your website build folder.
"""
subprocess.run(["npm", "install"], cwd=path_to_website_dir, check=True)
subprocess.run(["ls"], cwd=path_to_website_dir, check=True)
subprocess.run(["npm", "run", "build"], cwd=path_to_website_dir, check=True)


""" 
    Start of paramiko client code.
"""
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


""" 
    Uploads the local build files to hostinger's build folder.
"""
try:

    client.connect(ssh_ip_env,port=ssh_port_env, username=ssh_username_env, password=ssh_password_env)

    # Create SFTP client from the SSH connection
    sftp = client.open_sftp()

    # Define local and remote directories
    local_directory = path_to_build_dir
    remote_directory = path_to_hostinger_public_dir

    # Function to upload all files in a directory (including subdirectories)
    # Ususally a build folder has a static folder.
    def upload_directory(local_dir, remote_dir):
        for root, dirs, files in os.walk(local_dir):

            # Create the corresponding remote directory
            remote_path = os.path.join(remote_dir, os.path.relpath(root, local_dir))
            try:
                sftp.mkdir(remote_path)
            except IOError:
                pass  # Ignore if the directory already exists

            # Upload all files in the current directory
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_path, file)
                sftp.put(local_file, remote_file)
                print(f"Uploaded {local_file} to {remote_file}")

    # Upload the entire directory
    upload_directory(local_directory, remote_directory)
    print("Upload completed successfully.")

except paramiko.AuthenticationException:
    print("Authentication failed, please check your username and/or password.")

except paramiko.SSHException as e:
    print(f"SSH connection error: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    sftp.close()
    client.close()