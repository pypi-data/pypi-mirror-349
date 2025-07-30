from odoo import models, fields


class KnowledgePageHighlight(models.Model):
    _name = "knowledge.page.highlight"
    _description = "Knowledge Page Highlight"

    name = fields.Char(string="Name", required=True, translate=True)
    code = fields.Char(
        string="Code", required=True, help="Unique code to identify the highlight."
    )
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(default=True)
    page_ids = fields.Many2many(
        "document.page",
        relation="page_highlight_rel",
        column1="highlight_id",
        column2="page_id",
        string="Pages",
    )

    _sql_constraints = [
        ("unique_name", "unique(name)", "Tags name must me unique"),
        ("unique_code", "unique(code)", "Tags code must me unique"),
    ]
