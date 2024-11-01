import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

#setup ports
ardiPort = 'COM3'
baudrate =  9600
arduino = None #variable for the serial connection

#connect to arduino and send limit to the temp sensor
def ConnectToThing():
    global arduino
    try:
        arduino = serial.Serial(ardiPort, baudrate)
        time.sleep(2) #wait for the thing to connect
        lbConnection.config(text="Status: Connected", fg="green")
        messagebox.showinfo("Connection", "Connection Stablished")
        ReadTheThing() #starts reading data at a different tread
    except serial.SerialException:
        messagebox.showerror("Error", "Either I made an oopsie or you have to check your ports")

#Function for disconnect from arduino
def DisconnectThing():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConnection.config(text="Status: Not connected", fg="red")
        messagebox.showinfo("Connection", "Connection Terminated")
    else:
        messagebox.showwarning("Warning", "There's no connection, what are you doing?")

#send temp limit to arduino
def SendLimitToThing():
    global arduino
    if arduino and arduino.is_open:
        try:
            limit = tbTempLim.get()
            if limit.isdigit(): #Verify if the limit is a valid number
                arduino.write(f"{limit}\n".encode()) #send limit to arduino
                arduino.flush()
                messagebox.showinfo("Sent", f"Temperature limit ({limit} degrees) has been sent")
            else:
                messagebox.showerror("Error", "Enter a number for the limit??")
        except Exception as ex:
            messagebox.showerror("Error", f"I made an oopsie and failed to send the limit {ex}")
    else:
        messagebox.showwarning("Warning", "There's no connection, what are you doing?")

#Function to read data from arduino
def readFromArduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip() #Reads temp from the arduino
            if "Temp" in data:
                print(data)
                tempValue = data.split(":")[1].strip()
                lbTemp.config(text=f"{tempValue} degrees Celcius")
                time.sleep(1)
        except Exception as ex:
            print(f"Something happend. Couldn't read data: {ex}")
            break

#function for start reading on a separate thread
def ReadTheThing():
    thread = threading.Thread(target=readFromArduino)
    thread.daemon = True
    thread.start()

#Configuring GUI

window = tk.Tk()
window.title("Temp monitoring interface")
window.geometry("400x300")

#title tag
lbTitleTemp = tk.Label(window, text="Current temperature", font=("Arial", 12))
lbTitleTemp.pack(pady=10)

#Show temp tag
lbTemp = tk.Label(window, text="-- degrees C", font=("Arial", 24))
lbTemp.pack()

#tag for connection state 
lbConnection = tk.Label(window, text="Status: Not Connected", fg="red", font=("Arial", 12))
lbConnection.pack(pady=5)

#For entering temp limit
lbTempLimit = tk.Label(window, text="Temperature limit")
lbTempLimit.pack(pady=5)
tbTempLim = tk.Entry(window, width=10)
tbTempLim.pack(pady=5)

#Send temp button
btnSend = tk.Button(window, text="Send limit", command=SendLimitToThing, font=("Arial", 12))
btnSend.pack()

#connect button
btnConnect = tk.Button(window, text="Connect", command=ConnectToThing, font=("Arial", 12))
btnConnect.pack(pady=5)

#disconect butt
btnDisconnect = tk.Button(window, text="Disconnect", command=DisconnectThing, font=("Arial", 12))
btnDisconnect.pack(pady=5)

#alway rember to execute interface
window.mainloop()
