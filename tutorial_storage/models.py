from django.db import models

# 이 앱의 "문장쓰기" 데모는 core.comment_store가 제공하는 공용 저장소를 사용한다.
# (로컬 개발: core.Comment ORM 모델 / Vercel KV 연결 시: 실제 Upstash Redis)
