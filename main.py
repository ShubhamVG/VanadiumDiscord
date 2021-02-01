"""This is not for use or anything. Just an experimental try."""

import asyncio, discord, tkinter.scrolledtext
from discord.ext import commands, tasks
import threading
from tkinter import *

#Testing and debugging stuff.
dm = My_DM_ID    #DMChannel to test DM related stuff.
gen = General_Channel_ID    #GuildChannel for testing purposes.

#Event checker and loop.i.e., handlers.
checker = threading.Event()
loop = asyncio.new_event_loop()

#Discord Bot
token = Get_Your_Own_Token
bot = commands.Bot(command_prefix='bruh',loop=loop,intents=discord.Intents.all())

#Button and other functional commands of GUI.
def enter(event=None):
    if e1.get() != '':    #Just to not mistakenly try to send empty messages.
        checker.set()

#Main GUI/Master window.
(root:=Tk()).title("Vanadium Discord")
root.configure(bg=COLOR)
root.resizable(width=True, height=True)
root.geometry("480x568+0+0")    #I don't know why I chose this dumb size but fix it.

#The part where your messages will be shown.
(c_a:=tkinter.scrolledtext.ScrolledText(root)).pack()
c_a.config(state='disabled')    #Just to not mess-up the messages.
(e1:=Entry(root)).pack()
(b1:=Button(text='Send',command=enter,master=root)).pack()
root.bind('<Return>', enter)

#The Discord bot set-up part.
@bot.event
async def on_ready():
    await gui_frame.start()
@tasks.loop(seconds=0)
async def gui_frame():
    if checker.is_set():
        try:
            await bot.get_channel(gen).send(e1.get())
        except discord.errors.Forbidden:
            c_a.config(state='normal')
            c_a.insert(INSERT,"Vi: Something went wrong as expected.")
            c_a.config(state='disabled')
        e1.delete(0,END)
        checker.clear()

@bot.event
async def on_message(msg):
    c_a.config(state='normal')
    c_a.insert(INSERT,f"{msg.author.name}: {msg.content}\n---------------------------------------------------------\n")    #I don't actually know how to use this. Especially the tk.INSERT part.
    c_a.yview('end')
    c_a.config(state='disabled')

def lup():
    loop.run_until_complete(bot.start(token))

def kill_program():
    root.destroy()
    asyncio.run_coroutine_threadsafe(bot.logout(),loop=loop)
    loop.call_soon_threadsafe(loop.stop)

threading.Thread(target=loop.run_until_complete,args=(bot.start(token),), daemon=True).start()
root.protocol("WM_DELETE_WINDOW", kill_program)
root.mainloop()
