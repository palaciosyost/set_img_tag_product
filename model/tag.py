from odoo import models, fields, api



class TagImageProduct(models.Model):
    _inherit = 'product.tag'

    def set_image_product(self):
        products = self.env['product.template'].search([('product_tag_ids', 'in', self.id)])
        for product in products:
            product.image_1920 = self.image