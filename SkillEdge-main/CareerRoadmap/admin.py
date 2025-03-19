from django.contrib import admin
from .models import Roadmap, RoadmapMilestone, Resource

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class MilestoneInline(admin.TabularInline):
    model = RoadmapMilestone
    extra = 1

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'user__username')
    inlines = [MilestoneInline]

@admin.register(RoadmapMilestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'roadmap', 'order')
    list_filter = ('roadmap',)
    search_fields = ('title', 'description')
    inlines = [ResourceInline]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'milestone')
    list_filter = ('resource_type',)
    search_fields = ('title', 'description')
