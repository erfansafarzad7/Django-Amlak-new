from django.contrib import admin
from .models import Category, Option, Item, Type, Image


class AllPriceFilter(admin.SimpleListFilter):
    """
    Custom all price admin filter.
    """
    title = 'قیمت کل'
    parameter_name = 'All Price'

    def lookups(self, request, model_admin):
        return (
            (300_000_000, '500/000/000'),
            (500_000_000, '500/000/000'),
            (1_000_000_000, '1/000/000/000'),
            (2_000_000_000, '2/000/000/000'),
            (3_000_000_000, '3/000/000/000'),
            (4_000_000_000, '4/000/000/000'),
            (5_000_000_000, '5/000/000/000'),
            (10_000_000_000, '10/000/000/000'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(total_price__lte=self.value()).order_by('all_price')


class OptionInline(admin.TabularInline):
    model = Item.options.through
    extra = 5


class ImageInline(admin.TabularInline):
    model = Item.images.through
    extra = 5


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # form = ItemAdminForm
    inlines = [OptionInline, ImageInline]
    search_fields = ('code', 'address')
    list_display = ('code', 'type', 'category', 'total_price', 'rent_price', 'area', 'short_description', 'created')
    list_filter = (AllPriceFilter, 'category', 'area', 'type')
    fieldsets = (
        (None, {
            'fields': ('code', )
        }),
        (None, {
            'fields': ('address', 'description', 'notes'),
        }),
        (None, {
            'fields': ('area', 'total_price', 'rent_price'),
        }),
        (None, {
            'fields': ('category', 'type'),
        }),
    )


admin.site.register(Option)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Image)




# class BookInline(admin.TabularInline):
#     model = Book
#     extra = 1
#
#
# inlines = [BookInline]




# class BookInline(admin.TabularInline):
#     model = Library.books.through  # The through model for the Many-to-Many relationship
#     extra = 1
#
#
# inlines = [BookInline]


