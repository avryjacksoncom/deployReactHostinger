# deployReactHostinger
  - I had an issue with updating my portfolio website automatically. Hostinger's platform to host domains had an deploy feature or auto deploy feature that did not work 
    for me becuase I was using react. It said it needed like console.something, which was php related.
    
- Key things:
- Summary: It connects your terminal and and with the hosting terminal dir. via SSH
-  Only runs with pw. Will make one with ssh keys.
- Works for updating react projects that have a build folder. (or customize how you wish)
- Don't know if it works with other framewroks, hosting sites and or tech stacks. Only works for front end react with Hostinger.
- So this program runs npm install and git commands, (if don't need them feel free to comment some subproccess)
- runs npm run build, grabs those files, and uses paramiko (SSH library), connects to the hostinger and uploads all the files
  in the Build folder to hosingers dir public HTML.
  
- You Have to set env varialbles for your path. For example below.


# Paths to directorys
pathToEnv = os.path.expanduser("~/.find_env")  # Automatically find your env file.
load_dotenv(pathToEnv)

path_to_website_dir = os.getenv("PATHTOMAIN")
path_to_build_dir = os.getenv("PATHTOBUILD")
path_to_hostinger_public_dir = os.getenv("PATHTOHOSTINGERPUBLIC")
path_to_git_dir = os.getenv("GITDIRECTORY")

- If you dont know how to do that ill give a little tutorial on how. I can make a feature later so you can just make them automatically. - Can edit out some of the listing commands if you want. I had them there to see if commands were working code works or not. 
