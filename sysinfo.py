import os
import time
import datetime
import subprocess


# Global variables
LOG_FILE = ".main.log"
INFO_FILE = ".info.txt"

# Error handling function - Used to write errors to a log file ####
def error_handling(error):
    write_log("Error: " + str(error))
###################################################################

# Function that gets total, used and free RAM & swap memory #######
def get_ram_info():
    try:
        info = subprocess.check_output(['free', '-m']).decode('utf-8').splitlines()

        ram_info = []
        for line in info:
            if line.startswith("Mem:") or line.startswith("Swap:"):
                parts = line.split()
                total = float(parts[1]) / 1024
                used = float(parts[2]) / 1024
                free = total - used
                ram_info.append(f"{parts[0]:<5}    Total: {total:>6.2f}GB   Used: {used:>6.2f}GB   Free: {free:>6.2f}GB")
        
        return ram_info
    except Exception as e:
        error_handling(f"Exception occurred: {str(e)}")
####################################################################

# Log functions - Used to create and write to a log file ##########
def create_log():
    with open(LOG_FILE, "a") as log:
        log.write("Log file created at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

def write_log(input):
    with open(LOG_FILE, "a") as log:
        log.write(input + "\n")
###################################################################

# Info functions - Used to create and write to a info file ########
def write_info(input):
    try:
        with open(INFO_FILE, "w") as info:
            info.write(input)
    except Exception as e:
        error_handling(e)
###################################################################



def Main():
    if not os.path.isfile(LOG_FILE):
        create_log()

    #write_log("Program started at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        while True:
            ram_info = get_ram_info()
            sysinfo_ram = f"{str(ram_info[0])}\n{str(ram_info[1])}"

            write_info(f"{sysinfo_ram}")

            subprocess.run(["clear"])
            subprocess.run(["cat", INFO_FILE])

            time.sleep(.5)
    except Exception as e:
        error_handling(e)


    #write_log("Program ended at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    Main()