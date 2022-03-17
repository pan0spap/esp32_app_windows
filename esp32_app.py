from asyncio.subprocess import PIPE
from cgitb import text
from faulthandler import disable
from posixpath import split
from sys import stdout
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from tkinter.ttk import Separator
import serial.tools.list_ports
import os
import subprocess
from tkinter import ttk
import time


available_port = False
set_boot = False
set_par = False
set_modbus = False
filename = ''


def get_ports():
    return list(serial.tools.list_ports.comports())

def select_port(port):
    global available_port
    available_port = True
    
       
    
def load_file():
    global set_boot, set_par, set_modbus, path_boot, path_partition, path_modbus, filename
    filename = filedialog.askopenfilename(filetypes = [("All Files",".*")])
    if len(filename) > 0:
        file = filename.split('/')[-1]
    
        if file == 'bootloader.bin':
            path_boot = filename
            entry_boot.insert(-1, path_boot)
            entry_boot.configure(state=DISABLED)
            set_boot = True
    
        if file == 'partition-table.bin':
            path_partition = filename
            entry_par.insert(-1, path_partition)
            entry_par.configure(state=DISABLED)
            set_par = True

        if file != 'bootloader.bin' and file != 'partition-table.bin':
            path_modbus = filename
            entry_app.insert(-1, path_modbus)
            entry_app.configure(state=DISABLED)
            set_modbus = True
            
    

def chip_info():
    out = os.popen('cmd /c "C:/Users/user/Desktop/esp-idf/export.bat && cd C:/Users/user/Desktop/esp-idf/components/esptool_py/esptool && esptool.py read_mac"').read()
    
    mac = out.split("MAC: ")[1].split("\n")[0]
    chip = out.split("Chip ")[1].split("\n")[0]
    features = out.split("Features: ")[1].split("\n")[0]
    crystal = out.split("Crystal ")[1].split("\n")[0]
    
    
    if not entry_mac.get():
        entry_mac.insert(-1 ,mac)
    else:
        entry_mac.delete(0, 'end')
        entry_mac.insert(-1, mac)
    
    if not entry_chip.get():
        entry_chip.insert(-1 ,chip)
    else:
        entry_chip.delete(0, 'end')
        entry_chip.insert(-1, chip)

    if not entry_features.get():
        entry_features.insert(-1 ,features)
    else:
        entry_features.delete(0, 'end')
        entry_features.insert(-1, features)

    if not entry_crystal.get():
        entry_crystal.insert(-1 ,crystal)
    else:
        entry_crystal.delete(0, 'end')
        entry_crystal.insert(-1, crystal)    



def erase_button(por):
    if available_port == True: 
        tkinter.messagebox.showinfo('Process', 'This may take a while! \n Please wait!')
        out = os.popen('cmd /c "C:/Users/user/Desktop/esp-idf/export.bat && cd C:/Users/user/Desktop/esp-idf/components/esptool_py/esptool && esptool.py -p{} erase_flash"'.format(por)).read()
        output = out.split('Chip erase ')[1].split('\n')[0]
        value = 'Chip erase ' + output
        
        if out.find(value):
            tkinter.messagebox.showinfo('Complete', value)
        else:
            tkinter.messagebox.showerror('Error', 'Something went wrong!')
    else:
        tkinter.messagebox.showerror('Error', 'You must select a port!')


                    
def button_write(com):
    if available_port == True:
        if set_boot == True and set_par == True and set_modbus == True:
            tkinter.messagebox.showinfo('Process', 'This may take a while! \n Please wait!')
            out = os.popen('cmd /c "C:/Users/user/Desktop/esp-idf/export.bat && cd C:/Users/user/Desktop/esp-idf/components/esptool_py/esptool && esptool.py -p{} --chip esp32 -p{}  --baud 2000000 --before default_reset --after no_reset write_flash --flash_size detect 0x1000 {} 0x8000 {} 0x10000 {}"'.format(com, com, path_boot, path_partition, path_modbus)).read()
            o = out.split('Wrote ')[1].split('\n')[0]
            val = 'Wrote ' + o
            if out.find(val):
                tkinter.messagebox.showinfo('Complete', val)
            else:
                tkinter.messagebox.showerror('Error', 'Something went wrong!')    
        else:
            tkinter.messagebox.showerror('Error', 'You must select all bin files!') 
    else:
        tkinter.messagebox.showerror('Error', 'You must select port!')


