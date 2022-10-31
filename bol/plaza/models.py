from decimal import Decimal

import dateutil.parser


class Field:
    def parse(self, api, xml, instance):
        raise NotImplementedError


class TextField(Field):
    def parse(self, api, xml, instance):
        return xml.text


class BooleanField(Field):
    def parse(self, api, xml, instance):
        return xml.text == "true"


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
        if text[10] == "+":
            text = text[:10] + "T00:00:00" + text[10:]
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


class Model:
    @classmethod
    def parse(cls, api, xml):
        m = cls()
        m.xml = xml
        for element in xml:
            if "}" in element.tag:
                tag = element.tag.partition("}")[2]
            elif ":" in element.tag:
                tag = element.tag.partition(":")[2]
            else:
                tag = element.tag
            field = getattr(m.Meta, tag, TextField())
            setattr(m, tag, field.parse(api, element, m))
        return m


class ModelList(list, Model):
    @classmethod
    def parse(cls, api, xml):
        ml = cls()
        ml.xml = xml
        item_tag = getattr(ml.Meta, "item_type_tag", None)
        for element in xml:
            if item_tag and item_tag != element.tag:
                continue
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


class Invoice(Model):
    class Meta:
        pass


class InvoiceListItem(Model):
    class Meta:
        pass


class Invoices(ModelList):
    class Meta:
        item_type = InvoiceListItem
        item_type_tag = "InvoiceListItem"


class Price(Model):
    class Meta:
        PriceAmount = DecimalField()
        BaseQuantity = DecimalField()


class InvoiceSpecificationItem(Model):
    class Meta:
        Price = ModelField(Price)


class InvoiceSpecification(Model):
    class Meta:
        Item = ModelField(InvoiceSpecificationItem)
        pass


class InvoiceSpecifications(ModelList):
    class Meta:
        item_type = InvoiceSpecification


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


class ProcessStatus(Model):
    class Meta:
        pass
