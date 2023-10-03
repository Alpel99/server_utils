import subprocess
import time

DELAY = 5 # MINUTES

def check_who():
    res_who = subprocess.run(['/usr/bin/who'], capture_output=True)

    r = str(res_who.stdout, 'UTF-8').strip()

    names = [line.split(None, 1)[0] for line in r.splitlines()]
    if len(names) > 0:
        print(f"The following users are on the server: {names}")
        return len(names)
    else:
        return 0


def check_factorio(name):
    path = "/home/camilo/" + name + "/factorio-console.log"
    subprocess.run(["/usr/bin/screen", "-S", name, "-X", "stuff", "/players\n"])
    time.sleep(0.1)
    with open(path, 'r') as file:
        line_list = list(file)
        line_list.reverse()
        #last_line = file.readlines()[-1]
        r = 0
        for line in line_list:
            # print(r, line)
            # Players (3):
            if "Players (" in line:
                break
            if "(online)" in line:
                r += 1
        if r > 0:
            print(f"There are {r} playrs online in {name}.")
            return r
        else:
            return 0

def check_minecraft(path):
    # alternative: get https://mcapi.us/server/status?ip=alpel.ddns.net&port=65432
    subprocess.run(["/usr/bin/screen", "-S", "minecraft", "-X", "stuff", "/list\n"])
    time.sleep(0.1)
    with open(path, 'r') as file:
        last_line = file.readlines()[-1]
    start_index = last_line.find("are") + len("are")
    end_index = last_line.find("of", start_index)
    if start_index != -1 and end_index != -1:
        resmc = last_line[start_index:end_index].strip()
        # print("Extracted value:", resmc)
    else:
        print("MC substring error")
        return False
    if int(resmc) > 0:
        print(f"There are {resmc} players online in minecraft")
        return int(resmc)
    else:
        return 0

def checkAll():
    global funclist
    r = False
    for i,f in enumerate(funclist):
        t = f()
        reslist[i] = t
        r = r or True if t > 0 else r
        # r = r or t
    return r

def shutdown_query():
    if(not checkAll()):
        time.sleep(DELAY*60)
        if(not checkAll()):
            subprocess.run(["/bin/bash", "/home/camilo/utils/shutdown.sh"])
            
funclist = []
funclist.append(lambda: check_who())
funclist.append(lambda: check_factorio("factorio_cse"))
funclist.append(lambda: check_factorio("factorio_adrian"))
funclist.append(lambda: check_minecraft("/home/camilo/minecraft/logs/latest.log"))
reslist = [0]*len(funclist)

if __name__ == "__main__":
    # checkAll()
    # print(reslist)
    shutdown_query()

