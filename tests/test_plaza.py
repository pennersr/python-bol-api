from decimal import Decimal
from datetime import datetime
from dateutil.tz import tzoffset

from bol.plaza.api import PlazaAPI, TransporterCode

from httmock import HTTMock, urlmatch


ORDERS_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<bns:Orders
    xmlns:bns="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd">
  <bns:Order>
    <bns:OrderId>123</bns:OrderId>
    <bns:DateTimeCustomer>2015-09-23T12:30:36</bns:DateTimeCustomer>
    <bns:DateTimeDropShipper>2015-09-23T12:30:36</bns:DateTimeDropShipper>
    <bns:CustomerDetails>
      <bns:ShipmentDetails>
        <bns:SalutationCode>01</bns:SalutationCode>
        <bns:Firstname>Jan</bns:Firstname>
        <bns:Surname>Janssen</bns:Surname>
        <bns:Streetname>Shipmentstraat</bns:Streetname>
        <bns:Housenumber>42</bns:Housenumber>
        <bns:HousenumberExtended>bis</bns:HousenumberExtended>
        <bns:AddressSupplement>3 hoog achter</bns:AddressSupplement>
        <bns:ZipCode>1000 AA</bns:ZipCode>
        <bns:City>Amsterdam</bns:City>
        <bns:CountryCode>NL</bns:CountryCode>
        <bns:Email>nospam4me@myaccount.com</bns:Email>
        <bns:DeliveryPhoneNumber>12345</bns:DeliveryPhoneNumber>
        <bns:Company>The Company</bns:Company>
      </bns:ShipmentDetails>
      <bns:BillingDetails>
        <bns:SalutationCode>02</bns:SalutationCode>
        <bns:Firstname>Jans</bns:Firstname>
        <bns:Surname>Janssen</bns:Surname>
        <bns:Streetname>Billingstraat</bns:Streetname>
        <bns:Housenumber>1</bns:Housenumber>
        <bns:HousenumberExtended>a</bns:HousenumberExtended>
        <bns:AddressSupplement>Onder de brievenbus</bns:AddressSupplement>
        <bns:ZipCode>5000 ZZ</bns:ZipCode>
        <bns:City>Amsterdam</bns:City>
        <bns:CountryCode>NL</bns:CountryCode>
        <bns:Email>dontemail@me.net</bns:Email>
        <bns:DeliveryPhoneNumber>67890</bns:DeliveryPhoneNumber>
        <bns:Company>Bol.com</bns:Company>
      </bns:BillingDetails>
    </bns:CustomerDetails>
    <bns:OrderItems>
      <bns:OrderItem>
        <bns:OrderItemId>123</bns:OrderItemId>
        <bns:EAN>9789062387410</bns:EAN>
        <bns:OfferReference>PARTNERREF001</bns:OfferReference>
        <bns:Title>Regelmaat en Inbakeren</bns:Title>
        <bns:Quantity>1</bns:Quantity>
        <bns:OfferPrice>123.45</bns:OfferPrice>
        <bns:PromisedDeliveryDate>Binnen 24 uur</bns:PromisedDeliveryDate>
        <bns:TransactionFee>19.12</bns:TransactionFee>
      </bns:OrderItem>
    </bns:OrderItems>
  </bns:Order>
