from django.contrib import admin

from .models import Amenity, Room


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )
    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
    )

    search_fields = ("owner__username",)

    def total_amenities(self, room):
        return room.amenities.count()

    def rating(self, room):
        count = room.reviews.all().count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):
                total_rating += review["rating"]
            avg_rating = total_rating / count
            return round(avg_rating, 2)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
