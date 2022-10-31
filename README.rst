==============
python-bol-api
==============

.. image:: https://travis-ci.org/pennersr/python-bol-api.png
   :target: http://travis-ci.org/pennersr/python-bol-api

.. image:: https://img.shields.io/pypi/v/python-bol-api.svg
   :target: https://pypi.python.org/pypi/python-bol-api

.. image:: https://pennersr.github.io/img/bitcoin-badge.svg
   :target: https://blockchain.info/address/1AJXuBMPHkaDCNX2rwAy34bGgs7hmrePEr

.. image:: https://pennersr.github.io/img/emacs-badge.svg
   :target: https://www.gnu.org/software/emacs/

A Python wrapper for the bol.com API. Currently rather incomplete, as
it offers only those methods required for my own projects so far.


Open API
========

Instantiate the API::

    >>> from bol.openapi.api import OpenAPI
    >>> api = OpenAPI('api_key')

Invoke a method::

    >>> data = api.catalog.products(['1004004011187773', '1004004011231766'])

JSON data is returned "as is":

    >>> data['products'][0]['ean']
    u'0093155141650'


Plaza API
=========

Instantiate the API::

    >>> from bol.plaza.api import PlazaAPI
    >>> api = PlazaAPI('public_key', 'private_key', test=True)

Invoke a method::

    >>> open_orders = api.orders.list()

Fields are derived 1:1 from the bol.com API XML, including
CamelCase conventions::

    >>> open_orders[0].Buyer.BillingDetails.Streetname
    'Billingstraat'

Fields are properly typed::

    >>> open_orders[0].Paid
    True
    >>> open_orders[0].OrderItems[0].TransactionFee
    Decimal('19.12')
    >>> open_orders[0].DateTimeDropShipper
    datetime.datetime(2014, 2, 10, 12, 7, 7)

Access the underlying XML::

    >>> from xml.etree import ElementTree
    >>> ElementTree.tostring(open_orders[0].Buyer.BillingDetails.xml)
    '<ns0:BillingDetails xmlns:ns0="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd"><ns0:SalutationCode>02</ns0:SalutationCode><ns0:FirstName>Jans</ns0:FirstName><ns0:Surname>Janssen</ns0:Surname><ns0:Streetname>Billingstraat</ns0:Streetname><ns0:Housenumber>1</ns0:Housenumber><ns0:HousenumberExtended>a</ns0:HousenumberExtended><ns0:AddressSupplement>Onder de brievanbus huisnummer 1</ns0:AddressSupplement><ns0:ZipCode>5000 ZZ</ns0:ZipCode><ns0:City>Amsterdam</ns0:City><ns0:CountryCode>NL</ns0:CountryCode><ns0:Email>dontemail@me.net</ns0:Email><ns0:Telephone>67890</ns0:Telephone><ns0:Company>Bol.com</ns0:Company></ns0:BillingDetails>'

Create a shipment::

    >>> from bol.plaza.api import TransporterCode
    >>> status = api.shipments.create(
        order_item_id=item.order_item.item_id,
        date_time=datetime.now(),
        expected_delivery_date=None,
        shipment_reference="some-ref-123",
        transporter_code=TransporterCode.GLS,
        track_and_trace="5678901234")
    >>> status.eventType
    "CONFIRM_SHPMENT"


Retailer API
============

Supports the BOL API V3, documented here: https://developers.bol.com/apiv3authentication/

Instantiate the API::

    >>> from bol.retailer.api import RetailerAPI
    >>> api = RetailerAPI()

Authenticate::

    >>> api.login('client_id', 'client_secret')

Invoke a method::

    >>> orders = api.orders.list()
    >>> order = api.orders.get(orders[0].orderId)

Fields are derived 1:1 from the bol.com API, including lower-CamelCase
conventions::

    >>> order.customerDetails.shipmentDetails.streetName
    'Billingstraat'

Fields are properly typed::

    >>> repr(order.dateTimeOrderPlace)
    datetime.datetime(2020, 2, 12, 16, 6, 17, tzinfo=tzoffset(None, 3600))
    >>> repr(order.orderItems[0].offerPrice)
    Decimal('106.52')

Access the underlying raw (unparsed) data at any time::

    >>> order.raw_data
    >>> order.raw_content


Running the tests
=================

First, create virtualenv for project and install dev dependencies::

    python -m venv .venv
    . .venv/bin/activate
    pip install -e . -r requirements.txt

Then, just run the code linters and unit tests::

    black .
    isort .
    pytest .

