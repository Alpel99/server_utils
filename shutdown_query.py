import subprocess
import json
import time

DELAY = 10 # MINUTES

def check_who():
    res_who = subprocess.run(['/usr/bin/who'], capture_output=True)

    r = str(res_who.stdout, 'UTF-8').strip()

    names = [line.split(None, 1)[0] for line in r.splitlines()]
    if len(names) > 0:
        print(f"Someone is using the server: {names}")
        return True
    else:
        return False


def check_factorio(path):
    with open(path, 'r') as file:
        data = json.load(file)
    res = data.get("players")
    if res == None:
        return False
    if len(res) > 0:
        print(f"There are {res} players online in factorio.")
        return True

def check_minecraft(path):
    subprocess.run(["/usr/bin/screen", "-S", "minecraft", "-X", "stuff", '"/list^M"'])
    time.sleep(0.1)
    with open(path, 'r') as file:
        last_line = file.readlines()[-1]
    start_index = last_line.find("are") + len("are")
    end_index = last_line.find("of", start_index)
    if start_index != -1 and end_index != -1:
        resmc = last_line[start_index:end_index].strip()
        print("Extracted value:", resmc)
    else:
        print("Substring not found in the string.")
    if int(resmc) > 0:
        return True
    else:
        return False

def checkAll():
    global funclist
    r = False
    for f in funclist:
        r = r or f()
    return r

if __name__ == "__main__":
    global funclist
    funclist = []
    """
    funclist.append(lambda: check_who())
    funclist.append(lambda: check_factorio("/home/camilo/factorio_cse/factorio/player-data.json"))
    funclist.append(lambda: check_factorio("/home/camilo/factorio_adrian/factorio/player-data.json"))
    funclist.append(lambda: check_minecraft("/home/camilo/minecraft/logs/latest.log"))

    if(not checkAll()):
        time.sleep(DELAY*60)
        if(not checkAll()):
            subprocess.run(["/bin/bash", "/home/camilo/utils/shutdown.sh"])
    """
    
    check_who()
    check_factorio("player-data.json")
    check_minecraft("latest.log")
