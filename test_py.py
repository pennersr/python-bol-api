#!/usr/bin/env python




from bol.plaza.api import PlazaAPI
from xml.etree import ElementTree



prod_public_key = 'rxfpVEGQrJCPruJaOhwdqGVxxyWnHMey'
prod_private_key = 'hmQMllfwguQyXYpuoquDUdnpvBccQlOYwScdfoXubMcNfLrmoQqbpSncotpCWtVcMscDNNoQCWRzofbkSTEFEBBlMRfCitXoEEQsYgCrnHbdxONHNtIbvXNZJHFvGMEHairMLdbFbfjCQPsZLoddRlNOMWnfsGzNpSqJsoMoZrdLmGyVwjYYxSWnEfrEkaTRyaLIDFOkgHpErMjIGMDqZVAuyiOcPgGXSpUqLNFcqNcpeGvLrvvJwUMwIakTlUIy'


public_key = 'BMWwKbEsujRfcOGLsPzqSSBcXOCvclwO'
private_key = 'bjOZlUUNBqkfyjFiykcoDAeYbZrmMAGVTfFNjbZuGkWRBHKVzfjflbmCIGMxVbjUWptiKecEVyFFHpuaEbSybtYblRLECIPcaPzLlnaUdpktQhdMhevxUIwHHEnMnrgvOEQtcUviRDrsbCoTvHCXRLkhUmYZeGQstBmtCZuyhnpwKlbCMpjEDQcjroTHbLaKEemdbjScusTbxLjhcHehXsclqFBdkVJlRcalUufGhDgAcMQTwxpyECvvknHMFcOL'



# api = PlazaAPI(prod_public_key, prod_private_key, test=False)
# print "api => ",dir(api)
# shipping_label = api.labels.get(2053581240)
# print "shipping_label => ",shipping_label
# shipping_label = api.PurchasableShippingLabels.getSingle(106603145,'PLR00000015')
# print "shipping_label => ",shipping_label


api = PlazaAPI(prod_public_key, prod_private_key, test=False)
print "\n\n test.pt=> dir(api) => ",dir(api)
print "\n\n test.pt=> dir(api.return_items) => ",dir(api.return_items)
return_items = api.return_items.getUnhandled()
print "test.pt=> return_items => ",return_items

# open_orders = api.orders.list()


#  # ['CustomerDetails', 'DateTimeCustomer', 'DateTimeDropShipper', 'Meta', 'OrderId', 'OrderItems', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'parse', 'xml']
# print "open_orders[0].xml => ",ElementTree.tostring(open_orders[0].xml)
# print "open_orders[0].CustomerDetails => ",dir(open_orders[0].CustomerDetails)
# # print "open_orders[0].CustomerDetails => ",ElementTree.tostring(open_orders[0].CustomerDetails)
# print "open_orders[0].CustomerDetails => ",dir(open_orders[0].CustomerDetails.BillingDetails)
# print "open_orders[0].CustomerDetails => ",open_orders[0].CustomerDetails.BillingDetails
# # print "open_orders[0].Buyer.BillingDetails => ",open_orders[0].Buyer.BillingDetails



