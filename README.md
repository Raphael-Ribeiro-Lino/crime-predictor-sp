# Crime Predictor SP – Transformando dados em prevenção e segurança

**Crime Predictor SP** é uma aplicação de Inteligência Artificial desenvolvida pelo grupo **Machine Thinkers**, com o objetivo de prever a quantidade de ocorrências criminais em municípios do estado de **São Paulo**. A aplicação utiliza técnicas de **Machine Learning supervisionado** e oferece uma **interface web interativa**.

---

## Sobre a Aplicação

A previsão de crimes se tornou uma ferramenta essencial para **agências de segurança e órgãos públicos**, permitindo compreender padrões e antecipar onde os crimes são mais prováveis de ocorrer. Com isso, é possível alocar recursos de forma mais eficiente, reduzir a criminalidade e aumentar a **segurança pública**.

O sistema utiliza **dados históricos de criminalidade** de municípios do estado de São Paulo, abrangendo diferentes tipos de crime, como:

- Homicídio Doloso 
- Roubo
- Furto
- Roubo e Furto de veículos

O modelo de **Random Forest Regression** do **scikit-learn** recebe como entrada o **ano, município e tipo de crime**, criando múltiplas “árvores de decisão” para prever a taxa de criminalidade. Em seguida, a média das previsões de todas as árvores gera o valor final, garantindo **alta precisão** em relação a um modelo de árvore única.  

O modelo apresentou uma **precisão de 96,52%** no conjunto de teste, demonstrando robustez e confiabilidade.

---

## Funcionalidades

- Previsão de **4 categorias diferentes de crime**.  
- Cobertura de **10 municípios mais populosos do estado de São Paulo**.  
- Dados históricos de criminalidade para treino e análise.  
- **Random Forest Regression** para previsões precisas.  
- Interface web interativa para seleção de cidade, tipo de crime e ano.  
- Resultado da previsão exibido de forma clara e imediata.  

---

## Link da Aplicação

Acesse a aplicação online: [crime-predictor-sp](https://crime-predictor-sp.onrender.com)  

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Raphael-Ribeiro-Lino/crime-predictor-sp.git
```
Acesse o diretório do projeto:

```bash
cd crime-predictor-sp
```

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

Execute a aplicação:
```bash
python app.py
```

## Como Usar
- Abra a aplicação executando app.py.

- Selecione a cidade, tipo de crime e ano desejados.

- Clique no botão “Prever Casos” para gerar a previsão da taxa de criminalidade.

- O resultado será exibido na tela de forma clara e visual.

## Contribuição

Contribuições são bem-vindas! Para contribuir com o projeto:

- Faça um fork do repositório.

- Crie uma branch para sua feature ou correção de bug.

- Faça as alterações necessárias e realize commit.

- Envie um pull request, explicando detalhadamente suas alterações.

- Certifique-se de seguir as convenções de código do projeto e adicionar testes quando necessário.
