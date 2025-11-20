from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    is_sellable = fields.Boolean('Verkoopbaar volgens criteria', default=False)
