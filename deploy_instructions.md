# 🚀 CEO Dashboard 배포 가이드

## 📋 현재 상태
- Flask 애플리케이션: `ceo_brief_app.py`
- 포트: 8081
- 템플릿: `templates/ceo_dashboard.html`

## 🎯 즉시 배포 방법 (추천)

### 1️⃣ **Render.com (무료, 가장 쉬움)**

#### 준비 작업
```bash
# 1. 포트 설정 수정 (production용)
# ceo_brief_app.py 마지막 줄을 다음으로 변경:
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=False, host='0.0.0.0', port=port)
```

#### 배포 단계
1. **GitHub 저장소 생성**
   - github.com에서 새 저장소 생성
   - 코드 업로드

2. **Render 계정 생성**
   - render.com 접속
   - GitHub로 로그인

3. **Web Service 생성**
   - "New Web Service" 클릭
   - GitHub 저장소 선택
   - 설정:
     - **Name**: `yanadoo-ceo-dashboard`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python ceo_brief_app.py`

4. **자동 배포**
   - 몇 분 후 `https://yanadoo-ceo-dashboard.onrender.com` 형태의 URL 생성

### 2️⃣ **Railway.app (무료, 자동화)**

1. railway.app 접속
2. GitHub로 로그인
3. "Deploy from GitHub repo" 선택
4. 저장소 선택하면 자동 배포

### 3️⃣ **Vercel (정적 사이트)**

Flask를 정적 HTML로 변환:
```bash
# 정적 파일 생성
python generate_static.py
```

### 4️⃣ **ngrok (임시/테스트용)**

현재 로컬 서버를 즉시 공개:
```bash
# ngrok 설치 후
ngrok http 8081
# 생성된 URL로 접근 가능
```

## 🔧 배포 전 수정사항

### requirements.txt 확인
```
Flask==2.3.3
Werkzeug==2.3.7
```

### 환경변수 대응
```python
# ceo_brief_app.py에 추가
import os

# Debug 모드 비활성화
debug_mode = os.environ.get('FLASK_ENV') != 'production'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
```

## 🌟 권장 순서

1. **즉시 테스트**: ngrok 사용
2. **무료 배포**: Render.com 
3. **장기 운영**: AWS/GCP

## 📱 모바일 최적화 (선택사항)

CSS에 반응형 추가:
```css
@media (max-width: 768px) {
    .grid-4 { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr; }
    .grid-2 { grid-template-columns: 1fr; }
}
```

## 🔒 보안 설정 (운영환경)

```python
# 환경변수로 시크릿 키 설정
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# CORS 설정 (필요시)
from flask_cors import CORS
CORS(app)
```

## 📊 접속 방법

배포 완료 후:
- **Desktop**: 브라우저에서 URL 접속
- **Mobile**: 동일 URL로 모바일 최적화 버전 확인
- **관리자**: `/admin` 경로로 데이터 수정

## 🎯 다음 단계

1. 도메인 연결 (선택사항)
2. SSL 인증서 (자동)
3. 모니터링 설정
4. 자동 백업 구성 