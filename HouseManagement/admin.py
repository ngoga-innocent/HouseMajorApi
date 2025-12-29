from django.contrib import admin
from .models import HouseCategory,HouseFeatureAssignment,House,HouseFeatureImage,AdditionalFeatures,HouseImages,Proximity,Agent
from .form import HouseFeatureAssignmentForm
# Register your models here.
admin.site.register(HouseCategory)
admin.site.register(AdditionalFeatures)
# admin.site.register(Agent)
class HouseFeatureImageInline(admin.TabularInline):
    model = HouseFeatureImage
    extra = 1  # how many empty forms to display
class HouseFeatureAssignmentInline(admin.TabularInline):
    model = HouseFeatureAssignment
    form = HouseFeatureAssignmentForm
    extra = 1
    show_change_link = True
class HouseImageInlinde(admin.TabularInline):
    model=HouseImages
    extra=1
    show_change_link=True
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone']
    search_fields = ['name', 'phone']
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    inlines = [HouseFeatureAssignmentInline,HouseImageInlinde]
    list_display = ['id', 'address', 'price', 'payment_category']
    search_fields = ['location', 'description']
@admin.register(HouseFeatureAssignment)
class HouseFeatureAssignmentAdmin(admin.ModelAdmin):
    inlines = [HouseFeatureImageInline]
    list_display = ['house', 'feature','available_number']
    search_fields = ['house__address', 'feature__name']

    class Media:
        js = ('js/conditional_fields.js',)
@admin.register(Proximity)
class Proximity(admin.ModelAdmin):
    model=Proximity
    list_display=['id','name','latitude','longitude']
    list_filter=('created_at',)
