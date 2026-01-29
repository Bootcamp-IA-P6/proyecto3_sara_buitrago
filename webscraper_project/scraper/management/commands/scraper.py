from django.core.management.base import BaseCommand
from scraper.services.scrape import scrape_website
from scraper.models import ScrapedDataEdit

class Command(BaseCommand):
    help = "Run the web scraper"
    # Hereda de BaseCommand, lo que permite que este comando sea ejecutable mediante python manage.py <nombre_comando>.

    def handle(self, *args, **kwargs):
        # Ejecuta función
        data = scrape_website()
        print("Scraped Data:", data)  # Agrega esta línea para depurar
        # Guarda
        for item in data:
            ScrapedDataEdit.objects.create(name=item["name"], price=item["price"], discount=item["discount"])
        # Confirma
        self.stdout.write(self.style.SUCCESS("Scraping completed!"))
