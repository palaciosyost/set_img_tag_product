from odoo import models

class TagImageProduct(models.Model):
    _inherit = 'product.tag'

    def set_image_product(self, batch_size=2000):
        self.ensure_one()
        tag_img = self.image
        if not tag_img:
            return 0

        last_id = 0
        total = 0
        ProductTemplate = self.env['product.template']

        while True:
            # Buscar productos relacionados al tag, por batch
            products = ProductTemplate.search([
                ('product_tag_ids', 'in', self.id),
                ('id', '>', last_id)
            ], order='id', limit=batch_size)

            if not products:
                break

            # Actualizar imagen en lote
            products.write({'image_1920': tag_img})
            last_id = products[-1].id
            total += len(products)

            # Invalida cache por seguridad
            self.env.invalidate_all()

        return total
