# Contador binário com Raspberry Pi
Este projeto implementa um contador numérico e binário utilizando um Raspberry Pi, cinco LEDs, um display de sete segmentos com quatro dígitos e um registo de deslocamento 74HC595.

O utilizador escolhe um número entre 1 e 31. O objetivo é incrementar o contador até esse valor, apresentando:
- O valor decimal no display de sete segmentos;
- A representação binária através de cinco LEDs;
- O valor atual no terminal.

## Funcionalidades
- Solicita um número entre 1 e 31;
- Valida o valor introduzido;
- Representa números de 1 a 31 em binário através de cinco LEDs;
- Controla um display de sete segmentos com quatro dígitos;
- Utiliza multiplexagem para controlar os dígitos do display;
- Utiliza um registo de deslocamento 74HC595;
- Liberta os pinos GPIO quando o programa é interrompido.

## Material necessário
- Raspberry Pi com Raspberry Pi OS;
- Cinco LEDs;
- Cinco resistências adequadas para os LEDs, por exemplo 220 Ω ou 330 Ω;
- Display de sete segmentos com quatro dígitos;
- Registo de deslocamento 74HC595;
- Resistências adequadas para os segmentos do display;
- Breadboard;
- Cabos jumper.
- Ligações GPIO
- O código utiliza a numeração BCM dos pinos GPIO.

## Registo de deslocamento 74HC595
| Sinal | GPIO BCM | Função | 
|---|---|---| 
| SDI | 24 | Entrada de dados |
| RCLK | 23	| Clock do registo |
| SRCLK	| 18 | Clock de deslocamento|

## LEDs do contador binário
| Posição binária | GPIO BCM |
|---|---|
| Bit 1 | 5 | 
| Bit 2 | 6 |
| Bit 3 | 13 |
| Bit 4 | 19 |
| Bit 5 | 26 |

Os LEDs representam um número binário de cinco bits. Dependendo da ordem física das ligações, o GPIO 5 poderá representar o bit mais significativo e o GPIO 26 o bit menos significativo.

## Seleção dos dígitos do display
|Dígito	|GPIO BCM|
|---|---|
|Dígito 1|	10|
|Dígito 2|	22|
|Dígito 3|	27|
|Dígito 4|	17|

## Requisitos de software
- Python 3;
- Biblioteca RPi.GPIO;
- Raspberry Pi OS ou outro sistema compatível com os pinos GPIO do Raspberry Pi.

A biblioteca pode ser instalada com:

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```
Em sistemas que permitam a instalação através do pip:
```bash
python3 -m pip install RPi.GPIO
````
## Instalação
Clone ou descarregue o projeto:
```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_PROJETO
```
Guarde o código num ficheiro, por exemplo:
```text
contador.py
```
Confirme todas as ligações antes de ligar o circuito. Os LEDs e os segmentos do display devem utilizar resistências adequadas para limitar a corrente.

## Utilização
Execute o programa no Raspberry Pi:

```bash
python3 contador.py
```
Quando solicitado, introduza um número entre 1 e 31:
```text
Nº 1 - 31?: 15
```
Valores fora do intervalo são rejeitados e o programa volta a pedir outro número.

Para terminar a execução, utilize:
```text
Ctrl+C
```
## Funcionamento
### Tabela binária
A variável x contém as representações binárias dos números de 1 a 31:

```python
x = [
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0],
    # ...
    [1, 1, 1, 1, 1]
]
```
Cada posição é enviada para um dos cinco LEDs.

### Display de sete segmentos
A variável number contém os padrões necessários para apresentar os algarismos de 0 a 9:

```python
number = (
    0xc0, 0xf9, 0xa4, 0xb0, 0x99,
    0x92, 0x82, 0xf8, 0x80, 0x90
)
```
A função hc595_shift() envia cada padrão para o registo de deslocamento.

### Multiplexagem
A função pickDigit() ativa apenas um dígito de cada vez. A função loop() alterna rapidamente entre os quatro dígitos, criando a impressão de que todos estão ligados em simultâneo.

### Encerramento
Quando o utilizador pressiona Ctrl+C, a função destroy() é chamada para libertar os recursos GPIO.

### Estrutura das funções
- setup() - configura os pinos GPIO como saídas;
- clearDisplay() - limpa os segmentos do display;
- hc595_shift(data) - envia oito bits para o 74HC595;
- pickDigit(digit) - seleciona um dos quatro dígitos;
- Binary_counter() - atualiza os LEDs e incrementa o contador;
- loop() - atualiza continuamente o display;
- destroy() - limpa a configuração dos GPIO e cancela o temporizador.
