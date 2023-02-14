# -*- coding: utf-8 -*-
import tkinter.tix
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import MultiListbox as table
from tkinter import filedialog
from tkinter.filedialog import askopenfile

users = ["admin", "admin", "Ostrava", "Porubská 12/123", "79000", "profiles/profilovka.png"]
isLogged = False
data = [
    ["Kapsička Ontario Chicken and Codfish in Broth", "Ontario", "80g", 34, "images/k1.png",
     "Doplňkové krmivo pro kočky s kuřecím masem a treskou ve vývaru. Krmivo z pečlivě vybraných surovin s extraktem "
     "z čaje pro podporu svěžího dechu s obsahem taurinu pro podporu zdravého srdce a zraku obohacené o zeleninu."],
    ["Kapsička Ontario Tuna in Broth", "Ontario", "80g", 34, "images/kapsicka-ontario-tuna-in-broth-80g-default.png",
     ""],
    ["Kapsička Rasco Premium Cat Kitten Turkey in Gravy", "Rasco", "85g", 19,
     "images/kapsicka-rasco-premium-cat-kitten-turkey-in-gravy-85g-default.png", ""],
    ["Kapsička Ontario Tuna in Broth2", "Ontario", "80g", 34, "images/kapsicka-ontario-tuna-in-broth-80g-default.png",
     ""]]
kosik = []
celkem = 0
actualItem = data[0]
mainColor = '#bccaf7'
bottomColor = '#121d40'


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, width=490, height=400, background='white')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, background=mainColor, highlightbackground="black",
                         highlightthickness=2)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def raise_frame(frame):
    frame.tkraise()


# Define a function for switching the frames
def change_to_mainMenu():
    mainMenu.pack(fill='both', expand=1)
    cart.pack_forget()
    loginFrame.pack_forget()
    itemFrame.pack_forget()
    editFrame.pack_forget()
    profileFrame.pack_forget()


def change_to_cart():
    cart.pack(fill='both', expand=1)
    mainMenu.pack_forget()
    loginFrame.pack_forget()
    itemFrame.pack_forget()
    editFrame.pack_forget()
    profileFrame.pack_forget()


def change_to_login():
    loginFrame.pack(fill='both', expand=1)
    mainMenu.pack_forget()
    cart.pack_forget()
    itemFrame.pack_forget()
    editFrame.pack_forget()
    profileFrame.pack_forget()


def change_to_edit():
    editFrame.pack(fill='both', expand=1)
    mainMenu.pack_forget()
    cart.pack_forget()
    itemFrame.pack_forget()
    loginFrame.pack_forget()
    profileFrame.pack_forget()


def change_to_profile():
    profileFrame.pack(fill='both', expand=1)
    mainMenu.pack_forget()
    cart.pack_forget()
    itemFrame.pack_forget()
    loginFrame.pack_forget()
    editFrame.pack_forget()


def checkIfLogged():
    global isLogged
    if isLogged:
        change_to_profile()
    else:
        change_to_login()


