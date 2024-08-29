from peewee import *

db = PostgresqlDatabase(
"bearingsdb",
    host="dpg-cr3vor3v2p9s73cj9rq0-a.singapore-postgres.render.com",
    port=5432,
    user="bearingsdb_user",
    password="yQFq9qk4UQZB8sZoAGKAhsPTJUqHNFqR"
)


class Category(Model):
    idCategory = IntegerField(primary_key=True, column_name='idCategory')
    categoryName = TextField()
    categoryPicture = TextField()

    class Meta:
        database = db
        db_table = 'tblCategory'


class Manufacturer(Model):
    idManufacturer = IntegerField(primary_key=True, column_name='idManufacturer')
    manufacturerName = IntegerField()
    manufacturerPicture = IntegerField()

    class Meta:
        database = db
        db_table = 'tblManufacturer'


if __name__ == '__main__':
    records = Manufacturer.select()
    for record in records:
        print(record.idManufacturer, record.manufacturerName)