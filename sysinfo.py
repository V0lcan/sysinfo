import os, time, datetime

# Global variables
log_file = ".log.txt"
info_file = ".info.txt"

# Error handling function - Used to write errors to a log file ####
def error_handling(error):
    write_log("Error: " + str(error))
###################################################################

# Function that gets total, used and free RAM & swap memory #######
def get_ram_info():
    try:
        info = os.popen('free -m').readlines()
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
        error_handling(e)
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
    try:
        with open(f"{info_file}", "w") as info:
            info.write(input)
    except Exception as e:
        error_handling(e)
###################################################################



def Main():
    if os.path.isfile(f"{log_file}") == False:
        create_log()

    #write_log("Program started at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        while True:
            sysinfo_ram = f"{str(get_ram_info()[0])}\n{str(get_ram_info()[1])}"

            write_info(f"{sysinfo_ram}")

            time.sleep(10)
    except Exception as e:
        error_handling(e)


    #write_log("Program ended at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    Main()