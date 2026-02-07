#!/bin/bash

# CodeMentor Setup Script

echo "🚀 Setting up CodeMentor..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY before continuing!"
    echo "   Get your API key from: https://console.anthropic.com/"
    read -p "Press enter when you've added your API key..."
fi

echo "🐳 Building Docker containers..."
docker-compose build

echo "🔧 Starting services..."
docker-compose up -d

echo "⏳ Waiting for database to be ready..."
sleep 5

echo "📊 Running migrations..."
docker-compose exec web python manage.py migrate

echo "👤 Creating superuser..."
echo "You'll be prompted to create an admin account:"
docker-compose exec web python manage.py createsuperuser

echo "✅ Setup complete!"
echo ""
echo "🌐 Access the application at: http://localhost:8000"
echo "🔐 Admin panel at: http://localhost:8000/admin"
echo ""
echo "Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"
