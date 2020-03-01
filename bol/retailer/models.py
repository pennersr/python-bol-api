import json
import sys
from datetime import date
from decimal import Decimal

import dateutil.parser


def _is_str(v):
    if sys.version_info >= (3, 0, 0):
        string_types = str,
    else:
        string_types = basestring,
    return isinstance(v, string_types)


def parse_json(content):
    return json.loads(content, parse_float=Decimal)


class Field(object):
    def parse(self, api, raw_data, instance):
        raise NotImplementedError


class RawField(Field):
    def parse(self, api, raw_data, instance):
        return raw_data


class DecimalField(Field):
    def parse(self, api, raw_data, instance):
        return Decimal(raw_data)


class DateTimeField(Field):
    def parse(self, api, raw_data, instance):
        return dateutil.parser.parse(raw_data)


class DateField(Field):
    def parse(self, api, raw_data, instance):
        parts = raw_data.split("-")
        if len(parts) != 3:
            raise ValueError(raw_data)
        iparts = list(map(int, parts))
        return date(*iparts)


class ModelField(Field):
    def __init__(self, model):
        self.model = model

    def parse(self, api, xml, instance):
        return self.model.parse(api, xml)


class BaseModel(object):
    @classmethod
    def parse(cls, api, content):
        m = cls()
        if _is_str(content):
            m.raw_content = content
            m.raw_data = parse_json(content)
        else:
            m.raw_content = None
            m.raw_data = content
        return m


class Model(BaseModel):
    @classmethod
    def parse(cls, api, content):
        m = super(Model, cls).parse(api, content)
        for tag, v in m.raw_data.items():
            field = getattr(m.Meta, tag, RawField())
            setattr(m, tag, field.parse(api, v, m))
        return m


class ModelList(list, BaseModel):
    @classmethod
    def parse(cls, api, content):
        ml = super(ModelList, cls).parse(api, content)
        items_key = getattr(ml.Meta, "items_key", None)
        if items_key:
            items = ml.raw_data.get(items_key)
        else:
            items = ml.raw_data
        if items:
            for item in items:
                ml.append(ml.Meta.item_type.parse(api, item))
        return ml


class BillingDetails(Model):
    class Meta:
        pass


class ShipmentDetails(Model):
    class Meta:
        pass


class CustomerDetails(Model):
    class Meta:
        shipmentDetails = ModelField(ShipmentDetails)
        billingDetails = ModelField(BillingDetails)


class Price(Model):
    class Meta:
        PriceAmount = DecimalField()
        BaseQuantity = DecimalField()


class OrderItem(Model):
    class Meta:
        offerPrice = DecimalField()
        transactionFee = DecimalField()
        latestDeliveryDate = DateField()
        expiryDate = DateField()


class OrderItems(ModelList):
    class Meta:
        item_type = OrderItem


class Order(Model):
    class Meta:
        customerDetails = ModelField(CustomerDetails)
        orderItems = ModelField(OrderItems)
        dateTimeOrderPlaced = DateTimeField()


class Orders(ModelList):
    class Meta:
        item_type = Order
        items_key = "orders"


class ShipmentItem(Model):
    class Meta:
        orderDate = DateTimeField()
        latestDeliveryDate = DateTimeField()


class ShipmentItems(ModelList):
    class Meta:
        item_type = ShipmentItem


class Transport(Model):
    class Meta:
        pass


class Shipment(Model):
    class Meta:
        shipmentDate = DateTimeField()
        shipmentItems = ModelField(ShipmentItems)
        transport = ModelField(Transport)


class Shipments(ModelList):
    class Meta:
        item_type = Shipment
        items_key = "shipments"


class ProcessStatus(Model):
    class Meta:
        createTimestamp = DateTimeField()


class ProcessStatuses(ModelList):
    class Meta:
        items_key = "processStatuses"
        item_type = ProcessStatus


class Invoice(Model):
    class Meta:
        pass


class Invoices(ModelList):
    class Meta:
        item_type = Invoice
        items_key = "invoiceListItems"


class InvoiceSpecificationItem(Model):
    class Meta:
        pass


class InvoiceSpecification(ModelList):
    class Meta:
        item_type = InvoiceSpecificationItem
        items_key = "invoiceSpecification"
