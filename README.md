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
```

- 한번에 아이템 실행
```shell
python3 multi_runner.py 
```


- 개별 실행 cu, gs, seven11, emart24
```shell
python -m gs.gs_item 
```



## Structure

```
.
├── cu
│   ├── cu_common.py
│   ├── cu_event.py
│   ├── cu_item.py
│   └── cu_item_pb.py
├── emart24
│   ├── emart24_common.py
│   ├── emart24_event.py
│   └── emart24_item.py
├── gs
│   ├── gs_common.py
│   ├── gs_event.py
│   ├── gs_item.py
│   └── gs_item_pb.py
── seven11
│   ├── seven11_common.py
│   ├── seven11_item.py
│   └── seven11_new_product.py
├── README.md
├── multi_runner.py
├── requirements.txt
└── venv
```

## Dependencies

```
beautifulsoup4==4.12.2
certifi==2023.5.7
charset-normalizer==3.1.0
idna==3.4
requests==2.31.0
soupsieve==2.4.1
urllib3==2.0.2
```
