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

    def search(self, query):
        """
        query might be 'Harry Potter', 'an_EAN' or 'an_ISBN'.
        For exact search, use extra quotation marks, for example:
        '"Harry Potter"'.
        """
        path = 'search/'
        return self.request('GET', path, {'q': query})


class OpenAPI(object):

    def __init__(self, api_key, timeout=None, session=None):
        self.api_key = api_key
        self.url = 'https://api.bol.com'
        self.version = 'v4'
        self.catalog = CatalogMethods(self)
        self.timeout = timeout
        self.session = session or requests.Session()

    def request(self, method, uri, params={}):
        resp = self.session.get(
            self.url + uri,
            params=dict(params, **{'apikey': self.api_key}),
            timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data