# <ns0:Order xmlns:ns0="https://plazaapi.bol.com/services/xsd/v2/plazaapi.xsd">
#     <ns0:OrderId>123</ns0:OrderId>
#     <ns0:DateTimeCustomer>2017-07-05T09:19:59.806+02:00</ns0:DateTimeCustomer>
#     <ns0:DateTimeDropShipper>2017-07-05T09:19:59.806+02:00</ns0:DateTimeDropShipper>
#     <ns0:CustomerDetails>
#         <ns0:ShipmentDetails>
#             <ns0:SalutationCode>01</ns0:SalutationCode>
#             <ns0:Firstname>Jan</ns0:Firstname>
#             <ns0:Surname>Janssen</ns0:Surname>
#             <ns0:Streetname>Shipmentstraat</ns0:Streetname>
#             <ns0:Housenumber>42</ns0:Housenumber>
#             <ns0:HousenumberExtended>bis</ns0:HousenumberExtended>
#             <ns0:AddressSupplement>3 hoog achter</ns0:AddressSupplement>
#             <ns0:ExtraAddressInformation>extra adres info</ns0:ExtraAddressInformation>
#             <ns0:ZipCode>1000 AA</ns0:ZipCode>
#             <ns0:City>Amsterdam</ns0:City>
#             <ns0:CountryCode>NL</ns0:CountryCode>
#             <ns0:Email>nospam4me@myaccount.com</ns0:Email>
#             <ns0:Company>The Company</ns0:Company>
#             <ns0:DeliveryPhoneNumber>0201234567</ns0:DeliveryPhoneNumber>
#         </ns0:ShipmentDetails>
#         <ns0:BillingDetails>
#             <ns0:SalutationCode>02</ns0:SalutationCode>
#             <ns0:Firstname>Jans</ns0:Firstname>
#             <ns0:Surname>Janssen</ns0:Surname>
#             <ns0:Streetname>Billingstraat</ns0:Streetname>
#             <ns0:Housenumber>1</ns0:Housenumber>
#             <ns0:AddressSupplement>Onder de brievanbus huisnummer 1</ns0:AddressSupplement>
#             <ns0:ExtraAddressInformation>extra adres info</ns0:ExtraAddressInformation>
#             <ns0:ZipCode>5000 ZZ</ns0:ZipCode>
#             <ns0:City>Amsterdam</ns0:City>
#             <ns0:CountryCode>NL</ns0:CountryCode>
#             <ns0:Email>dontemail@me.net</ns0:Email>
#             <ns0:Company>Bol.com</ns0:Company>
#             <ns0:VatNumber>0001</ns0:VatNumber>
#         </ns0:BillingDetails>
#     </ns0:CustomerDetails>
#     <ns0:OrderItems>
#         <ns0:OrderItem>
#             <ns0:OrderItemId>123</ns0:OrderItemId>
#             <ns0:EAN>9789062387410</ns0:EAN>
#             <ns0:OfferReference>PARTNERREF001</ns0:OfferReference>
#             <ns0:Title>Harry Potter</ns0:Title>
#             <ns0:Quantity>2</ns0:Quantity>
#             <ns0:OfferPrice>123.45</ns0:OfferPrice>
#             <ns0:TransactionFee>1.50</ns0:TransactionFee>
#             <ns0:PromisedDeliveryDate>2017-07-05+02:00</ns0:PromisedDeliveryDate>
#             <ns0:OfferCondition>AS_NEW</ns0:OfferCondition>
#             <ns0:CancelRequest>false</ns0:CancelRequest>
#         </ns0:OrderItem>
#     </ns0:OrderItems>
# </ns0:Order>






# even with your production keys ....


