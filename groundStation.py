import os


#FOLDERNAME = "Pranav"
FOLDERNAME = "Joseph"
#FOLDERNAME = "Nishita"
#FOLDERNAME = "Raymond"

def main():
    # Confirm connection w/ sat
    # Need to write

    # After confirming connection, start running both processes
    os.system("sudo obexpushd -B -n -o /home/pi/Julius-Freezer/Images/%s &" % FOLDERNAME)
    os.system("python3 gitPush.py &")

if __name__ == "__main__":
    main()


