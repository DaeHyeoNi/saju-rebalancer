FROM python:3.12-slim

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# 의존성 파일 먼저 복사 (레이어 캐시 활용)
COPY pyproject.toml uv.lock* ./

# 의존성 설치 (가상환경 없이 시스템에 직접 설치)
RUN uv sync --frozen --no-dev --no-install-project

# 소스 코드 복사
COPY . .

# 로그 디렉터리 생성
RUN mkdir -p logs

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
