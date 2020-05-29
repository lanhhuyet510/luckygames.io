# luckygames.io

1. Install python3: https://www.python.org/downloads/ 
2. pip3 install requests pyOpenSSL
3. pip3 install secrets (Trên windows sẽ bị fail ở đoạn cuối nhưng vẫn chạy đc)
4. Sửa coin name muốn chơi trong code
5. Sửa HEADER trong code (Login => F12 => Refresh => Bet 1 bet bất kỳ => Click vào request luckygames.io/play/ => Lấy cookie và User-Agent)

Update: một số acc cần sửa cả "Acept-language" (cách lấy tương tự) 

Update: sửa 'hash' ở dòng 30 và 60 trong request (cách làm như trên) 


6. chạy: ``python3 dice45_io-bak.py &``

Có thể chạy bước 6 nhiều lần cho nhanh (tối đa ~10)

7. Bonus: Sửa trong code biến DOMAIN sang cc, cx, ws và chạy lại bước 6 thêm 10 lần => 1 lúc chạy được 40 bot, mạng khoẻ thì cho lên 100 bot cũng được
