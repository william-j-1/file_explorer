import sys
import os
import shutil
from tkinter import *
import pyperclip
import shutil
currently_stored=[]


# used to create the source , entry box and buttons which are permanently in the programme



file_explorer=Tk()
current_directory= Entry(file_explorer,width=70)
current_directory.grid(row=0,column=0)
current_directory.insert(0,"ㅤ")
foward=Button(file_explorer,text="->",command=lambda:foward())
backward=Button(file_explorer,text="<-",command=lambda:go_back())
sort=Button(file_explorer,text="sort alphabetically",command=lambda:sort_alphabetically())
sort.grid(row=0,column=3)
foward.grid(row=0,column=2)
backward.grid(row=0,column=1)
photo=PhotoImage(file=r"C:\Users\w_jor\Pictures\file_image.png")
paper_piece=PhotoImage(file=r"C:\Users\w_jor\Pictures\paper_file.png")
class Stack(object):
    def __init__(self):
        self.items=[]
    def push(self,item=''):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
        pass
    def clear(self):
        self.items=[]

stack= Stack()

def go_backwards():
    a = get_current_class()
    new_list = globals()[a].list
    for i in new_list:
        globals()[i].button.destroy

def foward():
    open_value=stack.pop()
    globals()[open_value].create_list()
    globals()[open_value].add_to_page()
    globals()[open_value].remove_buttons()
    globals()[open_value].open_file()



def go_back():
    value=current_directory.get()

    first_class=get_current_class()
    previous_class=get_previous_class()

    globals()[first_class].go_back()
    get_rest()
    globals()[previous_class].open_file()
    stack.push(first_class)

def open_sorted(list):

    row_count = 1
    column_count = 0
    for i in list:
        file_or_folder(i, File)
        if column_count < 4:
            globals()[i].button.grid(row=row_count, column=column_count)

            list.append(i)
            column_count = column_count + 1
        else:
            globals()[i].button.grid(row=row_count, column=column_count)
            list.append(i)
            row_count = row_count + 1
            column_count = 0


def get_current_class(): # gets the current class from the directory
    gcc_directory=current_directory.get()
    slash = "\{}".format("")
    position = [pos for pos, char in enumerate(gcc_directory) if char == slash]
    final_slash=position[len(position)-1]
    return gcc_directory[final_slash+1:len(gcc_directory)]

def get_previous_class(): # gets the previous class from the directory
    directory=str(current_directory.get())
    slash="\{}".format("")
    position = [pos for pos, char in enumerate(directory) if char == slash]
    start_index = position[len(position) - 2]
    end_index = position[len(position) - 1]
    return directory[start_index + 1:end_index]

def get_rest(): # used to get the directory up until the final slash
    directory=str(current_directory.get())
    slash = "\{}".format("")
    position = [pos for pos, char in enumerate(directory) if char == slash]
    a=len(position)-1
    end_index = position[a]
    altered=directory[0:end_index]
    current_directory.delete(0, END)
    current_directory.insert(END, altered)
def delete_buttons(): # uses list to delete buttons from current folder open
    global current_list
    for i in current_list:
        globals()[i].button.pack_forget()



def sort_alphabetically():
    to_sort=get_current_class()
    list_to_work=globals()[to_sort].list
    sorted_list=sorted(list_to_work)
    globals()[to_sort].remove_buttons()
    open_sorted(sorted_list)



#def clear_list():
#  return
def delete_specific_button(button_name):
    button_name.destroy()


def file_or_folder(i,type): # used to determine whether the button is a file or a folder
    test_directory=str(current_directory.get())+"\{}".format("") + i
    isDirectory=os.path.isdir(test_directory)
    if isDirectory == True:
        globals()[i]= type(i)
    else:
        globals()[i]=Open(i)

