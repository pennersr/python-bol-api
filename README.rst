==============
python-bol-api
==============

A Python wrapper for the bol.com API. Currently rather incomplete, as
it offers only those methods required for my own projects so far.


Usage
=====

Instantiate the API::

    >>> from bol.api import PlazaAPI
    >>> api = PlazaAPI('public_key', 'private_key', test=True)

Invoke a method::

    >>> open_orders = api.orders.open()

Fields are derived 1:1 from the bol.com API XML, including
CamelCase conventions::

    >>> open_orders[0].Buyer.BillingDetails.Streetname
    'Billingstraat'

Fields are properly typed:

    >>> open_orders[0].Paid
    True

    >>> open_orders[0].OpenOrderItems[0].TransactionFee
    Decimal('19.12')

    >>> open_orders[0].DateTimeDropShipper
    datetime.datetime(2014, 2, 10, 12, 7, 7)
