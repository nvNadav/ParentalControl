import threading

keyboard_thread=threading.Thread(target=lambda :0,name="keyboard")
keyboard_thread.start()
print (keyboard_thread.name)
