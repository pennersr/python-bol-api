from decimal import Decimal
from datetime import datetime

from bol.plaza.api import PlazaAPI

from httmock import HTTMock, urlmatch


ORDERS_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<bns:OpenOrders xmlns:bns="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd">
  <bns:OpenOrder>
    <bns:OrderId>123</bns:OrderId>
    <bns:DateTimeCustomer>2015-09-23T12:30:36</bns:DateTimeCustomer>
    <bns:DateTimeDropShipper>2015-09-23T12:30:36</bns:DateTimeDropShipper>
    <bns:Paid>true</bns:Paid>
    <bns:Buyer>
      <bns:ShipmentDetails>
        <bns:SalutationCode>01</bns:SalutationCode>
        <bns:FirstName>Jan</bns:FirstName>
        <bns:Surname>Janssen</bns:Surname>
        <bns:Streetname>Shipmentstraat</bns:Streetname>
        <bns:Housenumber>42</bns:Housenumber>
        <bns:HousenumberExtended>bis</bns:HousenumberExtended>
        <bns:AddressSupplement>3 hoog achter</bns:AddressSupplement>
        <bns:ZipCode>1000 AA</bns:ZipCode>
        <bns:City>Amsterdam</bns:City>
        <bns:CountryCode>NL</bns:CountryCode>
        <bns:Email>nospam4me@myaccount.com</bns:Email>
        <bns:Telephone>12345</bns:Telephone>
        <bns:Company>The Company</bns:Company>
      </bns:ShipmentDetails>
      <bns:BillingDetails>
        <bns:SalutationCode>02</bns:SalutationCode>
        <bns:FirstName>Jans</bns:FirstName>
        <bns:Surname>Janssen</bns:Surname>
        <bns:Streetname>Billingstraat</bns:Streetname>
        <bns:Housenumber>1</bns:Housenumber>
        <bns:HousenumberExtended>a</bns:HousenumberExtended>
        <bns:AddressSupplement>Onder de brievanbus huisnummer 1</bns:AddressSupplement>
        <bns:ZipCode>5000 ZZ</bns:ZipCode>
        <bns:City>Amsterdam</bns:City>
        <bns:CountryCode>NL</bns:CountryCode>
        <bns:Email>dontemail@me.net</bns:Email>
        <bns:Telephone>67890</bns:Telephone>
        <bns:Company>Bol.com</bns:Company>
      </bns:BillingDetails>
    </bns:Buyer>
    <bns:OpenOrderItems>
      <bns:OpenOrderItem>
        <bns:OrderItemId>123</bns:OrderItemId>
        <bns:EAN>9789062387410</bns:EAN>
        <bns:ReferenceCode>PARTNERREF001</bns:ReferenceCode>
        <bns:Title>Regelmaat en Inbakeren</bns:Title>
        <bns:Quantity>1</bns:Quantity>
        <bns:Price>123.45</bns:Price>
        <bns:DeliveryPeriod>Binnen 24 uur</bns:DeliveryPeriod>
        <bns:TransactionFee>19.12</bns:TransactionFee>
      </bns:OpenOrderItem>
    </bns:OpenOrderItems>
  </bns:OpenOrder>
</bns:OpenOrders>"""


PAYMENTS_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<bns:Payments xmlns:bns="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd">
  <bns:Payment>
    <bns:CreditInvoiceNumber>123</bns:CreditInvoiceNumber>
    <bns:DateTimePayment>2015-09-23T21:35:43</bns:DateTimePayment>
    <bns:PaymentAmount>425.77</bns:PaymentAmount>
    <bns:PaymentShipments>
      <bns:PaymentShipment>
        <bns:PackageSlipNumber>456</bns:PackageSlipNumber>
        <bns:OrderId>123001</bns:OrderId>
        <bns:PaymentShipmentAmount>425.77</bns:PaymentShipmentAmount>
        <bns:PaymentStatus>FINAL</bns:PaymentStatus>
        <bns:DateTimeShipment>2015-09-23T21:35:43</bns:DateTimeShipment>
        <bns:PaymentShipmentItems>
          <bns:PaymentShipmentItem>
            <bns:OrderItemId>123001001</bns:OrderItemId>
            <bns:EAN>9789062387410</bns:EAN>
            <bns:ReferenceCode>PARTNERREF001</bns:ReferenceCode>
            <bns:Quantity>1</bns:Quantity>
            <bns:Price>425.77</bns:Price>
            <bns:ShippingContribution>1.95</bns:ShippingContribution>
            <bns:TransactionFee>10.00</bns:TransactionFee>
            <bns:TotalAmount>425.77</bns:TotalAmount>
            <bns:ShipmentStatus>NORMAL</bns:ShipmentStatus>
          </bns:PaymentShipmentItem>
        </bns:PaymentShipmentItems>
      </bns:PaymentShipment>
    </bns:PaymentShipments>
  </bns:Payment>
</bns:Payments>"""


