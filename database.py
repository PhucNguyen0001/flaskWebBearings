from peewee import *

db = PostgresqlDatabase(
    "bearingsdb",
    host="dpg-cr3vor3v2p9s73cj9rq0-a.singapore-postgres.render.com",
    port=5432,
    user="bearingsdb_user",
    password="yQFq9qk4UQZB8sZoAGKAhsPTJUqHNFqR"
)


class BaseModel(Model):
    class Meta:
        database = db

class Manufacturer(BaseModel):
    idManufacturer = IntegerField(primary_key=True, column_name='idManufacturer')
    manufacturerName = CharField()
    manufacturerPicture = TextField()

    class Meta:
        table_name = 'tblManufacturer'


class Category(BaseModel):
    idCategory = IntegerField(primary_key=True, column_name='idCategory')
    categoryName = CharField()
    categoryPicture = TextField()

    class Meta:
        table_name = 'tblCategory'


class Parameter(BaseModel):
    idParameter = IntegerField(primary_key=True, column_name='idParameter')
    describe = TextField()

    class Meta:
        table_name = 'tblParameter'


class Bearing(BaseModel):
    idBearing = IntegerField(primary_key=True, column_name='idBearing')
    bearingName = TextField()
    idManufacturer = ForeignKeyField(Manufacturer, backref='bearings', column_name='idManufacturer')
    idCategory = ForeignKeyField(Category, backref='bearings', column_name='idCategory')
    bearingDescribe = TextField(null=True)
    bearingPicture = TextField(null=True)

    class Meta:
        table_name = 'tblBearings'


class BearingParameter(BaseModel):
    idBearingParameter = IntegerField(primary_key=True, column_name='idBearingParameter')
    idBearing = ForeignKeyField(Bearing, backref='parameters', column_name='idBearing')
    idParameter = ForeignKeyField(Parameter, backref='parameters', column_name='idParameter')
    value = IntegerField()

    class Meta:
        table_name = 'tblBearing_Parameter'


def add_category(categoryName, categoryPicture):
    query = Category.insert(categoryName=categoryName,
                            categoryPicture=categoryPicture)
    query.execute()


def add_manufacturer(manufacturerName, manufacturerPicture):
    query = Manufacturer.insert(manufacturerName=manufacturerName,
                                manufacturerPicture=manufacturerPicture)
    query.execute()


def select_vongbi():
    query = db.execute_sql("""
        select "bearingName", "manufacturerName", "categoryName", "idBearing"
        from "tblBearings"
        join "tblCategory" on "tblBearings"."idCategory" = "tblCategory"."idCategory"
        join "tblManufacturer" on "tblBearings"."idManufacturer" = "tblManufacturer"."idManufacturer"
    """)
    return query



def add_bearing(product_code, manufacturer_id, category_id, bearing_describe, image_str, parameters):
    with db.atomic() as transaction:
        try:
            new_bearing = Bearing.create(
                bearingName=product_code,
                idManufacturer=manufacturer_id,
                idCategory=category_id,
                bearingDescribe=bearing_describe,
                bearingPicture=image_str
            )

            for parameter_id, value in parameters.items():
                BearingParameter.create(
                    idBearing=new_bearing.idBearing,
                    idParameter=parameter_id,
                    value=value
                )

            return new_bearing
        except Exception as e:
            transaction.rollback()
            raise e



def get_bearing_by_id(bearing_id):
    return Bearing.get_by_id(bearing_id)

def update_bearing(bearing_id, product_code, manufacturer_id, category_id, bearing_describe, image_str, parameters):
    with db.atomic() as transaction:
        try:
            bearing = Bearing.get_by_id(bearing_id)
            bearing.bearingName = product_code
            bearing.idManufacturer = manufacturer_id
            bearing.idCategory = category_id
            bearing.bearingDescribe = bearing_describe
            if image_str:
                bearing.bearingPicture = image_str
            bearing.save()

            # Update or create parameters
            for parameter_id, value in parameters.items():
                BearingParameter.update_or_create(
                    idBearing=bearing.idBearing,
                    idParameter=parameter_id,
                    defaults={'value': value}
                )

            return bearing
        except Exception as e:
            transaction.rollback()
            raise e



if __name__ == '__main__':
    # records = select_vongbi()
    # for record in records:
    #     print(record[0], record[1], record[2])
    # print(records)
    records = Parameter.select()
    for record in records:
        print(record.idParameter, record.describe)
