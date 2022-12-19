from pathlib import Path
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse

from fpdf import FPDF

from recipes.models import IngredientInRecipe


def create_pdf_shopping_list(request):
    """Сформируй файл pdf со списком покупок."""

    pdf = FPDF(orientation='P', unit='mm', format='A5')
    pdf.add_page()
    font_full_name = Path(
        Path(settings.BASE_DIR).parent,
        'data/DejaVuSansCondensed.ttf'
    )
    pdf.add_font(family='DejaVu', style='', fname=font_full_name, uni=True)

    ingredients = IngredientInRecipe.objects.filter(
        recipe__in_shopping_cart__user=request.user
    ).values_list(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount'))
    pdf.set_font('DejaVu', '', 18)
    pdf.cell(75)
    pdf.cell(h=0, w=15, txt='Список покупок', align='R', ln=2)
    pdf.cell(h=7.5, w=15, txt='', ln=1)
    pdf.set_font('DejaVu', '', 14)
    [pdf.cell(
        h=6.5,
        w=10,
        txt=f'- {ingredient[0]} - '
            f'{ingredient[2]} '
            f'{ingredient[1]}',
        align='L', ln=1) for ingredient in ingredients
     ]

    filename = 'shoppinglist.pdf'
    response = HttpResponse(
        pdf.output(dest='S').encode('latin-1'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = ('attachment;'
                                       f'filename={filename}')
    return response
