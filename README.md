# FileEncryptionApp
Приложение для шифрование файлов и хранения ключей на сервере.  
## Как это работает
 * Пользователь регистрируется на сервере, где для него создается AES-ключ.
 * Также пользователь генерирует и передает свой открытый RSA-ключ.
 * Для шифрования/дешифровки файлов клиент делает запрос к серверу, чтобы получить ключ AES.
 * Ключ AES шифруется открытым ключом RSA и отправляется клиенту
 * Клиент расшифровывает ключ AES закрытым ключом RSA и использует его для шифрования файла
 * Также алгоритм использует режим AEAD и аутентифицирует файлы с помощью MAC
 * При дешифровке файл проверяется на подлинность
## Как запустить
Сначала запускается сервер, потом клиент
### Запуск сервера
Зайдите в папку  **server**  
Запуск базы данных:
```
 ./run_postgres.sh 
```
Запуск приложения (приложение работает на Flask):  
1) Создайте виртуальное окружение python и установите зависимости:
```
pip3 install -r requirements.txt
```
2) Запуск приложения:
```
python3 app.py
```
### Запуск клиента
Зайдите в папку  **client**  
Установка зависимостей:
```
npm install
```
Запуск приложения (приложение работает на electron.js):
```
npm run start
```

## Как использовать
<img src="https://raw.githubusercontent.com/malmakova-na/FileEncryptionApp/main/images/img1.png" width="40%" height="430px"></img>
<img src="https://raw.githubusercontent.com/malmakova-na/FileEncryptionApp/main/images/img2.png" width="40%" height="410px"></img>
 * При первом входе вам нужно зарегистрироваться по нажатию кнопки "Registrate"
 * Если вы хотите зашифровать файл, то выбирете его по кнопке "Encrypt", после чего будет создан зашифрованный файл в той же папке *имя_файла*.encrypt
 * Для расшифровки файла .encrypt, используйте кнопку  "Decrypt"
