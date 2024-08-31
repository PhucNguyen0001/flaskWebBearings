document.getElementById('formFile').addEventListener('change', function(event) {
            const file = event.target.files[0];
            const imagePreview = document.getElementById('imagePreview');
            const warningMessage = document.getElementById('warningMessage');

            if (file) {
                const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
                if (validImageTypes.includes(file.type)) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        imagePreview.src = e.target.result;
                        imagePreview.style.display = 'block';
                        warningMessage.style.display = 'none';
                    };
                    reader.readAsDataURL(file);
                } else {
                    imagePreview.style.display = 'none';
                    warningMessage.style.display = 'block';
                }
            }
        });