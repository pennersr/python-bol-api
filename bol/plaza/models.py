from decimal import Decimal
import dateutil.parser


class Field(object):

    def parse(self, api, xml, instance):
        raise NotImplementedError


class TextField(Field):

    def parse(self, api, xml, instance):
        return xml.text


class BooleanField(Field):

    def parse(self, api, xml, instance):
        return xml.text == 'true'


class DecimalField(Field):

    def parse(self, api, xml, instance):
        return Decimal(xml.text)


class DateTimeField(Field):

    def parse(self, api, xml, instance):
        # WORKAROUND: At least on the test API I am bumping into this kind of
        # data: '2016-09-19+02:00'. Here, the time seems missing, only the
        # timezone offset is present. Let's detect this and handle gracefully.
        # Contacted BOL, awaiting reply...
        text = xml.text
        if text[10] == '+':
            text = text[:10] + 'T00:00:00' + text[10:]
        # (end WORKAROUND)
        return dateutil.parser.parse(text)


class IntegerField(Field):

    def parse(self, api, xml, instance):
        return int(xml.text)


class ModelField(Field):

    def __init__(self, model):
        self.model = model

    def parse(self, api, xml, instance):
        return self.model.parse(api, xml)


class Model(object):

    @classmethod
    def parse(cls, api, xml):
        m = cls()
        m.xml = xml
        for element in xml.getchildren():
            tag = element.tag.partition('}')[2]
            field = getattr(m.Meta, tag, TextField())
            setattr(m, tag, field.parse(api, element, m))
        return m


class ModelList(list, Model):

    @classmethod
    def parse(cls, api, xml):
        ml = cls()
        ml.xml = xml
        for element in xml.getchildren():
            ml.append(ml.Meta.item_type.parse(api, element))
        return ml


class BillingDetails(Model):

    class Meta:
        pass


class ShipmentDetails(Model):

    class Meta:
        pass


class CustomerDetails(Model):

    class Meta:
        ShipmentDetails = ModelField(ShipmentDetails)
        BillingDetails = ModelField(BillingDetails)


class OrderItem(Model):

    class Meta:
        OfferPrice = DecimalField()
        TransactionFee = DecimalField()
        Quantity = IntegerField()


class OrderItems(ModelList):

    class Meta:
        item_type = OrderItem


class Order(Model):

    class Meta:
        CustomerDetails = ModelField(CustomerDetails)
        OrderItems = ModelField(OrderItems)
        DateTimeCustomer = DateTimeField()
        DateTimeDropShipper = DateTimeField()


class Orders(ModelList):

    class Meta:
        item_type = Order


class PaymentShipmentItem(Model):

    class Meta:
        Quantity = IntegerField()
        OfferPrice = DecimalField()
        TransactionFee = DecimalField()
        TotalAmount = DecimalField()
        ShippingContribution = DecimalField()


class PaymentShipmentItems(ModelList):

    class Meta:
        item_type = PaymentShipmentItem


class PaymentShipment(Model):

    class Meta:

        PaymentShipmentAmount = DecimalField()
        ShipmentDate = DateTimeField()
        PaymentShipmentItems = ModelField(PaymentShipmentItems)


class PaymentShipments(ModelList):

    class Meta:
        item_type = PaymentShipment


class Payment(Model):

    class Meta:
        PaymentShipments = ModelField(PaymentShipments)
        DateTimePayment = DateTimeField()
        PaymentAmount = DecimalField()


class Payments(ModelList):

    class Meta:
        item_type = Payment


class ShipmentItem(Model):

    class Meta:
        OrderItem = ModelField(OrderItem)


class ShipmentItems(ModelList):

    class Meta:
        item_type = ShipmentItem


class Transport(Model):

    class Meta:
        pass


class Shipment(Model):

    class Meta:
        ShipmentDate = DateTimeField()
        ExpectedDeliveryDate = DateTimeField()
        ShipmentItems = ModelField(ShipmentItems)
        Transport = ModelField(Transport)


class Shipments(ModelList):

    class Meta:
        item_type = Shipment


class Labels(Model):

    class Meta:
        TransporterCode = TextField()
        LabelType = TextField()
        MaxWeight = TextField()
        MaxDimensions = TextField()
        RetailPrice = DecimalField()
        PurchasePrice = DecimalField()
        Discount = DecimalField()
        ShippingLabelCode = TextField()


class PurchasableShippingLabels(ModelList):

    class Meta:
        item_type = Labels


class RI_CustomerDetails(Model):

    class Meta:
        SalutationCode = IntegerField()
        FirstName = TextField()
        Surname = TextField()
        Streetname = TextField()
        Housenumber = IntegerField()
        HousenumberExtended = TextField()
        ZipCode = TextField()
        City = TextField()
        CountryCode = TextField()
        Email = TextField()
        DeliveryPhoneNumber = IntegerField()
        Company = TextField()


class Item(Model):

    class Meta:
        ReturnNumber = IntegerField()
        OrderId = IntegerField()
        ShipmentId = IntegerField()
        EAN = TextField()
        Title = TextField()
        Quantity = TextField()
        ReturnDateAnnouncement = TextField()
        ReturnReason = TextField()
        customer_details = RI_CustomerDetails


class ReturnItems(ModelList):

    class Meta:
        item_type = Item


class ProcessStatusLinks(Model):

    class Meta:
        link = IntegerField()


class ProcessStatus(Model):

    class Meta:
        id = IntegerField()
        sellerId = IntegerField()
        entityId = IntegerField()
        eventType = TextField()
        status = TextField()
        createTimestamp = TextField()
        ReturnDateAnnouncement = TextField()
        ReturnReason = TextField()
        item_type = ProcessStatusLinks()

# models used for 'get single offer' method  ::
# RetailerOfferStatus, RetailerOffer, RetailerOffers, OffersResponse


class RetailerOfferStatus(Model):

    class Meta:
        Published = BooleanField()
        ErrorCode = TextField()
        ErrorMessage = TextField()


class RetailerOffer(Model):

    class Meta:
        EAN = TextField()
        Condition = TextField()
        Price = DecimalField()
        DeliveryCode = TextField()
        QuantityInStock = DecimalField()
        UnreservedStock = DecimalField()
        Publish = BooleanField()
        ReferenceCode = TextField()
        Description = TextField()
        Title = TextField()
        FulfillmentMethod = TextField()
        item_type = RetailerOfferStatus()


class RetailerOffers(ModelList):

    class Meta:
        item_type = RetailerOffer()


class OffersResponse(ModelList):

    class Meta:
        item_type = RetailerOffers()


# models used for 'OffersExport' method  :: OfferFileUrl, OfferFile
class OfferFileUrl(Model):

    class Meta:
        Url = TextField()


class OfferFile(Model):

    class Meta:
        item_type = OfferFileUrl()


# models used for 'Delete' method  ::
# DeleteBulkRequest, RetailerOfferIdentifier
class RetailerOfferIdentifier(Model):

    class Meta:
        EAN = TextField()
        Condition = TextField()


class DeleteBulkRequest(ModelList):

    class Meta:
        item_type = RetailerOfferIdentifier()
