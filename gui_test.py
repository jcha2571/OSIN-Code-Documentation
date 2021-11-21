import os
from guizero import App, Text, TextBox, PushButton, Slider, Drawing, error
from git import Repo
# def calculate():
#     if not height.value.isdigit() or not width.value.isdigit():
#         error("Input error", "You must type in numbers for height and width")
#     # Depth is allowed to be a digit or blank
#     elif not depth.value.isdigit() and depth.value != "":
#         error("Input error", "You must type in a number for depth")
# 
#     # Perform the calculation
#     else:
#         area = int( height.value ) * int( width.value )
#         if depth.value == "":        
#             result.value = str(area) + "cm squared"
#         else:
#             volume = area * int(depth.value)
#             result.value = str(volume) + "cm cubed"
def push_check_vals():
    push_but = PushButton(app, text="Enter")
    push_but.value 
    #if
    
app = App(title="Julius Freezer GUI Colony Area Calculator")
              
def open_images():
    os.system("cd /home/pi/Julius-Freezer/Images/")
    os.system("git pull")
    os.system("ls")

welcome_message = Text(app, text="Welcome to the Julius-Freezer GUI", size = 18, font="Roboto Mono", color="red")
welcome_message1 = Text(app, text="Please input name of the orbit operator data you'd like to see:", size = 8, font="Roboto Mono", color="black")
desired_orbit_personname = TextBox(app)
userinput = PushButton(app, text="Enter")
welcome_message2 = Text(app, text="Welcome %s" % (userinput.value))
drawing = Drawing(app)
open_images()
drawing.graph()
app.display
