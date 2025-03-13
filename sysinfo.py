import os
import time
import datetime
import subprocess


# Global variables
LOG_FILE = ".main.log"
INFO_FILE = ".info.txt"

# Error handling function - Used to write errors to a log file ####
def log_error(error):
    write_log(f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Error: " + str(error))
###################################################################

# Function that gets total, used and free RAM & swap memory #######
def get_ram_info():
    try:
        info = subprocess.check_output(['free', '-m'], text=True).splitlines() # Get the output of free -m

        # For each line in the output, check if it starts with "Mem:" or "Swap:"
        # If it does, split the line into parts and calculate the total, used and free RAM and swap memory.
        ram_info = []
        for line in info:
            if line.startswith("Mem:") or line.startswith("Swap:"):
                parts = line.split()
                total = float(parts[1]) / 1024
                used = float(parts[2]) / 1024
                if used > total:
                    used = total
                free = total - used
                
                # Add the info to the ram_info list
                ram_info.append(f"{parts[0]:<5} Total: {total:>6.2f}GB | Used: {used:>6.2f}GB | Free: {free:>6.2f}GB")

        return ram_info
    except Exception as e:
        log_error(e)
####################################################################

# Function that gets CPU core loads ################################
def get_cpu_load():
    try:
        info = subprocess.check_output(['mpstat', '-P', 'ALL', '1', '1'], text=True).split("\n") # Get the output of mpstat -P ALL 1 1
        
        # For each line in the output, check if it contains "all" or "CPU"
        # If it does, skip the line. If it doesn't, split the line into parts and calculate the CPU load.
        cpu_loads = []
        for line in info:
            if "all" in line or "CPU" in line:
                continue
            if line.strip():
                line = line.split()

                if len(line[2]) < 2:
                    cpu_loads.append(f"CPU {line[2]:<2}: {round(100 - float(line[-1]), 2):>5.2f}%")  # %idle is the last column
        
        cpu_loads = " | ".join(cpu_loads)
        return cpu_loads
    except Exception as e:
        log_error(e)
####################################################################

# Log functions - Used to create and write to a log file ##########
def create_log():
    with open(LOG_FILE, "a") as log:
        log.write("Log file created at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

def write_log(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")
###################################################################

# Info functions - Used to create and write to a info file ########
def write_info(info_content):
    try:
        with open(INFO_FILE, "w") as info:
            info.write(info_content)
    except Exception as e:
        log_error(e)
###################################################################



def Main():
    # Check to see if there is no log file and create one if there isn't.
    if not os.path.isfile(LOG_FILE):
        create_log()

    write_log("Program started at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        subprocess.call(["clear"]) # Clear the terminal
    except Exception as e:
        log_error(e)

    try:
        while True:

            # Gget the RAM info and format it for the info file.
            ram_info = get_ram_info()
            sysinfo_ram = f"{str(ram_info[0])}\n{str(ram_info[1])}"
            
            # Get the CPU info which is already in a formated state.
            cpu_info = get_cpu_load()

            # Write the RAM and CPU info to the info file
            write_info(f"{sysinfo_ram}\n\n{cpu_info}")

        
            with open(INFO_FILE, "r") as info_file:
                print(info_file.read())

            # Move cursor to the top of the terminal. This makes it look like the info is being updated.
            print("\033[H", end="")

            # Wait 3 seconds before getting the info again. Helps reduce system resource usage.
            time.sleep(3)
    except Exception as e:
        log_error(e)


    write_log("Program ended at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    Main()