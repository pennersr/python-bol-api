import json

from bol.openapi.api import OpenAPI

from httmock import HTTMock, urlmatch


RESPONSE = {
    "products": [{
        "id": "9200000019250795",
        "ean": "4044163011066",
        "gpc": "sto",
        "title": "Christopeit AL-1 - Hometrainer - Zilver",
        "specsTag": "Christopeit",
        "rating": 40,
        "shortDescription": "De AL 1 van Christopeit is een top ",
        "longDescription": "De AL 1 van Christopeit is een top hometrainer",
        "attributeGroups": [
            {
                "title": "Productinformatie"
            },
            {
                "title": "Productspecificaties",
                "attributes": [
                    {
                        "key": "TYPE_OF_EXERCISE_MACHINE_NP",
                        "label": "Soort product",
                        "value": "Hometrainer"
                    }
                ]
            }
        ],
        "urls": [{
            "key": "DESKTOP",
            "value": "http://www.bol.com/nl/p/christopeit-al-1-hometrainer-zilver/9200000019250795/"
        }],
        "images": [{
            "type": "IMAGE",
            "key": "XS",
            "url": "http://s.s-bol.com/imgbase0/imagebase/mini/FC/5/9/7/0/9200000019250795.jpg"
        }],
        "media": [{
            "type": "IMAGE",
            "key": "XL",
            "url": "http://s.s-bol.com/imgbase0/imagebase/large/FC/5/9/7/0/9200000019250795.jpg"
        }],
        "offerData": {
            "bolCom": 0,
            "nonProfessionalSellers": 0,
            "professionalSellers": 1,
            "offers": [{
                "id": "1001024447376003",
                "condition": "Nieuw",
                "price": 229.0,
                "availabilityCode": "17",
                "availabilityDescription": "Op werkdagen voor 15.00 uur",
                "comment": "Op werkdagen voor 15.00 uur besteld is",
                "seller": {
                    "id": "835124",
                    "sellerType": "Grootzakelijke verkoper",
                    "displayName": "Buffalo",
                    "topSeller": False,
                    "logo": "JPG",
                    "sellerRating": {
                        "ratingMethod": "THREE_MONTHS",
                        "sellerRating": "8.4",
                        "deliveryTimeRating": "8.8",
                        "shippingRating": "8.8",
                        "serviceRating": "8.3"
                    },
                    "recentReviewCounts": {
                        "positiveReviewCount": 463,
                        "neutralReviewCount": 76,
                        "negativeReviewCount": 25,
                        "totalReviewCount": 564
                    },
                    "allReviewsCounts": {
                        "positiveReviewCount": 1283,
                        "neutralReviewCount": 275,
                        "negativeReviewCount": 83,
                        "totalReviewCount": 1641
                    },
                    "sellerInformation": "Buffalo\r\n\r\nSport en Spel",
                    "useWarrantyRepairConditions": False,
                    "approvalPercentage": "94.9"
                },
                "bestOffer": True
            }]
        },
        "parentCategoryPaths": []
    }]
}


@urlmatch(path=r'/catalog/v4/products/1,2$')
def products_stub(url, request):
    return {
        'status_code': 200,
        'content': json.dumps(RESPONSE).encode('utf-8'),
    }


def test_openapi():
    with HTTMock(products_stub):
        api = OpenAPI('secret')

        products = api.catalog.products(['1', '2'])

        assert products == RESPONSE
