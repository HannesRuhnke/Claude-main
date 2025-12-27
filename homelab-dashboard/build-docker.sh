#!/bin/bash
# Homelab Dashboard V4 - Docker Build & Push Script
# Baut Images für AMD64, ARM64 und ARMv7 und pushed zu Docker Hub & GHCR

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Konfiguration
DOCKER_USERNAME="${DOCKER_USERNAME:-}"
IMAGE_NAME="homelab-dashboard"
VERSION="v4-ultimate"
PLATFORMS="linux/amd64,linux/arm64,linux/arm/v7"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Homelab Dashboard V4 - Docker Build${NC}"
echo -e "${BLUE}============================================${NC}\n"

# Prüfe Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker ist nicht installiert!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker gefunden${NC}"

# Prüfe Buildx
if ! docker buildx version &> /dev/null; then
    echo -e "${YELLOW}! Buildx nicht gefunden. Installiere...${NC}"
    docker buildx create --use
fi
echo -e "${GREEN}✓ Docker Buildx bereit${NC}"

# Docker Username prüfen
if [ -z "$DOCKER_USERNAME" ]; then
    echo -e "${YELLOW}? Docker Hub Username:${NC}"
    read -r DOCKER_USERNAME
fi

if [ -z "$DOCKER_USERNAME" ]; then
    echo -e "${RED}✗ Docker Username erforderlich!${NC}"
    exit 1
fi

# Docker Login
echo -e "\n${BLUE}Docker Hub Login...${NC}"
if ! docker login; then
    echo -e "${RED}✗ Docker Login fehlgeschlagen!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Login erfolgreich${NC}"

# Build-Optionen
echo -e "\n${YELLOW}Build-Optionen:${NC}"
echo "1) Nur lokal bauen (schnell, nur amd64)"
echo "2) Multi-Platform bauen und pushen (langsam, amd64+arm64+armv7)"
echo "3) Nur pushen (Image bereits gebaut)"
echo -e "${YELLOW}Auswahl [1-3]:${NC}"
read -r BUILD_OPTION

cd homelab-dashboard

case $BUILD_OPTION in
    1)
        # Nur lokal bauen
        echo -e "\n${BLUE}Baue Image lokal (amd64)...${NC}"
        docker buildx build \
            --platform linux/amd64 \
            --load \
            -t $DOCKER_USERNAME/$IMAGE_NAME:latest \
            -t $DOCKER_USERNAME/$IMAGE_NAME:$VERSION \
            -t $DOCKER_USERNAME/$IMAGE_NAME:v4 \
            -f Dockerfile-v4 \
            .

        echo -e "${GREEN}✓ Image gebaut: $DOCKER_USERNAME/$IMAGE_NAME:latest${NC}"
        echo -e "\n${YELLOW}Testen mit:${NC}"
        echo "docker run -p 5000:5000 $DOCKER_USERNAME/$IMAGE_NAME:latest"
        ;;

    2)
        # Multi-Platform Build & Push
        echo -e "\n${BLUE}Baue Multi-Platform Images...${NC}"
        echo -e "${YELLOW}Platforms: $PLATFORMS${NC}"
        echo -e "${YELLOW}Dies kann 10-20 Minuten dauern...${NC}\n"

        docker buildx build \
            --platform $PLATFORMS \
            --push \
            -t $DOCKER_USERNAME/$IMAGE_NAME:latest \
            -t $DOCKER_USERNAME/$IMAGE_NAME:$VERSION \
            -t $DOCKER_USERNAME/$IMAGE_NAME:v4 \
            -t ghcr.io/$DOCKER_USERNAME/$IMAGE_NAME:latest \
            -t ghcr.io/$DOCKER_USERNAME/$IMAGE_NAME:$VERSION \
            -f Dockerfile-v4 \
            --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
            --build-arg VCS_REF=$(git rev-parse --short HEAD) \
            --build-arg VERSION=$VERSION \
            .

        echo -e "${GREEN}✓ Images gebaut und gepusht!${NC}"
        echo -e "\n${GREEN}Verfügbar als:${NC}"
        echo "  - $DOCKER_USERNAME/$IMAGE_NAME:latest"
        echo "  - $DOCKER_USERNAME/$IMAGE_NAME:v4"
        echo "  - $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
        echo "  - ghcr.io/$DOCKER_USERNAME/$IMAGE_NAME:latest"
        ;;

    3)
        # Nur pushen
        echo -e "\n${BLUE}Pushe bestehendes Image...${NC}"
        docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
        docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION
        docker push $DOCKER_USERNAME/$IMAGE_NAME:v4

        echo -e "${GREEN}✓ Images gepusht!${NC}"
        ;;

    *)
        echo -e "${RED}✗ Ungültige Auswahl!${NC}"
        exit 1
        ;;
esac

# Docker Hub URL
echo -e "\n${BLUE}============================================${NC}"
echo -e "${GREEN}✓ Fertig!${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "\n${YELLOW}Docker Hub:${NC}"
echo "https://hub.docker.com/r/$DOCKER_USERNAME/$IMAGE_NAME"

echo -e "\n${YELLOW}Verwendung:${NC}"
echo "docker pull $DOCKER_USERNAME/$IMAGE_NAME:latest"
echo "docker run -p 5000:5000 $DOCKER_USERNAME/$IMAGE_NAME:latest"

echo -e "\n${YELLOW}Unraid:${NC}"
echo "Verwende Template mit Repository: $DOCKER_USERNAME/$IMAGE_NAME:latest"

cd ..
