from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree
from unittest import TestCase

from .api import PlazaAPI
from .models import OpenOrders

open_orders_xml = '<?xml version="1.0" ?><bns:OpenOrders xmlns:bns="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd"><bns:OpenOrder><bns:OrderId>123</bns:OrderId><bns:DateTimeCustomer>2014-02-10T11:58:47</bns:DateTimeCustomer><bns:DateTimeDropShipper>2014-02-10T11:58:47</bns:DateTimeDropShipper><bns:Paid>true</bns:Paid><bns:Buyer><bns:ShipmentDetails><bns:SalutationCode>01</bns:SalutationCode><bns:FirstName>Jan</bns:FirstName><bns:Surname>Janssen</bns:Surname><bns:Streetname>Shipmentstraat</bns:Streetname><bns:Housenumber>42</bns:Housenumber><bns:HousenumberExtended>bis</bns:HousenumberExtended><bns:AddressSupplement>3 hoog achter</bns:AddressSupplement><bns:ZipCode>1000 AA</bns:ZipCode><bns:City>Amsterdam</bns:City><bns:CountryCode>NL</bns:CountryCode><bns:Email>nospam4me@myaccount.com</bns:Email><bns:Telephone>12345</bns:Telephone><bns:Company>The Company</bns:Company></bns:ShipmentDetails><bns:BillingDetails><bns:SalutationCode>02</bns:SalutationCode><bns:FirstName>Jans</bns:FirstName><bns:Surname>Janssen</bns:Surname><bns:Streetname>Billingstraat</bns:Streetname><bns:Housenumber>1</bns:Housenumber><bns:HousenumberExtended>a</bns:HousenumberExtended><bns:AddressSupplement>Onder de brievanbus huisnummer 1</bns:AddressSupplement><bns:ZipCode>5000 ZZ</bns:ZipCode><bns:City>Amsterdam</bns:City><bns:CountryCode>NL</bns:CountryCode><bns:Email>dontemail@me.net</bns:Email><bns:Telephone>67890</bns:Telephone><bns:Company>Bol.com</bns:Company></bns:BillingDetails></bns:Buyer><bns:OpenOrderItems><bns:OpenOrderItem><bns:OrderItemId>123</bns:OrderItemId><bns:EAN>9789062387410</bns:EAN><bns:ReferenceCode>PARTNERREF001</bns:ReferenceCode><bns:Title>Regelmaat en Inbakeren</bns:Title><bns:Quantity>1</bns:Quantity><bns:Price>123.45</bns:Price><bns:DeliveryPeriod>Binnen 24 uur</bns:DeliveryPeriod><bns:TransactionFee>19.12</bns:TransactionFee></bns:OpenOrderItem></bns:OpenOrderItems></bns:OpenOrder><bns:OpenOrder><bns:OrderId>321</bns:OrderId><bns:DateTimeCustomer>2014-02-10T11:58:47</bns:DateTimeCustomer><bns:DateTimeDropShipper>2014-02-10T11:58:47</bns:DateTimeDropShipper><bns:Paid>false</bns:Paid><bns:Buyer><bns:ShipmentDetails><bns:SalutationCode>01</bns:SalutationCode><bns:FirstName>Jan</bns:FirstName><bns:Surname>Janssen</bns:Surname><bns:Streetname>Shipmentstraat</bns:Streetname><bns:Housenumber>42</bns:Housenumber><bns:ZipCode>1000 AA</bns:ZipCode><bns:City>Amsterdam</bns:City><bns:CountryCode>NL</bns:CountryCode><bns:Email>nospam4me@myaccount.com</bns:Email></bns:ShipmentDetails><bns:BillingDetails><bns:SalutationCode>02</bns:SalutationCode><bns:FirstName>Jans</bns:FirstName><bns:Surname>Janssen</bns:Surname><bns:Streetname>Billingstraat</bns:Streetname><bns:Housenumber>1</bns:Housenumber><bns:ZipCode>5000 ZZ</bns:ZipCode><bns:City>Amsterdam</bns:City><bns:CountryCode>NL</bns:CountryCode><bns:Email>dontemail@me.net</bns:Email></bns:BillingDetails></bns:Buyer><bns:OpenOrderItems><bns:OpenOrderItem><bns:OrderItemId>321</bns:OrderItemId><bns:EAN>9789062387410</bns:EAN><bns:Title>Regelmaat en Inbakeren</bns:Title><bns:Quantity>1</bns:Quantity><bns:Price>123.45</bns:Price><bns:DeliveryPeriod>Binnen 24 uur</bns:DeliveryPeriod><bns:TransactionFee>19.12</bns:TransactionFee></bns:OpenOrderItem></bns:OpenOrderItems></bns:OpenOrder></bns:OpenOrders>'  # noqa


class ModelTest(TestCase):

    def test_model_parser(self):
        api = PlazaAPI('dummy', 'dummy')
        xml = ElementTree.fromstring(open_orders_xml)
        open_orders = OpenOrders.parse(api, xml)
        self.assertEqual(len(open_orders), 2)
        self.assertEqual(open_orders[0].Paid, True)
        self.assertEqual(open_orders[1].Paid, False)
        self.assertEqual(open_orders[0].OpenOrderItems[0].TransactionFee, Decimal('19.12'))
        self.assertEqual(open_orders[0].DateTimeCustomer,
                         datetime(2014, 2, 10, 11, 58, 47))
        self.assertEqual(open_orders[1].DateTimeDropShipper,
                         datetime(2014, 2, 10, 11, 58, 47))
