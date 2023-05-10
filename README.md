# convenience-store-info

## How to use 

- .env_sample을 보고 .env를 생성한다.
- python 환경 세팅을 한다.

```
git clone https://github.com/brightchul/convenience-store-info.git
python3 -m venv venv
. ./venv/bin/activate  # mac, window, linux에 따라 조금씩 다름
pip install -r requirements.txt

python3 ./cu/cu_item.py
```

## Dependencies

```
beautifulsoup4==4.12.2
certifi==2023.5.7
charset-normalizer==3.1.0
idna==3.4
python-dotenv==1.0.0
requests==2.30.0
soupsieve==2.4.1
urllib3==2.0.2
```
