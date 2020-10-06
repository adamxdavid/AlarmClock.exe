import tkinter as tk
from datetime import datetime
import winsound

#stores the two toned theme of app
theme_button = 'white'
general_theme = '#FFFF80'

#makes window with specifc dementions
Height = 500
Width = 400
root = tk.Tk()
root.title("Minimalist Alarm Clock By Adam D")
canvas = tk.Canvas(root,height=Height,width=Width)
canvas.pack()

#these two functions create classes (Menu, Settings) when called
def draw_menu():
	global a
	a = Menu()
	a.what_is_the_time()
	a.what_is_the_date()
	return a

def draw_settings():
	global b
	try:
		b.draw_widgets_again()
	except NameError:
		b = Settings()
		return b

class Menu:
	#initializing the main menu, creating frames, buttons, etc.
	def __init__(self):
		
		self.frame1 = tk.Frame(root, bg=general_theme)
		self.frame1.place(relwidth=1,relheight=1/4, anchor = 'n', relx=.5)

		self.frame2 = tk.Frame(root, bg=general_theme)
		self.frame2.place(relwidth=1,relheight=3/4,anchor='s',relx=.5,rely=1)
		
		self.label = tk.Label(self.frame1, text='No alarms set', bg = theme_button)
		self.label.place(anchor = 'n', relx = .5,rely = .1)
		
		self.label2 = tk.Label(self.frame1, text = 'loading...',bg = theme_button)
		self.label2.place(anchor = 'n', relx = .5,rely = .5, relheight = .3,relwidth = .3)
		
		self.label3 = tk.Label(self.frame1, text = 'loading...',bg = theme_button)
		self.label3.place(anchor = 'n', relx = .5, rely = .3)
		
		self.alarm_button = tk.Button(self.frame2,bd = 3,bg = theme_button, command = draw_settings)
		self.alarm_button.place(anchor = 'n', relx = .5,relheight=1/2.2,relwidth=.95,rely = 1/9)
		self.alarm_label = tk.Label(self.frame2, bg = theme_button, font = '32',)
		self.alarm_label.place(anchor = 'n', relx = 3/6,rely = 0.25,relwidth=1/4,relheight=1/8)
		
	def what_is_the_time(self):
		#getting time info from system
		time = datetime.now()
		year = time.year
		month = time.month
		day = time.day
		self.hour = time.hour
		self.minute = time.minute
		
		#this will be used in when is the next alarm function
		self.military_hour = self.hour
		
		#converting military to civilian time
		if self.hour > 12:
			self.hour = self.hour - 12
			self.am_or_pm = ' PM'
		elif self.hour == 0:
			self.hour = 12
			self.am_or_pm = ' AM'
		elif self.hour <= 12:
			self.am_or_pm = ' AM'
		
		self.minute_unmodified = self.minute
		#converting single digit minute to double digit
		if len(str(self.minute)) == 1:
			self.minute = '0' + str(self.minute)
		
		#this is how the time will display
		time_display = str(self.hour) + ':' + str(self.minute) + self.am_or_pm
		#after helps update the time on label2
		root.after(1000, self.what_is_the_time)
		self.label2['text'] = time_display
		
		return [self.hour, self.minute_unmodified]
		
	def what_is_the_date(self):
		self.tday = datetime.now()
		self.month = self.tday.month
		self.dayy = self.tday.day
		self.weekday_int = self.tday.isoweekday()
		if self.weekday_int == 1:
			self.day_of_week = 'Monday'
		if self.weekday_int == 2:
			self.day_of_week = 'Tuesday'
		if self.weekday_int == 3:
			self.day_of_week = 'Wednesday'
		if self.weekday_int == 4:
			self.day_of_week = 'Thursday'
		if self.weekday_int == 5:
			self.day_of_week = 'Friday'
		if self.weekday_int == 6:
			self.day_of_week = 'Saturday'
		if self.weekday_int == 7:
			self.day_of_week = 'Sunday'	
		if self.month == 1:
			self.the_month = 'January'
		if self.month == 2:
			self.the_month = 'February'
		if self.month == 3:
			self.the_month = 'March'
		if self.month == 4:
			self.the_month = 'April'
		if self.month == 5:
			self.the_month = 'May'
		if self.month == 6:
			self.the_month = 'June'
		if self.month == 7:
			self.the_month = 'July'
		if self.month == 8:
			self.the_month = 'August'
		if self.month == 9:
			self.the_month = 'September'
		if self.month == 10:
			self.the_month = 'October'
		if self.month == 11:
			self.the_month = 'November'
		if self.month == 12:
			self.the_month = 'December'
		self.the_date = (self.day_of_week+ ', ' + self.the_month+ ' '+ str(self.dayy))
		self.label3['text'] = self.the_date
		root.after(60000, self.what_is_the_date)
		
	def when_is_next_alarm(self):
		try:
			b.user_hour
		except:
			self.label['text'] = 'No alarms are currently set'
			return
			
		current_day = self.weekday_int
		
		#where ever the users slider is
		the_users_hour = b.user_hour
		
		#converting to military for calculations
		if b.user_ampm == 'PM':
			the_users_hour += 12
		
		minutes = 0
		hours = 0
		days = 0
		flag = True
		
		#is the alarm on the current day but has passed us already
		if b.alarm_list[current_day-1] == True and (the_users_hour - self.military_hour <= 0 or the_users_hour - self.military_hour == 0 and b.user_minute_int - self.minute_unmodified < 0):
				hours = 24 - (self.military_hour - the_users_hour)
				
				#this is to round off any minutes
				if hours == 24:
					hours = 23
				
				days = 6
				print("first one")
				self.label['text'] = f'Your next alarm is in {days} days and {hours} hours'
				#that is how many hours and minutes are left
				return
			
		#checking if its the next day but still within 24 hrs
		#try block prevents an index out of range on sundays
		try:
			x = b.alarm_list[current_day]
		except IndexError:
			x = 0
		else:
			x = current_day
		if b.alarm_list[x] == True and 24 - self.military_hour + the_users_hour <= 24:
			hours = 24 - self.military_hour + the_users_hour
			
			#this is to round off any extra minutes
			if hours == 24:
				hours = 23
				
			minutes = 60 - (self.minute_unmodified - b.user_minute_int)
			print(hours, minutes)
			print("layer 2")
			if minutes == 0:
				print("section 1")
				if hours == 1:
					self.label['text'] = f'Your next alarm is in {hours} hour'
				elif hours > 1:
					self.label['text'] = f'Your next alarm is in {hours} hours'
			elif hours == 0:
				print("section 2")			
				if minutes == 1:
					self.label['text'] = f'Your next alarm is in {minutes} minute'
				elif minutes > 0:
					self.label['text'] = f'Your next alarm is in {minutes} minutes'
			elif minutes != 0:
				print("section 3")
				if minutes == 1:
					if hours == 1:
						self.label['text'] = f'Your next alarm is in {hours} hour and {minutes} minute'
					elif hours > 1:
						self.label['text'] = f'Your next alarm is in {hours} hours and {minutes} minute'
				elif minutes > 1:
					if hours == 1:
						self.label['text'] = f'Your next alarm is in {hours} hour and {minutes} minutes'
					elif hours > 1:
						self.label['text'] = f'Your next alarm is in {hours} hours and {minutes} minutes'
			#you will return just how many hours are left till alarm
		else:
			while flag == True:
				if current_day + 1 <= 7:
					current_day+=1
				else:
					current_day = 1
				
				days += 1
				print (current_day, days)
				print(b.alarm_list[current_day-1])
				
				if b.alarm_list[current_day-1] == True:
					flag = False
					hours = the_users_hour - self.military_hour
					minutes = b.user_minute_int - self.minute_unmodified
					print(hours)
					if hours <= 0:
						self.label['text'] = f'Your next alarm is in {days} days'
					elif hours == 1:
						self.label['text'] = f'Your next alarm is in {days} days and {hours} hour'
					elif hours > 1:
						self.label['text'] = f'Your next alarm is in {days} days and {hours} hours'
						
		root.after(1000, self.when_is_next_alarm)
		
