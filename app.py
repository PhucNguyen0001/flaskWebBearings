from flask import Flask, render_template, request
from database import *
from base64forfiles import file_to_base64
app = Flask(__name__)




@app.route('/test')
def test():
    return render_template('themchungloai.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/qlchungloai')
def qlchungloai():
    return render_template('qlchungloai.html', category=Category.select())


@app.route('/qlhangsx')
def qlhangsx():
    return render_template('qlhangsx.html', manufacturer=Manufacturer.select())


@app.route('/qlvongbi')
def qlvongbi():
    return render_template('qlvongbi.html', bearings=select_vongbi())


@app.route('/themchungloai', methods=['GET', "POST"])
def themchungloai():
    if request.method == 'POST':
        categoryName = request.form.get('categoryName')
        file = request.files.get('pictureFile')
        if file:
            try:
                file_content = file.read()
                image_str = f"data:image/{file.filename.split('.')[-1]};base64,{file_to_base64(file_content)}"
                add_category(categoryName, image_str)
                return "Thêm thành công"
            except Exception as e:
                return f"Lỗi: {e}", 400
        else:
            return "No file uploaded"
    return render_template('themchungloai.html')


@app.route('/themhangsx', methods=['GET', "POST"])
def themhangsx():
    if request.method == 'POST':
        manufacturerName = request.form.get('manufacturerName')
        file = request.files.get('pictureFile')
        if file:
            try:
                file_content = file.read()
                image_str = f"data:image/{file.filename.split('.')[-1]};base64,{file_to_base64(file_content)}"
                add_manufacturer(manufacturerName, image_str)
                return "Thêm thành công"
            except Exception as e:
                return f"Lỗi: {e}", 400
        else:
            return "No file uploaded"
    return render_template('themhangsx.html')


@app.route('/themvongbi', methods=['GET', 'POST'])
def themvongbi():
    if request.method == 'POST':
        try:
            # Get basic bearing info
            product_code = request.form.get('productCode')
            manufacturer_id = request.form.get('manufacturer')
            category_id = request.form.get('category')
            bearing_describe = request.form.get('bearingDescribe')

            # Handle image upload
            file = request.files.get('pictureFile')
            image_str = None
            if file:
                file_content = file.read()
                image_str = f"data:image/{file.filename.split('.')[-1]};base64,{file_to_base64(file_content)}"

            # Collect parameters
            parameters = {}
            for key, value in request.form.items():
                if key.startswith('parameter-') and value:
                    parameter_id = int(key.split('-')[1])
                    parameters[parameter_id] = float(value)

            # Add bearing to database
            new_bearing = add_bearing(product_code, manufacturer_id, category_id, bearing_describe, image_str, parameters)

            return "Thêm vòng bi thành công"
        except Exception as e:
            return f"Lỗi: {e}", 400

    return render_template('themvongbi.html', 
                           listCategory=Category.select(Category.idCategory, Category.categoryName),
                           listManufacturer=Manufacturer.select(Manufacturer.idManufacturer, Manufacturer.manufacturerName),
                           listParameter=Parameter.select())


@app.route('/suavongbi/<int:bearing_id>', methods=['GET', 'POST'])
def suavongbi(bearing_id):
    bearing = get_bearing_by_id(bearing_id)
    if request.method == 'POST':
        try:
            # Get updated bearing info
            product_code = request.form.get('productCode')
            manufacturer_id = request.form.get('manufacturer')
            category_id = request.form.get('category')
            bearing_describe = request.form.get('description')

            # Handle image upload
            file = request.files.get('pictureFile')
            image_str = None
            if file:
                file_content = file.read()
                image_str = f"data:image/{file.filename.split('.')[-1]};base64,{file_to_base64(file_content)}"

            # Collect parameters
            parameters = {}
            for key, value in request.form.items():
                if key.startswith('parameter-') and value:
                    parameter_id = int(key.split('-')[1])
                    parameters[parameter_id] = float(value)

            # Update bearing in database
            update_bearing(bearing_id, product_code, manufacturer_id, category_id, bearing_describe, image_str, parameters)

            return "Cập nhật vòng bi thành công"
        except Exception as e:
            return f"Lỗi: {e}", 400

    # Create parameter_dict for GET request
    parameter_dict = {bp.idParameter.idParameter: bp.value for bp in bearing.parameters}

    return render_template('suavongbi.html', 
                           bearing=bearing,
                           listCategory=Category.select(Category.idCategory, Category.categoryName),
                           listManufacturer=Manufacturer.select(Manufacturer.idManufacturer, Manufacturer.manufacturerName),
                           listParameter=Parameter.select(),
                           parameter_dict=parameter_dict)


@app.route('/suachungloai/<int:category_id>', methods=['GET', 'POST'])
def suachungloai(category_id):
    category = Category.get_by_id(category_id)
    if request.method == 'POST':
        categoryName = request.form.get('categoryName')
        file = request.files.get('pictureFile')
        try:
            if file:
                file_content = file.read()
                image_str = f"data:image/{file.filename.split('.')[-1]};base64,{file_to_base64(file_content)}"
                category.categoryPicture = image_str
            category.categoryName = categoryName
            category.save()
            return "Cập nhật thành công"
        except Exception as e:
            return f"Lỗi: {e}", 400
    return render_template('suachungloai.html', category=category)


@app.route('/suahangsx/<int:manufacturer_id>', methods=['GET', 'POST'])
def suahangsx(manufacturer_id):
    manufacturer = Manufacturer.get_by_id(manufacturer_id)
    if request.method == 'POST':
        manufacturerName = request.form.get('manufacturerName')
        file = request.files.get('pictureFile')
        try:
            if file:
                file_content = file.read()
                image_str = f"data:image/{file.filename.split('.')[-1]};base64,{file_to_base64(file_content)}"
                manufacturer.manufacturerPicture = image_str
            manufacturer.manufacturerName = manufacturerName
            manufacturer.save()
            return "Cập nhật thành công"
        except Exception as e:
            return f"Lỗi: {e}", 400
    return render_template('suahangsx.html', manufacturer=manufacturer)


if __name__ == '__main__':
    app.run(debug=True)