class MainPage:
    def __init__(self, root):
        self.win = None
        self.row = IntVar()
        self.rowCart = IntVar()
        self.jmeno = StringVar()
        self.menubar = Menu(root)
        self.menubar.add_command(label="Editace", command=lambda: change_to_edit())
        self.menubar.add_command(label="Profil", command=lambda: checkIfLogged())
        root.config(menu=self.menubar)

        self.eText = StringVar()
        self.Header = Frame(mainMenu, highlightbackground="black", highlightthickness=2)
        self.Header.pack()
        self.listaHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.listaHeader.grid(row=1, column=0, columnspan=11)
        self.listaHeader.configure(background=bottomColor)
        self.Header.configure(background=mainColor)
        self.mainLabel = Label(self.Header, text='Obchod Hope', font='Helvetica 18 bold', background=mainColor)
        self.mainLabel.grid(row=0, column=0, pady=(10, 5), sticky=E)
        Button(self.listaHeader, text='=', background='pink', command=lambda: change_to_mainMenu()).grid(row=1,
                                                                                                         column=0,
                                                                                                         padx=(1, 100),
                                                                                                         ipadx=30,
                                                                                                         sticky=W)
        # photo = PhotoImage(file="images/cart_img1.png")
        Button(self.listaHeader, text='Košík', background='pink', command=lambda: change_to_cart()).grid(row=1,
                                                                                                         column=2,
                                                                                                         padx=(100, 1),
                                                                                                         ipadx=30,
                                                                                                         sticky=E)
        Button(self.listaHeader, text='Přihlásit se', background='pink', command=lambda: change_to_login()).grid(row=1,
                                                                                                                 column=3,
                                                                                                                 ipadx=30,
                                                                                                                 sticky=E)

        # FILTR A VYHLEDÁVÁNÍ
        self.filtrHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.filtrHeader.grid(row=2, column=0, columnspan=20, sticky="WE")
        self.filtrHeader.configure(background=mainColor)
        self.lb_find = Label(self.filtrHeader, font=('Helvetica 10 bold'), background=mainColor,
                             text='Vyhledávání:').grid(row=2, column=0, pady=(10, 5), sticky=W)
        self.find = Entry(self.filtrHeader, width=10, textvariable=self.eText)
        self.find.grid(row=2, column=1, pady=(10, 5), ipadx=30, sticky=E)
        self.findBtn = Button(self.filtrHeader, background='pink', text='Najít', command=self.prevod).grid(row=2,
                                                                                                           column=2,
                                                                                                           pady=(10, 5),
                                                                                                           padx=(10, 0),
                                                                                                           ipadx=30,
                                                                                                           sticky=W)
        self.lb_find = Label(self.filtrHeader, font=('Helvetica 12 bold'), background=mainColor, text='Filtry').grid(
            row=3, column=0, pady=(10, 5), sticky=W)
        self.lb_find = Label(self.filtrHeader, font=('Helvetica 10 bold'), background=mainColor, text='Výrobce:').grid(
            row=4, column=0, pady=(10, 5), sticky=W)
        self.var = IntVar()
        self.var.set(0)
        self.vyrobci = []
        self.vyrobceRB = Radiobutton(self.filtrHeader, font=('Helvetica 10'), background=mainColor, text='Vše',
                                     variable=self.var, value=0).grid(row=4, column=1, pady=(10, 5), ipadx=10, sticky=E)
        for x in data:
            if x[1] not in self.vyrobci:
                self.vyrobci.append(x[1])
        for x in self.vyrobci:
            self.vyrobceRB = Radiobutton(self.filtrHeader, font=('Helvetica 10'), background=mainColor, text=x,
                                         variable=self.var, value=self.vyrobci.index(x) + 1).grid(row=4,
                                                                                                  column=self.vyrobci.index(
                                                                                                      x) + 2,
                                                                                                  pady=(10, 5),
                                                                                                  ipadx=10, sticky=E)

        self.frame = ScrollableFrame(mainMenu)
        self.ca = []
        self.ca_item = []
        self.frame1 = []
        self.img = []
        self.resized_image = []
        self.new_image = []
        for x in data:
            if self.find.get() == '':
                self.frame1.append(Frame(self.frame.scrollable_frame, highlightbackground="black", highlightthickness=2,
                                         background=mainColor, highlightcolor='black'))
                self.frame1[data.index(x)].pack(fill="both", expand=True, ipadx=70, pady=0)
                self.frame1[data.index(x)].configure(background='white')
                self.ca.append(Canvas(self.frame1[data.index(x)], width=50, height=30, background="white"))
                self.ca[data.index(x)].pack(side=LEFT, padx=10)
                self.img.append(Image.open(x[4]))
                self.resized_image.append(self.img[data.index(x)].resize((50, 30), Image.ANTIALIAS))
                self.new_image.append(ImageTk.PhotoImage(self.resized_image[data.index(x)]))
                self.ca_item.append(self.ca[data.index(x)].create_image(25, 15, image=self.new_image[data.index(x)]))
                self.ca[data.index(x)].tag_bind(self.ca_item[data.index(x)], '<Button-1>',
                                                lambda x=x: self.change_to_item(x))
                self.label = Label(self.frame1[data.index(x)], text=x[0], background="white").pack()
                self.label4 = Label(self.frame1[data.index(x)], text=('Cena: ' + str(x[3]) + ' Kč'),
                                    background="white").pack()
                self.btnBuy = Button(self.frame1[data.index(x)], text='Koupit', background='pink',
                                     font='Helvetica 10 bold',
                                     command=lambda x=x: self.addToCart(x))
                self.btnBuy.pack(ipadx=30, pady=(5, 5))

        self.frame.pack()

        # KOSIK
        self.Header = Frame(cart, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.Header.pack(side=TOP)
        self.mainLabel = Label(self.Header, text='Obchod Hope', font=('Helvetica 18 bold'), background=mainColor)
        self.mainLabel.grid(row=0, column=0, pady=(10, 5), sticky=E)
        self.listaHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.listaHeader.grid(row=1, column=0, columnspan=11)
        self.listaHeader.configure(background=bottomColor)
        self.Header.configure(background=mainColor)

        self.btnMenu = Button(self.listaHeader, text='=', background='pink', command=lambda: change_to_mainMenu()).grid(
            row=1, column=0, padx=(1, 100), ipadx=30, sticky='nsew')
        # photo = PhotoImage(file="images/cart_img1.png")
        self.loginBtn = Button(self.listaHeader, text='Přihlásit se', background='pink',
                               command=lambda: change_to_login()).grid(row=1, column=3, ipadx=30, sticky='nsew')
        self.btnCart = Button(self.listaHeader, text='Košík', background='pink', command=lambda: change_to_cart()).grid(
            row=1, column=2, padx=(100, 1), ipadx=30, sticky='nsew')

        self.mainLabel = Label(cart, text='Košík')
        self.mlb = table.MultiListbox(self.Header,
                                      (('Název prduktu', 35), ('Výrobce', 10), ('váha', 6), ('cena', 6), ('kusu', 6)))
        cena = 0
        for i in range(len(kosik)):
            self.mlb.insert(END, (kosik[i][0], kosik[i][1], kosik[i][2], kosik[i][3], kosik[i][4]))
            cena += kosik[i][3] * kosik[i][4]
        self.mlb.grid(row=2, column=0, columnspan=11, sticky="WE")
        self.mlb.subscribe(lambda rowCart: self.setRow(rowCart))
        self.updateFrame = Frame(self.Header, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.updateFrame.grid(row=3, column=0, columnspan=11, sticky="WE")
        self.btn_add = Button(self.updateFrame, background='pink', text='Přidat', command= lambda: self.addToCartRow())
        self.btn_add.grid(row=0, column=0, pady=(5, 5), padx=(30,0), ipadx=30, sticky=W)
        self.btn_delete = Button(self.updateFrame, background='pink', text='Odstranit', command= lambda: self.deleteToCartRow())
        self.btn_delete.grid(row=0, column=1, pady=(5, 5), padx=(210,0), ipadx=30, sticky=E)



        self.sumPriceFrame = Frame(self.Header, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.sumPriceFrame.grid(row=4, column=0, columnspan=11, sticky="WE")
        self.price = Label(self.sumPriceFrame, background=mainColor, font=('Helvetica 10 bold'),
                           text='Celková cena: ' + str(celkem))
        self.price.pack(padx=(300, 1))

        self.infoFrame = Frame(self.Header, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.infoFrame.grid(row=5, column=0, columnspan=11, sticky="WE")
        self.lb_fname = Label(self.infoFrame, background=mainColor, text='Jmeno:').grid(row=1, column=1, pady=(5, 5),
                                                                                        ipadx=30, sticky=W)
        self.lb_fname_entry = Entry(self.infoFrame, width=10).grid(row=1, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.lb_lname = Label(self.infoFrame, background=mainColor, text='Příjmení:').grid(row=2, column=1, pady=(5, 5),
                                                                                           ipadx=30, sticky=W)
        self.lb_lname_entry = Entry(self.infoFrame, width=10).grid(row=2, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.lb_city = Label(self.infoFrame, background=mainColor, text='Město:').grid(row=3, column=1, pady=(15, 0),
                                                                                       ipadx=30, sticky=W)
        self.lb_city_entry = Entry(self.infoFrame, width=10).grid(row=3, column=2, pady=(5, 0), ipadx=40, sticky=W)
        self.lb_street = Label(self.infoFrame, background=mainColor, text='Ulice:').grid(row=4, column=1, pady=(5, 5),
                                                                                         ipadx=30, sticky=W)
        self.lb_street_entry = Entry(self.infoFrame, width=10).grid(row=4, column=2, pady=(5, 5), ipadx=40, sticky=W)

        self.platba = IntVar()
        self.platba.set(0)
        self.lb_cp = Label(self.infoFrame, background=mainColor, text='Č.P.:').grid(row=5, column=1, pady=(5, 5),
                                                                                    ipadx=30, sticky=W)
        self.lb_cp_entry = Entry(self.infoFrame, width=5).grid(row=5, column=2, pady=(5, 5), ipadx=10, sticky=W)
        self.lb_cp = Label(self.infoFrame, background=mainColor, font='Helvetica 10 bold', text='Způsob platby').grid(
            row=6, column=1, pady=(15, 5), ipadx=30, sticky=E)
        self.rb1 = Radiobutton(self.infoFrame, background=mainColor, font='Helvetica 10', text='Karta',
                               variable=self.platba, value=0).grid(row=7, column=1, pady=(0, 5), ipadx=30, sticky=W)
        self.rb2 = Radiobutton(self.infoFrame, background=mainColor, font='Helvetica 10', text='Hotově',
                               variable=self.platba, value=1).grid(row=8, column=1, pady=(5, 0), ipadx=30, sticky=W)
        self.btn_buy = Button(self.infoFrame, background='pink', text='Pokračovat', command=self.zaplaceno())
        self.btn_buy.grid(row=10, column=2, pady=(5, 5), ipadx=30, sticky=E)

        # LOGIN
        self.Header = Frame(loginFrame, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.Header.pack(side=TOP)
        self.mainLabel = Label(self.Header, text='Obchod Hope', font=('Helvetica 18 bold'), background=mainColor)
        self.mainLabel.grid(row=0, column=0, pady=(10, 5), sticky=E)
        self.listaHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.listaHeader.grid(row=1, column=0, columnspan=11)
        self.listaHeader.configure(background=bottomColor)
        self.Header.configure(background=mainColor)

        self.btnMenu = Button(self.listaHeader, text='=', background='pink', command=lambda: change_to_mainMenu()).grid(
            row=1, column=0, padx=(1, 100), ipadx=30, sticky='nsew')
        # photo = PhotoImage(file="images/cart_img1.png")
        self.loginBtn = Button(self.listaHeader, text='Přihlásit se', background='pink',
                               command=lambda: change_to_login()).grid(row=1, column=3, ipadx=30, sticky='nsew')
        self.btnCart = Button(self.listaHeader, text='Košík', background='pink', command=lambda: change_to_cart()).grid(
            row=1, column=2, padx=(100, 1), ipadx=30, sticky='nsew')

        self.infoFrame = Frame(self.Header, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.infoFrame.grid(row=4, column=0, columnspan=11, sticky="WE")
        self.lb_header = Label(self.infoFrame, font=('Helvetica 12 bold'), background=mainColor,
                               text='Přihlášení').grid(row=0, column=1, pady=(10, 5), ipadx=30, sticky=E)
        self.lb_email = Label(self.infoFrame, background=mainColor, text='Email:').grid(row=1, column=1, pady=(10, 5),
                                                                                        ipadx=30, sticky=E)
        self.lb_email_entry = Entry(self.infoFrame, width=10)
        self.lb_email_entry.grid(row=1, column=2, pady=(10, 5), ipadx=90, sticky=W)
        self.lb_password = Label(self.infoFrame, background=mainColor, text='Heslo:').grid(row=2, column=1,
                                                                                           pady=(10, 5), ipadx=30,
                                                                                           sticky=E)
        self.lb_password_entry = Entry(self.infoFrame, show="*", width=10)
        self.lb_password_entry.grid(row=2, column=2, pady=(10, 5), ipadx=90, sticky=W)
        self.btn_login = Button(self.infoFrame, background='pink', text='Přihlásit se', command=lambda: self.loginIn())
        self.btn_login.grid(row=10, column=2, pady=(5, 5), ipadx=30, sticky=E)

        # ITEM FRAME
        self.Header = Frame(itemFrame, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.Header.pack(side=TOP)
        self.mainLabel = Label(self.Header, text='Obchod Hope', font=('Helvetica 18 bold'), background=mainColor)
        self.mainLabel.grid(row=0, column=0, pady=(10, 5), sticky=E)
        self.listaHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.listaHeader.grid(row=1, column=0, columnspan=11)
        self.listaHeader.configure(background=bottomColor)
        self.Header.configure(background=mainColor)

        self.btnMenu = Button(self.listaHeader, text='=', background='pink', command=lambda: change_to_mainMenu()).grid(
            row=1, column=0, padx=(1, 100), ipadx=30, sticky='nsew')
        self.loginBtn = Button(self.listaHeader, text='Přihlásit se', background='pink',
                               command=lambda: change_to_login()).grid(row=1, column=3, ipadx=30, sticky='nsew')
        self.btnCart = Button(self.listaHeader, text='Košík', background='pink', command=lambda: change_to_cart()).grid(
            row=1, column=2, padx=(100, 1), ipadx=30, sticky='nsew')

        self.infoFrame = Frame(self.Header, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.infoFrame.grid(row=2, column=0, columnspan=11, sticky='NSEW')
        self.lb_header = Label(self.infoFrame, font=('Helvetica 12 bold'), background=mainColor,
                               text=actualItem[0]).grid(row=0, column=0, pady=(10, 5), columnspan=2, sticky='we')
        self.ca_itemFrame = Canvas(self.infoFrame, width=200, height=200, background=mainColor, highlightthickness=0)
        self.ca_itemFrame.grid(row=1, column=1, pady=(10, 5), sticky='NESW')
        self.img_itemFrame = (Image.open(actualItem[4]))
        self.resized_image_itemFrame = self.img_itemFrame.resize((150, 150), Image.ANTIALIAS)
        self.new_image_itemFrame = (ImageTk.PhotoImage(self.resized_image_itemFrame))
        self.ca_itemFrame.create_image(250, 100, image=self.new_image_itemFrame)
        self.infoFrame.grid_rowconfigure(1, weight=1)
        self.infoFrame.grid_columnconfigure(1, weight=1)
        self.lb_price = Label(self.infoFrame, font=('Helvetica 12 bold'), background=mainColor,
                              text='Váha: ' + str(actualItem[2])).grid(row=2, column=1, pady=(10, 5), ipadx=30,
                                                                       sticky='we')
        self.lb_vaha = Label(self.infoFrame, font=('Helvetica 12 bold'), background=mainColor,
                             text='Cena: ' + str(actualItem[3]) + ' Kč').grid(row=3, column=1, pady=(10, 5), ipadx=30,
                                                                              sticky='we')
        vcmd = (self.infoFrame.register(self.MoneyValidation), '%S')
        self.lb_kusu = Entry(self.infoFrame, font=('Helvetica 12'), background='white', validate='key', vcmd=vcmd,
                             width=4)
        self.lb_kusu.grid(row=4, column=1, pady=(10, 5), padx=(0, 0), ipadx=5)
        amount = 0
        if self.lb_kusu.get() != '':
            amount = int(self.lb_kusu.get())
        self.btn_koupit = Button(self.infoFrame, text='Koupit', font=('Helvetica 12 bold'), background='pink',
                                 command=lambda: self.addToCart(actualItem, amount))
        self.btn_koupit.grid(row=5, column=1, pady=(10, 5), ipadx=30, padx=(0, 0))
        self.lb_popis_header = Label(self.infoFrame, font=('Helvetica 12 bold'), background=mainColor,
                                     text="Popis:").grid(row=6, column=1, pady=(10, 5), ipadx=30, sticky='we')
        self.lb_popis = Label(self.infoFrame, font=('Helvetica 10'), background=mainColor, text=str(actualItem[5]),
                              wraplength=450).grid(row=7, column=1, pady=(0, 5), ipadx=30)

        # EDITACE
        self.Header = Frame(editFrame, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.Header.pack(side=TOP)
        self.mainLabel = Label(self.Header, text='Obchod Hope', font=('Helvetica 15 bold'), background=mainColor)
        self.mainLabel.grid(row=0, column=0, pady=(10, 5), sticky=E)
        self.listaHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.listaHeader.grid(row=1, column=0, columnspan=11)
        self.helpHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.helpHeader.grid(row=3, column=0, columnspan=11, pady=10)
        self.listaHeader.configure(background=bottomColor)
        self.helpHeader.configure(background='white')
        self.Header.configure(background=mainColor)

        self.btnMenu = Button(self.listaHeader, text='=', background='pink', command=lambda: change_to_mainMenu()).grid(
            row=1, column=0, padx=(1, 100), ipadx=30, sticky='nsew')
        self.loginBtn = Button(self.listaHeader, text='Přihlásit se', background='pink',
                               command=lambda: change_to_login()).grid(row=1, column=3, ipadx=30, sticky='nsew')
        self.btnCart = Button(self.listaHeader, text='Košík', background='pink', command=lambda: change_to_cart()).grid(
            row=1, column=2, padx=(100, 1), ipadx=30, sticky='nsew')

        self.filtrHeader = Frame(self.Header)
        self.filtrHeader.grid(row=2, column=0, columnspan=20, sticky="WE")
        self.filtrHeader.configure(background=mainColor)

        self.lb_find = Label(self.filtrHeader, font=('Helvetica 10 bold'), background=mainColor,
                             text='Vyhledávání:').grid(row=2, column=0, pady=(10, 5), sticky=W)
        self.find = Entry(self.filtrHeader, width=10, textvariable=self.eText)
        self.find.grid(row=2, column=1, pady=(5, 5), ipadx=30, sticky=E)
        self.findBtn = Button(self.filtrHeader, background='pink', text='Najít', command=self.prevod).grid(row=2,
                                                                                                           column=2,
                                                                                                           pady=(10, 5),
                                                                                                           padx=(10, 0),
                                                                                                           ipadx=30,
                                                                                                           sticky=W)
        self.lb_find = Label(self.filtrHeader, font=('Helvetica 12 bold'), background=mainColor, text='Filtry').grid(
            row=3, column=0, pady=(5, 0), sticky=W)
        self.lb_find = Label(self.filtrHeader, font=('Helvetica 10 bold'), background=mainColor, text='Výrobce:').grid(
            row=4, column=0, pady=(10, 5), sticky=W)
        self.var = IntVar()
        self.var.set(0)
        self.vyrobci = []
        self.vyrobceRB = Radiobutton(self.filtrHeader, font=('Helvetica 10'), background=mainColor, text='Vše',
                                     variable=self.var, value=0).grid(row=4, column=1, pady=(5, 5), ipadx=10, sticky=E)
        for x in data:
            if x[1] not in self.vyrobci:
                self.vyrobci.append(x[1])
        for x in self.vyrobci:
            self.vyrobceRB = Radiobutton(self.filtrHeader, font=('Helvetica 10'), background=mainColor, text=x,
                                         variable=self.var, value=self.vyrobci.index(x) + 1).grid(row=4,
                                                                                                  column=self.vyrobci.index(
                                                                                                      x) + 2,
                                                                                                  pady=(5, 5), ipadx=10,
                                                                                                  sticky=E)
        # editFrame.configure(background=mainColor)
        self.mlb2 = table.MultiListbox(self.helpHeader,
                                       (('Název prduktu', 35), ('Výrobce', 10), ('váha', 6), ('cena', 6)))
        for i in range(len(data)):
            self.mlb2.insert(END, (data[i][0], data[i][1], data[i][2], data[i][3]))
        self.mlb2.pack(padx=10, pady=5, fill=BOTH)
        self.mlb2.subscribe(lambda row: self.edit(row))

        self.nb = ttk.Notebook(self.helpHeader)
        self.p1 = Frame(self.nb)
        self.p2 = Frame(self.nb)
        self.p3 = Frame(self.nb)
        self.nb.pack()
        self.p3.pack(side=BOTTOM)
        self.p1.pack(side=BOTTOM)
        self.nb.add(self.p3, text="Info")
        self.nb.add(self.p1, text="Popis")

        # name
        self.lb_name = Label(self.p3, text='Jmeno:')
        self.lb_name_entry = Entry(self.p3, width=10)
        self.lb_name.grid(row=1, column=1, pady=(10, 5), ipadx=30, sticky=E)
        self.lb_name_entry.grid(row=1, column=2, pady=(10, 5), ipadx=90, sticky=W)
        root.columnconfigure(1, weight=10)
        # vyrobce
        self.lb_vyrobce = Label(self.p3, text='Výrobce:')
        self.lb_vyrobce_entry = Entry(self.p3, width=10)
        self.lb_vyrobce.grid(row=3, column=1, pady=(5, 5), ipadx=30, sticky=E)
        self.lb_vyrobce_entry.grid(row=3, column=2, pady=(5, 5), sticky=W)
        # vaha
        self.lb_vaha = Label(self.p3, text='Váha:')
        self.lb_vaha_entry = Entry(self.p3, width=10)
        self.lb_vaha.grid(row=5, column=1, pady=(5, 5), ipadx=30, sticky=E)
        self.lb_vaha_entry.grid(row=5, column=2, pady=(5, 5), sticky=W)
        # cena
        self.lb_cena = Label(self.p3, text='Cena:')
        self.lb_cena_entry = Entry(self.p3, width=10)
        self.lb_cena.grid(row=7, column=1, pady=(5, 5), ipadx=30, sticky=E)
        self.lb_cena_entry.grid(row=7, column=2, pady=(5, 5), sticky=W)
        # fotka
        b1 = Button(self.p3, text='Nahrát fotku', background='pink',
                    width=10, command=lambda: self.upload_file())
        b1.grid(row=8, column=1, padx=(5, 5), pady=(5, 5), sticky='WE')
        # popis
        self.lb_popis = Label(self.p1, text='Popis:')
        self.lb_popis_entry = Text(self.p1, height=5, width=40)
        self.lb_popis.grid(row=8, column=1, pady=(5, 100), ipadx=30, sticky=E)
        self.lb_popis_entry.grid(row=8, column=2, pady=(10, 10), padx=(0, 20), sticky='WE')
        # pridat
        self.buttonFrame = Frame(self.helpHeader)
        self.buttonFrame.pack()
        self.buttonFrame.configure(background='white')
        self.btn_pridat = Button(self.buttonFrame, text='Přidat', background='pink', command=self.new_win_add)
        self.btn_pridat.grid(row=10, column=1, pady=(5, 5), padx=(15, 15), ipadx=30, sticky=E)
        self.btn_update = Button(self.buttonFrame, text='Upravit', background='pink', command=self.new_win_edit)
        self.btn_update.grid(row=10, column=2, pady=(5, 5), padx=(15, 15), ipadx=30, sticky=E)
        self.btn_delete = Button(self.buttonFrame, text='Odstranit', background='pink', command=self.new_win_del)
        self.btn_delete.grid(row=10, column=3, pady=(5, 5), padx=(15, 15), ipadx=30, sticky=E)

        # PROFILE
        self.Header = Frame(profileFrame, background=mainColor, highlightbackground='black', highlightthickness=2)
        self.Header.pack(side=TOP)
        self.mainLabel = Label(self.Header, text='Obchod Hope', font=('Helvetica 15 bold'), background=mainColor)
        self.mainLabel.grid(row=0, column=0, pady=(10, 5), sticky=E)
        self.listaHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.listaHeader.grid(row=1, column=0, columnspan=11)
        self.helpHeader = Frame(self.Header, highlightbackground="black", highlightthickness=2)
        self.helpHeader.grid(row=3, column=0, columnspan=11, pady=50)
        self.listaHeader.configure(background=bottomColor)
        self.helpHeader.configure(background='white')
        self.Header.configure(background=mainColor)

        self.btnMenu = Button(self.listaHeader, text='=', background='pink', command=lambda: change_to_mainMenu()).grid(row=1, column=0, padx=(1, 100), ipadx=30, sticky='nsew')
        self.loginBtn = Button(self.listaHeader, text='Přihlásit se', background='pink', command=lambda: change_to_login()).grid(row=1, column=3, ipadx=30, sticky='nsew')
        self.btnCart = Button(self.listaHeader, text='Košík', background='pink', command=lambda: change_to_cart()).grid( row=1, column=2, padx=(100, 1), ipadx=30, sticky='nsew')
        self.img_profile = Image.open(users[5])
        self.img_resized_profile = self.img_profile.resize((100, 100))  # new width & height
        self.img_profile = ImageTk.PhotoImage(self.img_resized_profile)
        self.b3 = Label(self.helpHeader, image=self.img_profile)  # using Button
        self.b3.grid(row=0, column=0, sticky='nsew')
        Label(self.helpHeader, text='Username: ' + users[0]).grid(row=1, column=0, sticky='nsew')
        Label(self.helpHeader, text='Jméno: ' + users[0]).grid(row=2, column=0, sticky='nsew')
        Label(self.helpHeader, text='Příijmení: ' + users[0]).grid(row=3, column=0, sticky='nsew')

        self.notebook = ttk.Notebook(self.helpHeader)
        self.fr1 = Frame(self.notebook)
        self.fr2 = Frame(self.notebook)
        self.notebook.grid(row=6, column=0, sticky='nsew')
        self.fr1.pack(side=BOTTOM)
        self.notebook.add(self.fr1, text="Adresa")
        Label(self.fr1, text='Město: ' + users[2]).grid(row=0, column=1, columnspan=4, padx=60, sticky='w')
        Label(self.fr1, text='Ulice: ' + users[3]).grid(row=1, column=1, columnspan=4, padx=60, sticky='w')
        Label(self.fr1, text='PSČ: ' + users[4]).grid(row=2, column=1, columnspan=4, padx=60, sticky='w')

        self.fr2.pack(side=BOTTOM)
        self.notebook.add(self.fr2, text="Edit")
        self.login_fname = Label(self.fr2, text='Jmeno:').grid(row=1, column=0, pady=(5, 5),
                                                               ipadx=30, sticky=W)
        self.login_fname_entry = Entry(self.fr2, width=10)
        self.login_fname_entry.insert(END, users[0])
        self.login_fname_entry.grid(row=1, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.login_lname = Label(self.fr2, text='Příjmení:').grid(row=2, column=0, pady=(5, 5), ipadx=30, sticky=W)
        self.login_lname_entry = Entry(self.fr2, width=10)
        self.login_lname_entry.insert(END, users[0])
        self.login_lname_entry.grid(row=2, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.login_city = Label(self.fr2, text='Město:').grid(row=3, column=0, pady=(15, 5), ipadx=30, sticky=W)
        self.login_city_entry = Entry(self.fr2, width=10)
        self.login_city_entry.insert(END, users[2])
        self.login_city_entry.grid(row=3, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.login_street = Label(self.fr2, text='Ulice:').grid(row=4, column=0, pady=(5, 5), ipadx=30, sticky=W)
        self.login_street_entry = Entry(self.fr2, width=10)
        self.login_street_entry.insert(END, users[3])
        self.login_street_entry.grid(row=4, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.lb_cp_entry = Entry(self.fr2, width=5)
        self.lb_cp = Label(self.fr2, text='PSČ').grid(row=5, column=0, pady=(5, 5), ipadx=30, sticky=W)
        self.lb_cp_entry.insert(END, users[4])
        self.lb_cp_entry.grid(row=5, column=2, pady=(5, 5), ipadx=30, sticky=W)
        self.btn_edit_profile = Button(self.fr2, text='Upravit', background='pink', command=self.win_editProfile)
        self.btn_edit_profile.grid(row=10, column=2, pady=(5, 5), padx=(15, 15), ipadx=30, sticky=E)

    def loginIn(self):
        global isLogged
        if users[0] == self.lb_email_entry.get() and users[1] == self.lb_password_entry.get():
            isLogged = True
            change_to_profile()
        else:
            self.win_error()

    def win_editProfile(self):
        self.win = Toplevel()
        self.win.grab_set()
        self.b = Label(self.win, text="Chcete upravit své údaje?")
        self.b.pack()
        self.b_yes = Button(self.win, text="Ano", background='pink', font='Helvetica 10 bold',
                            command=lambda: [self.win.destroy(), self.win.grab_release()],
                            height=1, width=5)
        self.b_yes.pack(side=LEFT, padx=5, pady=10)
        self.b_no = Button(self.win, text="Ne", background='pink', font='Helvetica 10 bold',
                           command=lambda: [self.win.destroy(), self.win.grab_release()], height=1,
                           width=5)
        self.b_no.pack(side=LEFT, padx=5, pady=10)


    def win_error(self):
        self.win = Toplevel()
        self.win.grab_set()
        self.b = Label(self.win, text="Špatně zadané údaje")
        self.b.pack()
        self.b_no = Button(self.win, text="OK", background='pink', font='Helvetica 10 bold',
                           command=lambda: [self.win.destroy(), self.win.grab_release()], height=1,
                           width=5)
        self.b_no.pack(padx=5, pady=10)

    def upload_file(self, event=None):
        global img
        print("snjs")
        f_types = [('Png Files', '*.png')]
        self.acutal_filename = filedialog.askopenfilename(filetypes=f_types)
        img = Image.open(self.acutal_filename)
        img_resized = img.resize((30, 30))  # new width & height
        img = ImageTk.PhotoImage(img_resized)
        self.b2 = Label(self.p3, image=img)  # using Button
        self.b2.grid(row=8, column=2, sticky=W)

    def pridaniZbozi(self, event=None):
        jmeno = self.lb_name_entry.get()
        vyrobce = self.lb_vyrobce_entry.get()
        vaha = self.lb_vaha_entry.get()
        cena = int(self.lb_cena_entry.get())
        popis = self.lb_popis_entry.get('1.0', END)
        data.append([jmeno, vyrobce, vaha, cena, self.acutal_filename, popis])
        i = len(data) - 1
        self.mlb2.insert(END, (data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5]))

    def editaceZbozi(self, event=None):
        jmeno = self.lb_name_entry.get()
        vyrobce = self.lb_vyrobce_entry.get()
        vaha = self.lb_vaha_entry.get()
        cena = int(self.lb_cena_entry.get())
        popis = self.lb_popis_entry.get('1.0', END)
        data[self.row] = [jmeno, vyrobce, vaha, cena, self.acutal_filename, popis]
        self.mlb2.delete(0, END)
        for i in range(len(data)):
            self.mlb2.insert(END, (data[i][0], data[i][1], data[i][2], data[i][3]))

    def odstraneniZbozi(self, event=None):
        del data[self.row]
        self.mlb2.delete(0, END)
        for i in range(len(data)):
            self.mlb2.insert(END, (data[i][0], data[i][1], data[i][2], data[i][3]))

    def new_win_add(self):
        self.win = Toplevel()
        self.win.grab_set()
        self.b = Label(self.win, text="Chcete přidat nový produkt?")
        self.b.pack()
        self.b_yes = Button(self.win, text="Ano", background='pink', font='Helvetica 10 bold',
                            command=lambda: [self.pridaniZbozi(), self.win.destroy(), self.win.grab_release()],
                            height=1, width=5)
        self.b_yes.pack(side=LEFT, padx=5, pady=10)
        self.b_no = Button(self.win, text="Ne", background='pink', font='Helvetica 10 bold',
                           command=lambda: [self.win.destroy(), self.win.grab_release()], height=1,
                           width=5)
        self.b_no.pack(side=LEFT, padx=5, pady=10)

    def new_win_edit(self):
        self.win = Toplevel()
        self.win.grab_set()
        self.b = Label(self.win, text="Chcete upravit produkt?")
        self.b.pack()
        self.b_yes = Button(self.win, text="Ano", background='pink', font='Helvetica 10 bold',
                            command=lambda: [self.editaceZbozi(), self.win.destroy(), self.win.grab_release()],
                            height=1, width=5)
        self.b_yes.pack(side=LEFT, padx=5, pady=10)
        self.b_no = Button(self.win, text="Ne", background='pink', font='Helvetica 10 bold',
                           command=lambda: [self.win.destroy(), self.win.grab_release()], height=1, width=5)
        self.b_no.pack(side=LEFT, padx=5, pady=10)

    def new_win_del(self):
        self.win = Toplevel()
        self.win.grab_set()
        self.b = Label(self.win, text="Chcete odstranit produkt?")
        self.b.pack()
        self.b_yes = Button(self.win, text="Ano", background='pink', font='Helvetica 10 bold',
                            command=lambda: [self.odstraneniZbozi(), self.win.destroy(), self.win.grab_release()],
                            height=1, width=5)
        self.b_yes.pack(side=LEFT, padx=5, pady=10)
        self.b_no = Button(self.win, text="Ne", background='pink', font='Helvetica 10 bold',
                           command=lambda: [self.win.destroy(), self.win.grab_release()], height=1, width=5)
        self.b_no.pack(side=LEFT, padx=5, pady=10)

    def edit(self, row):
        self.row = row
        print(data[row])
        self.jmeno.set(data[row][0])
        self.lb_name_entry.delete(0, END)
        self.lb_vyrobce_entry.delete(0, END)
        self.lb_vaha_entry.delete(0, END)
        self.lb_cena_entry.delete(0, END)
        self.lb_popis_entry.delete('1.0', END)
        self.lb_name_entry.insert(0, data[row][0])
        self.lb_vyrobce_entry.insert(0, data[row][1])
        self.lb_vaha_entry.insert(0, data[row][2])
        self.lb_cena_entry.insert(0, data[row][3])
        self.acutal_filename = data[row][4]
        img = Image.open(self.acutal_filename)
        img_resized = img.resize((30, 30))  # new width & height
        img = ImageTk.PhotoImage(img_resized)
        b2 = Button(self.p3, image=img)  # using Button
        b2.grid(row=8, column=2, sticky=W)
        self.lb_popis_entry.insert(INSERT, data[row][5])

    def change_to_item(self, chosenitem):
        itemFrame.pack_forget()
        itemFrame.pack(fill='both', expand=1)
        global actualItem
        del actualItem
        actualItem = chosenitem
        mainMenu.pack_forget()
        cart.pack_forget()
        loginFrame.pack_forget()

    def MoneyValidation(self, S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        self.infoFrame.bell()
        return False

    def setRow(self, row):
        print("snjs")
        self.rowCart = row

    def deleteToCartRow(self):
        print("help")
        if len(kosik) > 0:
            print("me")
            row = self.rowCart
            kosik.pop(row)
            self.mlb.delete(0, END)
            sizeOfCart = len(kosik) - 1
            celkem = 0
            for sizeOfCart in range(len(kosik)):
                self.mlb.insert(END, (
                    kosik[sizeOfCart][0], kosik[sizeOfCart][1], kosik[sizeOfCart][2], kosik[sizeOfCart][3],
                    kosik[sizeOfCart][4]))
                celkem += kosik[sizeOfCart][3] * kosik[sizeOfCart][4]
            self.price['text'] = 'Celková cena: ' + str(celkem)

    def addToCartRow(self):
        print("help")
        if len(kosik) > 0:
            print("me")
            row = self.rowCart
            kosik[row][4] += 1
            self.mlb.delete(0, END)
            sizeOfCart = len(kosik) - 1
            celkem = 0
            for sizeOfCart in range(len(kosik)):
                self.mlb.insert(END, (
                    kosik[sizeOfCart][0], kosik[sizeOfCart][1], kosik[sizeOfCart][2], kosik[sizeOfCart][3],
                    kosik[sizeOfCart][4]))
                celkem += kosik[sizeOfCart][3] * kosik[sizeOfCart][4]
            self.price['text'] = 'Celková cena: ' + str(celkem)

    def addToCart(self, zbozi, amount=1):
        exist = False
        for z in kosik:
            if z[0] == zbozi[0]:
                exist = True
                ind = kosik.index(z)
        if not exist:
            kosik.append([zbozi[0], zbozi[1], zbozi[2], zbozi[3], int(amount)])
            sizeOfCart = len(kosik) - 1
            self.mlb.insert(END, (
                kosik[sizeOfCart][0], kosik[sizeOfCart][1], kosik[sizeOfCart][2], kosik[sizeOfCart][3],
                kosik[sizeOfCart][4]))
            global celkem
            celkem += kosik[sizeOfCart][3] * kosik[sizeOfCart][4]
            self.price['text'] = 'Celková cena: ' + str(celkem)
        else:
            kosik[ind][4] += amount
            self.mlb.delete(0, END)
            sizeOfCart = len(kosik) - 1
            celkem = 0
            for sizeOfCart in range(len(kosik)):
                self.mlb.insert(END, (
                    kosik[sizeOfCart][0], kosik[sizeOfCart][1], kosik[sizeOfCart][2], kosik[sizeOfCart][3],
                    kosik[sizeOfCart][4]))
                celkem += kosik[sizeOfCart][3] * kosik[sizeOfCart][4]
            self.price['text'] = 'Celková cena: ' + str(celkem)

    def filtr(self):
        filtr = []
        if self.var.get() != 0:
            for x in data:
                if self.vyrobci[self.var.get() - 1] in x[1]:
                    filtr.append(x)
        return filtr

    def zaplaceno(self):
        print(":)")

    def first_helper(self, x):
        return lambda x: self.change_to_item(x)

    def prevod(self, event=None):
        self.frame.pack_forget()

        for x in self.frame1:
            x.pack_forget()
        self.ca = []
        self.frame1 = []
        self.img = []
        self.resized_image = []
        self.new_image = []

        filtrList = self.filtr()
        take = []
        if len(filtrList) != 0:
            for x in filtrList:
                if '' != self.find.get():
                    if self.find.get() in x[0]:
                        take.append(x)
                else:
                    take.append(x)
        else:
            for x in data:
                if '' != self.find.get():
                    if self.find.get() in x[0]:
                        take.append(x)
                else:
                    take.append(x)

        for x in take:
            self.frame1.append(Frame(self.frame.scrollable_frame, highlightbackground="black", highlightthickness=2,
                                     background=mainColor, highlightcolor='black'))
            self.frame1[take.index(x)].pack(fill="both", expand=True, ipadx=70, pady=0)
            self.frame1[take.index(x)].configure(background='white')
            self.ca.append(Canvas(self.frame1[take.index(x)], width=50, height=30, background="white"))
            self.ca[take.index(x)].pack(side=LEFT, padx=10)
            self.img.append(Image.open(x[4]))
            self.resized_image.append(self.img[take.index(x)].resize((50, 30), Image.ANTIALIAS))
            self.new_image.append(ImageTk.PhotoImage(self.resized_image[take.index(x)]))
            self.ca_item.append(self.ca[take.index(x)].create_image(25, 15, image=self.new_image[take.index(x)]))
            self.ca[take.index(x)].tag_bind(self.ca_item[take.index(x)], '<Button-1>',
                                            lambda x=x: self.change_to_item(x))
            Label(self.frame1[take.index(x)], text=x[0], background="white").pack()
            Label(self.frame1[take.index(x)], text=('Cena: ' + str(x[3]) + ' Kč'), background="white").pack()
            self.btnBuy = Button(self.frame1[take.index(x)], text='Koupit', background='pink', font='Helvetica 10 bold',
                                 command=lambda x=x: self.addToCart(x))
            self.btnBuy.pack(ipadx=30, pady=(5, 5))

        self.frame.pack()


root = Tk()
root.configure(background='white', highlightbackground='black', highlightthickness=2)
mainMenu = Frame(root)
mainMenu.configure(background='white', highlightbackground='black', highlightthickness=2)
cart = Frame(root)
cart.configure(background='white', highlightbackground='black', highlightthickness=2)
loginFrame = Frame(root)
itemFrame = Frame(root)
itemFrame.configure(background='white', highlightbackground='black', highlightthickness=2)
editFrame = Frame(root)
editFrame.configure(background='white', highlightbackground='black', highlightthickness=2)
profileFrame = Frame(root)
profileFrame.configure(background='white', highlightbackground='black', highlightthickness=2)

root.wm_title("Hlavní stránka")
app = MainPage(root)
change_to_mainMenu()
root.mainloop()