class File:
    def __init__(self,name):
        self.name=name
        self.directory=str(current_directory.get())+"\{}".format("") + self.name   # creates the directory address
        self.button=Button(file_explorer,text=self.name,image=photo,compound="top",command=lambda:[self.create_list,self.add_to_page(),
                                                                        self.open_file(),self.remove_buttons(),
                                                                        self.check_open(),stack.clear()]) # creates the button
        self.button.bind("<Button-3>",lambda event :self.right_click())
        self.list=[]
    def add_to_page(self): # when button is pressed this function changes the directory
        current_directory.delete(0,END)
        current_directory.insert(END,self.directory)
    def create_list(self): # creates list which stores all names of files in the directory. When opened it will be used
        list_index=os.listdir(self.directory)
        for i in list_index:
            self.list.append(i)

    def get_previous_class(self):  # uses the directroy to work out the previous class in case the programme needs it
        directory=self.directory
        slash="\{}".format("")
        position = [pos for pos, char in enumerate(directory) if char == slash]
        start_index = position[len(position) - 2]
        end_index = position[len(position) - 1]
        return directory[start_index + 1:end_index]

    def remove_buttons(self): # used to remove the current buttons on the programme so new buttons can be placed
        name=self.get_previous_class()
        list_of=globals()[name].list
        for i in list_of:
            globals()[i].button.destroy()
    def add_to(self):
        name_for_directory = "sidemenu_" + self.name
        currently_stored.append(name_for_directory)


    def right_click(self):# used to create side menu for every buttons
        name_for_directory="sidemenu_"+self.name
        currently_stored.append(name_for_directory)
        globals()[name_for_directory]=Tk()
        open=Button(globals()[name_for_directory],text="open",command=lambda:[self.create_list,self.add_to_page(),
                                                                        self.open_file(),self.remove_buttons(),
                                                                              ])
        open.grid(row=1,column=0)
        open_new=Button(globals()[name_for_directory],text="open in new window")
        open_new.grid(row=2,column=0)
        path_new=Button(globals()[name_for_directory],text="copy path",command=lambda:self.copy_directory())
        path_new.grid(row=3,column=0)
        delete=Button(globals()[name_for_directory],text="delete",command=lambda:self.delete())
        delete.grid(row=4,column=0)
        globals()[name_for_directory].mainloop()
    # creates menu for each individual class

    def copy_directory(self): # allows to copy file path
        pyperclip.copy(self.directory)
    def delete(self): # allows to delete file
        shutil.rmtree(self.directory)


    def check_open(self):
        for i in range(len(currently_stored)):
            if currently_stored[i]==None:
                break
            else:
                globals()[currently_stored[i]].destroy()
                del currently_stored[i]





    def go_back(self):
        list_to_back=globals()[self.name].list
        for i in list_to_back:
            globals()[i].button.destroy()


    def open_file(self): # used to add buttons to page when button is clicked. Once clicked everything will be added
        file_ope = os.listdir(self.directory)
        row_count = 1
        column_count = 0
        for i in file_ope:
            file_or_folder(i,File)
            if column_count < 4:
                globals()[i].button.grid(row=row_count, column=column_count)

                self.list.append(i)
                column_count = column_count + 1
            else:
                globals()[i].button.grid(row=row_count, column=column_count)
                self.list.append(i)
                row_count = row_count + 1
                column_count = 0



    def clear(self):
        return
    def add(self):
        return
class Open(File): # Class for files not folder
    def __init__(self,name):
        self.name=name
        self.directory=str(current_directory.get())+"\{}".format("") + self.name
        self.button=Button(file_explorer,text=self.name,image=paper_piece,compound="top",command=lambda:self.start_file())
        self.button.bind("<Button-3>",lambda event:self.right_click())
    def start_file(self):
        os.startfile(self.directory)
    def right_click(self):
        name_for_directory = "sidemenu_" + self.name
        currently_stored.append(name_for_directory)
        globals()[name_for_directory] = Tk()
        open = Button(globals()[name_for_directory], text="open", command=lambda: [self.start_file()])
        open.grid(row=1, column=0)

        path_new = Button(globals()[name_for_directory], text="copy path", command=lambda: self.copy_directory())
        path_new.grid(row=3, column=0)
        delete = Button(globals()[name_for_directory], text="delete", command=lambda: self.delete())
        delete.grid(row=4, column=0)
        globals()[name_for_directory].mainloop()





class CDrive(File): # used to access the first class which is the C drive
    def __init__(self,name):
        super().__init__(name)
        self.directory=self.name +"\\{}".format("")
        self.button= Button(file_explorer,text=self.name,command=lambda:[self.create_list(),self.add_to_page(),
                                                        self.open_file_second(),delete_specific_button(self.button),
                                                                         self.check_open()])
       # self.button.bind("<Button-3>", lambda event: self.right_click(), self.add_to())
    def open_file_second(self):
        file_ope = os.listdir(self.directory)
        row_count = 1
        column_count = 0
        for i in file_ope:
            file_or_folder(i,second_open)
            if column_count < 4:
                globals()[i].button.grid(row=row_count, column=column_count)
                column_count = column_count + 1
            else:
                globals()[i].button.grid(row=row_count, column=column_count)
                row_count = row_count + 1
                column_count = 0

    def get_previous_class(self):
        directory = self.directory
        slash = "\{}".format("")
        position = [pos for pos, char in enumerate(directory) if char == slash]
        end_index = position[len(position) - 1]

        return directory[0:end_index]

    def create_list(self):
        list_index = os.listdir(self.directory)
        for i in list_index:
            self.list.append(i)
    def remove_buttons(self):
        return
       # name = self.get_previous_class()
        #for i in globals()[name].list:
         #   globals()[i].button.destroy


class second_open(File): # used for the second opened.
    def __init__(self,name):
        super().__init__(name)
        self.directory=str(current_directory.get())+self.name

    def get_previous_class(self):
        directory = self.directory
        slash = "\{}".format("")
        #position = [pos for pos, char in enumerate(directory) if char == slash]
        #end_index = position[0:]

        return directory[0]

    def remove_buttons(self):
        address = self.directory[0]
        for i in globals()[address].list:
            globals()[i].button.destroy()

    def create_list(self):
        list_index = os.listdir(self.directory)
        for i in list_index:
            self.list.append(i)
    def open_file(self):
        file_ope = os.listdir(self.directory)
        row_count = 1
        column_count = 0
        for i in file_ope:
            file_or_folder(i,File)
            if column_count < 4:
                globals()[i].button.grid(row=row_count, column=column_count)
                self.list.append(i)
                column_count = column_count + 1
            else:
                globals()[i].button.grid(row=row_count, column=column_count)
                self.list.append(i)
                row_count = row_count + 1
                column_count = 0









C=CDrive("C:")

C.button.grid(row=1,column=0)







file_explorer.mainloop()


