import os
import time
import datetime
import subprocess
import termcolor

# TODO
# - Add a function that gets the disk usage of each disk. NOTE: The one I have now only gets the root disk (I think).
# - Add a function that gets the CPU temperature
# - Add a function that gets the system fans speed
# - IDEA: Add custom motd that reads a random message from a file every day

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
                
                if used > total * 0.9:
                    used_colored = termcolor.colored(f"{used:>6.2f}", "red")
                elif used > total * 0.7:
                    used_colored = termcolor.colored(f"{used:>6.2f}", "yellow")
                else:
                    used_colored = termcolor.colored(f"{used:>6.2f}", "green")

                if free < total * 0.1:
                    free_colored = termcolor.colored(f"{free:>6.2f}", "red")
                elif free < total * 0.3:
                    free_colored = termcolor.colored(f"{free:>6.2f}", "yellow")
                else:
                    free_colored = termcolor.colored(f"{free:>6.2f}", "green")

                # Add the info to the ram_info list
                ram_info.append(f"{parts[0]:<5} Total: {total:>6.2f}GB | Used: {used_colored}GB | Free: {free_colored}GB")

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
                    line[2] = int(line[2]) + 1

                    if round(100 - float(line[-1]), 2) > 90:
                        cpu_loads.append(f"CPU {line[2]:<2}: {termcolor.colored(round(100 - float(line[-1]), 2), 'red')}%")
                    elif round(100 - float(line[-1]), 2) > 70:
                        cpu_loads.append(f"CPU {line[2]:<2}: {termcolor.colored(round(100 - float(line[-1]), 2), 'yellow')}%")
                    else:
                        cpu_loads.append(f"CPU {line[2]:<2}: {termcolor.colored(round(100 - float(line[-1]), 2), 'green')}%")

        cpu_loads = " | ".join(cpu_loads)
        
        return cpu_loads + "         " # The extra spaces helps clear any text that is left over from the previous output
    except Exception as e:
        log_error(e)
####################################################################

# Function that gets uptime ########################################
def get_uptime():
    try:
        info = subprocess.check_output(['uptime', '-p'], text=True).strip() # Get the output of uptime -p
        info = info.replace("up ", "Uptime: ")
        return info + "         " # The extra spaces helps clear any text that is left over from the previous output
    except Exception as e:
        log_error(e)
####################################################################

# Function that gets disk usage ####################################
# NOTE: I don't know wether this will give the total of all disks or just the root disk. I'll look into it later.
def get_digk_usage():
    try:
        info = subprocess.check_output(["df", "-h", "--total" ], text=True).splitlines() # Get the output of df -h --total
        status = ""
        # Go trough the output and get the line that starts with "total"
        for line in info:
            if line.startswith("total"):
                
                # Split the line into a list and format the collected info into a readable string
                info = line.split()
                
                if int(info[2][:-1]) > int(info[1][:-1]) * 0.9:
                    info[2] = termcolor.colored(f"{info[2]}", "red")
                    info[3] = termcolor.colored(f"{info[3]}", "red")
                elif int(info[2][:-1]) > int(info[1][:-1]) * 0.7:
                    info[2] = termcolor.colored(f"{info[2]}", "yellow")
                    info[3] = termcolor.colored(f"{info[3]}", "yellow")
                elif int(info[2][:-1]) < int(info[1][:-1]) * 0.7:
                    info[2] = termcolor.colored(f"{info[2]}", "green")
                    info[3] = termcolor.colored(f"{info[3]}", "green")

                info = f"Disk usage - Total: {info[1]}  |  Used: {info[2]}  |  Free: {info[3]}  {status}"

        return info + "         " # The extra spaces helps clear any text that is left over from the previous output
    except Exception as e:
        log_error(e)
####################################################################

# Function that gets network usage ################################
def get_bandwidth(interval=1):
    def get_bytes():
        with open('/proc/net/dev', 'r') as f:
            data = f.readlines()
        stats = {}
        for line in data[2:]:
            parts = line.split()
            interface = parts[0].strip(':')
            stats[interface] = {
                'rx': int(parts[1]),
                'tx': int(parts[9])
            }
        return stats

    stats1 = get_bytes()
    time.sleep(interval)
    stats2 = get_bytes()

    network_usage = {}
    for interface in stats1:
        if interface in stats2:
            rx_rate = (stats2[interface]['rx'] - stats1[interface]['rx']) / interval / 1024
            tx_rate = (stats2[interface]['tx'] - stats1[interface]['tx']) / interval / 1024
            network_usage[interface] = {
                'download_kbps': rx_rate,
                'upload_kbps': tx_rate
            }

    network_info = ""
    for interface, data in network_usage.items():
        network_info += f"{interface}:  ↓ {data['download_kbps']:.2f} Kbps - ↑ {data['upload_kbps']:.2f} Kbps  | "

    return network_info + "         " # The extra spaces helps clear any text that is left over from the previous output
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

            divider = "_" * 130

            uptime = get_uptime()

            # Gget the RAM info
            ram_info = get_ram_info()
            sysinfo_ram = f"{str(ram_info[0])}\n {str(ram_info[1])}"
            
            # Get the CPU info which is already in a formated state.
            cpu_info = get_cpu_load()

            network_info = get_bandwidth()

            # Write the info to the info file
            write_info(f" {get_uptime()}\n{divider}\n\n {sysinfo_ram}\n{divider}\n\n {get_cpu_load()}\n{divider}\n\n {get_digk_usage()}\n{divider}\n\n {get_bandwidth()}\n{divider}\n")

        
            with open(INFO_FILE, "r") as info_file:
                print(info_file.read())

            # Move cursor to the top of the terminal. This makes it look like the info is being updated.
            print("\033[H", end="")

            # Wait 3 seconds before getting the info again. Helps reduce system resource usage.
            time.sleep(1)
    except Exception as e:
        log_error(e)


    write_log("Program ended at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    Main()