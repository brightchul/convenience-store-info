# convenience-store-info

## How to use 

- python 환경 세팅을 한다.

```shell
git clone https://github.com/brightchul/convenience-store-info.git
cd convenience-store-info

# venv 생성
python3 -m venv venv

# venv 실행
# linux : bin/activate
# window : Scripts/activate
. ./venv/bin/activate  

# 라이브러리 설치
pip install -r requirements.txt

# 실행 cu, gs, seven11, emart24
python3 ./cu/cu_item.py

# 한번에 전부 실행
python3 multi_runner.py 
```

## Structure

```
.
├── cu
│   └── cu_item.py
├── emart24
│   └── emart24_item.py
├── gs
│   └── gs_item.py
├── seven11
│   └── seven11_item.py
├── multi_runner.py
├── README.md
├── requirements.txt
└── venv
```

## Dependencies

```
beautifulsoup4==4.12.2
certifi==2023.5.7
charset-normalizer==3.1.0
idna==3.4
requests==2.30.0
soupsieve==2.4.1
urllib3==2.0.2
```
