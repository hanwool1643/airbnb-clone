from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words"

    parameter_name = "word" #url

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"), #첫번째는 url, 두번째는 어드민패널에 표시
            ("awesome", "Awesome"),
            ("great", "Great"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews

class StarFilter(admin.SimpleListFilter):
    title = "Filter by stars"
    parameter_name = "start"

    def lookups(self, requset, model_admin):
        return [
            ("bad", "Bad"),
            ("good", "Good"),
        ]
    def queryset(self, request, queryset): #self는 class 자체, queryset은 reviews 모두
        star = self.value() # lookups에서 선택한 필터종류
        if star == "bad":
            return queryset.filter(rating__lt=3)
        elif star == "good":
            return queryset.filter(rating__gte=3)
        else:
            return queryset

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        StarFilter,
        "rating",
        "user__is_host",
        "room__categories",
        "room__pet_friendly",
    )
