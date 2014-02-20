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
        return dateutil.parser.parse(xml.text)


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


class Buyer(Model):

    class Meta:
        ShipmentDetails = ModelField(ShipmentDetails)
        BillingDetails = ModelField(BillingDetails)


class OpenOrderItem(Model):

    class Meta:
        Price = DecimalField()
        TransactionFee = DecimalField()
        Quantity = IntegerField()


class OpenOrderItems(ModelList):

    class Meta:
        item_type = OpenOrderItem


class OpenOrder(Model):

    class Meta:
        Paid = BooleanField()
        Buyer = ModelField(Buyer)
        OpenOrderItems = ModelField(OpenOrderItems)
        DateTimeCustomer = DateTimeField()
        DateTimeDropShipper = DateTimeField()


class OpenOrders(ModelList):

    class Meta:
        item_type = OpenOrder


class PaymentShipmentItem(Model):

    class Meta:
        Quantity = IntegerField()
        Price = DecimalField()
        TransactionFee = DecimalField()
        TotalAmount = DecimalField()
        ShippingContribution = DecimalField()


class PaymentShipmentItems(ModelList):

    class Meta:
        item_type = PaymentShipmentItem


class PaymentShipment(Model):

    class Meta:

        PaymentShipmentAmount = DecimalField()
        DateTimeShipment = DateTimeField()
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