</bns:Orders>"""


PAYMENTS_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<bns:Payments
    xmlns:bns="http://plazaapi.bol.com/services/xsd/plazaapiservice-1.0.xsd">
  <bns:Payment>
    <bns:CreditInvoiceNumber>123</bns:CreditInvoiceNumber>
    <bns:DateTimePayment>2015-09-23T21:35:43</bns:DateTimePayment>
    <bns:PaymentAmount>425.77</bns:PaymentAmount>
    <bns:PaymentShipments>
      <bns:PaymentShipment>
        <bns:ShipmentId>456</bns:ShipmentId>
        <bns:OrderId>123001</bns:OrderId>
        <bns:PaymentShipmentAmount>425.77</bns:PaymentShipmentAmount>
        <bns:PaymentStatus>FINAL</bns:PaymentStatus>
        <bns:ShipmentDate>2015-09-23T21:35:43</bns:ShipmentDate>
        <bns:PaymentShipmentItems>
          <bns:PaymentShipmentItem>
            <bns:OrderItemId>123001001</bns:OrderItemId>
            <bns:EAN>9789062387410</bns:EAN>
            <bns:OfferReference>PARTNERREF001</bns:OfferReference>
            <bns:Quantity>1</bns:Quantity>
            <bns:OfferPrice>425.77</bns:OfferPrice>
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


SHIPMENTS_RESPONSE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Shipments xmlns="https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
    <Shipment>
        <ShipmentId>123</ShipmentId>
        <ShipmentDate>2016-09-19T18:21:59.324+02:00</ShipmentDate>
        <ExpectedDeliveryDate>2016-09-19+02:00</ExpectedDeliveryDate>
        <ShipmentReference>shipmentReferentie</ShipmentReference>
        <ShipmentItems>
            <ShipmentItem>
                <OrderItem>
                    <OrderItemId>5612423</OrderItemId>
                    <OrderId>7464</OrderId>
                    <OrderItemSequenceNumber>2</OrderItemSequenceNumber>
                    <OrderDate>2016-09-17T18:21:59.324+02:00</OrderDate>
                    <PromisedDeliveryDate>2016-09-20+02:00</PromisedDeliveryDate>
                    <EAN>9789062387410</EAN>
                    <Title>Harry Potter</Title>
                    <Quantity>1</Quantity>
                    <OfferPrice>123.45</OfferPrice>
                    <OfferCondition>NEW</OfferCondition>
                    <OfferReference>MijnOffer 123</OfferReference>
                    <FulfilmentMethod>FBR</FulfilmentMethod>
                </OrderItem>
            </ShipmentItem>
        </ShipmentItems>
        <Transport>
            <TransportId>8444626</TransportId>
            <TransporterCode>DHLFORYOU</TransporterCode>
            <TrackAndTrace>3stest</TrackAndTrace>
            <ShippingLabelId>349</ShippingLabelId>
        </Transport>
        <CustomerDetails>
            <FirstName>Jan</FirstName>
            <Surname>Janssen</Surname>
            <Streetname>Vogelstraat</Streetname>
            <Housenumber>42</Housenumber>
            <HousenumberExtended>bis</HousenumberExtended>
            <AddressSupplement>3 hoog achter</AddressSupplement>
            <ExtraAddressInformation>extra adres info</ExtraAddressInformation>
            <ZipCode>1000 AA</ZipCode>
            <City>Amsterdam</City>
            <CountryCode>NL</CountryCode>
            <Email>nospam4me@myaccount.com</Email>
            <DeliveryPhoneNumber>12345</DeliveryPhoneNumber>
            <Company>The Company</Company>
            <VatNumber>VatNumber12</VatNumber>
        </CustomerDetails>
    </Shipment>
    <Shipment>
        <ShipmentDate>2016-09-19T18:21:59.325+02:00</ShipmentDate>
        <ShipmentItems>
            <ShipmentItem>
                <OrderItem>
                    <OrderItemId>8812523</OrderItemId>
                    <OrderId>7464</OrderId>
                    <OrderItemSequenceNumber>2</OrderItemSequenceNumber>
                    <OrderDate>2016-09-17T18:21:59.325+02:00</OrderDate>
                    <EAN>9789062387410</EAN>
                    <Quantity>1</Quantity>
                    <OfferPrice>123.45</OfferPrice>
                    <OfferCondition>NEW</OfferCondition>
                    <FulfilmentMethod>FBR</FulfilmentMethod>
                </OrderItem>
            </ShipmentItem>
        </ShipmentItems>
        <Transport>
            <ShippingLabelId>1807</ShippingLabelId>
        </Transport>
        <CustomerDetails>
            <FirstName>Jan</FirstName>
            <Surname>Janssen</Surname>
            <Streetname>Vogelstraat</Streetname>
            <Housenumber>42</Housenumber>
            <ZipCode>1000 AA</ZipCode>
            <City>Amsterdam</City>
            <CountryCode>NL</CountryCode>
            <Email>nospam4me@myaccount.com</Email>
        </CustomerDetails>
    </Shipment>
</Shipments>
"""


