from django.contrib import admin

from .models import CustomUser, ReadingList, BookReview, ReviewLike


admin.site.register(CustomUser)
admin.site.register(ReadingList)
admin.site.register(BookReview)
admin.site.register(ReviewLike)

