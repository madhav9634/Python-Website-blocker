# Importing all the modules
from tkinter import *
from tkinter.messagebox import *

# Setting the file location and the localhost IP address for the GUI
host_files = {
    'Windows': r'C:\Windows\System32\drivers\etc\hosts',
    'Linux': '/etc/hosts'  # Fixed path for Linux
}
localhost = '127.0.0.1'

# Function to block websites
def block(win):
    def block_websites(websites):
        host_file = host_files['Windows']  # Adjust based on OS
        sites_to_block = list(websites.split(' , '))  # Splitting the websites entered by the user

        # Save blocked websites to a text file
        with open('blocked_websites.txt', 'a') as blocked_websites_txt:
            for site in sites_to_block:
                blocked_websites_txt.write(site + '\n')

        # Modify the hosts file to block websites
        try:
            with open(host_file, 'r+') as hostfile:
                content_in_file = hostfile.read()
                for site in sites_to_block:
                    if site not in content_in_file:
                        hostfile.write(localhost + '\t' + site + '\n')
                        showinfo('Websites blocked!', message='We have blocked the websites you wanted blocked!')
                    else:
                        showinfo('Website Already blocked!', 'A website you entered is already blocked')
        except PermissionError:
            showerror('Permission Denied', 'Please run the application as an administrator to block websites.')

    # GUI for blocking websites
    blck_wn = Toplevel(win, background='LightBlue')
    blck_wn.title("Block a website")
    blck_wn.geometry('300x200')
    blck_wn.resizable(False, False)

    Label(blck_wn, text='Block websites', background='LightBlue', font=("Georgia", 16)).place(x=80, y=0)
    Label(blck_wn, text='(Enter the websites separated only by \' , \')', background='LightBlue',
          font=("Times", 13)).place(x=0, y=35)
    Label(blck_wn, text='Enter the URLs (www.<sitename>.com):', background='LightBlue', font=('Times', 13)).place(
        x=0, y=70)

    sites = Text(blck_wn, width=35, height=3)
    sites.place(x=0, y=100)

    submit_btn = Button(blck_wn, text='Submit', bg='MidnightBlue', command=lambda: block_websites(sites.get('1.0', END).strip()))
    submit_btn.place(x=100, y=160)


# Function to unblock websites
def unblock(win):
    def unblock_websites(websites_to_unblock):
        host_file = host_files['Windows']

        # Modify the hosts file to unblock websites
        try:
            with open(host_file, 'r+') as hostfile:
                content_in_file = hostfile.readlines()
                hostfile.seek(0)

                for line in content_in_file:
                    if not any(site in line for site in websites_to_unblock.split(', ')):
                        hostfile.write(line)

                hostfile.truncate()
        except PermissionError:
            showerror('Permission Denied', 'Please run the application as an administrator to unblock websites.')
            return

        # Remove unblocked websites from the text file
        with open('blocked_websites.txt', 'r+') as blocked_websites_txt:
            file_content = blocked_websites_txt.readlines()
            blocked_websites_txt.seek(0)

            for line in file_content:
                if not any(site in line for site in websites_to_unblock.split(', ')):
                    blocked_websites_txt.write(line)

            blocked_websites_txt.truncate()

        showinfo('Success', 'Website(s) Unblocked!')

    # Get a list of all blocked websites
    try:
        with open('blocked_websites.txt', 'r') as blocked_websites:
            blck_sites = blocked_websites.read().splitlines()
    except FileNotFoundError:
        blck_sites = []  # Handle case where the file doesn't exist

    # GUI for unblocking websites
    unblck_wn = Toplevel(win, background='Aquamarine')
    unblck_wn.title("Unblock a website")
    unblck_wn.geometry('285x200')
    unblck_wn.resizable(False, False)

    Label(unblck_wn, text='Unblock websites', background='Aquamarine', font=("Georgia", 16)).place(x=80, y=0)
    Label(unblck_wn, text='Select the URLs that you want to unblock:', background='Aquamarine', font=('Times', 13)).place(x=0, y=70)

    # Creating a dropdown menu from the text file to get the sites that are blocked
    blck_sites_strvar = StringVar(unblck_wn)
    if blck_sites:
        blck_sites_strvar.set(blck_sites[0])
        dropdown = OptionMenu(unblck_wn, blck_sites_strvar, *blck_sites)
        dropdown.config(width=20)
        dropdown.place(x=60, y=100)

        submit_btn = Button(unblck_wn, text='Submit', bg='MidnightBlue',
                            command=lambda: unblock_websites(blck_sites_strvar.get()))
        submit_btn.place(x=100, y=160)
    else:
        Label(unblck_wn, text='No websites to unblock', bg='Aquamarine').place(x=70, y=100)


# Creating a GUI master window
root = Tk()
root.title("Madhav Website Blocker")
root.geometry('400x300')
root.wm_resizable(False, False)

# Creating and setting the locations of all the components of the GUI
Label(root, text='Madhav Website Blocker', font=("Comic Sans MS", 16)).place(x=45, y=0)
Label(root, text='What do you want to do?', font=("Helvetica", 14)).place(x=90, y=40)

Button(root, text='Block a Website', font=('Times', 16), bg='SpringGreen4', command=lambda: block(root)).place(x=110, y=100)
Button(root, text='Unblock a Website', font=('Times', 16), bg='SpringGreen4', command=lambda: unblock(root)).place(x=100, y=150)

root.mainloop()
