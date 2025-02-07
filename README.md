# mysql_config_dff
Python & MYSQL 

## 🖥️ 만든 이유
MySQL 프로젝트를 진행하다 보면 여러 인스턴스를 사용하게 되는데, 같은 서비스의 인스턴스끼리 설정(config)을 비교해야 할 일이 자주 발생합니다.

### 📌 기능  
- MySQL Instance간 Config 비교 / 검색

### Requiremaent
 - 방화벽 설정 ( Local PC(WIndow) -> MySQL )
 - Python Module
   - pandas / PyMYSQL / openpyxl
 - 접속DB 계정 정보
 - DB 정보 엑셀 파일
 - ![image](https://github.com/user-attachments/assets/f3122330-6408-4d2e-a127-3dc62d8e9624)


### 실행 방법
```
pip install pandas
pip install PyMySQL 
pip install openpyxl

python [파이썬코드파일] --save_path [DB접속 정보 엑셀 파일 위치]

C:\Users\user201203\Desktop\python\mysql_config_diff> python mysql_config_diff.py --save_path C:\Users\user201203\Desktop\python\mysql_config_diff\connection_list.xlsx
[['game', 'aws_3306', '43.203.199.175', 3306], ['game', 'aws_3307', '43.203.199.175', 3307], ['game', 'aws_3308', '43.203.199.175', 3308]]
```

### 결과 화면
![image](https://github.com/user-attachments/assets/10a57675-f668-4a15-b501-500a8c7ff7f5)
