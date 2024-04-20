Documentação do Projeto Poli invaders para a disciplina PCS3635 - Laboratório Digital I da Escola Politécnica da USP feito pelos alunos do 3° ano de engenharia de computação:
- Celso Tadaki Sinoka
- Henrique Ramos de Godoy
- Lucas Suzin Bertan

Orientado pelo professor Reginaldo Arakaki, este projeto visa recriar o jogo Space Invaders Utilizando uma FPGA e com visualização em uma matriz de LEDs.

Dentro deste repositório você encontrará todos os códigos em Verilog responsáveis por realizar a lógica do jogo, além do código em python para realizar a conexão MQTT e ser possível de visualizar os pontos feitos em jogo na tela de seu computador. Além dos códigos para Arduino para a utilização de um joystick.

Conteúdo:
- Polinvaders.py: Código em python para a implementação do gêmeo digital, dispondo de uma tela para a visualização dos pontos do jogador ao jogar na placa fpga.
- Polinvaders.ino: Código em ino para o esp32, serve para possibilitar a comunicação da FPGA com o esp e a propagação da contagem de pontos para o broker MQTT do HIVEMQ.
- Polinvaders_final.qar: Código final em qar, arquivo compacto para o quartus, contendo todo o conteúdo do projeto em verilog para ser implementado na FPGA.
