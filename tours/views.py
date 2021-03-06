from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from rest_framework import viewsets, serializers
from tours.models import Tour, Zone, User


@login_required()
def index(request):
    tours = Tour.objects.all()
    zones = Zone.objects.all()

    return render(request, "index.html", {"tours": tours, "zonas": zones})


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializador para atender las conversiones para User """

    class Meta:
        # Se define sobre que modelo actua
        model = User
        # Se definen los campos a incluir
        fields = ('id', 'name', 'last_name', 'email',
                  'birthday', 'genre', 'key', 'type')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class TourSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializador para atender las conversiones para User """

    class Meta:
        # Se define sobre que modelo actua
        model = Tour
        # Se definen los campos a incluir
        fields = ('id', 'name', 'operator', 'type',
                  'description', 'img', 'pais',
                  'zonaSalida', 'zonaLlegada')


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all().order_by('id')
    serializer_class = TourSerializer


class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializador para atender las conversiones para User """

    tours = TourSerializer(many=True, read_only=True)

    class Meta:
        # Se define sobre que modelo actua
        model = Zone
        # Se definen los campos a incluir
        fields = ('id', 'name', 'description', 'latitud',
                  'longitud', 'tours_salida', 'tours_llegada')


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all().order_by('id')
    serializer_class = ZoneSerializer
