import tkinter as tk 
import requests
from bs4 import BeautifulSoup
import datetime
import pyperclip

list_websites = []
list_websites_copy = []

def send():
	global txt_url, txt_date, txt_author, list_websites, lbl_clipboard, list_websites_copy, txt_publication, isperiodique
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
	URL = txt_url.get('1.0',tk.END).strip()
	txt_url.delete('1.0',tk.END)
	try:
		page = requests.get(URL, headers=headers)
		if page.status_code == 404:
			txt_url.insert('1.0', 'Invalid URL')

		else:
			soup = BeautifulSoup(page.content, 'html.parser')
			
			title = soup.title.text.strip()

			author = txt_author.get('1.0', tk.END).strip()
			txt_author.delete('1.0', tk.END)

			author = author.split()
			if not author:
				author = 'ANONYME'

			elif len(author) == 2:
				first, last = author
				author = last.upper() + ' ' +  first.title()
			else:
				author = ' '.join(author).upper()

			date = txt_date.get('1.0', tk.END).strip()
			if date == '':
				date = datetime.datetime.now()
				months = {'January':'janvier', 'February':'février', 
			'March':'mars', 'April':'avril', 'May':'mai', 
			'June':'juin', 'July':'juillet', 'August':'août', 
			'September':'septembre', 'October':'octobre', 
			'November':'novembre', 'December':'décembre'}

				eng_month = date.strftime('%B')
				months = months[eng_month] 
				date = date.strftime(f"%d {months} %Y")

			if isperiodique:
				publication = txt_publication.get('1.0', tk.END).strip()
				txt_publication.delete('1.0', tk.END)
				domain = URL.split('://')[-1].split('www.')[-1].split('/')[0].capitalize().strip()

				source = f'{author}. «{title}», {domain}, {publication}, [En ligne], {URL} (page consultée le {date})'
			else:
				source = f'{author}. {title}, [En ligne], {URL} (page consultée le {date})'
			list_websites.append(source)
			list_websites_copy.append(source)
			list_websites.sort()
			show_websites = '\n\n'.join(list_websites)
			size = lbl_clipboard.winfo_width() *0.9
			lbl_clipboard.configure(text=show_websites, wrap=size)
	except:
		txt_url.insert('1.0', 'Invalid URL')

def delete():
	global list_websites, lbl_clipboard, list_websites_copy
	try:
		remove = list_websites_copy.pop()
		list_websites.remove(remove)
		list_websites.sort()
	except IndexError:
		pass
	show_websites = '\n\n'.join(list_websites)
	size = lbl_clipboard.winfo_width() *0.9
	lbl_clipboard.configure(text=show_websites, wrap=size)

def copy():
	global list_websites
	show_websites = '\n\n'.join(list_websites)
	pyperclip.copy(show_websites)
	lbl_clipboard.configure(text=show_websites, wrap=size)

def language_select():
	global btn_language, language
	if btn_language['text'] == 'English':
		btn_language.configure(text='Français')
		language = 'French'
	elif btn_language['text'] == 'Français':
		btn_language.configure(text='English')
		language = 'English'

def periodiques():
	global title_txt, copy_txt, author_txt, language, send_txt, delete_txt, isperiodique, publication_txt
	isperiodique = True
	if language == 'French':
		title_txt = 'Périodiques'
		copy_txt = 'Copiez'
		author_txt = 'Author'
		send_txt = 'Send'
		delete_txt = 'Delete'
		publication_txt = 'Date de publication'

	elif language == 'English':
		title_txt = 'Periodique'
		copy_txt = 'Copy'
		author_txt = 'Author'
		send_txt = 'Send'
		delete_txt = 'Delete'
		publication_txt = 'Date of publication'

	new_window()

def websites():
	global title_txt, copy_txt, author_txt, language, send_txt, delete_txt, isperiodique
	isperiodique = False
	if language == 'French':
		title_txt = 'Sites Internet'
		copy_txt = 'Copiez'
		author_txt = 'Auteur'
		send_txt = 'Envoyer'
		delete_txt = 'Supprimer'

	elif language == 'English':
		title_txt = 'Websites'
		copy_txt = 'Copy'
		author_txt = 'Author'
		send_txt = 'Send'
		delete_txt = 'Delete'

	new_window()

