function previewImage(event, previewId) {
    const input = event.target;
    const preview = document.getElementById(previewId);

    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        preview.src = e.target.result;
      };
      reader.readAsDataURL(input.files[0]);
    } else {
      preview.src = "";
    }
  }

  const interrogacao = document.querySelector('.interrogacao');
  const infoBox = document.getElementById('infoBox');
  const closeButton = document.getElementById('closeButton');

  interrogacao.addEventListener('click', () => {
      infoBox.style.display = 'block';
  });

  closeButton.addEventListener('click', () => {
      infoBox.style.display = 'none';
  });