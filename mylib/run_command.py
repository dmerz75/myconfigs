import subprocess

def run_command(invocation):
    print type(invocation),invocation
    pipe=subprocess.Popen(invocation,stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    if stderr != None:
        print 'stderr >> ',stderr