def new_window():
	global window, title_txt, copy_txt, author_txt, send_txt, delete_txt, txt_url, txt_date, txt_author, lbl_clipboard, isperiodique, publication_txt, txt_publication
	window.destroy()
	window = tk.Tk()  

	window.rowconfigure(1, weight=1)
	window.columnconfigure(0, weight=1)

	lbl_title = tk.Label(master=window, text=title_txt)
	lbl_title.grid(row=0, column=0, sticky='ew')

	frm_work = tk.Frame(master=window, width=20, height=20)
	frm_work.columnconfigure(1, weight=1)
	frm_work.rowconfigure(0, weight=1)
	frm_work.grid(row=1, column=0, sticky='nsew')

	frm_outputs = tk.Frame(master=frm_work)
	frm_outputs.columnconfigure(0, weight=1)
	frm_outputs.rowconfigure(0, weight=10)
	frm_outputs.rowconfigure(1, weight=1)

	frm_outputs.grid(row=0, column=1, sticky='nsew')

	frm_inputs = tk.Frame(master=frm_work)
	frm_inputs.columnconfigure([0,1], weight=1)
	
	if isperiodique:
		frm_inputs.rowconfigure([0,1,2,3], weight=1)
	else:
		frm_inputs.rowconfigure([0,1,2], weight=1)
	frm_inputs.grid(row=0,column=0, sticky='nsew')

	lbl_clipboard = tk.Label(master=frm_outputs, text='Your bibliographie will appear here', height=20, width=100, justify=tk.LEFT)
	lbl_clipboard.grid(row=0, column=0, sticky='nsew')

	frm_outputs_btns = tk.Frame(master=frm_outputs)
	frm_outputs_btns.rowconfigure(0, weight=1)
	frm_outputs_btns.columnconfigure([0,1,2], weight=1)
	frm_outputs_btns.grid(row=1, column=0, sticky='nsew')

	btn_send = tk.Button(master=frm_outputs_btns, text=send_txt, command=send)
	btn_send.grid(row=0, column=0, padx=2, pady=5, sticky='nsew')

	btn_delete = tk.Button(master=frm_outputs_btns, text=delete_txt, command=delete)
	btn_delete.grid(row=0, column=1, padx=2, pady=5, sticky='nsew')

	btn_copy = tk.Button(master=frm_outputs_btns, text=copy_txt, command=copy)
	btn_copy.grid(row=0, column=2, padx=2, pady=5, sticky='nsew')

	lbl_url = tk.Label(master=frm_inputs, text='Url')
	lbl_url.grid(row=0, column=0, sticky='nsew')

	lbl_date = tk.Label(master=frm_inputs, text='Date')
	lbl_date.grid(row=1, column=0, sticky='nsew')

	lbl_author = tk.Label(master=frm_inputs, text=author_txt)
	lbl_author.grid(row=2, column=0, sticky='nsew')

	if isperiodique:
		lbl_publication = tk.Label(master=frm_inputs, text=publication_txt)
		lbl_publication.grid(row=3, column=0, sticky='nsew')

		txt_publication = tk.Text(master=frm_inputs, height=1, width=20)
		txt_publication.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

	txt_url = tk.Text(master=frm_inputs, height=1, width=20)
	txt_url.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

	txt_date = tk.Text(master=frm_inputs, height=1, width=20)
	txt_date.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

	txt_author = tk.Text(master=frm_inputs, height=1, width=20)
	txt_author.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

	window.mainloop()

def select():
	global window, btn_language, language
	language = 'English'
	window = tk.Tk()
	window.rowconfigure([0,1], minsize=50, weight=1)
	window.columnconfigure(0, minsize=50, weight=1)

	frm_options = tk.Frame(master=window)
	frm_options.columnconfigure([0,1], minsize=50, weight=1)
	frm_options.rowconfigure(0, minsize=50, weight=1)
	frm_options.grid(row=0, column=0, sticky='nsew')

	btn_website = tk.Button(master=frm_options, text="Websites\nSites Internet", command=websites)
	btn_website.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

	btn_periodique = tk.Button(master=frm_options, text="Periodique\nPériodiques", command=periodiques)
	btn_periodique.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

	btn_language = tk.Button(master=window, text='English', command=language_select)
	btn_language.grid(row=1,column=0, padx=5, pady=5, sticky='nsew')
	window.mainloop()
	
if __name__ == '__main__':
	select()
