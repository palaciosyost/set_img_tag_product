from odoo import models, fields, api



class TagImageProduct(models.Model):
    _inherit = 'product.tag'

    def set_image_product(self, batch_size=2000, commit_each_batch=False):
        """
        Copia la imagen del tag a image_1920 de todos los product.template que tengan este tag.
        - batch_size: tamaño del lote (1000–5000 suele ir bien)
        - commit_each_batch: úsalo en cron/procesos largos (no en botón normal)
        """
        self.ensure_one()

        # imagen binaria del tag
        tag_img = self.image
        if not tag_img:
            return 0

        ProductT = self.env['product.template'].with_context(prefetch_fields=False)

        last_id = 0
        total = 0

        while True:
            domain = [
                ('product_tag_ids', 'in', self.id),
                ('id', '>', last_id),
            ]
            batch = ProductT.search(domain, order='id', limit=batch_size)
            if not batch:
                break

            # 1 write por lote (mucho más rápido)
            batch.write({'image_1920': tag_img})

            total += len(batch)
            last_id = batch[-1].id

            # Para crons/procesos largos ayuda a no reventar RAM/locks
            if commit_each_batch:
                self.env.cr.commit()

        return total
