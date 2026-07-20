#!/usr/bin/env python3

import subprocess

def get_processes():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    ps_output = result.stdout.splitlines()
    return ps_output

def parse_process(line):
  p = line.split(None, 10)

  return {
     "user": p[0],
     "pid": p[1],
     "cpu": p[2],
     "mem": p[3],
     "command": p[10]
  }
  
def parse_all(data):
   processes = []
   for line in data[1:]:
      processes.append(parse_process(line))

   return processes

def top_cpu(processes, n):
   cpu_sort = sorted(processes, key=lambda x: float(x["cpu"]), reverse=True)
   return cpu_sort[:n]




data = get_processes()
#print(f"Total processes: {len(data)}")
#print(data[0])
#print(data[1])  
#print(parse_process(data[1]))

all_processes = parse_all(data)
print(f"Parsed {len(all_processes)} processes\n")
print(all_processes[0])
print(all_processes[1])

top = top_cpu(all_processes, 5)
for p in top:
   print(f"{p['command'][:30]} CPU: {p['cpu']}%")


    
        

