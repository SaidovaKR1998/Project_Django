from django import forms
from .models import Product

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы - добавляем CSS-классы и атрибуты для всех полей
        """
        super().__init__(*args, **kwargs)

        # Проходим по всем полям формы
        for field_name, field in self.fields.items():
            # Базовые классы Bootstrap для всех полей
            field.widget.attrs['class'] = 'form-control'

            # Добавляем placeholder в зависимости от типа поля
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название продукта...'
                field.widget.attrs['autofocus'] = 'autofocus'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Опишите продукт...'
                field.widget.attrs['rows'] = '4'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'
                field.widget.attrs['min'] = '0'
                field.widget.attrs['step'] = '0.01'
            elif field_name == 'category':
                field.widget.attrs['class'] = 'form-select'  # Специальный класс для select

            # Добавляем aria-label для доступности
            if field.label:
                field.widget.attrs['aria-label'] = f"Поле {field.label}"

            # Для полей с ошибками добавляем специальный класс
            if field_name in self.errors:
                field.widget.attrs['class'] += ' is-invalid'

    def clean_name(self):
        """Проверяем название на отсутствие запрещенных слов."""
        name = self.cleaned_data['name'].lower()

        for word in FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(f"Название содержит запрещенное слово: '{word}'.")

        return self.cleaned_data['name']

    def clean_description(self):
        """Проверяем описание на отсутствие запрещенных слов."""
        description = self.cleaned_data['description'].lower()

        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f"Описание содержит запрещенное слово: '{word}'.")

        return self.cleaned_data['description']

    def clean_price(self):
        """Проверяем, что цена не отрицательная."""
        price = self.cleaned_data.get('price')

        if price is None:
            return price

        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной. Введите положительное значение.")

        if price == 0:
            raise forms.ValidationError("Цена не может быть нулевой. Введите положительное значение.")

        return price