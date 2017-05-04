#!/usr/bin/env python
"""包含一个Name实例，以及StreetAddres， Phone(home, work, telefacsimile, pager, mobile)
Email(home, work),或许需要一些Date实例(birthday, wedding, anniversary)"""

class NewAddrBookEntry(object):
    'new address book entry class'
    def __init__(self, nm, ph):
        self.name = Name(nm)
        self.phone = Phone(nm)
        print('Created instance for:', self,name)