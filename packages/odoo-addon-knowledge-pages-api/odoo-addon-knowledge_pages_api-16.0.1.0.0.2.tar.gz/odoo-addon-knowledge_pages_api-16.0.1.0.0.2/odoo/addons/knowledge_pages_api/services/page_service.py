# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from werkzeug.urls import url_decode
import logging


_logger = logging.getLogger(__name__)


class KnowledgeCategoriesAPI(Component):
    _name = "knowledge.categories.api"
    _inherit = "base.rest.service"
    _usage = "knowledge"
    _default_auth = "api_key"
    _collection = "api_common_base.services"
    _description = """
    Knowledge Categories API
    Access to the knowledge categories with GET method
    """

    def _get_query_schema_general(self):
        return {
            "lang": {
                "type": "string",
                "required": False,
                "allowed": self.env["res.lang"]
                .search([("active", "=", True)])
                .mapped(lambda x: x.code),
            },
            "category_initial": {
                "type": "string",
                "required": False,
            },
        }

    def _get_query_schema_specific(self):
        to_return = self._get_query_schema_general()
        del to_return["category_initial"]
        return to_return

    #   --  CATEGORIES ENDPOINT  --

    @restapi.method(
        [(["/categories/"], "GET")],
        input_param=restapi.CerberusValidator("_get_query_schema_general"),
    )  # noqa
    def get_categories(self, category_initial=None, lang=None):
        return self._get_categories_internally(
            category_initial=category_initial, lang=lang
        )

    @restapi.method(
        [(["/categories/<string:reference>"], "GET")],
        input_param=restapi.CerberusValidator("_get_query_schema_specific"),
    )  # noqa
    def get_categories_by_reference(self, reference, lang=None):
        return self._get_categories_internally(category_initial=reference, lang=lang)

    def _get_categories_internally(self, category_initial=None, lang=None):
        domain = [
            ("type", "=", "category"),
            ("is_api_available", "=", True),
        ]
        if category_initial:
            # For a specific category
            domain.append(("api_reference", "=", category_initial))
        else:
            # For the general use...
            domain.append(("parent_id", "=", False))
        categories = self.env["document.page"].search(
            domain, limit=bool(category_initial)
        )
        if not categories:
            raise ValidationError("Record doesn't exists or is unavaliable")
        result = []
        for category in categories:
            result.append(category.export_api_json(unfold=False, lang=lang))
        _logger.debug(result)
        return request.make_json_response(result)

    #   --  PAGES ENDPOINT  --

    @restapi.method(
        [(["/page/<string:reference>"], "GET")],
        input_param=restapi.CerberusValidator("_get_query_schema_specific"),
    )
    def get_page(self, reference, lang=None):
        page = self.env["document.page"].search(
            [("api_reference", "=", reference)], limit=1
        )
        if not page.exists() or not page.is_api_available or page.type != "content":
            raise ValidationError("Record doesn't exist or is unavaliable")
        result = page.export_api_json(unfold=True, lang=lang)
        _logger.debug(result)
        return request.make_json_response(result)

    @restapi.method(
        [(["/page/tag/<string:tag>"], "GET")],
        input_param=restapi.CerberusValidator("_get_query_schema_specific"),
    )
    def get_page_by_tag(self, tag, lang=None):
        ctx = {"lang": lang or self.env.user.lang}

        tag_ids = (
            self.env["document.page.tag"]
            .with_context(ctx)
            .search([("name", "=ilike", tag)])
            .ids
        )
        if not tag_ids:  # ORM won't return archived tags, no need to check for active
            raise ValidationError("No active tag was found with the name '%s'" % tag)

        pages = (
            self.env["document.page"]
            .with_context(ctx)
            .search(
                [
                    ("tag_ids", "in", tag_ids),
                    ("is_api_available", "=", True),
                    ("type", "=", "content"),
                ]
            )
        )

        # We should check the parenting path so it is eligible
        pages = pages.filtered(lambda page: page._is_this_api_available())
        if not pages:
            raise ValidationError("Record doesn't exists or is unavaliable")

        result = [
            page.export_api_json(unfold=False, lang=lang, breadcrumbs=True)
            for page in pages
        ]
        _logger.debug(result)
        return request.make_json_response(result)

    #   --  SEARCH ENDPOINT  --

    @restapi.method(
        [(["/search/<string:keyword>"], "GET")],
        input_param=restapi.CerberusValidator("_get_query_schema_specific"),
    )  # noqa
    def search_page(self, keyword, lang=None):
        keyword = [a for a in url_decode(keyword).keys()][
            0
        ]  # decoding the search term keyword
        if lang:
            pages_object = self.env["document.page"].with_context({"lang": lang})
        else:
            pages_object = self.env["document.page"].with_context(
                {"lang": self.env.user.lang}
            )

        pages = pages_object.search(
            [
                ("type", "=", "content"),
                ("is_api_available", "=", True),
                ("name", "ilike", keyword),
            ]
        )
        # pages = pages | pages_object.search_translated_api_content(keyword)
        if not pages:
            raise ValidationError("Record doesn't exists or is unavaliable")
        # We should check the parenting path so it is eligible
        pages = pages.filtered(lambda page: page._is_this_api_available())
        result = [
            page.export_api_json(unfold=False, lang=lang, breadcrumbs=True)
            for page in pages
        ]
        _logger.debug(result)
        return request.make_json_response(result)

    #   --  PAGES BY HIGHLIGHTED ENDPOINT  --

    @restapi.method(
        [(["/highlighted/<string:highlighted_code>"], "GET")],
        input_param=restapi.CerberusValidator("_get_query_schema_specific"),
    )  # noqa
    def get_highlighted_pages(self, highlighted_code, lang=None):
        highlight = self.env["knowledge.page.highlight"].search(
            [("code", "=", highlighted_code)], limit=1
        )
        if not highlight.exists() or not highlight.active:
            raise ValidationError(
                "The specified highlight does not exist or is inactive."
            )

        page_ids = highlight.page_ids
        if not page_ids:
            raise ValidationError("No pages found for the highlighted code.")
        page_ids = page_ids.filtered(lambda page: page._is_this_api_available())
        if not page_ids:
            raise ValidationError("No pages found for the highlighted code.")
        result = [
            page.export_api_json(unfold=True, lang=lang, breadcrumbs=True)
            for page in page_ids
        ]

        _logger.debug(result)
        return request.make_json_response(result)
