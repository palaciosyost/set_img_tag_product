from odoo import models, api

class TagImageProduct(models.Model):
    _inherit = 'product.tag'

    def set_image_product(self, batch_size=300, commit_each_batch=True):
        self.ensure_one()

        tag_img = self.image
        if not tag_img:
            return 0

        ProductT = self.env['product.template'].with_context(
            prefetch_fields=False,
            tracking_disable=True,
            mail_notrack=True,
        )

        last_id = 0
        total = 0

        while True:
            batch = ProductT.search(
                [('product_tag_ids', 'in', self.id), ('id', '>', last_id)],
                order='id',
                limit=batch_size
            )
            if not batch:
                break

            # Savepoint para que si algo falla no mate todo
            with self.env.cr.savepoint():
                batch.write({'image_1920': tag_img})

            total += len(batch)
            last_id = batch[-1].id

            if commit_each_batch:
                self.env.cr.commit()
                # MUY importante en procesos largos: libera cache ORM
                self.env.invalidate_all()

        return total
