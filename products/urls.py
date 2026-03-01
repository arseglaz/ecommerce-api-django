from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, ProductViewSet, ReviewViewSet

router = SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = router.urls
