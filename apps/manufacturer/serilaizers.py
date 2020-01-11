from rest_framework import serializers
from .models import Manufacturer, ProductModel

class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = "__all__"

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"


    def validate(self, attrs):
        manufacturer_obj = attrs["vendor"]
        try:
            manufacturer_obj.productmodel_set.get(model_name__exact=attrs["model_name"])
            raise serializers.ValidationError("该型号已经存在")
        except ProductModel.DoesNotExist:
            return attrs

    def to_representation(self, instance):
        vendor = instance.vendor
        ret = super(ProductModelSerializer, self).to_representation(instance)
        ret["vendor"] = {
            "id": vendor.id,
            "name": vendor.vendor_name
        }
        return ret