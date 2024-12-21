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

  // const interrogacao = document.querySelector('.interrogacao');
  // const infoBox = document.getElementById('infoBox');
  // const closeButton = document.getElementById('closeButton');

  // interrogacao.addEventListener('click', () => {
  //     infoBox.style.display = 'block';
  // });

  // closeButton.addEventListener('click', () => {
  //     infoBox.style.display = 'none';
  // });

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


function mascaraCPF(cpf) {
  let valor = cpf.value;
  valor = valor.replace(/\D/g, ''); // Remove tudo que não for dígito
  valor = valor.replace(/(\d{3})(\d)/, "$1.$2"); // Coloca o primeiro ponto
  valor = valor.replace(/(\d{3})(\d)/, "$1.$2"); // Coloca o segundo ponto
  valor = valor.replace(/(\d{3})(\d{2})$/, "$1-$2"); // Coloca o hífen
  cpf.value = valor;
}

document.querySelector('form').addEventListener('submit', function(event) {
  const cpf = document.getElementById('cpf');
  
  if (cpf.value.length < 14) {
    alert('O CPF deve ter pelo menos 14 caracteres');
    event.preventDefault(); // Impede o envio do formulário
  }
  
});

function togglePasswordVisibility(inputId, toggleButton) {
  const passwordInput = document.getElementById(inputId);

  // Alternar o tipo do input
  if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      toggleButton.innerHTML = '<i class="fas fa-eye-slash"></i>';
  } else {
      passwordInput.type = 'password';
      toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
  }
}

