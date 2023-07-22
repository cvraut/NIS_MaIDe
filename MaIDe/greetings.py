# file to store the greetings functions and anything to get printed to the console

def startup_message(version, contact):
    msg = "MaIDe v" + version + " by " + contact
    print("="*len(msg)+"\n"+msg+"\n"+"="*len(msg))
    
def welcome_message(user):
    print("Hello " + user + ", welcome to MaIDe!")
    
def check_run_status():
    print("Checking last run status...")