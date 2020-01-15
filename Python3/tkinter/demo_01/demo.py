import webbrowser
from PIL import ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

def gamerun():
    print('run game...')

def init_menu(root, imgGame, imgHelp):
    menubar =Menu(root)
    root.config(menu = menubar)

    #实例化菜单1，创建下拉菜单，调用add_separate创建分割线
    menu1 =Menu(menubar,tearoff = 0)
    menubar.add_cascade(label = "Edit",menu = menu1)
    menu1.add_command(label = "Do Nothing")
    menu1.add_separator()
    menu1.add_command(label = "Quit",command = root.quit)

    menu2 =Menu(menubar,tearoff = 0)
    menubar.add_cascade(label = "More",menu = menu2)
    menu2.add_command(label = "New Job",image = imgGame ,compound= "left",command = lambda:gamerun())

    
    menu2.add_command(label = "Tkinter",image = imgHelp,compound = "left",command =
    lambda:webbrowser.open("http://effbot.org/tkinterbook/tkinter-index.htm"))


def init_userinfo(root):
    frame_user_info = ttk.LabelFrame(root, text='UserInfo:')
    frame_user_info.pack(side=TOP, fill=X)

    # myLabel= Label(frame_user_info, text='UserInfo:', font="Helvetica 10 bold")
    # myLabel["relief"]=tk.SOLID#设置label的样式
    # myLabel["width"]=10
    # myLabel["height"]=5
    # myLabel.pack(side=LEFT)
    # myLabel.grid(row=0, sticky=W)
    Label(frame_user_info, text="Username").grid(row=1, sticky=W)
    Label(frame_user_info, text="Password").grid(row=2, sticky=W)
    username = Entry(frame_user_info).grid(row=1, column=1, sticky=E)
    password = Entry(frame_user_info, show='*').grid(row=2, column=1, sticky=E)
    # Button(frame_user_info, text="Login").grid(row=2, column=1, sticky=E)

def init_radio(root):
    frame_radio = ttk.Labelframe(root, text='Radio Test',padding=20)
    frame_radio.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    books = ['C++', 'Python', 'Linux', 'Java']
    i = 0
    books_radio = []
    for book in books:
        intVar = IntVar()
        books_radio.append(intVar)
        Radiobutton(frame_radio, text=book,value=i,variable=intVar,command=changed).pack(side=LEFT)
        i = i + 1 


def changed():
    print('value changed')

def init_checkbutton(root):
    frame_checkbutton = ttk.Labelframe(root, text='Checkbutton Test',padding=20)
    frame_checkbutton.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    books = ['C++', 'Python', 'Linux', 'Java']
    i = 0
    books_checkbox = []
    for book in books:
        strVar = StringVar()
        books_checkbox.append(strVar)
        cb = ttk.Checkbutton(frame_checkbutton,
            text = book,
            variable = strVar, 
            onvalue = i,
            offvalue = 'None',
            command = changed) 
        cb.pack(anchor=W)
        i += 1

def init_combobox(root):
    frame_combobox = ttk.Labelframe(root, text='Combobox Test',padding=20)
    frame_combobox.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    strVar = StringVar()
    # 创建Combobox组件
    cb = ttk.Combobox(frame_combobox,
        textvariable=strVar, # 绑定到self.strVar变量
        postcommand=changed) # 当用户单击下拉箭头时触发self.choose方法
    cb.pack(side=TOP)
    # 为Combobox配置多个选项
    cb['values'] = ['Python', 'Ruby', 'Kotlin', 'Swift']

def show_it():
    messagebox.showinfo(title='Alert', message="Please try again!")

def init_showinfo(root):
    frame_showinfo = ttk.LabelFrame(root, text='ShowInfoTest:')
    frame_showinfo.pack(side=TOP, fill=X)
    Button(frame_showinfo, text="Click Me", command=show_it).pack(side=LEFT, fill=Y)
    

def init_ui():
    root = Tk()
    # root.geometry('580x680+200+100')
    root.resizable(width = False, height = False) 
    root.title("Test")
    root.iconbitmap('login.ico')
    imgGame = PhotoImage(file='game.png')
    imgHelp = ImageTk.PhotoImage(file="help.png")
    init_menu(root, imgGame, imgHelp)
    init_userinfo(root)
    init_showinfo(root)
    init_radio(root)
    init_checkbutton(root)
    init_combobox(root)
    root.mainloop()

if __name__ == '__main__':
    init_ui()