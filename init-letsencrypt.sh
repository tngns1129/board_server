#!/bin/bash

# Docker Compose가 설치되었는지 확인
if ! [ -x "$(command -v docker-compose)" ]; then
  echo '오류: docker-compose가 설치되지 않았습니다.' >&2
  exit 1
fi

# 도메인 설정
domains=(semo962046.duckdns.org)
rsa_key_size=4096
data_path="./data/certbot"
email="semo962046@gmail.com" # 유효한 이메일 주소를 추가하는 것이 좋습니다.
staging=0 # 테스트 중인 경우 1로 설정하여 요청 제한을 피할 수 있습니다.

# 데이터 경로 확인
if [ -d "$data_path" ]; then
  read -p "해당 도메인에 대한 기존 데이터가 발견되었습니다. 계속하고 기존 인증서를 대체하시겠습니까? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

# TLS 매개변수 다운로드
if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "TLS 매개변수를 다운로드합니다..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

# 인증서 및 개인 키 디렉토리 생성 및 권한 설정
echo "인증서 및 개인 키 디렉토리를 생성하고 권한을 설정합니다..."
path="/etc/letsencrypt/live/$domains"
mkdir -p "$path"
chown -R ec2-user "$data_path"

# 더미 인증서 생성
echo "더미 인증서를 생성합니다..."
docker-compose -f docker-compose.yml run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

# Nginx 시작
echo "Nginx를 시작합니다..."
docker-compose -f docker-compose.yml up --force-recreate -d nginx
echo

# 이전 인증서 제거
echo "이전 인증서를 제거합니다..."
docker-compose -f docker-compose.yml run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$domains && \
  rm -Rf /etc/letsencrypt/archive/$domains && \
  rm -Rf /etc/letsencrypt/renewal/$domains.conf" certbot
echo

# Let's Encrypt 인증서 요청
echo "Let's Encrypt 인증서를 요청합니다..."
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

if [ $staging -eq 1 ]; then staging_arg="--staging"; fi

docker-compose -f docker-compose.yml run --rm --entrypoint "\
  certbot certonly --webroot -w
