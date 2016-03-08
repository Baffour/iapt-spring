#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#


# SMTP message templates. 
# SMS does not need a subject line.
TEMPLATES = dict(
    email = """From: %(frm)s\r
To: %(to)s\r
Subject: %(subject)s\r
%(body)s""",
    sms = """From: %(frm)s\r
To: %(to)s\r
%(body)s""",
)


def open_smtp(settings):
    """
    Connects to the SMTP server using mail.settings.
    
    Returns SMTP server object, connected and logged in.
    """
    import smtplib
     
    (host, port) = settings.server.split(":")
    (username, password) = settings.login.split(":")
    
    try:
        serv = smtplib.SMTP(host, port)
        serv.ehlo()
        serv.starttls()
        serv.ehlo()
        serv.login(username, password)
    except:
        serv = None
    
    return serv
    
def send(message, record, 
         typ='email', 
         serv=None, 
         close_smtp=False,
         logger=None):
    """
    Sends a ``message`` to ``record`` by ``typ`` using ``serv``. Optionally
    closes the smtp connection if ``close_smtp=True``.
    
    If ``serv=None`` it will create a new SMTP server object using ``open_smtp()``.
        Also, it will close the smtp connection autmatically if serv=None
    """
    
    # If we don't have a server object, make one
    # and set it to close before returning from this
    # function. Useful if we only need to send a
    # one shot message.
    if not serv:
        serv = open_smtp()
        close_smtp = True
           
    # Create the SMTP message context
    context = dict(
        frm=mail.settings.sender,
        to=panel[typ],
        subject=message.subject,
        body=message.content,
        footer=footer, 
    )
    
    # Create the SMTP message
    the_msg = TEMPLATES[typ] % context
    
    # Send the email
    serv.sendmail(context['frm'], context['to'], the_msg)
    
    # Log the action
    if callable(logger):
        logger(
            msg = message,
            panel = panel,
            sent_on = datetime.now()
        )
    
    # Optionally close it (in case this is a one-use case)
    if close_smtp:
        serv.close()
    
    return True
    
