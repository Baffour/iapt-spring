# The following file is provided by
# http://code.google.com/p/django-sms/source/browse/trunk/sms/fixtures/initial_data.json

# You may also find these lists from
# http://en.wikipedia.org/wiki/List_of_carriers_providing_SMS_transit#
# And
# http://www.mutube.com/projects/open-email-to-sms/gateway-list
# http://www.topbits.com/how-to-send-text-messages-free.html
# http://www.notepage.net/smtp.htm
#
# Which may include more than what is listed here.


CARRIERS = [
    {
        "pk": 1,
        "model": "sms.Carrier",
        "fields": {
            "name": "Speakout (USA GSM)",
            "gateway": "%(phone_number)s@cingularme.com"
        }
    },
    {
        "pk": 2,
        "model": "sms.Carrier",
        "fields": {
            "name": "Airtel (Karnataka, India)",
            "gateway": "%(phone_number)s@airtelkk.com"
        }
    },
    {
        "pk": 3,
        "model": "sms.Carrier",
        "fields": {
            "name": "Airtel Wireless (Montana, USA)",
            "gateway": "%(phone_number)s@sms.airtelmontana.com"
        }
    },
    {
        "pk": 4,
        "model": "sms.Carrier",
        "fields": {
            "name": "Alaska Communications Systems",
            "gateway": "%(phone_number)s@msg.acsalaska.com"
        }
    },
    {
        "pk": 5,
        "model": "sms.Carrier",
        "fields": {
            "name": "Alltel Wireless",
            "gateway": "%(phone_number)s@message.alltel.com"
        }
    },
    {
        "pk": 6,
        "model": "sms.Carrier",
        "fields": {
            "name": "aql",
            "gateway": "%(phone_number)s@text.aql.com"
        }
    },
    {
        "pk": 7,
        "model": "sms.Carrier",
        "fields": {
            "name": "AT&T Wireless",
            "gateway": "%(phone_number)s@txt.att.net"
        }
    },
    {
        "pk": 8,
        "model": "sms.Carrier",
        "fields": {
            "name": "AT&T Mobility (formerly Cingular)",
            "gateway": "%(phone_number)s@txt.att.net"
        }
    },
    {
        "pk": 9,
        "model": "sms.Carrier",
        "fields": {
            "name": "AT&T Enterprise Paging",
            "gateway": "%(phone_number)s@page.att.net"
        }
    },
    {
        "pk": 10,
        "model": "sms.Carrier",
        "fields": {
            "name": "Bell Mobility & Solo Mobile (Canada)",
            "gateway": "%(phone_number)s@txt.bell.ca or"
        }
    },
    {
        "pk": 11,
        "model": "sms.Carrier",
        "fields": {
            "name": "Boost Mobile",
            "gateway": "%(phone_number)s@myboostmobile.com"
        }
    },
    {
        "pk": 12,
        "model": "sms.Carrier",
        "fields": {
            "name": "BPL Mobile (Mumbai, India)",
            "gateway": "%(phone_number)s@bplmobile.com"
        }
    },
    {
        "pk": 13,
        "model": "sms.Carrier",
        "fields": {
            "name": "Cellular One (Dobson)",
            "gateway": "%(phone_number)s@mobile.celloneusa.com"
        }
    },
    {
        "pk": 14,
        "model": "sms.Carrier",
        "fields": {
            "name": "Cingular (Postpaid)",
            "gateway": "%(phone_number)s@cingularme.com"
        }
    },
    {
        "pk": 15,
        "model": "sms.Carrier",
        "fields": {
            "name": "Centennial Wireless",
            "gateway": "%(phone_number)s@cwemail.com"
        }
    },
    {
        "pk": 16,
        "model": "sms.Carrier",
        "fields": {
            "name": "Cingular (GoPhone prepaid)",
            "gateway": "%(phone_number)s@cingularme.com"
        }
    },
    {
        "pk": 17,
        "model": "sms.Carrier",
        "fields": {
            "name": "Claro (Brasil)",
            "gateway": "%(phone_number)s@clarotorpedo.com.br"
        }
    },
    {
        "pk": 18,
        "model": "sms.Carrier",
        "fields": {
            "name": "Claro (Nicaragua)",
            "gateway": "%(phone_number)s@ideasclaro-ca.com"
        }
    },
    {
        "pk": 19,
        "model": "sms.Carrier",
        "fields": {
            "name": "Comcel",
            "gateway": "%(phone_number)s@comcel.com.co"
        }
    },
    {
        "pk": 20,
        "model": "sms.Carrier",
        "fields": {
            "name": "Cricket",
            "gateway": "%(phone_number)s@sms.mycricket.com"
        }
    },
    {
        "pk": 21,
        "model": "sms.Carrier",
        "fields": {
            "name": "CTI",
            "gateway": "%(phone_number)s@sms.ctimovil.com.ar"
        }
    },
    {
        "pk": 22,
        "model": "sms.Carrier",
        "fields": {
            "name": "Emtel (Mauritius)",
            "gateway": "%(phone_number)s@emtelworld.net"
        }
    },
    {
        "pk": 23,
        "model": "sms.Carrier",
        "fields": {
            "name": "Fido(Canada)",
            "gateway": "%(phone_number)s@fido.ca"
        }
    },
    {
        "pk": 24,
        "model": "sms.Carrier",
        "fields": {
            "name": "General Communications Inc.",
            "gateway": "%(phone_number)s@msg.gci.net"
        }
    },
    {
        "pk": 25,
        "model": "sms.Carrier",
        "fields": {
            "name": "Globalstar (satellite)",
            "gateway": "%(phone_number)s@msg.globalstarusa.com"
        }
    },
    {
        "pk": 26,
        "model": "sms.Carrier",
        "fields": {
            "name": "Helio",
            "gateway": "%(phone_number)s@myhelio.com"
        }
    },
    {
        "pk": 27,
        "model": "sms.Carrier",
        "fields": {
            "name": "Illinois Valley Cellular",
            "gateway": "%(phone_number)s@ivctext.com"
        }
    },
    {
        "pk": 28,
        "model": "sms.Carrier",
        "fields": {
            "name": "Iridium (satellite)",
            "gateway": "%(phone_number)s@msg.iridium.com"
        }
    },
    {
        "pk": 29,
        "model": "sms.Carrier",
        "fields": {
            "name": "i wireless",
            "gateway": "%(phone_number)s.iws@iwspcs.net"
        }
    },
    {
        "pk": 30,
        "model": "sms.Carrier",
        "fields": {
            "name": "Meteor (Ireland)",
            "gateway": "%(phone_number)s@sms.mymeteor.ie"
        }
    },
    {
        "pk": 31,
        "model": "sms.Carrier",
        "fields": {
            "name": "Mero Mobile (Nepal)",
            "gateway": "%(phone_number)s@sms.spicenepal.com"
        }
    },
    {
        "pk": 32,
        "model": "sms.Carrier",
        "fields": {
            "name": "MetroPCS",
            "gateway": "%(phone_number)s@mymetropcs.com"
        }
    },
    {
        "pk": 33,
        "model": "sms.Carrier",
        "fields": {
            "name": "Movicom",
            "gateway": "%(phone_number)s@movimensaje.com.ar"
        }
    },
    {
        "pk": 34,
        "model": "sms.Carrier",
        "fields": {
            "name": "Mobitel (Sri Lanka)",
            "gateway": "%(phone_number)s@sms.mobitel.lk"
        }
    },
    {
        "pk": 35,
        "model": "sms.Carrier",
        "fields": {
            "name": "Movistar (Colombia)",
            "gateway": "%(phone_number)s@movistar.com.co"
        }
    },
    {
        "pk": 36,
        "model": "sms.Carrier",
        "fields": {
            "name": "MTN (South Africa)",
            "gateway": "%(phone_number)s@sms.co.za"
        }
    },
    {
        "pk": 37,
        "model": "sms.Carrier",
        "fields": {
            "name": "MTS (Canada)",
            "gateway": "%(phone_number)s@text.mtsmobility.com"
        }
    },
    {
        "pk": 38,
        "model": "sms.Carrier",
        "fields": {
            "name": "Nextel (United States)",
            "gateway": "%(phone_number)s@messaging.nextel.com"
        }
    },
    {
        "pk": 39,
        "model": "sms.Carrier",
        "fields": {
            "name": "Nextel (M\u00c3\u00a9xico)",
            "gateway": "%(phone_number)s@msgnextel.com.mx"
        }
    },
    {
        "pk": 40,
        "model": "sms.Carrier",
        "fields": {
            "name": "Nextel (Argentina)",
            "gateway": "TwoWay.%(phone_number)s@nextel.net.ar"
        }
    },
    {
        "pk": 41,
        "model": "sms.Carrier",
        "fields": {
            "name": "Orange Polska (Poland)",
            "gateway": "digit@orange.pl"
        }
    },
    {
        "pk": 42,
        "model": "sms.Carrier",
        "fields": {
            "name": "Plus GSM (Poland)",
            "gateway": "%(phone_number)s@text.plusgsm.pl"
        }
    },
    {
        "pk": 43,
        "model": "sms.Carrier",
        "fields": {
            "name": "President's Choice (Canada)",
            "gateway": "%(phone_number)s@txt.bell.ca"
        }
    },
    {
        "pk": 44,
        "model": "sms.Carrier",
        "fields": {
            "name": "Qwest",
            "gateway": "%(phone_number)s@qwestmp.com"
        }
    },
    {
        "pk": 45,
        "model": "sms.Carrier",
        "fields": {
            "name": "Rogers (Canada)",
            "gateway": "%(phone_number)s@pcs.rogers.com"
        }
    },
    {
        "pk": 46,
        "model": "sms.Carrier",
        "fields": {
            "name": "Sasktel (Canada)",
            "gateway": "%(phone_number)s@sms.sasktel.com"
        }
    },
    {
        "pk": 47,
        "model": "sms.Carrier",
        "fields": {
            "name": "Setar Mobile email (Aruba)",
            "gateway": "%(phone_number)s@mas.aw"
        }
    },
    {
        "pk": 48,
        "model": "sms.Carrier",
        "fields": {
            "name": "Sprint (PCS)",
            "gateway": "%(phone_number)s@messaging.sprintpcs.com"
        }
    },
    {
        "pk": 49,
        "model": "sms.Carrier",
        "fields": {
            "name": "Sprint (Nextel)",
            "gateway": "%(phone_number)s@messaging.nextel.com"
        }
    },
    {
        "pk": 50,
        "model": "sms.Carrier",
        "fields": {
            "name": "Suncom",
            "gateway": "%(phone_number)s@tms.suncom.com"
        }
    },
    {
        "pk": 51,
        "model": "sms.Carrier",
        "fields": {
            "name": "T-Mobile",
            "gateway": "%(phone_number)s@tmomail.net"
        }
    },
    {
        "pk": 52,
        "model": "sms.Carrier",
        "fields": {
            "name": "T-Mobile (Austria)",
            "gateway": "%(phone_number)s@sms.t-mobile.at"
        }
    },
    {
        "pk": 53,
        "model": "sms.Carrier",
        "fields": {
            "name": "T-Mobile (UK)",
            "gateway": "%(phone_number)s@t-mobile.uk.net"
        }
    },
    {
        "pk": 54,
        "model": "sms.Carrier",
        "fields": {
            "name": "Telus Mobility (Canada)",
            "gateway": "%(phone_number)s@msg.telus.com"
        }
    },
    {
        "pk": 55,
        "model": "sms.Carrier",
        "fields": {
            "name": "Thumb Cellular",
            "gateway": "%(phone_number)s@sms.thumbcellular.com"
        }
    },
    {
        "pk": 56,
        "model": "sms.Carrier",
        "fields": {
            "name": "Tigo (Formerly Ola)",
            "gateway": "%(phone_number)s@sms.tigo.com.co"
        }
    },
    {
        "pk": 57,
        "model": "sms.Carrier",
        "fields": {
            "name": "Unicel",
            "gateway": "%(phone_number)s@utext.com"
        }
    },
    {
        "pk": 58,
        "model": "sms.Carrier",
        "fields": {
            "name": "US Cellular",
            "gateway": "%(phone_number)s@email.uscc.net"
        }
    },
    {
        "pk": 59,
        "model": "sms.Carrier",
        "fields": {
            "name": "Verizon",
            "gateway": "%(phone_number)s@vtext.com"
        }
    },
    {
        "pk": 60,
        "model": "sms.Carrier",
        "fields": {
            "name": "Virgin Mobile (Canada)",
            "gateway": "%(phone_number)s@vmobile.ca"
        }
    },
    {
        "pk": 61,
        "model": "sms.Carrier",
        "fields": {
            "name": "Virgin Mobile (USA)",
            "gateway": "%(phone_number)s@vmobl.com"
        }
    }
]

