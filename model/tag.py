from odoo import models

class TagImageProduct(models.Model):
    _inherit = 'product.tag'

    def set_image_product_sql(self, batch_size=2000):
        self.ensure_one()
        tag_img = self.image
        if not tag_img:
            return 0

        last_id = 0
        total = 0

        while True:
            self.env.cr.execute("""
                WITH to_upd AS (
                    SELECT pt.id
                    FROM product_template pt
                    JOIN product_tag_product_template_rel rel
                      ON rel.product_template_id = pt.id
                    WHERE rel.product_tag_id = %s
                      AND pt.id > %s
                    ORDER BY pt.id
                    LIMIT %s
                )
                UPDATE product_template pt
                   SET image_1920 = %s,
                       write_date = NOW()
                  FROM to_upd
                 WHERE pt.id = to_upd.id
                 RETURNING pt.id
            """, (self.id, last_id, batch_size, tag_img))

            ids = [r[0] for r in self.env.cr.fetchall()]
            if not ids:
                break

            total += len(ids)
            last_id = ids[-1]

            self.env.cr.commit()
            self.env.invalidate_all()

        return total
