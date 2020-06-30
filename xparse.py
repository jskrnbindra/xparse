import logging
from lxml import etree
from io import StringIO
from ExtractionFailedException import ExtractionFailedException


class XParse(object):
    """
    Parser to extract a lead from an email.
    """

    LEAD_TYPE_BUYER = 'BUYER'
    LEAD_TYPE_SELLER = 'SELLER'

    XPATH = {
        'name':       "//td/font[@class='font16']/strong",
        'phone':      "//td/font[text()='Every minute counts, make contact as soon as possible']",
        'email':      "//td/font[text()='Every minute counts, make contact as soon as possible'']",
        'beds':       "//font[normalize-space(text())='Beds']",
        'listed':     "//tr/td/font[last() and @class='font12' and normalize-space(text())='Listed']",
        'searching':  "//tr/td/font[last() and @class='font12' and normalize-space(text())='Searching']"
    }

    def __init__(self, html):
        self.tree = self.to_dom_tree(html)

    def extract_lead(self):
        name = self.extract_name()
        lead_type = self.infer_lead_type()
        contact_info = self.extract_contact_info()
        property_details = self.extract_property_details()

        lead = {'name': name, 'type': lead_type}
        lead.update(contact_info)
        lead.update(property_details)

        return lead

    def extract_name(self):
        matches = self.tree.xpath(XParse.XPATH['name'])
        if not matches:
            raise ExtractionFailedException('name')
        return str(matches[0].text).strip()

    def extract_contact_info(self):
        matches = self.tree.xpath(XParse.XPATH['phone'])
        if not matches:
            raise ExtractionFailedException('contact info')
        first_tr = matches[0].getparent().getparent()

        phone_tr = first_tr.getnext()
        email_tr = phone_tr.getnext()

        phone_ele = phone_tr.xpath('td/font/a')[0]
        phone = str(phone_ele.text).strip()

        email_ele = email_tr.xpath('td/font/a')[0]
        email = str(email_ele.text).strip()

        return {
            'phone': phone,
            'email': email
        }

    def extract_property_details(self):

        def move_to_address_node(beds_node):
            return beds_node.getprevious().getprevious()\
                .getprevious().getprevious()

        matches = self.tree.xpath(XParse.XPATH['beds'])
        if not matches:
            raise ExtractionFailedException('beds')
        beds_parent = matches[0]
        beds, baths = [x.text.strip() for x in beds_parent.getchildren()]
        address_parent = move_to_address_node(beds_parent)
        address = address_parent.xpath('strong/a')
        if not address:
            raise ExtractionFailedException('address')
        address = address[0].text.strip()

        return {
            'beds': beds,
            'baths': baths,
            'address': address
        }

    def infer_lead_type(self):
        contains_searching = self.tree.xpath(XParse.XPATH['searching'])
        if contains_searching:
            return XParse.LEAD_TYPE_BUYER
        contains_listed = self.tree.xpath(XParse.XPATH['listed'])
        if contains_listed:
            return XParse.LEAD_TYPE_SELLER
        raise ExtractionFailedException('lead_type')

    @staticmethod
    def to_dom_tree(html):
        html_as_file = StringIO(html)
        html_parser = etree.HTMLParser()
        dom_tree = etree.parse(html_as_file, parser=html_parser)

        return dom_tree
