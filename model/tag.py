from odoo import models, _
import logging

_logger = logging.getLogger(__name__)

class TagImageProduct(models.Model):
    _inherit = 'product.tag'

    def set_image_product(self, batch_size=2000):
        """Set this tag's image to all linked product templates, in batches."""
        self.ensure_one()

        tag_img = self.image
        if not tag_img:
            _logger.info("Etiqueta '%s' no tiene imagen asignada. Proceso cancelado.", self.name)
            return 0

        ProductTemplate = self.env['product.template']
        total_updated = 0
        offset_id = 0

        while True:
            # Obtener lote de productos con esta etiqueta y id mayor al anterior
            products = ProductTemplate.search([
                ('product_tag_ids', 'in', self.id),
                ('id', '>', offset_id)
            ], order='id', limit=batch_size)

            if not products:
                break

            products.write({'image_1920': tag_img})
            offset_id = products[-1].id
            total_updated += len(products)

            # Invalida caché para mantener datos consistentes
            self.env.invalidate_all()

        _logger.info("Imagen de la etiqueta '%s' aplicada a %d productos.", self.name, total_updated)
        return total_updated
