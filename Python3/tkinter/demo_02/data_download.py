import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import cx_Oracle
import pyodbc
import configparser
import pandas as pd
from datetime import datetime


class DBInfo(object):
    def __init__(self, host='', port='', user='', pwd='', service=''):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.service = service

    def __str__(self):
        return f"host:{self.host}, port:{self.port}, user:{self.user}, pwd:{self.pwd}, service:{self.service}"


class SqlServerInfo(DBInfo):
    def __init__(self, host='', port='', user='', pwd='', service=''):
        super().__init__(host, port, user, pwd, service)
        self.conn_str = ''

    def connect(self):
        self.conn_str = f"DRIVER={{SQL Server}};SERVER={self.service};UID={self.user};PWD={self.pwd}"
        driver_name = 'SQL Server'
        driver_names = [x for x in pyodbc.drivers() if x.endswith('for SQL Server') or 'SQL Server Native Client' in x]
        if len(driver_names) > 0:
            driver_name = driver_names[0]
            self.conn_str = self.conn_str.replace('SQL Server', driver_name)
        return pyodbc.connect(self.conn_str)


class OracleInfo(DBInfo):
    def __init__(self, host='', port='', user='', pwd='', service=''):
        super().__init__(host, port, user, pwd, service)
        self.conn_str = "{user}/{pwd}@{host}:{port}/{service}"

    def connect(self):
        return cx_Oracle.connect(self.conn_str.format(user=self.user, pwd=self.pwd,
                                                      host=self.host, port=self.port, service=self.service))


class BaseUI(object):
    entry_user = None
    entry_pwd = None
    frame_control = None

    def __init__(self, title='UI'):
        self.root = tk.Tk()
        self.root.title(title)
        self.frame = self.create_new_frame()

    def init_frame(self):
        self.frame = self.create_new_frame()

    def create_new_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, expand=True, side=tk.TOP)
        frame.config(relief=tk.GROOVE, bd=2)
        return frame

    def init_input_field(self, frame=None, text='', val='', row=0, column=0, with_star=False):
        if frame is None:
            frame = self.frame
        tk.Label(frame, text=text).grid(row=row, column=column, sticky=tk.W)
        entry = tk.Entry(frame)
        entry.grid(row=row, column=column + 1)
        if with_star:
            entry.config(show="*")
            entry.insert(tk.END, val)
        return entry

    def init_user_pwd_entry(self, row=0, user_val=''):
        self.init_frame()
        self.entry_user = self.init_input_field(text="Username:", val=user_val, row=row, column=0)
        self.entry_pwd = self.init_input_field(text="Password:", row=row + 1, column=0, with_star=True)

    def init_control_buttons(self, row=0):
        self.frame_control = self.create_new_frame()
        tk.Button(self.frame_control, text='Start', command=self.do_ok).grid(row=row, column=0, sticky=tk.W, pady=4)
        tk.Button(self.frame_control, text='Quit', command=self.frame.quit).grid(row=row, column=1, sticky=tk.W, pady=4)