@urlmatch(path=r'/services/rest/orders/v1/open$')
def orders_stub(url, request):
    return ORDERS_RESPONSE


@urlmatch(path=r'/services/rest/payments/v1/payments/201501$')
def payments_stub(url, request):
    return PAYMENTS_RESPONSE


def test_orders():
    with HTTMock(orders_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        orders = api.orders.open()
        assert len(orders) == 1

        order = orders[0]
        assert order.OrderId == '123'
        assert order.Paid is True

        assert order.Buyer.BillingDetails.SalutationCode == '02'
        assert order.Buyer.BillingDetails.FirstName == 'Jans'
        assert order.Buyer.BillingDetails.Surname == 'Janssen'
        assert order.Buyer.BillingDetails.Streetname == 'Billingstraat'
        assert order.Buyer.BillingDetails.Housenumber == '1'
        assert order.Buyer.BillingDetails.HousenumberExtended == 'a'
        assert order.Buyer.BillingDetails.AddressSupplement == 'Onder de brievanbus huisnummer 1'
        assert order.Buyer.BillingDetails.ZipCode == '5000 ZZ'
        assert order.Buyer.BillingDetails.City == 'Amsterdam'
        assert order.Buyer.BillingDetails.CountryCode == 'NL'
        assert order.Buyer.BillingDetails.Email == 'dontemail@me.net'
        assert order.Buyer.BillingDetails.Telephone == '67890'
        assert order.Buyer.BillingDetails.Company == 'Bol.com'

        assert order.Buyer.ShipmentDetails.SalutationCode == '01'
        assert order.Buyer.ShipmentDetails.FirstName == 'Jan'
        assert order.Buyer.ShipmentDetails.Surname == 'Janssen'
        assert order.Buyer.ShipmentDetails.Streetname == 'Shipmentstraat'
        assert order.Buyer.ShipmentDetails.Housenumber == '42'
        assert order.Buyer.ShipmentDetails.HousenumberExtended == 'bis'
        assert order.Buyer.ShipmentDetails.AddressSupplement == '3 hoog achter'
        assert order.Buyer.ShipmentDetails.ZipCode == '1000 AA'
        assert order.Buyer.ShipmentDetails.City == 'Amsterdam'
        assert order.Buyer.ShipmentDetails.CountryCode == 'NL'
        assert order.Buyer.ShipmentDetails.Email == 'nospam4me@myaccount.com'
        assert order.Buyer.ShipmentDetails.Telephone == '12345'
        assert order.Buyer.ShipmentDetails.Company == 'The Company'

        assert len(order.OpenOrderItems) == 1
        item = order.OpenOrderItems[0]

        assert item.OrderItemId == '123'
        assert item.EAN == '9789062387410'
        assert item.ReferenceCode == 'PARTNERREF001'
        assert item.Title == 'Regelmaat en Inbakeren'
        assert item.Quantity == 1
        assert item.Price == Decimal('123.45')
        assert item.DeliveryPeriod == 'Binnen 24 uur'
        assert item.TransactionFee == Decimal('19.12')


def test_payments():
    with HTTMock(payments_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        payments = api.payments.payments(2015, 1)

        assert len(payments) == 1
        payment = payments[0]
        assert payment.PaymentAmount == Decimal('425.77')
        assert payment.DateTimePayment == datetime(2015, 9, 23, 21, 35, 43)
        assert payment.CreditInvoiceNumber == '123'
        assert len(payment.PaymentShipments) == 1
        shipment = payment.PaymentShipments[0]
        assert shipment.OrderId == '123001'
        assert shipment.PackageSlipNumber == '456'
        assert shipment.PaymentShipmentAmount == Decimal('425.77')
        assert shipment.PaymentStatus == 'FINAL'
