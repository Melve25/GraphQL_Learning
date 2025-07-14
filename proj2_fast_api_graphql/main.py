import uvicorn
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

# Имитация баз данных
BOOKS_DATA = [
	{
		'id': '1',
		'title': '1984',
		'author': 'George William',
		'publicationYear': 1949
	},
	{
		'id': '2',
		'title': 'Hello World',
		'author': 'Max',
		'publicationYear': 2025
	}
]

# Описание типов данных через strawberry
@strawberry.type
class Book:
	"""
	Описание нашей книги.
	"""
	id: strawberry.ID
	title: str
	author: str
	publicationYear: Optional[int]

# Описание корневой Query
@strawberry.type
class Query:
	""" Корневые запросы API. """
	# В strawberry резолверы - это просто методы класса
	# Имя метода становиться именем поля в GraphQL схеме.

	@strawberry.field(description='Получить все книги')
	def all_books(self) -> List[Book]:
		# Просто возвращаем данные strawberry сам преобразует словари в Book объекты.
		return [Book(**book_data) for book_data in BOOKS_DATA]
	
	@strawberry.field(description='Получить одну книгу по id')
	def book_by_id(self, id: strawberry.ID) -> Optional[Book]:
		# Ищем книгу в списке по id
		for book_data in BOOKS_DATA:
			if book_data['id'] == id:
				return Book(**book_data)
		return None # если книги нету
	

# Создание и запуск приложения

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema)

app = FastAPI()

app.include_router(graphql_app, prefix='/graphql')

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8000)