from django.core.management.base import BaseCommand
from apps.seed import main


class Command(BaseCommand):
	help = 'Seeds the database with initial data'

	def handle(self, *args, **options):
		main()
