from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor

from PIL import ImageGrab, Image
import win32gui

from sklearn.externals import joblib

win_width = 280
win_height = 280
bgcolor = '#000000'


class Application(Frame):
    """一个经典的GUI写法"""

    def __init__(self, master=None):
        """初始化方法"""
        super().__init__(master)  # 调用父类的初始化方法
        self.x = 0
        self.y = 0
        self.fgcolor = 'white'
        self.lastdraw = 0
        self.start_flag = False
        self.master = master
        self.pack()
        self.createWidget()
        self.grid()


    def createWidget(self):
        """创建画图区域"""
        self.drawpad = Canvas(self, width=win_width, height=win_height, bg=bgcolor)
        self.drawpad.pack()
        # 创建按钮
        self.btn_start = Button(self, name='start', text='开始')
        self.btn_start.pack(side='left', padx=3)
        self.btn_pen = Button(self, name='pen', text='画笔')
        self.btn_pen.pack(side='left', padx=3)
        self.btn_line_arrow = Button(self, name='screen_capture', text='预测')
        self.btn_line_arrow.pack(side='left', padx=3)
        self.btn_clear = Button(self, name='clear', text='清屏')
        self.btn_clear.pack(side='left', padx=3)
        self.btn_color = Button(self, name='color', text='颜色')
        self.btn_color.pack(side='left', padx=3)

        self.text = Label(self, text='predict:', fg='red')
        self.text.pack(side="left", padx=3)

        self.v = StringVar()
        self.text = Label(self, textvariable=self.v)
        self.text.pack(side="left", padx=3)

        # 绑定事件
        self.btn_line_arrow.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.btn_pen.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.btn_clear.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.btn_color.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.drawpad.bind('<ButtonRelease-1>', self.stopDraw)  # 左键释放按钮

    def eventManager(self, event):
        name = event.widget.winfo_name()
        print(name)
        self.start_flag = True
        if name == 'screen_capture':
            # 左键拖动
            self.CaptureScreen()
        elif name == 'pen':
            self.drawpad.bind('<B1-Motion>', self.mypen)
        elif name == 'clear':
            self.drawpad.delete('all')
        elif name == 'color':
            c = askcolor(color=self.fgcolor, title='请选择颜色')
            print(c)  # c的值 ((128.5, 255.99609375, 0.0), '#80ff00')
            self.fgcolor = c[1]

    def startDraw(self, event):
        self.drawpad.delete(self.lastdraw)
        if self.start_flag:
            self.start_flag = False
            self.x = event.x
            self.y = event.y

    def stopDraw(self, event):
        self.start_flag = True
        self.lastdraw = 0

    # def myline(self, event):
    #     self.startDraw(event)
    #     self.lastdraw = self.drawpad.create_line(self.x, self.y, event.x, event.y, fill=self.fgcolor)


    def mypen(self, event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.drawpad.create_line(self.x, self.y, event.x, event.y, fill=self.fgcolor, width=20)
        self.x = event.x
        self.y = event.y



    def CaptureScreen(self):
        cv = self.drawpad
        HWND = win32gui.GetFocus()
        rect=win32gui.GetWindowRect(HWND)
        x = rect[0]
        x1=x+cv.winfo_width()
        y = rect[1]
        y1=y+cv.winfo_height()
        im=ImageGrab.grab((x,y,x1,y1))
        im = im.resize((28, 28), Image.ANTIALIAS)
        im.save("second4.png",'png')

        # 模型预测
        im = Image.open('./second4.png')
        model = joblib.load('./model1.pkl')
        im = im.convert('L')
        tv = list(im.getdata())
        pred = model.predict([tv])
        self.v.set(pred[0])



if __name__ == '__main__':
    root = Tk()
    root.title('画图窗口')
    root.geometry('280x350')
    app = Application(master=root)
    root.mainloop()
