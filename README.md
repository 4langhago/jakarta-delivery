간단 배포/실행 안내

로컬에서 정적 사이트를 서빙하고 WhatsApp 주문 흐름을 확인하려면 다음을 사용하세요.

의존성 설치 (가상환경 권장):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

로컬 서버 실행:

```powershell
python serve_local.py --port 8000
```

브라우저가 자동으로 열리지 않으면 `http://localhost:8000/index.html` 로 접속하세요.

PDF에서 메뉴 이미지 추출:

```powershell
python extract_all_images.py "C:\Users\YOU\Downloads\토박.pdf" --out menu_images
```

PDF 텍스트에서 메뉴 파싱:

```powershell
python read_menu.py --file "C:\Users\YOU\Downloads\menu.pdf" --output parsed_menu.json
```

배포:

- 정적 배포: 이 디렉터리를 GitHub Pages에 푸시하거나, 정적 웹호스팅(S3, Netlify 등)에 업로드하면 됩니다.
- 자동화가 필요하면 알려주세요. 저는 GitHub 리포지토리 생성/푸시 스크립트를 추가해 드릴 수 있습니다.
