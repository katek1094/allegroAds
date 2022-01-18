class Offer:
    def __init__(self, *, id_number: int, price: float, title: str, link: str):
        self.id_number = id_number
        self.price = price
        self.title = title
        self.link = link

    def __repr__(self):
        return self.title


class Category:
    def __init__(self, *, name: str, url: str, offers_amount: int, subcategories: [], offers: [], level: int):
        self.name = name
        self.url = url
        self.offers_amount = offers_amount
        for subcategory in subcategories:
            if not isinstance(subcategory, Category):
                raise ValueError('subcategory is not and instance of Category class!')
        self.subcategories = subcategories
        for offer in offers:
            if not isinstance(offer, Offer):
                raise ValueError('offer is not and instance of Offer class!')
        self.offers = offers
        self.level = level

    def __repr__(self):
        return self.name
