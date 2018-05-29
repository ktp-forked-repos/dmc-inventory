from django.db import models
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField


@register_snippet
class ProductCategory(models.Model):
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('text'),
    ]

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"

    def __str__(self):
        return self.text


class ProductPageCategory(Orderable, models.Model):
    page = ParentalKey('ProductPage', on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('category'),
    ]

    def __str__(self):
        return str(self.category)


class ProductType(Page):
    subpage_types = ['ProductPage']
    search_fields = [
        index.SearchField('title'),
    ]

    content_panels = [
        FieldPanel('title'),
    ]


class ProductPage(Page):
    parent_page_types = ['ProductType']
    code = models.CharField(max_length=255)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    description = RichTextField(blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('code'),
        index.SearchField('description', classname="full"),
    ]

    content_panels = [
        FieldPanel('title'),
        FieldPanel('code'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
        InlinePanel('categories', label="Categories"),
    ]

    @property
    def type(self):
        return ProductType.objects.ancestor_of(self).first()
