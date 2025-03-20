function mascaraMatricula(matricula){
    let valor = matricula.value;
    valor = valor.replace(/\D/g, ''); // Remove tudo que não for dígito
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2"); // Coloca o hífen
    valor = valor.replace(/(\d{3})(\d{1})$/, "$1-$2"); // Coloca o hífen
    matricula.value = valor;
}

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
  const overlay = document.getElementById('overlay');
  const infoBox = document.getElementById('infoBox');
  const closeButton = document.getElementById('closeButton');

  interrogacao.addEventListener('click', () => {
      overlay.style.display = 'block';
      infoBox.style.display = 'block';
  });

  closeButton.addEventListener('click', () => {
      overlay.style.display = 'none';
      infoBox.style.display = 'none';
  });

  overlay.addEventListener('click', () => {
      overlay.style.display = 'none';
      infoBox.style.display = 'none';
  });