from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
    # не, мне нравятся ваши рецепты ;)
}


class RecipeView(View):
    def get(self, request, recipe_name):
        servings = request.GET.get('servings', 1)  # Получаем параметр servings, по умолчанию 1
        try:
            servings = int(servings)  # Конвертируем в целое число
            if servings < 1:
                return JsonResponse({'error': 'Количество порций должно быть положительным целым числом.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Неверный формат для servings.'}, status=400)

        recipe = DATA.get(recipe_name)
        if not recipe:
            return JsonResponse({'error': 'Рецепт не найден.'}, status=404)

        # Умножаем количество ингредиентов на количество порций
        recipe_scaled = {ingredient: round(amount * servings, 2) for ingredient, amount in recipe.items()}

        context = {
            'recipe': recipe_scaled,
        }

        return JsonResponse(context)
