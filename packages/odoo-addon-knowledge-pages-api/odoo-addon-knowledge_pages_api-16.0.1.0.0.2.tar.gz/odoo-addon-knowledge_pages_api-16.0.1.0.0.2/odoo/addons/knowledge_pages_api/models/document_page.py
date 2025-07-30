from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

try:
    from jinja2.lexer import name_re as old_name_re
    import re

    name_re = re.compile("^%s$" % old_name_re.pattern)

except Exception:
    _logger.error("Jinja2 is not available")


class DocumentPage(models.Model):
    _inherit = "document.page"
    _order = "api_sequence"

    _sql_constraints = [
        (
            "unique_api_reference",
            "UNIQUE(api_reference)",
            _("API Reference field must be unique."),
        )
    ]

    is_api_available = fields.Boolean(
        string="Is available in API",
    )
    api_reference = fields.Char(
        compute="_compute_slug_api_reference",
        string="API Reference",
        help="The reference used to point to a particular Page or Category",
        store=True,
        readonly=False,
    )
    api_sequence = fields.Integer(string="API Sequence")
    api_highlighted_ids = fields.Many2many(
        "knowledge.page.highlight",
        relation="page_highlight_rel",
        column1="page_id",
        column2="highlight_id",
        string="Highlighted",
    )

    def _compute_slug_api_reference(self):
        for record in self:
            if not record.name:
                continue
            slug = self._string_to_slug(
                record.name
                + ((" " + record.parent_id.name) if record.parent_id else "")
            )
            domain = []
            i = 0
            if record.id:
                domain.append(("id", "!=", record.id))
            while self.search_count(domain + [("api_reference", "=", slug)]):
                i += 1
                slug = self._string_to_slug(
                    record.name
                    + ((" " + record.parent_id.name) if record.parent_id else "")
                    + " "
                    + str(i)
                )
            record.api_reference = slug

    def _string_to_slug(self, s):
        """Converts arbitrary string to slug."""
        # Remove symbols and replace spaces with underscores.
        cleaned = re.sub("[^\w\s-]", "", s).strip().lower()  # noqa
        slugified = re.sub("[-\s]+", "_", cleaned)  # noqa
        return slugified

    @api.constrains("api_reference")
    def _check_api_reference(self):
        for record in self:
            if record.is_api_available:
                if not record.api_reference:
                    continue
                if not name_re.match(record.api_reference):
                    raise ValidationError(_("API Reference is not valid"))
                if self.search(
                    [
                        ("api_reference", "=", record.api_reference),
                        ("id", "!=", record.id),
                    ]
                ):
                    raise ValidationError(_("API Reference must be unique"))

    @api.onchange("is_api_available")
    def _onchange_is_api_available(self):
        for record in self:
            if record.is_api_available and not record.api_reference:
                record._compute_slug_api_reference()

    def get_api_breadcrumb(self):
        self.ensure_one()
        """
        Retrieves a dictionary as a comprehensive breadcrumb with names and their references respectively.
        """
        breadcrumb = {
            "names": [self.name],  # String sequence
            "references": [self.api_reference],  # Int sequence
        }
        if self.parent_id:
            parent_breadcrumb = self.parent_id.get_api_breadcrumb()
            breadcrumb["names"] += parent_breadcrumb.get("names")
            breadcrumb["references"] += parent_breadcrumb.get("references")
        return breadcrumb

    def _is_this_api_available(self):
        self.ensure_one()
        # We need to check the tree for all the parents to be api_available
        if self.parent_id:
            return bool(
                self.is_api_available and self.parent_id._is_this_api_available()
            )
        else:
            return self.is_api_available

    def export_api_json(self, unfold=False, lang=False, breadcrumbs=False):
        self.ensure_one()
        if not self._is_this_api_available():
            return []
        if lang:
            record = self.with_context({"lang": lang})
        else:
            record = self.with_context({"lang": self.env.user.lang})

        if record.type == "category":
            children = record.child_ids.filtered(lambda child: child.is_api_available)
            return {
                "reference": record.api_reference,
                "name": record.name,
                "type": record.type,
                "content": record.translated_api_content,
                "api_sequence": record.api_sequence,
                "childs": list(
                    child.export_api_json(unfold, record.env.context.get("lang"))
                    for child in children
                ),
            }
        elif record.type == "content":
            to_return = {
                "name": record.name,
                "reference": record.api_reference,
                "api_sequence": record.api_sequence,
                "type": record.type,
                "tags": [tag.name for tag in record.tag_ids],
            }

            # if not unfold then the flow comes from categories endpoint.
            if unfold:
                to_return.update(
                    {
                        "content": record.translated_api_content,
                        "parent_reference": record.parent_id.api_reference,
                    }
                )
            else:
                to_return.update(
                    {
                        "highlighted": [
                            [hl.name, hl.code] for hl in record.api_highlighted_ids
                        ]
                    }
                )

            # Now for the breadcrumbs
            if breadcrumbs:
                to_return.update({"breadcrumb": record.get_api_breadcrumb()})
            return to_return
