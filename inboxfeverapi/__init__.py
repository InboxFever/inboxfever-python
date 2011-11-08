import sys
from simplejson import loads, dumps
from traceback import format_tb

import logging
logging = logging.getLogger('inboxfeverapi')

def getEmailRequestFromJSON(request):
    try:
        d = loads(request)
        email_request = Email_Request(d)
        return email_request
    except:
        logging.error('Got exception converting from JSON to Email_Request: \n%s\n%s\n%s\n%s\n', request, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])))

    return None

def JSONSerializeHandler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'toDict'):
        return obj.toDict()
    else:
        logging.error('problem serilaizing: -->%s<--', obj)
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


class InboxFeverObject():
    def getJSON(self):
        return dumps(self, default=JSONSerializeHandler)

    @classmethod
    def fromJSON(cls, jsonString):
        """ converts a jsonString representing a dictionary form of an InboxFeverObject to an InboxFeverObject object """
        try:
            d = loads(jsonString)
        except:
            logging.error('Got exception converting from JSON: \n%s\n%s\n%s\n%s\n', jsonString, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])))
            d = {}
        return cls.fromDict(d)


class Email_Response(InboxFeverObject):
    def __init__(self, subject, to_address, from_address=None, context={}, attachments=[], email_id=None, app_id=None, template=None, text=None, html=None):

        self.subject = subject
        self.to_address = to_address
        self.from_address = from_address
        self.context = context
        self.attachments = attachments
        self.email_id = email_id
        self.template = template
        self.request_id = None
        self.app_id = app_id

        if(text == ""):
            self.text = None
        else:
            self.text = text

        if(html == ""):
            self.html = None
        else:
            self.html = html

    @classmethod
    def fromDict(cls, d):
        template = d.get('template', None)
        subject = d.get('subject')
        to_address = Email_Address({"address":d.get('to')})
        print "to address: "+str(to_address.address)
        from_address = d.get('from')
        context = d.get('context', {})
        attachments = d.get('attachments', [])
        app_id = d.get('app_id')
        email_id = d.get('email_id')

        if(d.get('text') == ""):
            text = None
        else:
            text = d.get('text', None)

        if(d.get('html') == ""):
            html = None
        else:
            html = d.get('html', None)

        return cls(subject, to_address, from_address, context, attachments, email_id, app_id, template, text, html)

    def toDict(self):
        d = {}
        d['subject'] = self.subject
        d['to'] = self.to_address
        d['from'] = self.from_address
        d['context'] = self.context
        d['attachments'] = self.attachments
        d['app_id'] = self.app_id
        d['email_id'] = self.email_id
        d['template'] = self.template
        d['text'] = self.text
        d['html'] = self.html
        return d



class Email_Address(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.name = d.get('name')
            self.address = d.get('address')
            self.params = d.get('params')
        except:
            logging.error('Got exception on Email_Address init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )

    def toDict(self):
        return self.__dict__


class Email_Request(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.updated = d.get('updated')
            self.created = d.get('created')
            self.thread_id = d.get('thread_id')
            self.email_id = d.get('email_id')
            self.request_id = d.get('request_id')
            self.from_address = Email_Address(d.get('from', {}))
            self.reply_to = d.get('reply_to')
            self.to_address = Email_Address(d.get('to', {}))
            self.headers = d.get('headers', {})
            self.to_list = [Email_Address(address_dict) for address_dict in d.get('to_list')]
            self.cc_list = [Email_Address(address_dict) for address_dict in d.get('cc_list')]
            self.attachments = d.get('attachments', [])
            self.text = d.get('text')
            self.html = d.get('html')
            self.subject = d.get('subject')
        except:
            logging.error('Got exception on Email_Request init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )

    def toDict(self):
        d = {}
        d['updated'] = self.updated
        d['created'] = self.created
        d['thread_id'] = self.thread_id
        d['email_id'] = self.email_id
        d['request_id'] = self.request_id
        d['from'] = self.from_address
        d['reply_to'] = self.reply_to
        d['to'] = self.to_address
        d['headers'] = self.headers
        d['to_list'] = self.to_list
        d['cc_list'] = self.cc_list
        d['attachments'] = self.attachments
        d['text'] = self.text
        d['html'] = self.html
        d['subject'] = self.subject

        return d

