const inputImage = document.querySelector('#id_image');
const selectedImageContainer = document.querySelector('#selected-image-container');
const selectedImage = document.querySelector('#selected-image');

inputImage.addEventListener('change', () => {
    const file = inputImage.files[0];
    if (file) {
        selectedImageContainer.style.display = 'block';
        const imageUrl = URL.createObjectURL(file);
        selectedImage.src = imageUrl;
    } else {
        selectedImageContainer.style.display = 'none';
        selectedImage.src = '';
    }
});
