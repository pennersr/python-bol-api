import requests

__all__ = ['OpenAPI']


class MethodGroup(object):

    def __init__(self, api, group):
        self.api = api
        self.group = group

    def request(self, method, path):
        uri = '/{group}/{version}/{path}'.format(
            group=self.group,
            method=method,
            path=path,
            version=self.api.version)
        return self.api.request(method, uri)


class CatalogMethods(MethodGroup):

    def __init__(self, api):
        super(CatalogMethods, self).__init__(api, 'catalog')

    def products(self, product_ids):
        path = 'products/' + ','.join(product_ids)
        return self.request('GET', path)


class OpenAPI(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://api.bol.com'
        self.version = 'v4'
        self.catalog = CatalogMethods(self)

    def request(self, method, uri):
        resp = requests.get(self.url + uri,
                            params={'apikey': self.api_key})
        resp.raise_for_status()
        data = resp.json()
        return data