CREATE_SHIPMENT_RESPONSE = \
    """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns1:ProcessStatus
    xmlns:ns1="https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
    <ns1:id>0</ns1:id>
    <ns1:sellerId>12345678</ns1:sellerId>
    <ns1:entityId>123</ns1:entityId>
    <ns1:eventType>CONFIRM_SHIPMENT</ns1:eventType>
    <ns1:description>Confirm shipment for order item 123.</ns1:description>
    <ns1:status>PENDING</ns1:status>
</ns1:ProcessStatus>
"""

UPDATE_TRANSPORT_RESPONSE = \
     """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns1:ProcessStatus
     xmlns:ns1="https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
     <ns1:id>0</ns1:id>
     <ns1:sellerId>925853</ns1:sellerId>
     <ns1:entityId>1</ns1:entityId>
     <ns1:eventType>CHANGE_TRANSPORT</ns1:eventType>
     <ns1:description>Change transport with id 1.</ns1:description>
     <ns1:status>PENDING</ns1:status>
</ns1:ProcessStatus>
"""


@urlmatch(path=r'/services/rest/orders/v2$')
def orders_stub(url, request):
    return ORDERS_RESPONSE


@urlmatch(path=r'/services/rest/payments/v2/201501$')
def payments_stub(url, request):
    return PAYMENTS_RESPONSE


@urlmatch(path=r'/services/rest/shipments/v2$')
def shipments_stub(url, request):
    return SHIPMENTS_RESPONSE


