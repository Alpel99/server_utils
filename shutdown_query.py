import subprocess
import json

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



if __name__ == "__main__":
    check_who()
    check_factorio("player-data.json")
