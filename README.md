# 📦 PC Parts Scraping & Dataset Suite

Um conjunto de scripts Python para realizar scraping, limpeza e organização de informações de hardware de computadores a partir do site **PCPartPicker**. Ideal para montar bancos de dados organizados para análise de mercado, consultas técnicas ou alimentar sistemas de recomendação.

---

## 📁 Estrutura

```
.
├── scraping_partpicker.py  # Scraping de especificações do site PCPartPicker
├── clear_data.py           # Limpeza e estruturação de dados extraídos
├── data/                   # Dados extraídos e processados
└── README.md               # Este arquivo
```

---

## 📦 scraping_partpicker.py

Script para realizar scraping de especificações de componentes de PC no site **[PCPartPicker](https://pcpartpicker.com)**.

### 📌 Funcionalidades:
- Busca a lista de componentes com dados básicos (modelo, link e specs rápidas).
- Se `detail=True`, acessa cada página individual e coleta todas as especificações detalhadas.
- Utiliza **SeleniumBase** e **BeautifulSoup** para controle de navegador e parsing de HTML.
- Salva os dados no diretório `data/` em arquivos `.json`.

### 📝 Como usar:
```bash
pip install seleniumbase beautifulsoup4 tqdm numpy
python scraping_partpicker.py
```

---

## 🧹 clear_data.py

Script para limpar, organizar e padronizar os dados extraídos do **PCPartPicker**.

### 📌 Funcionalidades:
- Lê arquivos JSON brutos gerados pelo scraper.
- Para cada tipo de componente (CPU, GPU, RAM, Storage, PSU, Motherboard), aplica uma função de limpeza que:
  - Renomeia chaves.
  - Converte tipos de dados.
  - Remove ou trata valores ausentes.
- Salva os dados organizados no diretório `data/` com o sufixo `_clean.json`.

### 📝 Como usar:
```bash
python clear_data.py
```

> 📌 Obs: Os componentes a serem processados devem estar ativados no dicionário `components` dentro do script.

---

## 📊 Quantidade de Registros

- **Total de componentes:** _21630_
- **CPUs:** _628_
- **GPUs:** _6496_
- **Placas-mãe:** _1235_
- **Memórias RAM:** _3500_
- **Dispositivos de armazenamento:** _6395_
- **Fontes de alimentação:** _3376_

---

## 📂 Dados Organizados

Os arquivos limpos e padronizados estão no diretório `data/`, estruturados em arquivos JSON separados por categoria, prontos para análises, visualizações ou integração em sistemas.

### 📖 Descrição dos Campos:

#### 🖥️ CPU (`cpu_clean.json`)

| Campo              | Descrição                                                   |
|:------------------|:------------------------------------------------------------|
| `manufacturer`     | Fabricante do processador                                   |
| `model`            | Modelo                                                       |
| `socket`           | Tipo de socket                                               |
| `n_cores`          | Número de núcleos                                            |
| `base_clock_spd`   | Frequência base das Performance Cores                        |
| `boost_clock_spd`  | Frequência boost das Performance Cores                       |
| `consumption`      | Consumo energético (TDP)                                     |
| `integrated_gpu`   | GPU integrada (se houver)                                    |

#### 🎮 GPU (`gpu_clean.json`)

| Campo          | Descrição                   |
|:---------------|:----------------------------|
| `manufacturer` | Fabricante                   |
| `model`        | Modelo                       |
| `consumption`  | Consumo energético (TDP)     |
| `vram`         | Quantidade de VRAM           |
| `vram_spd`     | Frequência da VRAM           |

#### 🖧 Motherboard (`motherboard_clean.json`)

| Campo              | Descrição                                                     |
|:------------------|:--------------------------------------------------------------|
| `manufacturer`     | Fabricante                                                     |
| `model`            | Modelo                                                         |
| `socket`           | Tipo de socket compatível                                      |
| `board_size`       | Formato da placa (ATX, Micro ATX, etc.)                        |
| `n_ram_slots`      | Quantidade de slots de memória RAM                             |
| `Memory Type`      | Tipo de memória compatível                                     |
| `Memory Capacity`  | Capacidade máxima de RAM suportada                             |
| `Supported Ramspeeds` | Velocidades suportadas de RAM                               |
| `SATA`             | Quantidade de portas SATA                                       |
| `M.2`              | Quantidade de slots M.2                                         |
| `PCI-E x1/x4/x8/x16` | Quantidade de slots PCI-Express de cada tipo                  |
| `USB 3 Headers`    | Quantidade de headers USB 3.x                                   |

#### 🧠 RAM (`ram_clean.json`)

| Campo        | Descrição                     |
|:------------|:------------------------------|
| `manufacturer` | Fabricante                  |
| `model`      | Modelo                         |
| `generation` | Geração (DDR4, DDR5...)        |
| `size`       | Tamanho de cada módulo         |
| `frequency`  | Frequência em MHz              |

#### 💾 Storage (`storage_clean.json`)

| Campo        | Descrição                               |
|:-------------|:------------------------------------------|
| `manufacturer` | Fabricante                                |
| `model`      | Modelo                                     |
| `capacity`   | Capacidade de armazenamento                |
| `io`         | Interface (SATA, NVMe, etc.)               |
| `type`       | Tipo de armazenamento (SSD, HDD, etc.)     |
| `rpm`        | Velocidade de rotação (apenas para HDDs)   |

#### ⚡ PSU (`psu_clean.json`)

| Campo        | Descrição                      |
|:-------------|:---------------------------------|
| `manufacturer` | Fabricante                      |
| `model`      | Modelo                            |
| `power`      | Potência total (Watts)             |
| `rate`       | Certificação de eficiência        |

---

## 📦 Dependências

- `seleniumbase`
- `beautifulsoup4`
- `numpy`
- `tqdm`
- `requests`
- `pandas`

Para instalar tudo de uma vez:
```bash
pip install seleniumbase beautifulsoup4 numpy tqdm requests pandas
```

---

## ▶️ Como Rodar

### Scraping:
```bash
python scraping_partpicker.py
```

### Limpeza:
```bash
python clear_data.py
```

Os dados limpos ficarão disponíveis no diretório `data/`, com sufixo `_clean.json`.
