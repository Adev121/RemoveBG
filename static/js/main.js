document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');
    const originalImage = document.getElementById('originalImage');
    const processedImage = document.getElementById('processedImage');
    const processingSpinner = document.getElementById('processingSpinner');
    const downloadBtn = document.getElementById('downloadBtn');
    const sampleImages = document.querySelectorAll('.sample-image');

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    // Sample image click handlers
    sampleImages.forEach(img => {
        img.addEventListener('click', () => {
            fetch(img.src)
                .then(response => response.blob())
                .then(blob => {
                    const file = new File([blob], 'sample.jpg', { type: 'image/jpeg' });
                    handleFile(file);
                });
        });
    });

    function handleFile(file) {
        if (!file || !file.type.startsWith('image/')) {
            showError('Please select a valid image file');
            return;
        }

        // Show preview section
        preview.classList.remove('d-none');
        processedImage.classList.add('d-none');
        processingSpinner.classList.remove('d-none');
        downloadBtn.classList.add('d-none');

        // Display original image
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // Process image
        const formData = new FormData();
        formData.append('file', file);

        fetch('/remove-bg', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to process image');
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            processedImage.src = url;
            processedImage.classList.remove('d-none');
            processingSpinner.classList.add('d-none');
            downloadBtn.classList.remove('d-none');

            // Setup download button
            downloadBtn.onclick = () => {
                const a = document.createElement('a');
                a.href = url;
                a.download = 'processed-image.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
        })
        .catch(error => {
            showError(error.message);
            processingSpinner.classList.add('d-none');
        });
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        preview.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
    }
});
