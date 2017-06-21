import time
import requests
import hmac
import hashlib
import base64
from datetime import datetime
import collections
from enum import Enum

from xml.etree import ElementTree

from .models import Orders, Payments, Shipments, ProcessStatus


__all__ = ['PlazaAPI']


class TransporterCode(Enum):
    """
    https://developers.bol.com/documentatie/plaza-api/developer-guide-plaza-api/appendix-a-transporters/
    """
    DHLFORYOU = 'DHLFORYOU'
    UPS = 'UPS'
    KIALA_BE = 'KIALA-BE'
    KIALA_NL = 'KIALA-NL'
    TNT = 'TNT'
    TNT_EXTRA = 'TNT-EXTRA'
    TNT_BRIEF = 'TNT_BRIEF'
    TNT_EXPRESS = 'TNT-EXPRESS'
    SLV = 'SLV'
    DYL = 'DYL'
    DPD_NL = 'DPD-NL'
    DPD_BE = 'DPD-BE'
    BPOST_BE = 'BPOST_BE'
    BPOST_BRIEF = 'BPOST_BRIEF'
    BRIEFPOST = 'BRIEFPOST'
    GLS = 'GLS'
    FEDEX_NL = 'FEDEX_NL'
    FEDEX_BE = 'FEDEX_BE'
    OTHER = 'OTHER'
    DHL = 'DHL'
    DHL_DE = 'DHL_DE'
    DHL_GLOBAL_MAIL = 'DHL-GLOBAL-MAIL'
    TSN = 'TSN'
    FIEGE = 'FIEGE'
    TRANSMISSION = 'TRANSMISSION'
    PARCEL_NL = 'PARCEL-NL'
    LOGOIX = 'LOGOIX'
    PACKS = 'PACKS'

    @classmethod
    def to_string(cls, transporter_code):
        if isinstance(transporter_code, TransporterCode):
            transporter_code = transporter_code.value
        assert transporter_code in map(
            lambda c: c.value, list(TransporterCode))
        return transporter_code


class MethodGroup(object):

    def __init__(self, api, group):
        self.api = api
        self.group = group

    def request(self, method, path='', params={}, data=None):
        uri = '/services/rest/{group}/{version}{path}'.format(
            group=self.group,
            version=self.api.version,
            path=path)
        xml = self.api.request(method, uri, params=params, data=data)
        return xml

    def create_request_xml(self, root, **kwargs):
        elements = self._create_request_xml_elements(1, **kwargs)
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<{root} xmlns="https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
{elements}
</{root}>
""".format(root=root, elements=elements)
        return xml

    def _create_request_xml_elements(self, indent, **kwargs):
        # sort to make output deterministic
        kwargs = collections.OrderedDict(sorted(kwargs.items()))
        xml = ''
        for tag, value in kwargs.items():
            if value is not None:
                prefix = ' ' * 4 * indent
                if isinstance(value, dict):
                    text = '\n{}\n{}'.format(
                        self._create_request_xml_elements(
                            indent + 1, **value),
                        prefix)
                elif isinstance(value, datetime):
                    text = value.isoformat()
                else:
                    text = str(value)
                # TODO: Escape! For now this will do I am only dealing
                # with track & trace codes and simplistic IDs...
                if xml:
                    xml += '\n'
                xml += prefix
                xml += "<{tag}>{text}</{tag}>".format(
                    tag=tag,
                    text=text
                )
        return xml


class OrderMethods(MethodGroup):

    def __init__(self, api):
        super(OrderMethods, self).__init__(api, 'orders')

    def list(self):
        xml = self.request('GET')
        return Orders.parse(self.api, xml)


class PaymentMethods(MethodGroup):

    def __init__(self, api):
        super(PaymentMethods, self).__init__(api, 'payments')

    def list(self, year, month):
        xml = self.request('GET', '/%d%02d' % (year, month))
        return Payments.parse(self.api, xml)


class ProcessStatusMethods(MethodGroup):

    def __init__(self, api):
        super(ProcessStatusMethods, self).__init__(api, 'process-status')

    def get(self, id):
        xml = self.request('GET', '/{}'.format(id))
        return ProcessStatus.parse(self.api, xml)


class ShipmentMethods(MethodGroup):

    def __init__(self, api):
        super(ShipmentMethods, self).__init__(api, 'shipments')

    def list(self, page=None):
        if page is not None:
            params = {'page': page}
        else:
            params = None
        xml = self.request('GET', params=params)
        return Shipments.parse(self.api, xml)

    def create(self, order_item_id, date_time, expected_delivery_date,
               shipment_reference=None, transporter_code=None,
               track_and_trace=None):
        if transporter_code:
            transporter_code = TransporterCode.to_string(
                transporter_code)
        xml = self.create_request_xml(
            'ShipmentRequest',
            OrderItemId=order_item_id,
            DateTime=date_time,
            ShipmentReference=shipment_reference,
            ExpectedDeliveryDate=expected_delivery_date,
            Transport={
                'TransporterCode': transporter_code,
                'TrackAndTrace': track_and_trace
            })
        response = self.request('POST', data=xml)
        return ProcessStatus.parse(self.api, response)


class TransportMethods(MethodGroup):

    def __init__(self, api):
        super(TransportMethods, self).__init__(api, 'transports')

    def update(self, id, transporter_code, track_and_trace):
        transporter_code = TransporterCode.to_string(transporter_code)
        xml = self.create_request_xml(
            'ChangeTransportRequest',
            TransporterCode=transporter_code,
            TrackAndTrace=track_and_trace)
        response = self.request('PUT', '/{}'.format(id), data=xml)
        return ProcessStatus.parse(self.api, response)


class PlazaAPI(object):

    def __init__(self, public_key, private_key, test=False, timeout=None,
                 session=None):
        self.public_key = public_key
        self.private_key = private_key
        self.url = 'https://%splazaapi.bol.com' % ('test-' if test else '')
        self.version = 'v2'
        self.timeout = timeout
        self.orders = OrderMethods(self)
        self.payments = PaymentMethods(self)
        self.shipments = ShipmentMethods(self)
        self.process_status = ProcessStatusMethods(self)
        self.transports = TransportMethods(self)
        self.session = session or requests.Session()

    def request(self, method, uri, params={}, data=None):
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
        h = hmac.new(
            self.private_key.encode('utf-8'),
            msg.encode('utf-8'), hashlib.sha256)
        b64 = base64.b64encode(h.digest())

        signature = self.public_key.encode('utf-8') + b':' + b64

        headers = {'Content-Type': content_type,
                   'X-BOL-Date': date,
                   'X-BOL-Authorization': signature}
        request_kwargs = {
            'method': method,
            'url': self.url + uri,
            'params': params,
            'headers': headers,
            'timeout': self.timeout,
        }
        if data:
            request_kwargs['data'] = data
        resp = self.session.request(**request_kwargs)
        resp.raise_for_status()
        tree = ElementTree.fromstring(resp.content)
        return tree
