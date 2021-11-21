import time
from git import Repo

def main():

    repo = Repo("/home/pi/Julius-Freezer")
    origin = repo.remote("origin")

    while True:
        try:
            repo.git.add('--all')
        except:
            print("File still being modified")

        changedFiles = repo.index.diff("origin")

        if changedFiles == []:
            pass
        else:
            try:
                repo.index.commit("Updating files")
                origin.push()
            except:
                print("Failed to upload")

        time.sleep(10)

if __name__ == "__main__":
    main()