class DownloadUI(BaseUI):
    oracle_info = None
    sql_server_info = None
    entry_sql = ''
    label_output_file = './output.csv'
    frame_sql_server = None
    entry_service_sql_server = None
    frame_oracle = None
    entry_host_oracle = None
    entry_port_oracle = None
    entry_service_oracle = None

    def __init__(self, action):
        self.action = action
        super().__init__(title='Download Table')
        self.read_config()

        self.db_category_var = tk.IntVar()
        self.db_category_var.set(1)

        self.init_user_pwd_entry()
        self.init_sql_textbox()
        self.init_output_path()
        self.init_db_info_radios()
        self.init_db_info_details()
        self.init_control_buttons()
        tk.mainloop()

    def read_config(self):
        config = configparser.RawConfigParser()
        config.read('./DB.ini')
        self.oracle_info = OracleInfo(host=config['Oracle']['host'], port=config['Oracle']['port'],
                                      service=config['Oracle']['service'])
        self.sql_server_info = SqlServerInfo(service=config['SqlServer']['service'])

    def init_sql_textbox(self):
        self.init_frame()
        tk.Label(self.frame, text='sql:').grid(row=0, column=0, sticky=tk.W)
        self.entry_sql = tk.Text(self.frame, height=4, width=50)
        self.entry_sql.grid(row=1, column=0, stick=tk.W)

    def init_output_path(self):
        self.init_frame()
        tk.Label(self.frame, text='output path:').grid(row=0, column=0, sticky=tk.W)
        self.label_output_file = tk.Label(self.frame, text='./output.csv')
        self.label_output_file.grid(row=0, column=1, sticky=tk.W)
        tk.Button(self.frame, text='...', command=self.select_file).grid(row=0, column=2, sticky=tk.W, pady=4)

    def select_file(self):
        output_path = filedialog.asksaveasfilename(initialdir=".", titl="Select file",
                                                   filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        self.label_output_file['text'] = output_path

    def init_db_info_radios(self):
        self.init_frame()
        tk.Radiobutton(self.frame, text="SqlServer", command=self.change_db_type,
                       variable=self.db_category_var, value=1).grid(row=0, column=0, stick=tk.W)
        tk.Radiobutton(self.frame, text="Oracle", command=self.change_db_type,
                       variable=self.db_category_var, value=2).grid(row=0, column=1, stick=tk.W)

    def init_db_info_details(self):
        self.frame_sql_server = self.create_new_frame()
        self.entry_service_sql_server = self.init_input_field(frame=self.frame_sql_server, text='Service:', row=0,
                                                              column=0)
        self.entry_service_sql_server.insert(tk.END, self.sql_server_info.service)

        self.frame_oracle = self.create_new_frame()
        self.entry_host_oracle = self.init_input_field(frame=self.frame_oracle, text='Host:', row=0, column=0)
        self.entry_host_oracle.insert(tk.END, self.oracle_info.host)

        self.entry_port_oracle = self.init_input_field(frame=self.frame_oracle, text='Port:', row=1, column=0)
        self.entry_port_oracle.insert(tk.END, self.oracle_info.port)

        self.entry_service_oracle = self.init_input_field(frame=self.frame_oracle, text='Service:', row=2, column=0)
        self.entry_service_oracle.insert(tk.END, self.oracle_info.service)

        self.frame_oracle.pack_forget()

    def change_db_type(self):
        if self.db_category_var.get() == 1:
            self.frame_oracle.pack_forget()
            self.frame_sql_server.pack(fill=tk.X, expand=True, side=tk.TOP)
        else:
            self.frame_oracle.pack(fill=tk.X, expand=True, side=tk.TOP)
            self.frame_sql_server.pack_forget()
        self.frame_control.pack_forget()
        self.frame_control.pack(fill=tk.X, expand=True, side=tk.TOP)

    def do_ok(self):
        sql_str = self.entry_sql.get("1.0", "end-1c")

        if not (self.entry_user.get().strip() and self.entry_pwd.get().strip()):
            tkinter.messagebox.showerror(title='Error', message='Please input username and password!')
            return

        if not sql_str.strip():
            tkinter.messagebox.showerror(title='Error', message='Please input sql!')
            return

        self.root.withdraw()
        db_info = self.sql_server_info
        if self.db_category_var.get() == 2:
            db_info = self.oracle_info

        db_info.user = self.entry_user.get()
        db_info.pwd = self.entry_pwd.get()

        self.action(db_info, sql_str, self.label_output_file['text'])
        self.root.deiconify()


class DownloadAction(object):
    @classmethod
    def start_download(cls, db_info, sql_str, output_file_name):
        start_time = datetime.now()
        with db_info.connect() as conn:
            print(f'start query {sql_str}')
            sql_query = pd.read_sql_query(sql_str, conn)
            df = pd.DataFrame(sql_query)
            df.to_csv(output_file_name, index=False)
            end_time = datetime.now()
            print(f'save data to {output_file_name} finished. cost={end_time - start_time}s')


if __name__ == '__main__':
    DownloadUI(DownloadAction().start_download)
