from __future__ import annotations


class Offer:
    def __init__(self, *, id_number: int, price: float, title: str, link: str, category: Category):
        self.id_number = id_number
        self.price = price
        self.title = title
        self.link = link
        if not isinstance(category, Category):
            raise ValueError('category is not an instance of Category class!')
        self.category = category

    def __repr__(self):
        return self.title

    @property
    def category_list(self):
        return self.category.parents_list


class Category:
    def __init__(self, *, name: str, url: str, offers_amount: int, subcategories: [Category], offers: [Offer],
                 level: int,
                 parent: Category = None):
        self.name = name
        self.url = url
        self.offers_amount = offers_amount
        for subcategory in subcategories:
            if not isinstance(subcategory, Category):
                raise ValueError('subcategory is not an instance of Category class!')
        self.subcategories = subcategories
        for offer in offers:
            if not isinstance(offer, Offer):
                raise ValueError('offer is not an instance of Offer class!')
        self.offers = offers
        self.level = level
        if (not isinstance(parent, Category)) and (parent is not None):
            raise ValueError('parent is not an instance of Category lass!')
        self.parent = parent

    def __repr__(self):
        return self.name

    @property
    def parents_list(self):
        if self.parent is not None:
            if self.parent.parents_list is None:
                return self.name
            else:
                return self.parent.parents_list + ' - ' + self.name
        else:
            return None