# demo@trial:~/project/odoo/karan/git/github/python-bol-api$ ./test_py.py
# PlazaaAPI => __init__()->  public_key BMWwKbEsujRfcOGLsPzqSSBcXOCvclwO
# PlazaaAPI => __init__()->  private_key bjOZlUUNBqkfyjFiykcoDAeYbZrmMAGVTfFNjbZuGkWRBHKVzfjflbmCIGMxVbjUWptiKecEVyFFHpuaEbSybtYblRLECIPcaPzLlnaUdpktQhdMhevxUIwHHEnMnrgvOEQtcUviRDrsbCoTvHCXRLkhUmYZeGQstBmtCZuyhnpwKlbCMpjEDQcjroTHbLaKEemdbjScusTbxLjhcHehXsclqFBdkVJlRcalUufGhDgAcMQTwxpyECvvknHMFcOL
# PlazaaAPI => __init__()->  test False
# PlazaaAPI => __init__()->  self.url https://plazaapi.bol.com
# OrderMethods => __init__()->  api <bol.plaza.api.PlazaAPI object at 0x7f823a2cdc50>
# MethodGroup => __init__()->  group orders
# PaymentMethods => __init__()->  api <bol.plaza.api.PlazaAPI object at 0x7f823a2cdc50>
# MethodGroup => __init__()->  group payments
# ShipmentMethods => __init__()->  api <bol.plaza.api.PlazaAPI object at 0x7f823a2cdc50>
# MethodGroup => __init__()->  group shipments
# ProcessStatusMethods => __init__()->  api <bol.plaza.api.PlazaAPI object at 0x7f823a2cdc50>
# MethodGroup => __init__()->  group process-status
# TransportMethods => __init__()->  api <bol.plaza.api.PlazaAPI object at 0x7f823a2cdc50>
# MethodGroup => __init__()->  group transports
# PurchasableShippingLabelsMethods => __init__()->  api <bol.plaza.api.PlazaAPI object at 0x7f823a2cdc50>
# MethodGroup => __init__()->  group purchasable-shipping-labels
# api =>  ['PurchasableShippingLabels', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'orders', 'payments', 'private_key', 'process_status', 'public_key', 'request', 'session', 'shipments', 'timeout', 'transports', 'url', 'version']
# MethodGroup => request()->  method GET
# MethodGroup => request()->  path ?orderItemId=4283225730
# MethodGroup => request()->  params {}
# MethodGroup => request()->  data None
# PlazaAPI => request()->  method GET
# PlazaAPI => request()->  uri /services/rest/purchasable-shipping-labels/v2?orderItemId=4283225730
# PlazaAPI => request()->  params {}
# PlazaAPI => request()->  data None
# PlazaAPI => request()->  h  <hmac.HMAC instance at 0x7f82373b62d8>
# PlazaAPI => request()->  b64  El9osY0f1ZXHlOWDPLoxJlwqT+WT1TADjRU38mDz890=
# PlazaAPI => request()->  signature  BMWwKbEsujRfcOGLsPzqSSBcXOCvclwO:El9osY0f1ZXHlOWDPLoxJlwqT+WT1TADjRU38mDz890=
# PlazaAPI => request()->  request_kwargs {'url': 'https://plazaapi.bol.com/services/rest/purchasable-shipping-labels/v2?orderItemId=4283225730', 'headers': {'X-BOL-Authorization': 'BMWwKbEsujRfcOGLsPzqSSBcXOCvclwO:El9osY0f1ZXHlOWDPLoxJlwqT+WT1TADjRU38mDz890=', 'Content-Type': 'application/xml; charset=UTF-8', 'X-BOL-Date': 'Tue, 11 Jul 2017 19:41:56 GMT'}, 'params': {}, 'method': 'GET', 'timeout': None}
# PlazaAPI => request()->  resp <Response [401]>
# Traceback (most recent call last):
#   File "./test_py.py", line 22, in <module>
#     shipping_label = api.PurchasableShippingLabels.get(4283225730)
#   File "/home/demo/project/odoo/karan/git/github/python-bol-api/bol/plaza/api.py", line 218, in get
#     xml = self.request('GET', '?orderItemId={}'.format(id))
#   File "/home/demo/project/odoo/karan/git/github/python-bol-api/bol/plaza/api.py", line 77, in request
#     xml = self.api.request(method, uri, params=params, data=data)
#   File "/home/demo/project/odoo/karan/git/github/python-bol-api/bol/plaza/api.py", line 286, in request
#     asd = resp.raise_for_status()
#   File "/usr/lib/python2.7/dist-packages/requests/models.py", line 773, in raise_for_status
#     raise HTTPError(http_error_msg, response=self)
# requests.exceptions.HTTPError: 401 Client Error: Unauthorized
# demo@trial:~/project/odoo/karan/git/github/python-bol-api$



