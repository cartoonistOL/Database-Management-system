#!/usr/bin/env python
# coding: utf-8

# In[1]:
import tkinter
from tkinter import *
import sqlite3, sys


# In[2]:
from tkinter.messagebox import askyesno

import pandas as pd
from pypinyin import lazy_pinyin


class manager(tkinter.Frame):
    """
    root : tkinter.Tk()类
    rows_per_page ：每页显示多少行数据
    """
    def __init__(self, root=None,rows_per_page = 3):
        tkinter.Frame.__init__(self, root)
        self.initial()
        self.rows_per_page = rows_per_page

    def initial(self):
        self.curr_page = 1 # 当前页数
        self.data = []  # 保存书籍数据

        # 可变更文本设置
        self.book_name = StringVar()
        self.rack_no = StringVar()
        self.main = StringVar()
        self.type = StringVar()
        self.author = StringVar()
        self.publications = StringVar()
        self.page_num = StringVar()
        self.page_num.set("1 / 1 页")
        self.query1 = StringVar()
        self.query2 = StringVar()
        self.con = StringVar()

        # 输入框前的提示信息
        self.label1 = Label(root, text="书名:")
        self.label1.place(x=0, y=0)

        self.label2 = Label(root, text="编号:")
        self.label2.place(x=0, y=30)

        self.label3 = Label(root, text="描述:")
        self.label3.place(x=0, y=60)

        self.label4 = Label(root, text="类别:")
        self.label4.place(x=0, y=90)

        self.label5 = Label(root, text="作者:")
        self.label5.place(x=0, y=120)

        self.label6 = Label(root, text="出版社:")
        self.label6.place(x=0, y=150)

        self.label7 = Label(root, text="查询方式:")
        self.label7.place(x=0, y=200)

        self.label8 = Label(root, text="查询内容:")
        self.label8.place(x=130, y=200)

        self.label9 = Label(root, text="类别:")
        self.label9.place(x=140, y=262)

        self.page_lab = Label(root, textvariable=self.page_num)
        self.page_lab.grid(row=15, column=1)


        # 输入框
        self.e1 = Entry(root, textvariable=self.book_name)
        self.e1.place(x=100, y=0)

        self.e2 = Entry(root, textvariable=self.rack_no)
        self.e2.place(x=100, y=30)

        self.e3 = Entry(root, textvariable=self.main)
        self.e3.place(x=100, y=60)

        self.e4 = Entry(root, textvariable=self.type)
        self.e4.place(x=100, y=90)

        self.e5 = Entry(root, textvariable=self.author)
        self.e5.place(x=100, y=120)

        self.e6 = Entry(root, textvariable=self.publications)
        self.e6.place(x=100, y=150)

        self.e7 = Entry(root, textvariable=self.query1 ,width = 7)
        self.e7.place(x=70, y=200)

        self.e8 = Entry(root, textvariable=self.query2,width = 11)
        self.e8.place(x=200, y=200)

        self.e9 = Entry(root, textvariable=self.con, width=12)
        self.e9.place(x=190, y=262)

        self.t1 = Text(root, width=80, height=22)
        self.t1.grid(row=10, column=1,columnspan = 2)

        self.nextBtn = Button(root, text="下一页", command=self.next, width=10)
        self.nextBtn.grid(row=14, column=1)

        self.prevBtn = Button(root, text="上一页", command=self.prev, width=10)
        self.prevBtn.grid(row=13, column=1)

        self.sortBtn = Button(root, text="排序", command=self.sort, width=10)
        self.sortBtn.grid(row=12, column=1)

        self.querybtn = Button(root, text="条件查询", command=self.query_by_type, width=40)
        self.querybtn.place(x=0, y=227)

        self.b1 = Button(root, text="添加书籍", command=self.add_book, width=40)
        self.b1.grid(row=11, column=0)

        self.b2 = Button(root, text="查看所有书籍", command=self.view_book, width=40)
        self.b2.grid(row=12, column=0)

        self.b3 = Button(root, text="删除书籍", command=self.delete_book, width=40)
        self.b3.grid(row=13, column=0)

        self.b4 = Button(root, text="修改书籍信息", command=self.update_book, width=40)
        self.b4.grid(row=14, column=0)

        self.b5 = Button(root, text="按类别统计信息", command=self.summary, width=17)
        self.b5.place(x=0, y=257)

        self.b6 = Button(root, text="退出", command=self.clse, width=40)
        self.b6.grid(row=15, column=0)


    def connection(self):
        conn = None
        """建立sqllite连接"""
        try:
            conn = sqlite3.connect("book.db")
        except:
            print("连接数据库失败")
        return conn

    def check_value(self):
        """检查输入的值是否有遗漏"""
        flag_book = flag_rack = flag_main = flag_type =flag_at = flag_pc = 0
        if not self.book_name.get():
            self.t1.insert(END, "***请填写书名！***\n")
            flag_book = 1
        if not self.rack_no.get():
            self.t1.insert(END, "***请填写编号！***\n")
            flag_rack = 1
        else:
            if not self.rack_no.get().isdecimal():  # 判断字符串是否都是整数
                self.t1.insert(END, "***编号必须为整数！***\n")
                flag_rack = 1
        if not self.main.get():
            self.t1.insert(END, "***请填写描述信息！***\n")
            flag_main = 1
        if not self.type.get():
            self.t1.insert(END, "***请填写书籍类型！***\n")
            flag_type = 1
        if not self.author.get():
            self.t1.insert(END, "***请输入作者名称！***\n")
            flag_at = 1
        if not self.publications.get():
            self.t1.insert(END, "***请输入出版社！***\n")
            flag_pc = 1
        self.t1.insert(END, "==============================\n")
        if flag_book == 1 or flag_rack == 1 or flag_main == 1 or flag_type == 1 or flag_at == 1 or flag_pc == 1:
            return 1
        else:
            return 0


    # In[4]:


    def add_book(self):
        """添加书"""
        ret = self.check_value()  # 先检查输入的值是否有遗漏
        if ret == 0:
            conn = self.connection()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS book_table(NAME TEXT,rack_no INTEGER,main TEXT,type TEXT,author TEXT,publications TEXT)")
            """判断是否已存在"""
            cur.execute("select * from book_table WHERE rack_no=?", (int(self.rack_no.get()),))
            f = cur.fetchall()
            if len(f) != 0:
                self.t1.insert(END, f"编号{f[0][1]}已被占用\n")
                conn.close()
            else:
                cur.execute("insert into book_table values(?,?,?,?,?,?)",
                            (self.book_name.get(), int(self.rack_no.get()), self.main.get(), self.type.get(),self.author.get(), self.publications.get()))
                conn.commit()
                conn.close()
                self.t1.insert(END, "添加成功！\n")


    def view_book(self):
        self.pages = 1
        self.texts = []
        conn = self.connection()
        cur = conn.cursor()
        cur.execute("select * from book_table")
        self.data = cur.fetchall()  # 书籍信息list
        conn.close()
        self.shuchu(self.data)

    def next(self):
        try:
            self.show(1)
        except:
            pass
    def prev(self):
        try:
            self.show(-1)
        except:
            pass

    def show(self,x):
        """翻页功能"""
        self.curr_page += x
        if self.curr_page < 1:
            self.t1.insert(END, "\n当前已是第一页！\n")
            self.curr_page -= x
        elif self.curr_page > self.pages:
            self.t1.insert(END, "\n当前已是最后一页！\n")
            self.curr_page -= x
        else:
            self.t1.delete('1.0', 'end')
            text = self.texts[self.curr_page - 1]
            self.t1.insert(END, "书名           编号          描述            类别         作者         出版社\n")
            self.t1.insert(END, "———————————————————————————————————————\n")
            self.t1.insert(END, "———————————————————————————————————————\n\n")
            for k in text:
                self.t1.insert(END,self.format(k))
            self.page_num.set(f"{self.curr_page} / {self.pages} 页")



    # 添加按书名进行排序，编号第二依据
    def sort(self):
        if len(self.data) != 0:
            self.data.sort(key=lambda char: (lazy_pinyin(char[0])[0][0],char[1]))
            self.pages = 1  # 回到第一页
            self.shuchu(self.data)

    def query_by_type(self):
        a = ["书名", "描述","类别" ,"作者", "出版社"]
        b = ["NAME","main","type","author","publications"]
        dic = dict(zip(a,b))

        if self.query1.get() in dic.keys():
            by = dic[self.query1.get()]
            string = self.query2.get()
            self.query_by(by, string)
        else:
            self.t1.insert(END, "**没有此属性！" + "\n")


    def query_by(self, by, string):
        self.pages = 1
        self.texts = []
        conn = self.connection()
        cur = conn.cursor()
        q = f"select * from book_table where {by} = '{string}'"     # 这里一定要用单引号括起来
        cur.execute(q)
        data = cur.fetchall()  # 书籍信息list
        conn.close()
        self.shuchu(data)

    def format(self, strlist):
        """格式化list，返回字符串"""
        new = []
        for i in range(len(strlist)):
            if i == 0:
                new.append("《{:8}》".format(strlist[i][:8]))  # 书名号
            elif i == 1:
                new.append("{:4}".format(str(strlist[i])[:4]))  #书号短一点
            elif i == 2:
                new.append("{:15}".format(strlist[i][:15]))  #描述长一点
            else:
                new.append("{:8}".format(strlist[i][:8]))
        string = " | ".join(new) + "\n"
        return string

    def shuchu(self,data):
        """格式化输出"""
        self.texts = []
        if len(data) > self.rows_per_page:
            self.pages = (len(data) - 1) // self.rows_per_page + 1  # 计算页数
        for i in range(self.pages):
            self.texts.append(data[i * self.rows_per_page:i * self.rows_per_page + self.rows_per_page])  # 分页存储书籍信息
        first_page = self.texts[0]
        if len(data) == 0:
            self.t1.insert(END, "无结果！" + "\n")
        else:
            self.t1.delete('1.0', 'end')  # 清空内容
            self.t1.insert(END, "书名           编号          描述            类别         作者         出版社\n")
            self.t1.insert(END, "———————————————————————————————————————\n")
            self.t1.insert(END, "———————————————————————————————————————\n\n")
            for k in first_page:
                self.t1.insert(END, self.format(k))
                self.page_num.set(f"{self.curr_page} / {self.pages} 页")
            self.t1.insert(END, "\n===========================================\n")

    def summary(self):
        self.pages = 1
        self.texts = []
        ty = self.con.get()
        conn = self.connection()
        cur = conn.cursor()
        q = f"select * from book_table where type = '{ty}'"
        cur.execute(q)
        data = cur.fetchall()  # 书籍信息list
        conn.close()
        if len(data) != 0:

            # 输出书的信息
            self.shuchu(data)
            data = pd.DataFrame(data)
            describe = []
            for i in range(len(data.columns)):
                describe.append(list(data[i].describe()))    # 对每列进行统计
            most_zuozhe = [describe[4][2], describe[4][3]] # 出现次数最多的作者和次数

            zuozhe = f"{ty}类型出现次数最多的作者为“{most_zuozhe[0]}”，出现了“{most_zuozhe[1]}”次\n"
            most_chuban = [describe[5][2],describe[5][3]]
            chuban = f"最多的出版社为“{most_chuban[0]}”，出现了“{most_chuban[1]}”次\n"
            booksnum = f"{ty}类型共有{len(data)}本书\n"

            self.t1.insert(END, booksnum)
            self.t1.insert(END, zuozhe)
            self.t1.insert(END, chuban)
        else:
            self.t1.insert(END, "无结果！" + "\n")




    def delete_book(self):
        """删除书"""
        if self.rack_no.get():
            if not self.rack_no.get().isdecimal():
                self.t1.insert(END, "***编号必须为整数！***\n")
            else:
                # 确认是否删除
                t = askyesno(title='confirmation',
                    message="请确认是否删除！")
                if t:
                    conn = self.connection()
                    cur = conn.cursor()
                    cur.execute("select * from book_table WHERE rack_no=?", (int(self.rack_no.get()),))
                    f = cur.fetchall()
                    if len(f) == 0:
                        conn.close()
                        self.t1.insert(END, f"不存在{self.rack_no.get()}号书籍！！\n")
                    else:
                        cur.execute("DELETE FROM book_table WHERE rack_no=?", (int(self.rack_no.get()),))
                        conn.commit()
                        conn.close()
                        self.t1.insert(END, f"删除《{f[0][0]}》成功！！\n")
        else:
            self.t1.insert(END, "请输入书的编号来删除书！\n")


    def update_book(self):
        """修改书籍信息"""
        ret = self.check_value()
        if ret == 0:
            t = askyesno(title='confirmation',
                         message="请确认是否修改！")
            if t:
                #TODO
                # 确认是否更新
                conn = self.connection()
                cur = conn.cursor()
                cur.execute("UPDATE book_table SET NAME=?,rack_no=?,main=?,type=?,author=?,publications=? where rack_no=?", (
                self.book_name.get(), int(self.rack_no.get()), self.main.get(), self.type.get(), self.author.get(),self.publications.get(), int(self.rack_no.get())))
                conn.commit()
                conn.close()
                self.t1.insert(END, "成功更新！\n")


    def clse(self):
        t = askyesno(title='confirmation',
                     message="确认退出？")
        if t:
            root.destroy()



if __name__ == "__main__":
    root = Tk()
    root.title("Book Management System")
    app = manager(root,rows_per_page = 3)
    app.mainloop()





