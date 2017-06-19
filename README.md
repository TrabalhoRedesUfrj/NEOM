# NEOM
### Universidade Federal do Rio de Janeiro

 *Programa de envio e recebimento de mensagens no modelo Cliente/Servidor.
Por Amanda Camacho, Vinicius Souza e Braian Igreja.* 

Para instalar o programa, rodar o arquivo install no terminal.
```
./install.sh
```
Para instalar como servidor, colocar o argumento --server e para desinstalar, o argumento --uninstall.

Para utilizar o chat, rodar o arquivo Select_Server no servidor:
```
./Select_Server.py
```

Os clientes (que se comunicarão entre si) deverão rodar o arquivo NEOM:
```
./NEOM.py
```
Uma vez iniciado o programa, será requisitado que se faça o login e se digite o IP do servidor com o qual se quer 
comunicar. Se você não tem cadastro, pode selecionar a opção de criar um novo registro. Após se conectar, o *NEOM* pode
ser utilizado como um chat normal.

O programa oferece a segurança de **controle de acesso através** do cadastro de usuários e **confidenciabilidade** 
através de criptografia SSL.