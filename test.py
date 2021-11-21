from git import Repo
from picamera import PiCamera

camera = PiCamera(resolution = (600,600))
camera.rotation = 90

camera.capture("/home/pi/Pictures/rotationTest.jpg")


"""f = open("/home/pi/Julius-Freezer/Images/Pranav/test.txt", "a")
f.write("This is a test")
f.close()

repo =  Repo("/home/pi/Julius-Freezer")
origin = repo.remote("origin")

repo.git.add('--all')
print(repo.index.diff("origin"))
#repo.index.commit("Test")
#origin.push()
"""