def chip_clear():
    entry_mac.delete(0, 'end')  
    entry_chip.delete(0, 'end')
    entry_crystal.delete(0, 'end')
    entry_features.delete(0, 'end')


root = Tk()
root.title("Esp-32s-flasher")
root.geometry('900x350')


#menu bar
menubar = Menu(root)
root.config(menu=menubar)

#main tab ports
ports_menuTab =Menu(menubar, tearoff=0)
menubar.add_cascade(label='Ports', menu=ports_menuTab)

#sub tab Port
ports_portSub = Menu(ports_menuTab, tearoff=0)
ports_menuTab.add_cascade(label='Port: ', menu=ports_portSub)

#main tab config
config_menuTab = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Config", menu=config_menuTab)

#sub tab bootloader.bin
bootloader_subTab = Menu(config_menuTab, tearoff=0)
config_menuTab.add_command(label="Load bootloader.bin", command=load_file)

#sub tab partition-table.bin
partable_subTab = Menu(config_menuTab, tearoff=0)
config_menuTab.add_command(label="Load partition-table.bin", command=load_file)

#sub tab app.bin
app_subTab = Menu(config_menuTab, tearoff=0)
config_menuTab.add_command(label="Load app.bin", command=load_file)

#button erase
button_erase = Button(root, text='Erase flash', command=lambda: erase_button(p))
button_erase.place(x=800, y=20)

#button read_chip
button_read_chip = Button(root, text='Read chip', command=chip_info)
button_read_chip.place(x=0, y=150)

#label & entry mac
label_mac = Label(root, text='MAC:')
entry_mac = Entry(root)
label_mac.place(x=10, y=200,)
entry_mac.place(x=145, y=200, width=130)

#label $ entry chip
label_chip = Label(root, text='Chip')
entry_chip = Entry(root)
label_chip.place(x=10, y=230)
entry_chip.place(x=145, y=230, width=210)

#label & entry features
label_features = Label(root, text='Features:')
entry_features = Entry(root)
label_features.place(x=10, y=260)
entry_features.place(x=145, y=260, width=510)

#label & entry crystal
label_crystal = Label(root, text='Crystal')
entry_crystal = Entry(root)
label_crystal.place(x=400, y=230)
entry_crystal.place(x=460, y=230, width=70)

#button write
write_button = Button(root, text='Write', command=lambda: button_write(p))
write_button.place(x=800, y=50)


#label & entry bootloader
label_boot = Label(root, text='Bootloader path:')
label_boot.place(x=10, y=20)
entry_boot = Entry(root)
entry_boot.place(x=145, y=20, width=320)

#label & entry partition-table
label_par = Label(root, text='Partition table path:')
label_par.place(x=10, y=50)
entry_par = Entry(root)
entry_par.place(x=145, y=50, width=320)

#label & entry app
label_app = Label(root, text='App path:')
label_app.place(x=10, y=80)
entry_app = Entry(root)
entry_app.place(x=145, y=80, width=320)

seperator = ttk.Separator(root, orient='horizontal')
seperator.place(relx=0, rely=0.30, relwidth=1, relheight=0)

#button clear chip
clear_chip = Button(root, text='Clear chip', command=chip_clear)
clear_chip.place(x=100, y=150)

#ports
portlist = get_ports()
for i in range(len(portlist)):
    port = str(portlist[i])
    p = port.split(' ')[0]
    ports_portSub.add_command(label=port,command=lambda: select_port(p))


root.mainloop()