import subprocess
import time

DELAY = 10 # MINUTES

def check_who():
    res_who = subprocess.run(['/usr/bin/who'], capture_output=True)

    r = str(res_who.stdout, 'UTF-8').strip()

    names = [line.split(None, 1)[0] for line in r.splitlines()]
    if len(names) > 0:
        print(f"The following users are on the server: {names}")
        return True
    else:
        return False


def check_factorio(name):
    path = "/home/camilo/" + name + "/factorio/factorio-console.log"
    subprocess.run(["/usr/bin/screen", "-S", name, "-X", "stuff", "/players\n"])
    time.sleep(0.1)
    with open(path, 'r') as file:
        line_list = list(file)
        line_list.reverse()
        #last_line = file.readlines()[-1]
        r = 0
        for line in line_list:
            print(line)
            if "/players" in line:
                break
            if "(online)" in line:
                r += 1
        if r > 0:
            print(f"There are {r} playrs online in factorio.")
            return True
        else:
            return False

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
        print("Extracted value:", resmc)
    else:
        print("MC substring error")
        return True
    if int(resmc) > 0:
        print(f"There are {resmc} players online in minecraft")
        return True
    else:
        return False

def checkAll():
    global funclist
    r = False
    for f in funclist:
        t = f()
        r = r or t
    return r

if __name__ == "__main__":
    global funclist
    funclist = []

    check_factorio("factorio_cse")
    exit()
        
    funclist.append(lambda: check_who())
    funclist.append(lambda: check_factorio("factorio_cse"))
    funclist.append(lambda: check_factorio("factorio_adrian"))
    funclist.append(lambda: check_minecraft("/home/camilo/minecraft/logs/latest.log"))
    print(checkAll())
"""
    if(not checkAll()):
        time.sleep(DELAY*60)
        if(not checkAll()):
            subprocess.run(["/bin/bash", "/home/camilo/utils/shutdown.sh"])
"""    
    #check_who()
    #check_factorio("/home/camilo/factorio_adrian/factorio/player-data.json")
    #check_minecraft("/home/camilo/minecraft/logs/latest.log")
    #check_factorio("player-data.json")
    #check_minecraft("latest.log")
