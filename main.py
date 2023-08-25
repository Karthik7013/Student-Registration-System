from tkinter import *
from tkinter import messagebox,ttk,filedialog
from datetime import datetime,timezone
import sqlite3
from PIL import ImageTk,Image


class StudentRegistrationApp():


	def update(self):
		''' update the existing details of the student fields except id and date of registration'''
		self.update_btn.config(state = 'disabled')
		filed = [self._name,
		self.dob,
		self.radio,
		self.combo,
		self.ema,
		self._contact,
		self.f_name,
		self.m_name,
		self.occ,
		self.add]
		cloumns = ["name","dob","gender","course","email","contact","fathername","mothername","occupation","address"]
		for i in range(10):
			if i == 2:
				if self.radio.get() == 1:
					self.gender = 'Male'
					self.mycursor.execute(f'UPDATE data SET gender = (?) WHERE ID = {self.registration.get()}',(self.gender,))
					continue
				else:
					self.gender = 'Female'
					self.mycursor.execute(f'UPDATE data SET gender = (?) WHERE ID = {self.registration.get()}',(self.gender,))
					continue
			sql = f'UPDATE data SET {cloumns[i]} = (?) WHERE ID = {self.registration.get()}'
			value = filed[i].get()
			self.mycursor.execute(sql,(value,))
		if self.profile == None:
			pass
		else:
			self.mycursor.execute('UPDATE data SET profile = (?) WHERE ID = (?)',(self.profile,self.registration.get(),))
		confirm_update = messagebox.askquestion('confirm','Confirm to update')
		if confirm_update == 'yes':
			messagebox.showinfo('status','Updated Successfully !')
			self.mydb.commit()
			self.update_btn.config(state = 'normal')

		else:
			self.mydb.rollback()
			self.update_btn.config(state = 'normal')

	def search(self):
		''' search a student with the id '''

		if self.Search.get() != "" and self.Search.get().isdigit():
			self.student = self.Search.get()
			self.Search.set(self.student)
			self.mycursor.execute('select * from data where id = (?)',(self.Search.get(),))
			self.student_details = []
			for details in self.mycursor:
				self.student_details.extend(list(details))
			filed = [self._name,self.dob,self.radio,self.combo,self.ema,self._contact,self.f_name,self.m_name,self.occ,self.add,self.Date,self.profile,self.registration]
			if self.student_details !=[]:
				self.save_btn.config(state = 'disabled')
				self.update_btn.config(state = 'normal')

				self.date_entry.config(state = 'disabled')
				self.reg_entry.config(state = 'disabled')
				for f in range(13):
					for g in range(13):
						if f == g:
							if f==2:
								if self.student_details[2] =='Male':
									self.radio.set(value = 1)
									continue
								else:
									self.radio.set(value = 2)
									continue
							if f == 11 and g == 11:
								if self.student_details[11] != None:
									self.imgx = open(f'{self.student_details[12]}.jpg','wb')
									self.imgx.write(self.student_details[11])
									self.img = ImageTk.PhotoImage(Image.open(f'{self.student_details[12]}.jpg').resize((150,150)))# 
									self.lbl.configure(image = self.img)
									self.lbl.image = self.img
									continue
								else:
									self.lbl.configure(image = self.default_img)
									self.lbl.image = self.default_img
									continue
							filed[f].set(self.student_details[g])
						else:
							continue
			else:
				messagebox.showerror('status', 'Details Not Found !')
		else:
			messagebox.showerror('status', 'Enter Valid Roll Number !')

	def clear(self):
		''' clear all the entry fields set to default'''

		self._name.set("")
		self.dob.set("")
		self.ema.set("")
		self._contact.set("")
		self.f_name.set("")
		self.occ.set("")
		self.add.set("")
		self.m_name.set("")
		self.combo.set("Select Course")
		self.radio.set(value = 0)
		self.open_btn.config(state = 'normal')
		self.save_btn.config(state = 'normal')
		self.update_btn.config(state = 'disabled')
		self.registration.set(self.count+1)
		self.Date.set(self.date)
		self.lbl.configure(image = self.default_img)
		self.lbl.image = self.default_img
		self.profile = None

	def confirmData(self):

		'''confrim to save the details into database file'''

		confirm = messagebox.askquestion("status", 'Confirm to Save')
		if confirm == 'yes':
			values = (self._name.get(), self.dob.get(), self.gender, self.combo.get(), self.ema.get(), self._contact.get(), self.f_name.get(), self.m_name.get(), self.occ.get(), self.add.get(), self.Date.get(), self.profile, self.count+1)
			sql = "INSERT INTO data (name,dob,gender,course,email,contact,fathername,mothername,occupation,address,dt_reg,profile,ID) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
			self.mycursor.execute(sql,values)
			self.mydb.commit()
			messagebox.showinfo('Status',' Details Saved\n   Successfully!')
			self.count+=1
			self.clear()

	def save(self):
		''' collect all the data in the entry fields and run the corfirm data function '''

		self.fields = [self._name.get(),
				self.dob.get(),
				self.gender,
				self.combo.get(),
				self.ema.get(),
				self._contact.get().isdigit(),
				self.f_name.get(),
				self.m_name.get(),
				self.occ.get(),
				self.add.get(),
				self.profile]
		self.message = ['Enter Name',
		'Enter Date of Birth',
		'Select Gender',
		'Select Course',
		'Enter Email',
		'Enter Contact',
		'Enter Fater Name',
		'Enter Mother Name',
		'Enter Occupation',
		'Enter Address']

		for i in range(11):
			if i == 2:
				if self.fields[i] != None:
					continue
				else:
					messagebox.showerror('status','Select Gender')
					break

			if i == 5:
				if self.fields[i] == True and len(self._contact.get()) == 10:
					continue
				else:
					messagebox.showerror("status","Enter Contact")
					break
			if i == 3:
				if self.fields[i] != 'Select Course':
					continue
				else:
					messagebox.showerror("status","Select Course")
					break 
			if i == 10:
				if self.fields[10] != None:
					continue
				else:
					confirm_without_pic = messagebox.askquestion("status", 'Confirm Without Profile ?')
					if confirm_without_pic == 'yes':
						continue
					else:
						break
			if self.fields[i] != '':
				continue
			else:
				messagebox.showerror("status",f"{self.message[i]}")
				break
		else:
			self.confirmData()

	def open(self):
		'''display image and convert it into a  binary format'''

		self.file = filedialog.askopenfile(initialdir = 'C:\\Downloads', filetypes = (('','.jpg'),('','.png'),('','.jpeg')))
		if self.file == None:
			pass
		else:
			self.open_image = Image.open(self.file.name)
			resize_image = self.open_image.resize((150,150))
			self.open_image = ImageTk.PhotoImage(resize_image)
			self.lbl.configure(image = self.open_image)
			self.lbl.image = self.open_image
			self.load = open(self.file.name,'rb')
			self.profile = self.load.read()

	def selection(self):
		'''select the gender in the radio button'''

		value = self.radio.get()
		if value == 1:
			self.gender = "Male"
		else:
			self.gender = "Female"

	def __init__(self,root):

		''' Intialize the object of StudentRegistrationApp'''

		self.root = root
		self.root.iconbitmap(r'reg.ico')
		self.root.wm_geometry("1250x720+150+60")
		self.root.resizable(width = False,height = False)
		self.root.title("Registration_Portal")
		self.root.config(bg = "#04233b")
		self.mydb = sqlite3.connect('Student_details.db') # ----------connection to database ------------
		self.mycursor = self.mydb.cursor()
		self.mycursor.execute('SELECT ID FROM data ORDER BY ID DESC LIMIT 1')
		self.dist = 0
		self.count = 0
		for i in self.mycursor:
			self.count = sum(i)
		self.profile = None
		self.gender = None
		Label(self.root, text = "Email: abc_collage@gmail.com ", fg = "#04233b",font = ("arial", 8, "bold", "italic"), bg = "#acf3d4", anchor = 'e', width = 10,height = 3).pack(side = TOP,fill = "x")
		Label(self.root, text = "STUDENT REGISTRATION", font = ("arial", 25, "bold"), fg = "#acf3d4", bg = "#04233b", width = 10, height = 4,anchor = 'c').pack(side = TOP, fill = "x")
		self.Search = StringVar()
		self.s = Entry(self.root,textvariable= self.Search, font = ("", 20, "bold"), width = 15, bd = 5,relief = "sunken", bg = 'grey80')
		self.s.place(x = 890,y = 107)
		self.s.focus()
		Button(self.root, text = "Search",height = 2, width = 10, bd = 5,relief = "raise", fg = "#04233b", bg = "#acf3d4",command = self.search, font = ('helvetica', 10,'bold','italic')).place(x = 1129, y = 106)
		Label(self.root,text = "Registration No : ",font = ("arial", 15, "bold"), bg = "#04233b", fg = "#acf3d4").place(x = 100,y = 180)
		Label(self.root,text = "Date : ", font = ("arial", 15, "bold"), bg = "#04233b", fg = "#acf3d4").place(x = 500,y = 180)
		self.registration = StringVar()
		self.reg_entry = Entry(self.root, textvariable = self.registration, width = 10,font = ("arial",15), fg = "#04233b", bg = "white")
		self.reg_entry.place(x = 275,y = 180)
		self.registration.set(self.count+1)
		self.reg_entry.config(state = 'disabled')
		self.Date = StringVar()
		self.today = datetime.now()
		self.date = self.today.strftime("%d-%m-%Y")
		self.date_entry = Entry(root, textvariable = self.Date, width = 10, font= ("", 15), fg = "#04233b")
		self.date_entry.place(x = 570, y = 180)
		self.Date.set(self.date)
		self.date_entry.config(state = 'disabled')
				

		# #frame 01
		self.obj = LabelFrame(root,text = "Student Details", bd = 5, relief = "groove", width = 800, height = 230, font = ("arial", 15,"bold"), fg = "#04233b", bg = "#acf3d4")
		self.obj.place(x = 100,y = 220)
		Label(self.obj, text = "Name",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =50, y = 25)
		Label(self.obj, text = "Date of Birth",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =50, y = 80)
		Label(self.obj, text = "Gender",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =50, y = 140)
		Label(self.obj, text = "Course",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =450, y = 25)
		Label(self.obj, text = "Email",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =450, y = 80)
		Label(self.obj, text = "Contact",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =450, y = 140)
		self._name = StringVar()
		self.name = Entry(self.obj,textvariable = self._name,width = 15, font = ("", 15)).place(x =200, y = 25)
		self.dob = StringVar()
		self.dateOfBirth = Entry(self.obj,textvariable = self.dob, width = 15, font = ("", 15)).place(x =200, y = 80)
		self.radio = IntVar()
		self.r1 = Radiobutton(self.obj, text = "Male",variable = self.radio,value = 1, fg = "#04233b", bg = "#acf3d4", font = ("arial",10),command = self.selection)
		self.r1.place(x =200, y = 140)
		self.r2 = Radiobutton(self.obj, text = "Female",variable = self.radio,value = 2, fg = "#04233b", bg = "#acf3d4", font = ("arial",10),command = self.selection)
		self.r2.place(x =280, y = 140)
		self.combo = ttk.Combobox(self.obj, values = ["B.Tech(AERONAUTICAL ENGG)", "B.Tech(CSE)","B.Tech(ECE)","B.Tech(CIVIL ENGG)", "B.Tech(MEC ENGG)", "B.Tech(EEE)"], font = ("", 12), width = 16, state = 'r')
		self.combo.place(x = 550,y = 30)
		self.combo.set("Select Course")
		self.ema = StringVar()
		self.email = Entry(self.obj,textvariable = self.ema,width = 15, font = ("", 15)).place(x =550, y = 80)
		self._contact = StringVar()
		self.contact = Entry(self.obj,textvariable = self._contact,width = 15, font = ("", 15)).place(x =550, y = 140)

		#frame 02
		self.obj2 = LabelFrame(self.root,text = "Other Details", bd = 5, relief = "groove", width = 800, height = 230, font = ("arial", 15,"bold"), fg = "#04233b", bg = "#acf3d4")
		self.obj2.place(x = 100,y = 460)
		Label(self.obj2, text = "Father Name",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =50, y = 25)
		Label(self.obj2, text = "Occupation",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =50, y = 80)
		Label(self.obj2, text = "Address",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =50, y = 135)
		Label(self.obj2, text = "Mother Name",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b").place(x =400, y = 25)
		Label(self.obj2, text = "j",font = ("arial", 15, "bold"), bg = "#acf3d4", fg = "#04233b")
		self.f_name = StringVar()
		self.occ = StringVar()
		self.add = StringVar()
		self.m_name = StringVar()
		self.fname = Entry(self.obj2,textvariable = self.f_name,width = 15, font = ("", 15))
		self.fname.place(x =200, y = 25)
		self.occupation = Entry(self.obj2,textvariable = self.occ,width = 15, font = ("", 15))
		self.occupation.place(x =200, y = 80)
		self.address = Entry(self.obj2,textvariable = self.add,width = 15, font = ("", 15))
		self.address.place(x =200, y = 135)
		self.mname = Entry(self.obj2,textvariable = self.m_name,width = 15, font = ("", 15))
		self.mname.place(x =550, y = 25)

		# frame 03

		self.img_frame = Frame(root,bg = "#04233b")
		self.img_frame.place(x = 1003,y = 220)
		self.mycursor.execute('select * from picture')
		for i in self.mycursor:
			open('user.png','wb').write(i[0])
		self.default_img = ImageTk.PhotoImage(Image.open("user.png").resize((150,150)))
		self.lbl = Label(self.img_frame, image = self.default_img, bg = '#04233b')
		self.lbl.pack(fill = 'both')
		open_photo = save_photo = PhotoImage(file = r"open.png")
		self.open_btn = Button(self.root,image = open_photo, width = 155, bg = "limegreen", fg = "#04233b", command = self.open,height = 45)
		self.open_btn.place(x = 1000 ,y = 400)
		
		upd_photo = save_photo = PhotoImage(file = r"update.png")
		self.update_btn = Button(self.root,image = upd_photo, width = 155, bg = "orange",command = self.update,height = 45)
		self.update_btn.place(x = 1000 ,y = 475,rely = 0.01)
		self.update_btn.config(state = "disabled")

		save_photo = PhotoImage(file = r"save.png")
		self.save_btn = Button(self.root,image = save_photo, bg = "green",width = 155, command = self.save, height = 45,activebackground = "green")
		self.save_btn.place(x = 1000 ,y = 555,relx = 0,rely = 0.01)


		reset_photo = PhotoImage(file = r"reset.png")
		self.reset_btn = Button(self.root,image = reset_photo, width = 155, bg = "red", fg = "white",command = self.clear,height = 45,activebackground = "red",bd = 1)
		self.reset_btn.place(x = 1000 ,y = 635)
		self.marque = Label(self.root,text = "welcome to student registration portal 2022",bg = "#04233b",fg = '#acf3d4',font = ('',10,'italic',"bold"))
		self.marque.place(x = -270,y = 70)
		self.root.mainloop()

if __name__ == '__main__':
	root = Tk()
	startApp = StudentRegistrationApp(root)