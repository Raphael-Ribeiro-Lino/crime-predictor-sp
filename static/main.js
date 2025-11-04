window.onload = function () {
  // Referência ao select
  var year = document.getElementById("year-dropdown");

  // Cria a primeira opção "Selecione um ano"
  var defaultOption = document.createElement("OPTION");
  defaultOption.text = "Selecione um ano";
  defaultOption.value = "";
  defaultOption.disabled = true;
  defaultOption.selected = true;
  year.appendChild(defaultOption);

  // Adiciona os anos de 2000 a 2050
  for (var i = 2000; i <= 2050; i++) {
    var option = document.createElement("OPTION");
    option.text = i;
    option.value = i;
    year.appendChild(option);
  }
};