def test_orders():
    with HTTMock(orders_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        orders = api.orders.list()
        assert len(orders) == 1

        order = orders[0]
        assert order.OrderId == '123'

        assert order.CustomerDetails.BillingDetails.SalutationCode == '02'
        assert order.CustomerDetails.BillingDetails.Firstname == 'Jans'
        assert order.CustomerDetails.BillingDetails.Surname == 'Janssen'
        assert (
            order.CustomerDetails.BillingDetails.Streetname ==
            'Billingstraat')
        assert order.CustomerDetails.BillingDetails.Housenumber == '1'
        assert order.CustomerDetails.BillingDetails.HousenumberExtended == 'a'
        assert (
            order.CustomerDetails.BillingDetails.AddressSupplement ==
            'Onder de brievenbus')
        assert order.CustomerDetails.BillingDetails.ZipCode == '5000 ZZ'
        assert order.CustomerDetails.BillingDetails.City == 'Amsterdam'
        assert order.CustomerDetails.BillingDetails.CountryCode == 'NL'
        assert order.CustomerDetails.BillingDetails.Email == 'dontemail@me.net'
        assert (
            order.CustomerDetails.BillingDetails.DeliveryPhoneNumber ==
            '67890')
        assert order.CustomerDetails.BillingDetails.Company == 'Bol.com'

        assert order.CustomerDetails.ShipmentDetails.SalutationCode == '01'
        assert order.CustomerDetails.ShipmentDetails.Firstname == 'Jan'
        assert order.CustomerDetails.ShipmentDetails.Surname == 'Janssen'
        assert (
            order.CustomerDetails.ShipmentDetails.Streetname ==
            'Shipmentstraat')
        assert order.CustomerDetails.ShipmentDetails.Housenumber == '42'
        assert (
            order.CustomerDetails.ShipmentDetails.HousenumberExtended == 'bis')

        assert (
            order.CustomerDetails.ShipmentDetails.AddressSupplement ==
            '3 hoog achter')
        assert order.CustomerDetails.ShipmentDetails.ZipCode == '1000 AA'
        assert order.CustomerDetails.ShipmentDetails.City == 'Amsterdam'
        assert order.CustomerDetails.ShipmentDetails.CountryCode == 'NL'
        assert (
            order.CustomerDetails.ShipmentDetails.Email ==
            'nospam4me@myaccount.com')
        assert (
            order.CustomerDetails.ShipmentDetails.DeliveryPhoneNumber ==
            '12345')
        assert order.CustomerDetails.ShipmentDetails.Company == 'The Company'

        assert len(order.OrderItems) == 1
        item = order.OrderItems[0]

        assert item.OrderItemId == '123'
        assert item.EAN == '9789062387410'
        assert item.OfferReference == 'PARTNERREF001'
        assert item.Title == 'Regelmaat en Inbakeren'
        assert item.Quantity == 1
        assert item.OfferPrice == Decimal('123.45')
        assert item.PromisedDeliveryDate == 'Binnen 24 uur'
        assert item.TransactionFee == Decimal('19.12')


def test_order_process():
    @urlmatch(path=r'/services/rest/shipments/v2$')
    def create_shipment_stub(url, request):
        assert request.body == """<?xml version="1.0" encoding="UTF-8"?>
<ShipmentRequest xmlns="https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
    <DateTime>2016-10-01T01:08:17</DateTime>
    <OrderItemId>123</OrderItemId>
    <ShipmentReference>abc</ShipmentReference>
    <Transport>
        <TrackAndTrace>3S123</TrackAndTrace>
        <TransporterCode>GLS</TransporterCode>
    </Transport>
</ShipmentRequest>
"""
        return CREATE_SHIPMENT_RESPONSE

    with HTTMock(create_shipment_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        dt = datetime(2016, 10, 1, 1, 8, 17, 0)
        process_status = api.shipments.create(
            order_item_id='123',
            date_time=dt,
            expected_delivery_date=None,
            shipment_reference='abc',
            transporter_code=TransporterCode.GLS,
            track_and_trace='3S123')
        assert process_status.sellerId == '12345678'


def test_payments():
    with HTTMock(payments_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        payments = api.payments.list(2015, 1)

        assert len(payments) == 1
        payment = payments[0]
        assert payment.PaymentAmount == Decimal('425.77')
        assert payment.DateTimePayment == datetime(2015, 9, 23, 21, 35, 43)
        assert payment.CreditInvoiceNumber == '123'
        assert len(payment.PaymentShipments) == 1
        shipment = payment.PaymentShipments[0]
        assert shipment.OrderId == '123001'
        assert shipment.ShipmentId == '456'
        assert shipment.PaymentShipmentAmount == Decimal('425.77')
        assert shipment.PaymentStatus == 'FINAL'


def test_shipments():
    with HTTMock(shipments_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        shipments = api.shipments.list(1)

        assert len(shipments) == 2
        shipment = shipments[0]
        assert shipment.ShipmentDate == datetime(
            2016, 9, 19, 18, 21, 59, 324000, tzinfo=tzoffset(None, 7200))
        assert shipment.ExpectedDeliveryDate == datetime(
            2016, 9, 19, 0, 0, tzinfo=tzoffset(None, 7200))


def test_update_transport():
    @urlmatch(path=r'/services/rest/transports/v2/1$')
    def create_transport_stub(url, request):
        assert request.body == """<?xml version="1.0" encoding="UTF-8"?>
<ChangeTransportRequest xmlns=\
"https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
    <TrackAndTrace>3S123</TrackAndTrace>
    <TransporterCode>GLS</TransporterCode>
</ChangeTransportRequest>
"""
        return UPDATE_TRANSPORT_RESPONSE

    with HTTMock(create_transport_stub):
        api = PlazaAPI('api_key', 'api_secret', test=True)
        process_status = api.transports.update(
            1,
            track_and_trace='3S123',
            transporter_code=TransporterCode.GLS)
        assert process_status.sellerId == '925853'
