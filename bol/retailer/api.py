import requests

from .models import (
    Invoice,
    Invoices,
    InvoiceSpecification,
    Order,
    Orders,
    ProcessStatus,
    ProcessStatuses,
    Shipment,
    Shipments,
)

__all__ = ["RetailerAPI"]


class MethodGroup(object):
    def __init__(self, api, group):
        self.api = api
        self.group = group

    def request(self, method, path="", params={}, **kwargs):
        uri = path
        if not uri.startswith("/"):
            base = "retailer-demo" if self.api.demo else "retailer"
            uri = "/{base}/{group}{path}".format(
                base=base,
                group=self.group,
                path=("/{}".format(path) if path else ""),
            )
        return self.api.request(method, uri, params=params, **kwargs)


class OrderMethods(MethodGroup):
    def __init__(self, api):
        super(OrderMethods, self).__init__(api, "orders")

    def list(self, fulfilment_method=None, page=None):
        params = {}
        if fulfilment_method:
            params["fulfilment-method"] = fulfilment_method
        if page is not None:
            params["page"] = page
        resp = self.request("GET", params=params)
        return Orders.parse(self.api, resp.text)

    def get(self, order_id):
        resp = self.request("GET", path=order_id)
        return Order.parse(self.api, resp.text)

    def ship_order_item(
        self,
        order_item_id,
        shipment_reference=None,
        shipping_label_code=None,
        transporter_code=None,
        track_and_trace=None,
    ):
        payload = {}
        if shipment_reference:
            payload["shipmentReference"] = shipment_reference
        if shipping_label_code:
            payload["shippingLabelCode"] = shipping_label_code
        if transporter_code:
            payload.setdefault("transport", {})[
                "transporterCode"
            ] = transporter_code
        if track_and_trace:
            payload.setdefault("transport", {})[
                "trackAndTrace"
            ] = track_and_trace
        resp = self.request(
            "PUT", path="{}/shipment".format(order_item_id), json=payload
        )
        return ProcessStatus.parse(self.api, resp.text)

    def cancel_order_item(self, order_item_id, reason_code):
        payload = {"reasonCode": reason_code}
        resp = self.request(
            "PUT", path="{}/cancellation".format(order_item_id), json=payload
        )
        return ProcessStatus.parse(self.api, resp.text)


class ShipmentMethods(MethodGroup):
    def __init__(self, api):
        super(ShipmentMethods, self).__init__(api, "shipments")

    def list(self, fulfilment_method=None, page=None, order_id=None):
        params = {}
        if fulfilment_method:
            params["fulfilment-method"] = fulfilment_method.value
        if page is not None:
            params["page"] = page
        if order_id:
            params["order_id"] = order_id
        resp = self.request("GET", params=params)
        return Shipments.parse(self.api, resp.text)

    def get(self, shipment_id):
        resp = self.request("GET", path=str(shipment_id))
        return Shipment.parse(self.api, resp.text)


class ProcessStatusMethods(MethodGroup):
    def __init__(self, api):
        super(ProcessStatusMethods, self).__init__(api, "process-status")

    def get(self, entity_id, event_type, page=None):
        params = {"entity-id": entity_id, "event-type": event_type}
        if page:
            params["page"] = page
        resp = self.request("GET", params=params)
        return ProcessStatuses.parse(self.api, resp.text)


class InvoiceMethods(MethodGroup):
    def __init__(self, api):
        super(InvoiceMethods, self).__init__(api, "invoices")

    def list(self, period_start=None, period_end=None):
        params = {}
        resp = self.request("GET", params=params)
        return Invoices.parse(self.api, resp.text)

    def get(self, invoice_id):
        resp = self.request("GET", path=str(invoice_id))
        return Invoice.parse(self.api, resp.text)

    def get_specification(self, invoice_id, page=None):
        params = {}
        if page is not None:
            params["page"] = page
        resp = self.request(
            "GET", path="{}/specification".format(invoice_id), params=params
        )
        return InvoiceSpecification.parse(self.api, resp.text)


class RetailerAPI(object):
    def __init__(
        self,
        test=False,
        timeout=None,
        session=None,
        demo=False,
        api_url=None,
        login_url=None,
        refresh_token=None,
    ):
        self.demo = demo
        self.api_url = api_url or "https://api.bol.com"
        self.login_url = login_url or "https://login.bol.com"
        self.timeout = timeout
        self.refresh_token = refresh_token
        self.orders = OrderMethods(self)
        self.shipments = ShipmentMethods(self)
        self.invoices = InvoiceMethods(self)
        self.process_status = ProcessStatusMethods(self)
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def login(self, client_id, client_secret):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        resp = self.session.post(
            self.login_url + "/token",
            auth=(client_id, client_secret),
            data=data,
        )
        resp.raise_for_status()
        token = resp.json()
        self.set_access_token(token["access_token"])
        return token

    def refresh_access_token(
        self,
        username,
        password,
        refresh_token=None
    ):

        if refresh_token is None and self.refresh_token is None:
            raise ValueError("No 'refresh_token' provided")

        if refresh_token is None and self.refresh_token is not None:
            refresh_token = self.refresh_token

        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        resp = self.session.post(
            self.login_url + "/token",
            params=params,
            auth=(username, password),
        )
        resp.raise_for_status()
        data = resp.json()
        self.refresh_token = data["refresh_token"]
        self.set_access_token(data["access_token"])
        return data

    def set_access_token(self, access_token):
        self.session.headers.update(
            {
                "Authorization": "Bearer " + access_token,
                "Accept": "application/vnd.retailer.v3+json",
            }
        )

    def request(self, method, uri, params={}, **kwargs):
        request_kwargs = dict(**kwargs)
        request_kwargs.update(
            {
                "method": method,
                "url": self.api_url + uri,
                "params": params,
                "timeout": self.timeout,
            }
        )
        if "json" in request_kwargs:
            if "headers" not in request_kwargs:
                request_kwargs["headers"] = {}
            # If these headers are not added, the api returns a 400
            # Reference:
            #   https://api.bol.com/retailer/public/conventions/index.html
            request_kwargs["headers"].update({
                "content-type": "application/vnd.retailer.v3+json"
            })
        resp = self.session.request(**request_kwargs)
        resp.raise_for_status()
        return resp
