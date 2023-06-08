from rest_framework import serializers
from .models import Department, Personnel
from django.utils.timezone import now

class DepartmentSerializer(serializers.ModelSerializer):
    
    personnel_count = serializers.SerializerMethodField()     # bu field o deparmenttaki personeli saydırır. Aşağıda get metodu ile function olarak yazmamız lazım.
    
    class Meta:
        model = Department
        fields =("id", "name", "personnel_count")
    
    def get_personnel_count(self, obj):     # bu function ile o department altındaki personeli saydırıyoruz 
        return obj.personals.count()
    
class PersonnelSerializer(serializers.ModelSerializer):
    
    
    day_since_joined = serializers.SerializerMethodField()
    
    create_user_id = serializers.IntegerField(required=False)
    create_user = serializers.StringRelatedField()
    
    class Meta:
        model = Personnel
        fields = "__all__"
        
    # aşağıda, personneli oluşturan user'i göstermek için override ettiğimiz create metodu yerine views.py'da da aynısını yapabiliriz. 
    
    # def create(self, validated_data):
    #     validated_data["create_user_id"] = self.context['request'].user.id
    #     instance = Personnel.objects.create(**validated_data)
    #     return instance
    
    def get_day_since_joined(self, obj):
        return (now() - obj.start_date).days
    
    
class DepartmentPersonnelSerializer(serializers.ModelSerializer):
    
    personnel_count = serializers.SerializerMethodField()
    personals = PersonnelSerializer(many=True, read_only = True)
    
    class Meta:
        model = Department
        fields =("id", "name", "personnel_count", "personals")
    
    def get_personnel_count(self, obj):     
        return obj.personals.count()