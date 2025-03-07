import os, time, datetime

"""
This is a script that collects and writes system information to a file.
I use it to monitor the resource use on my Dell Poweredge R710.

!- NOTE -!
I have not yet tested it on anything other than my laptop so at the time of writing
I am not sure if it will work on other systems.
"""

# Global variables
log_file = ".log.txt"
info_file = ".info.txt"

# Function that gets total, used and free RAM & swap memory #######
def get_ram_info():
    info = os.popen('free -m').readlines()
    ram_info = []
    for line in info:
        if line.startswith("Mem:") or line.startswith("Swap:"):
            parts = line.split()
            total = float(parts[1]) / 1024
            used = float(parts[2]) / 1024
            free = total - used
            ram_info.append(f"{parts[0]} - Total: {total:.2f}GB   Used: {used:.2f}GB   Free: {free:.2f}GB")
    
    return ram_info
####################################################################

# Log functions - Used to create and write to a log file ##########
def create_log():
    with open(f"{log_file}", "a") as log:
        log.write("Log file created at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

def write_log(input):
    with open(f"{log_file}", "a") as log:
        log.write(input + "\n")
###################################################################

# Info functions - Used to create and write to a info file ########
def write_info(input):
    with open(f"{info_file}", "w") as info:
        info.write(input)
###################################################################




def Main():
    if os.path.isfile(f"{log_file}") == False:
        create_log()

    #write_log("Program started at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    while True:
        sysinfo_ram = f"{str(get_ram_info()[0])}\n{str(get_ram_info()[1])}"

        write_info(f"{sysinfo_ram}")

        time.sleep(10)

    #write_log("Program ended at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    Main()