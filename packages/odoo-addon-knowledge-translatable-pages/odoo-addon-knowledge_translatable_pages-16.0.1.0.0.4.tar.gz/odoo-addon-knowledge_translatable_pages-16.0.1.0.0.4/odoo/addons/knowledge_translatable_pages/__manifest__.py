# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Knowledge Translatable Pages",
    "version": "16.0.1.0.0",
    "description": """
        Translated Knowledge Pages and Categories
    """,
    "depends": [
        "base",
        "document_knowledge",
        "document_page",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Knowledge",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Translated Knowledge Pages and Categories
    """,
    "data": [
        "views/document_page_view.xml",
    ],
    "application": False,
    "installable": True,
}
