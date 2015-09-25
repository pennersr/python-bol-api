import time
import requests
import hmac
import hashlib
import base64
from xml.etree import ElementTree

__all__ = ['PlazaAPI']


from .models import OpenOrders, Payments


class MethodGroup(object):

    def __init__(self, api, group):
        self.api = api
        self.group = group

    def request(self, method, name):
        uri = '/services/rest/{group}/{version}/{name}'.format(
            group=self.group,
            version=self.api.version,
            name=name)
        xml = self.api.request(method, uri)
        return xml


class OrderMethods(MethodGroup):

    def __init__(self, api):
        super(OrderMethods, self).__init__(api, 'orders')

    def open(self):
        xml = self.request('GET', 'open')
        return OpenOrders.parse(self.api, xml)


class PaymentMethods(MethodGroup):

    def __init__(self, api):
        super(PaymentMethods, self).__init__(api, 'payments')

    def payments(self, year, month):
        xml = self.request('GET', 'payments/%d%02d' % (year, month))
        return Payments.parse(self.api, xml)


class PlazaAPI(object):

    def __init__(self, public_key, private_key, test=False):
        self.public_key = public_key
        self.private_key = private_key
        self.url = 'https://%splazaapi.bol.com' % ('test-' if test else '')
        self.version = 'v1'
        self.orders = OrderMethods(self)
        self.payments = PaymentMethods(self)

    def request(self, method, uri):
        content_type = 'application/xml; charset=UTF-8'
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        msg = """{method}

{content_type}
{date}
x-bol-date:{date}
{uri}""".format(content_type=content_type,
                date=date,
                method=method,
                uri=uri)
        h = hmac.new(self.private_key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256)
        b64 = base64.b64encode(h.digest())

        signature = self.public_key.encode('utf-8') + b':' + b64

        headers = {'Content-Type': content_type,
                   'X-BOL-Date': date,
                   'X-BOL-Authorization': signature}
        resp = requests.get(self.url + uri, headers=headers)
        resp.raise_for_status()
        tree = ElementTree.fromstring(resp.content)
        return tree
