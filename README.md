# NEOM
### Universidade Federal do Rio de Janeiro

 *Programa de envio e recebimento de mensagens no modelo Cliente/Servidor.
Por Amanda Camacho, Braian Igreja e Vinicius Souza.* 

Para instalar o programa, rodar o arquivo install no terminal.
```
./install.sh
```
Para instalar como servidor, colocar o argumento --server e para desinstalar, o argumento --uninstall.

A instalação de pacotes do python do install.sh só oferece suporte para Linux (em especial Ubuntu). Se for instalar em
outro sistema Unix, rodar o programa com o argumento --no-pkg e os pacotes terão que ser instalados por fora.

Para utilizar o chat, rodar o arquivo Select_Server no servidor. Se quiser especificar a porta usada, colocar como 
argumento. Caso não seja escolhida nenhuma porta, ele automaticamente usa a 5000.
```
./Select_Server.py
```

Os clientes (que se comunicarão entre si) deverão rodar o arquivo Select_Client.py no terminal, com os argumentos do IP
e a porta, para a versão sem interface gráfica:
```
./Select_Client.py localhost 5000
```
ou o NEOM.py no Shell Script:
```
NEOM.py
```
Uma vez iniciado o programa, será requisitado que se faça o login e se digite o IP do servidor com o qual se quer 
comunicar. Se você não tem cadastro, pode selecionar a opção de criar um novo registro. Após se conectar, o *NEOM* pode
ser utilizado como um chat normal.

O programa oferece a segurança de **controle de acesso** através do cadastro de usuários e **confidenciabilidade** 
através de criptografia SSL. Tem suporte para transmissão de imagens e arquivos em geral, além de outras funcionalidades
como uso de uma interface gráfica amigável.