#!/usr/bin/env python

# Unmail 0.0.1
# 2021 Xerz
 
import mailbox, pickle, traceback, os
from email.header import decode_header
from tkinter import Tk
from tkinter import filedialog

Tk().withdraw()

mb = mailbox.mbox(filedialog.askopenfilename(
	title="Choose an Mbox file", 
	filetypes=[("Mbox file", "*.mbox")]))
save_to = filedialog.askdirectory(
	title="Choose a destination directory") + '/'
 
if not os.path.exists(save_to): os.makedirs(save_to)

def save_attachments(mid):
    msg = mb.get_message(mid)
    if msg.is_multipart():
        DateReceived = msg['Date']
        
        for part in msg.get_payload():
            if str(part.get_filename()) == 'None':
                continue

            print()
            try:
                decoded_name = decode_header(part.get_filename())

                if isinstance(decoded_name[0][0], str):
                    name = decoded_name[0][0]
                else:
                    name_encoding = decoded_name[0][1]
                    name = decoded_name[0][0].decode(name_encoding)
                 
                name = '%s - %s' % (DateReceived, name)
                print('Saving %s' % (name))
                with open(save_to + name, 'wb') as f:
                    f.write(part.get_payload(decode=True))
            except:
                traceback.print_exc()

for mail in mb.keys():
	save_attachments(mail)
