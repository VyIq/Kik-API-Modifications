# xmpp/datatypes/*.py #
class OutgoingAddressBookMatching(XMPPElement):
    """
    Represents an outgoing request to match contacts
    """
    def __init__(self, account_email, contact_email):
        super().__init__()
        self.account_email = account_email
        self.contact_email = contact_email

    def serialize(self):
        timestamp = str(int(round(time.time() * 1000)))
        data = ('<iq type="set" id="{}">'
                '<match xmlns="kik:iq:matching">'
                '<context reason="talk-to" opt-status="opt-in" />'
                '<my d="1">'
                '<email>{}</email>'
                '</my>'
                '<contacts d="1">'
                '<email>{}</email>'
                '</contacts>'
                '</match>'
                '</iq>').format(self.message_id, account_email, contact_email)
        return data.encode()

# client.py
def check_email_contact(self, account_email, contact_email):
    """
    Checks contact_email for existence (not exactly a descriptive docstring)
    """
    log.info("[+] Checking for existence of email '{}'".format(contact_email))
    return self._send_xmpp_element(*.OutgoingAddressBookMatching(account_email, contact_email))

# Probably needs callback
