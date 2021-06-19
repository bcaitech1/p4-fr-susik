# OCR Chrome Extension

## demo
<p align="center"><img src="demo.GIF"></p>

## 실행
### Server (server 폴더)
학습된 모델을 다운 받아 server/checkpoints 디렉토리 안에 넣습니다.

- [SATRN](https://drive.google.com/file/d/1-3-Of5bZk5zxwZuetUwpK1VgPVwdhqob/view?usp=sharing)

```
pip install -r requirements.txt
python main.py
```


### Chrome Extension (boost_susik 폴더)
1. 위에서 서버를 시작한 다음 그에 대응하는 URL을 `content.js` 상단에 변수로 넣습니다.
    ```
    const SERVERL_URL='http://<YOUR_SERVER_IP>:<YOUR_SERVER_PORT>/susik_recognize';
    ```
2.  크롬 주소창에 `chrome://extensions/` 다음 주소를 입력하고, 
`boost_susik`이라는 폴더를 `압축해제된 확장 프로그램을 로드합니다.` 버튼을 클릭하여 로드합니다.

### Mixed Content Error
- HTTPS로 되어있는 웹사이트에서 서버 (HTTP)로 요청을 보내면 mixed content error가 뜨면서 요청이 보내지지 않습니다. 이런경우 크롬에서 서버 주소를 허용해주는 식으로 우회를 합니다.
  - 크롬에서 `chrome://flags/#unsafely-treat-insecure-origin-as-secure` 에 현재 서버 주소를 입력하는 식으로 우회합니다.