class Settings:
	def __init__(self):
		
		self.settings = tk.Frame(root, bg=general_theme)
		self.settings.place(relwidth=1,relheight=3/4,anchor='s',relx=.5,rely=1)
	
		self.confirm = tk.Button(self.settings, text = 'Confirm Alarm', bg = theme_button, command = self.confirm_alarm)
		self.confirm.place(relheight = 0.10, relwidth = 0.250, relx = .5,rely=.95, anchor = 's')
		
		the_time = a.what_is_the_time()
		
		self.slider_hour = tk.Scale(self.settings,orient='horizontal',from_= 1, to=12,length=220,bg = theme_button)
		self.slider_hour.place(anchor='n', relx=1/2,rely=1/20,)
		self.slider_hour.set(the_time[0])

		self.slider_minute = tk.Scale(self.settings,orient='horizontal',from_=0, to=59, length=300,bg = theme_button)
		self.slider_minute.place(anchor = 'n',relx = 1/2,rely = 2/9)
		self.slider_minute.set(the_time[1])

		#make it so if you hit am, it should change color,and if you hit pm, it changes color
		self.am = tk.Button(self.settings,text = 'AM',bg = theme_button, command = lambda: self.button_manager(self.am))
		self.am.place(anchor = 'ne',relx = .5,rely = 3/8, relwidth=.2,relheight=.1)

		self.pm = tk.Button(self.settings,text = 'PM',bg = theme_button, command = lambda: self.button_manager(self.pm))
		self.pm.place(anchor = 'nw',relx = .5,rely = 3/8, relwidth=.2,relheight=.1,)

		#make it so you can select which days you want, color changes
		self.mon = tk.Button(self.settings,text = 'Mon',bg = theme_button, command = lambda: self.button_manager(self.mon))
		self.mon.place(anchor = 'w',relx = 0,rely = 5/8, relwidth=1/7,relheight=.1)
		self.tue = tk.Button(self.settings,text = 'Tue',bg = theme_button, command = lambda: self.button_manager(self.tue))
		self.tue.place(anchor = 'w',relx = 1/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.wed = tk.Button(self.settings,text = 'Wed',bg = theme_button, command = lambda: self.button_manager(self.wed))
		self.wed.place(anchor = 'w',relx = 2/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.thu = tk.Button(self.settings,text = 'Thu',bg = theme_button, command = lambda: self.button_manager(self.thu))
		self.thu.place(anchor = 'w',relx = 3/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.fri = tk.Button(self.settings,text = 'Fri',bg = theme_button, command = lambda: self.button_manager(self.fri))
		self.fri.place(anchor = 'w',relx = 4/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.sat = tk.Button(self.settings,text = 'Sat',bg = theme_button, command = lambda: self.button_manager(self.sat))
		self.sat.place(anchor = 'w',relx = 5/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.sun = tk.Button(self.settings,text = 'Sun',bg = theme_button, command = lambda: self.button_manager(self.sun))
		self.sun.place(anchor = 'w',relx = 6/7,rely = 5/8, relwidth=1/7,relheight=.1)
		
	def button_manager(self, button):
		#when a button is pressed, it turns green, when it is pressed again, it turns back to normal
		if button['bg'] == theme_button:
			button['bg'] = 'light green'
		elif button['bg'] == 'light green':
			button['bg'] = theme_button
		
		
	#this will take the data given, store it, display it in menu
	def confirm_alarm(self):
		#this gets the current hour/min numbers the sliders are on
		self.user_hour = self.slider_hour.get()
		self.user_minute = self.slider_minute.get()
		
		#this figures if the user selected am or pm
		if self.am['bg'] == 'light green':
			self.user_ampm = 'AM'
			color_am = 'light green'
			color_pm = theme_button
		elif self.pm['bg'] == 'light green':
			self.user_ampm = 'PM'
			color_am = theme_button
			color_pm = 'light green'
		
		#figures out which days of the week were selected
		if self.mon['bg'] == 'light green':
			user_mon = True
			color_mon = 'light green'
		else:
			user_mon = False
			color_mon = theme_button
			
		if self.tue['bg'] == 'light green':
			user_tue = True
			color_tue = 'light green'
		else:
			user_tue = False
			color_tue = theme_button
			
		if self.wed['bg'] == 'light green':
			user_wed = True
			color_wed = 'light green'
		else:
			user_wed = False
			color_wed = theme_button
			
		if self.thu['bg'] == 'light green':
			user_thu = True
			color_thu = 'light green'
		else:
			user_thu = False
			color_thu = theme_button
			
		if self.fri['bg'] == 'light green':
			user_fri = True
			color_fri = 'light green'
		else:
			user_fri = False
			color_fri = theme_button
			
		if self.sat['bg'] == 'light green':
			user_sat = True
			color_sat = 'light green'
		else:
			user_sat = False
			color_sat = theme_button
			
		if self.sun['bg'] == 'light green':
			user_sun = True
			color_sun = 'light green'
		else:
			user_sun = False
			color_sun = theme_button

		#package data and display on one of the alarm labels in the Menu
		self.alarm_list = [
		user_mon, user_tue, user_wed, user_thu, user_fri, user_sat, user_sun
		]
		
		self.alarm_dict = {
		'user_mon':user_mon,
		'user_tue':user_tue,'user_wed':user_wed,'user_thu':user_thu,'user_fri':user_fri,
		'user_sat':user_sat,'user_sun':user_sun
		}
		
		self.color_dict = {
		'color_am':color_am,'color_pm':color_pm,'color_mon':color_mon,
		'color_tue':color_tue,'color_wed':color_wed,'color_thu':color_thu,'color_fri':color_fri,
		'color_sat':color_sat,'color_sun':color_sun
		}
		
		#alter the display of the alarm in Menu after drawing Menu
		draw_menu()
		
		#this preserves the unmodified version of user_minute
		self.user_minute_int = self.user_minute
		
		if len(str(self.user_minute)) == 1:
			self.user_minute = '0' + str(self.user_minute)
		a.alarm_label['text'] = f'{self.user_hour}:{self.user_minute} {self.user_ampm}'
		a.when_is_next_alarm()
		self.activate_alarm()
		
	def activate_alarm(self):
		#the core of the alarm clock, checks if day and time line up, plays sound if so
		if str(self.user_hour) == str(a.hour):
			if str(self.user_minute) == str(a.minute):
				if ' ' + self.user_ampm == a.am_or_pm:
					for key, value in self.alarm_dict.items():
						if value == True:
							if key == 'user_mon':
								if a.day_of_week == 'Monday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
							if key == 'user_tue':
								if a.day_of_week == 'Tuesday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
							if key == 'user_wed':
								if a.day_of_week == 'Wednesday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
							if key == 'user_thu':
								if a.day_of_week == 'Thursday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
							if key == 'user_fri':
								if a.day_of_week == 'Friday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
							if key == 'user_sat':
								if a.day_of_week == 'Saturday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
							if key == 'user_sun':
								if a.day_of_week == 'Sunday':
									winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME)
		root.after(60_000, self.activate_alarm)
	
	def draw_widgets_again(self):
		#tkinter cannot place an object multiple times, so we have to remake them to place it
		
		self.settings = tk.Frame(root, bg=general_theme)
		self.settings.place(relwidth=1,relheight=3/4,anchor='s',relx=.5,rely=1)
	
		self.confirm = tk.Button(self.settings, text = 'Confirm Alarm', bg = theme_button, command = self.confirm_alarm)
		self.confirm.place(relheight = 0.10, relwidth = 0.250, relx = .5,rely=.95, anchor = 's')
		
		the_time = a.what_is_the_time()
		
		self.slider_hour = tk.Scale(self.settings,orient='horizontal',from_= 1, to=12,length=220,bg = theme_button)
		self.slider_hour.place(anchor='n', relx=1/2,rely=1/20,)
		self.slider_hour.set(the_time[0])

		self.slider_minute = tk.Scale(self.settings,orient='horizontal',from_=0, to=59, length=300,bg = theme_button)
		self.slider_minute.place(anchor = 'n',relx = 1/2,rely = 2/9)
		self.slider_minute.set(the_time[1])
	
		#make it so if you hit am, it should change color,and if you hit pm, it changes color
		self.am = tk.Button(self.settings,text = 'AM',bg = self.color_dict['color_am'], command = lambda: self.button_manager(self.am))
		self.am.place(anchor = 'ne',relx = .5,rely = 3/8, relwidth=.2,relheight=.1)

		self.pm = tk.Button(self.settings,text = 'PM',bg = self.color_dict['color_pm'], command = lambda: self.button_manager(self.pm))
		self.pm.place(anchor = 'nw',relx = .5,rely = 3/8, relwidth=.2,relheight=.1,)

		#make it so you can select which days you want, color changes
		self.mon = tk.Button(self.settings,text = 'Mon',bg = self.color_dict['color_mon'], command = lambda: self.button_manager(self.mon))
		self.mon.place(anchor = 'w',relx = 0,rely = 5/8, relwidth=1/7,relheight=.1)
		self.tue = tk.Button(self.settings,text = 'Tue',bg = self.color_dict['color_tue'], command = lambda: self.button_manager(self.tue))
		self.tue.place(anchor = 'w',relx = 1/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.wed = tk.Button(self.settings,text = 'Wed',bg = self.color_dict['color_wed'], command = lambda: self.button_manager(self.wed))
		self.wed.place(anchor = 'w',relx = 2/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.thu = tk.Button(self.settings,text = 'Thu',bg = self.color_dict['color_thu'], command = lambda: self.button_manager(self.thu))
		self.thu.place(anchor = 'w',relx = 3/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.fri = tk.Button(self.settings,text = 'Fri',bg = self.color_dict['color_fri'], command = lambda: self.button_manager(self.fri))
		self.fri.place(anchor = 'w',relx = 4/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.sat = tk.Button(self.settings,text = 'Sat',bg = self.color_dict['color_sat'], command = lambda: self.button_manager(self.sat))
		self.sat.place(anchor = 'w',relx = 5/7,rely = 5/8, relwidth=1/7,relheight=.1)
		self.sun = tk.Button(self.settings,text = 'Sun',bg = self.color_dict['color_sun'], command = lambda: self.button_manager(self.sun))
		self.sun.place(anchor = 'w',relx = 6/7,rely = 5/8, relwidth=1/7,relheight=.1)
		
#runs the window
a = draw_menu()



root.mainloop()
