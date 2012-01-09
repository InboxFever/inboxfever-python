import sys, hashlib

try: from simplejson import loads, dumps
except ImportError: from json import loads, dumps

from traceback import format_tb
import urllib2


import logging
logger = logging.getLogger('inboxfever-api')

api_endpoint = "https://api.inboxfever.com/api/v1/email/send/"

class InboxFever():


    email_handlers = {}
    def __init__(self, app_id, app_secret):

        self.app_id = app_id
        self.app_secret = app_secret


    def send_email(self, to_address, from_address=None, subject=None, text=None, html=None, attachments=[]):

        # TODO: process cc list / to list
        email = Email.fromDict({"to":to_address,
                                "from":from_address,
                                "subject":subject,
                                "text":text,
                                "html":html,
                                "attachments":attachments,
                                "app_id":self.app_id,
                                "secret":self.app_secret})

        try:
            result = urllib2.urlopen(api_endpoint, data=email.getJSON())
        except Exception, e:
            logging.error( "Error: %s email_data=%s endpoint: %s",  str(e), email.getJSON(), api_endpoint )

    def isRequestValid(self, headers, request_body):

        # this should look for the x-if-auth header
        # then prepend the app_secret to the request body

        if "x-if-auth" in headers:
            auth_hash = hashlib.sha1(request_body+self.app_secret).hexdigest()
            if auth_hash == headers['x-if-auth']:
                return True

        return False


def getEmailRequestFromJSON(request):
    try:
        d = loads(request)
        email = Email.fromDict(d)
        return email
    except:
        logger.error('Got exception converting from JSON to Email_Request: \n%s\n%s\n%s\n%s\n', request, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])))

    return None

def JSONSerializeHandler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'toDict'):
        return obj.toDict()
    else:
        logger.error('problem serilaizing: -->%s<--', obj)
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
            logger.error('Got exception converting from JSON: \n%s\n%s\n%s\n%s\n', jsonString, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])))
            d = {}
        return cls.fromDict(d)


class Email(InboxFeverObject):

    def __init__(self, subject, to_address, from_address=None, status=None, context={},
                 attachments=[], email_id=None, app_id=None, request_id=None,
                 template=None, text=None, html=None, secret=None, updated=None,
                 created=None, thread_id=None, reply_to=None, headers=[], to_list=[], cc_list=[]):

        self.subject = subject
        self.to_address = to_address
        self.status = status
        self.from_address = from_address
        self.context = context
        self.attachments = attachments
        self.email_id = email_id
        self.template = template
        self.request_id = request_id
        self.app_id = app_id
        self.secret = secret
        self.updated = updated
        self.created = created
        self.thread_id = thread_id
        self.reply_to = reply_to
        self.headers = headers
        self.to_list = [Email_Address(address_dict) for address_dict in to_list]
        self.cc_list = [Email_Address(address_dict) for address_dict in cc_list]




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


        if type(d.get('to')) is dict:
            to_address = Email_Address(d.get('to'))
        else:
            to_address = Email_Address({"address":d.get('to')})

        #logging.info("from address: %s", str(d.get('from'))

        if type(d.get('from')) is dict:
            from_address = Email_Address(d.get('from'))
        elif d.get('from') is not None:
            from_address = Email_Address({"address":d.get('from')})
        else:
            from_address = None

        status = d.get('status')
        context = d.get('context', {})
        attachments = d.get('attachments', [])
        app_id = d.get('app_id')
        email_id = d.get('email_id')
        request_id = d.get('request_id')
        secret = d.get('secret')
        updated = d.get('updated')
        created = d.get('created')
        thread_id = d.get('thread_id')

        if type(d.get('reply_to')) is dict:
            reply_to  = Email_Address(d.get('replay_to'))
        elif d.get('reply_to') is not None:
            reply_to = Email_Address({"address":d.get('reply_to')})
        else:
            reply_to = None


        headers = d.get('headers', {})
        to_list = [Email_Address(address_dict) for address_dict in d.get('to_list', [])]
        cc_list = [Email_Address(address_dict) for address_dict in d.get('cc_list', [])]


        if(d.get('text') == ""):
            text = None
        else:
            text = d.get('text', None)

        if(d.get('html') == ""):
            html = None
        else:
            html = d.get('html', None)

        return cls(subject, to_address, from_address, status, context, attachments,
                   email_id, app_id, request_id, template, text, html, secret, updated,
                   created, thread_id, reply_to, headers, to_list, cc_list)

    def toDict(self):
        d = {}
        d['subject'] = self.subject
        d['to'] = self.to_address
        d['from'] = self.from_address
        d['context'] = self.context
        d['attachments'] = self.attachments
        d['app_id'] = self.app_id
        d['email_id'] = self.email_id
        d['request_id'] = self.request_id
        d['template'] = self.template
        d['text'] = self.text
        d['html'] = self.html
        if hasattr(self, "secret"):
            d['secret'] = self.secret

        d['updated'] = self.updated
        d['created'] = self.created
        d['thread_id'] = self.thread_id
        d['reply_to'] = self.reply_to
        d['headers'] = self.headers
        d['to_list'] = self.to_list
        d['cc_list'] = self.cc_list

        return d


class Email_Address(InboxFeverObject):
    def __init__(self, d):
        if d is None:
            d = {}
        elif isinstance(d, Email_Address):
            d = d.toDict()
                
        try:
            self.name = d.get('name')
            self.address = d.get('address')
            self.params = d.get('params')
        except:
            logger.error('Got exception on Email_Address init: \n%s\n%s\n%s\n%s\n', d, sys.exc_info()[0],sys.exc_info()[1],''.join(format_tb(sys.exc_info()[2])), )
    def toDict(self):
        return self.__dict__
    