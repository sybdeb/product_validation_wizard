from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductValidationWizard(models.TransientModel):
    _name = 'product.validation.wizard'
    _description = 'Product Validation Wizard'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    min_stock_required = fields.Integer('Minimale voorraad vereist', default=10)  # Configureerbaar 'x'
    is_valid = fields.Boolean('Geldig voor publicatie', compute='_compute_validity')
    reasons = fields.Text('Redenen voor afkeuring', compute='_compute_validity')
    image_present = fields.Boolean('Foto aanwezig', compute='_compute_checks')
    price_set = fields.Boolean('Prijs ingesteld', compute='_compute_checks')
    supplier_stock_ok = fields.Boolean('Leveranciersvoorraad OK', compute='_compute_checks')
    sellable_ok = fields.Boolean('Verkoopbaar volgens criteria', compute='_compute_checks')

    @api.depends('product_id', 'min_stock_required')
    def _compute_checks(self):
        for wizard in self:
            if not wizard.product_id:
                wizard.image_present = wizard.price_set = wizard.supplier_stock_ok = wizard.sellable_ok = False
                return

            product = wizard.product_id
            # Check 1: Foto aanwezig
            wizard.image_present = bool(product.image_1920)

            # Check 2: Prijs ingesteld
            wizard.price_set = product.list_price > 0

            # Check 3: Voorraad goedkoopste leverancier >= min_stock_required
            suppliers = product.seller_ids
            if not suppliers:
                wizard.supplier_stock_ok = False
            else:
                valid_suppliers = [s for s in suppliers if s.price is not False and s.price >= 0]
                if not valid_suppliers:
                    wizard.supplier_stock_ok = False
                else:
                    cheapest_supplier = min(valid_suppliers, key=lambda s: s.price)
                    stock_level = getattr(cheapest_supplier, 'supplier_stock', 0) or 0  # Uit supplier_pricelist_sync
                    wizard.supplier_stock_ok = stock_level >= wizard.min_stock_required

            # Check 4: Verkoopcriteria (custom veld; voeg toe aan product.product als nodig)
            wizard.sellable_ok = getattr(product, 'is_sellable', True)  # Default True als veld niet bestaat

    @api.depends('image_present', 'price_set', 'supplier_stock_ok', 'sellable_ok')
    def _compute_validity(self):
        for wizard in self:
            all_ok = wizard.image_present and wizard.price_set and wizard.supplier_stock_ok and wizard.sellable_ok
            wizard.is_valid = all_ok
            if not all_ok:
                reasons = []
                if not wizard.image_present: reasons.append('Geen foto')
                if not wizard.price_set: reasons.append('Geen prijs ingesteld')
                if not wizard.supplier_stock_ok: reasons.append(f'Voorraad goedkoopste leverancier < {wizard.min_stock_required}')
                if not wizard.sellable_ok: reasons.append('Niet verkoopbaar volgens criteria')
                wizard.reasons = '; '.join(reasons)
            else:
                wizard.reasons = ''

    def action_validate(self):
        if self.is_valid:
            self.product_id.write({'is_published': True})
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise ValidationError(f'Product niet goedgekeurd: {self.reasons}')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['product_id'] = self.env.context.get('active_id')
        return res
