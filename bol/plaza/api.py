import time
import requests
import hmac
import hashlib
import base64
from xml.etree import ElementTree

from .models import OpenOrders, Payments

__all__ = ['PlazaAPI']


PROCESS_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<ProcessOrders xmlns="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd">'  # noqa
        '<Shipments>'
            '<Shipment>'
                '<OrderId>{order_id}</OrderId>'
                '<DateTime>{date_time}</DateTime>'
                '<Transporter>'
                    '<Code>{code}</Code>'
                    '<TrackAndTraceCode>{transporter_code}</TrackAndTraceCode>'
                '</Transporter>'
                '<OrderItems>'
                    '{order_item_ids}'
                '</OrderItems>'
            '</Shipment>'
        '</Shipments>'
    '</ProcessOrders>')


# https://developers.bol.com/documentatie/plaza-api/developer-guide-plaza-api/appendix-a-transporters/
TRANSPORTER_CODES = {
    'DHLFORYOU',
    'UPS',
    'KIALA_BE',
    'KIALA_NL',
    'TNT',
    'TNT_EXTRA',
    'TNT_BRIEF',
    'SLV',
    'DYL',
    'DPD_NL',
    'DPD_BE',
    'BPOST_BE',
    'BPOST_BRIEF',
    'BRIEFPOST',
    'GLS',
    'FEDEX_NL',
    'FEDEX_BE',
    'OTHER',
    'DHL',
}


class MethodGroup(object):

    def __init__(self, api, group):
        self.api = api
        self.group = group

    def request(self, method, name, payload=None):
        uri = '/services/rest/{group}/{version}/{name}'.format(
            group=self.group,
            version=self.api.version,
            name=name)
        xml = self.api.request(method, uri, payload)
        return xml


class OrderMethods(MethodGroup):

    def __init__(self, api):
        super(OrderMethods, self).__init__(api, 'orders')

    def open(self):
        xml = self.request('GET', 'open')
        return OpenOrders.parse(self.api, xml)

    def process(self, order_id, date_time, code, transporter_code,
                order_item_ids):
        assert transporter_code in TRANSPORTER_CODES

        payload = PROCESS_XML.format(
            order_id=order_id,
            date_time=date_time.replace(microsecond=0).isoformat(),
            code=code,
            transporter_code=transporter_code,
            order_item_ids=''.join([
                '<Id>{}</Id>'.format(i) for i in order_item_ids]))

        response = self.request('POST', 'process', payload)
        return response.find('{http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd}ProcessOrderId').text


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

    def request(self, method, uri, payload=None):
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
        if method == 'GET':
            resp = requests.get(self.url + uri, headers=headers)
        elif method == 'POST':
            resp = requests.post(self.url + uri, headers=headers, data=payload)
        else:
            raise ValueError
        resp.raise_for_status()
        tree = ElementTree.fromstring(resp.content)
        return tree
