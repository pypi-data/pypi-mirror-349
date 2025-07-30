from odoo import models, fields, api
from odoo.tools.translate import code_translations


class DocumentPage(models.Model):
    _inherit = "document.page"

    name = fields.Char("Title", required=True, translate=True)  # IMP
    content = fields.Text(
        "Content",
        compute="_compute_content",
        inverse="_inverse_content",
        search="_search_content",
        required=True,
        copy=True,
        translate=True,  # IMP
        store=True,
    )
    translated_api_content = fields.Text(
        "Content",
        compute="_compute_translated_api_content",
        store=False,
    )

    def _compute_translated_api_content(self):
        for record in self:
            translated_content_record = False
            if record.content:
                lang = record.env.context.get("lang", self.env.user.lang)
                translated_content_record = self.get_translation(
                    record.content, lang, "document.page"
                )
            record.translated_api_content = (
                translated_content_record
                if translated_content_record
                else record.content
            )

    @api.model
    def search_translated_api_content(self, search_term):
        translated_content_record = []
        if search_term:
            lang = self.env.context.get("lang", self.env.user.lang)
            translated_content_record = self.get_translation(
                search_term, lang, "document.page"
            )
        return self.browse([res.get("res_id") for res in translated_content_record])

    @staticmethod
    def get_translation(source, lang, mods):
        translation = code_translations.get_web_translations(mods, lang)
        translation.update(code_translations.get_python_translations(mods, lang))
        return translation.get(source, source)
