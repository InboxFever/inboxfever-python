import sys
from simplejson import loads, dumps
from traceback import format_tb

import logging
logging = logging.getLogger('inboxfeverapi')

def getEmailActivityFromJSON(request):
    try:
        d = loads(request)
        email_activity = Email_Activity(d)
        return email_activity
    except:
        logging.error('Got exception converting from JSON: \n%s\n%s\n%s\n%s\n', request, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])))
        
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


class EmailResponse(InboxFeverObject):
    def __init__(self, app, template, subject, to_email, from_email, context={}, attachments=[], token=None):
        self.app = app
        self.template = template
        self.subject = subject
        self.to_email = to_email
        self.from_email = from_email
        self.context = context
        self.attachments = [EmailAttachment(url=s) for s in attachments]
        self.token = token
        
    @classmethod
    def fromJSON(cls, jsonString):
        """ converts a jsonString representing a dictionary form of Email_Response to an EmailResponse object """
        try:
            d = loads(jsonString)
        except:
            logging.error('Got exception converting from JSON: \n%s\n%s\n%s\n%s\n', jsonString, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])))
            d = {}
        return EmailResponse.fromDict(d)

    @classmethod
    def fromDict(cls, d):            
        app = Email_App(d.get('app'))
        template = d.get('template')
        subject = d.get('subject')
        to_email = Email_Address(d.get('to_email'))
        from_email = d.get('from_email')
        context = d.get('context')
        attachments = [Email_Attachment(dict=i) for i in d.get('attachments', [])]
        token = d.get('token')
        return EmailResponse(app, template, subject, to_email, from_email, context, attachments, token)

    def toDict(self):
        d = {}
        d['app'] = self.app
        d['template'] = self.template
        d['subject'] = self.subject
        d['to_email'] = self.to_email
        d['from_email'] = self.from_email
        d['context'] = self.context
        d['attachments'] = self.attachments
        d['token'] = self.token
        return d
    

class Email_Attachment(InboxFeverObject):
    def __init__(self, **kwargs):
        if 'dict' in kwargs:
            kwargs = kwargs.get('dict')
        
        self.url = kwargs.get('url')
        self.name = kwargs.get('name', 'attachment')
        
                
    def toDict(self):
        return self.__dict__
    
    def __repr__(self):
        return "Email_Attachment name: %(name)s url: %(url)s" % self.__dict__
    
        

class Email_Address(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.email_address = d.get('email_address')
            self.is_user = d.get('is_user')
            self.is_app = d.get('is_app')
            self.is_active = d.get('active')
            self.created = d.get('created')
            self.updated = d.get('updated')
            self.uasage_count = d.get('usage_count')
        except:
            logging.error('Got exception on init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )
    
    def toDict(self):
        d = {}
        d['email_address'] = self.email_address
        d['is_user'] = self.is_user
        d['is_app'] = self.is_app
        d['active'] = self.is_active
        d['created'] = self.created
        d['updated'] = self.updated
        d['usage_count'] = self.uasage_count
        return d


        

class Email_App_Author(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.fullname = d.get('fullname')
            self.email_address = d.get('email_address')
            self.website = d.get('website')            
        except:
            logging.error('Got exception on init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )
    
    def toDict(self):
        d = {}
        d['fullname'] = self.fullname
        d['email_address'] = self.email_address
        d['website'] = self.website            

        return d

class Email_App(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.name = d.get('name')
            self.title = d.get('title')
            self.author = Email_App_Author(d.get('author'))
            self.description = d.get('description')
            self.help = d.get('help')
            self.example_subject = d.get('example_subject')
            self.image_url = d.get('image_url')
            self.requires_activation = d.get('requires_activation')
            self.launched = d.get('launched')
            self.email_address = d.get('email_address')
            self.mailto = d.get('mail_to')
            self.from_address = d.get('from_address')
            self.created = d.get('created')
            self.updated = d.get('updated')        
        except:
            logging.error('Got exception on init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )
    
    def toDict(self):
        d = {}
        d['name'] = self.name
        d['title'] = self.title
        d['author'] = self.author
        d['description'] = self.description
        d['help'] = self.help
        d['example_subject'] = self.example_subject
        d['image_url'] = self.image_url
        d['requires_activation'] = self.requires_activation
        d['launched'] = self.launched
        d['email_address'] = self.email_address
        d['mail_to'] = self.mailto
        d['from_address'] = self.from_address
        d['created'] = self.created
        d['updated'] = self.updated        
        
        return d


class Email(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.to_address = Email_Address(d.get('to_address'))
            self.from_address = Email_Address(d.get('from_address'))
            self.subject = d.get('subject',u"")
            self.text = d.get('text',u"")
            self.html = d.get('html',u"")
            self.attachments = d.get('attachments',u"[]")
            self.created = d.get('created')
            self.updated = d.get('updated')
            self.params = d.get('params',u"")
            self.from_params = d.get('from_params',u"")
        except:
            logging.error('Got exception on init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )
    
    def toDict(self):
        d = {}
        d['to_address'] = self.to_address
        d['from_address'] = self.from_address
        d['subject'] = self.subject
        d['text'] = self.text
        d['html'] = self.html
        d['attachments'] = self.attachments
        d['created'] = self.created
        d['updated'] = self.updated
        d['params'] = self.params
        d['from_params'] = self.from_params

        return d
            

class Email_Activity(InboxFeverObject):
    def __init__(self, d):
        if not d:
            d = {}
        try:
            self.email_address = Email_Address(d.get('email_address'))
            self.email_app = Email_App(d.get('email_app'))
            self.in_msg = Email(d.get('in_msg'))
            self.out_msg = Email(d.get('out_msg'))
            self.created = d.get('created')
            self.updated = d.get('updated')
            self.started_processing = d.get('started_processing')
            self.stopped_processing = d.get('stopped_processing')
            self.token = d.get('token')
        except:
            logging.error('Got exception on init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )

    def toDict(self):
        d = {}
        d['email_address'] = self.email_address
        d['email_app'] = self.email_app
        d['in_msg'] = self.in_msg
        d['out_msg'] = self.out_msg
        d['created'] = self.created
        d['updated'] = self.updated
        d['started_processing'] = self.started_processing
        d['stopped_processing'] = self.stopped_processing
        d['token'] = self.token
        
        return d

    
