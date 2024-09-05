from django import forms
from catalog.models import Product, ProductVersion

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'content', 'preview', 'category', 'is_published', 'price']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if any(word in title.lower() for word in forbidden_words):
            raise forms.ValidationError("Название товара содержит запрещенные слова.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if any(word in content.lower() for word in forbidden_words):
            raise forms.ValidationError("Описание товара содержит запрещенные слова.")
        return content

class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = ['product', 'version_number', 'version_name', 'is_current']
        widgets = {
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'is_published', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }