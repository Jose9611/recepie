from django.db import models
from core.models import User

class Category(models.Model):
    level = models.IntegerField(default=1)
    icon = models.TextField(blank=True, null=True)
    name = models.TextField()
    main_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,related_name='SubCategories')
    icon_url = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    disclaimer = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_added_user')
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_updated_user', blank=True,
                                null=True)

    class Meta:
        db_table = 'Category'
