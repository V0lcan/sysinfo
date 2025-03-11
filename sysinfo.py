import os
import time
import datetime
import subprocess


# Global variables
LOG_FILE = ".main.log"
INFO_FILE = ".info.txt"

# Error handling function - Used to write errors to a log file ####
def log_error(error):
    write_log("Error: " + str(error))
###################################################################

# Function that gets total, used and free RAM & swap memory #######
def get_ram_info():
    try:
        info = subprocess.check_output(['free', '-m'], text=True).splitlines()

        ram_info = []
        for line in info:
            if line.startswith("Mem:") or line.startswith("Swap:"):
                parts = line.split()
                total = float(parts[1]) / 1024
                used = float(parts[2]) / 1024
                if used > total:
                    used = total
                free = total - used

                ram_info.append(f"{parts[0]:<5} Total: {total:.2f}GB Used: {used:.2f}GB Free: {free:.2f}GB")

        return ram_info
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
    if not os.path.isfile(LOG_FILE):
        create_log()

    #write_log("Program started at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        subprocess.call(["clear"])
    except Exception as e:
        log_error(e)

    try:
        while True:
            ram_info = get_ram_info()
            sysinfo_ram = f"{str(ram_info[0])}\n{str(ram_info[1])}"

            write_info(f"{sysinfo_ram}")

            with open(INFO_FILE, "r") as info_file:
                print(info_file.read())

            # Move cursor to the top of the terminal
            print("\033[H", end="")

            time.sleep(3)
    except Exception as e:
        log_error(e)


    #write_log("Program ended at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    Main()