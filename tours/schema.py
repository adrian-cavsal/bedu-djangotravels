from graphene_django import DjangoObjectType
import graphene

from tours.models import Salida, Tour, User, Zone


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ZoneType(DjangoObjectType):
    class Meta:
        model = Zone


class TourType(DjangoObjectType):
    class Meta:
        model = Tour


class SalidaType(DjangoObjectType):
    class Meta:
        model = Salida


class Query(graphene.ObjectType):
    """ Definición de las respuestas a las consultas posibles """

    # Se definen los posibles campos en las consultas
    all_users = graphene.List(UserType)  # allUsers
    all_zones = graphene.List(ZoneType)  # allZonas
    all_tours = graphene.List(TourType)  # allTours
    all_salidas = graphene.List(SalidaType)  # allSalidas

    # Se define las respuestas para cada campo definido
    def resolve_all_users(self, info, **kwargs):
        # Responde con la lista de todos registros
        return User.objects.all()

    def resolve_all_zones(self, info, **kwargs):
        # Responde con la lista de todos registros
        return Zone.objects.all()

    def resolve_all_tours(self, info, **kwargs):
        # Responde con la lista de todos registros
        return Tour.objects.all()

    def resolve_all_salidas(self, info, **kwargs):
        # Responde con la lista de todos registros
        return Salida.objects.all()


class CreateZone(graphene.Mutation):
    """ Permite realizar la operación de crear en la tabla Zona """

    class Arguments:
        """ Define los argumentos para crear una Zona """
        name = graphene.String(required=True)
        description = graphene.String()
        latitud = graphene.Decimal()
        longitud = graphene.Decimal()

    # El atributo usado para la respuesta de la mutación
    zone = graphene.Field(ZoneType)

    def mutate(self, info, name, description=None, latitud=None,
               longitud=None):
        """
        Se encarga de crear la nueva Zona donde sólo nombre es obligatorio, el
        resto de los atributos son opcionales.
        """
        zone = Zone(
            name=name,
            description=description,
            latitud=latitud,
            longitud=longitud
        )
        zone.save()

        # Se regresa una instancia de esta mutación y como parámetro la Zona
        # creada.
        return CreateZone(zone=zone)


class DeleteZone(graphene.Mutation):
    """ Permite realizar la operación de eliminar en la tabla Zona """
    class Arguments:
        """ Define los argumentos para eliminar una Zona """
        id = graphene.ID(required=True)

    # El atributo usado para la respuesta de la mutación, en este caso sólo se
    # indicará con la variuable ok true en caso de éxito o false en caso
    # contrario
    ok = graphene.Boolean()

    def mutate(self, info, id):
        """
        Se encarga de eliminar la nueva Zona donde sólo es necesario el atributo
        id y además obligatorio.
        """
        try:
            # Si la zona existe se elimina sin más
            zone = Zone.objects.get(pk=id)
            zone.delete()
            ok = True
        except Zone.DoesNotExist:
            # Si la zona no existe, se procesa la excepción
            ok = False
        # Se regresa una instancia de esta mutación
        return DeleteZone(ok=ok)


class UpdateZone(graphene.Mutation):
    """ Permite realizar la operación de modificar en la tabla Zona """
    class Arguments:
        """ Define los argumentos para modificar una Zona """
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        longitud = graphene.Float()
        latitud = graphene.Float()

    # El campo regresado como respuesta de la mutación, en este caso se regresa
    # la zona modificada.
    zone = graphene.Field(ZoneType)

    def mutate(self, info, id, name=None, description=None, longitud=None,
               latitud=None):
        """
        Se encarga de modificar la Zona identificada por el id.
        """
        try:
            # Si la zona existe se modifica
            zone = Zone.objects.get(pk=id)
            # Si algunos de los atributos es proporcionado, entonces se
            # actualiza
            if name is not None:
                zone.name = name
            if description is not None:
                zone.descripcion = description
            if latitud is not None:
                zone.latitud = latitud
            if longitud is not None:
                zone.longitud = longitud
            zone.save()
        except Zone.DoesNotExist:
            # Si la zona no existe, se procesa la excepción
            zone = None
        # Se regresa una instancia de esta mutación
        return UpdateZone(zone=zone)


class CreateTour(graphene.Mutation):
    """ Permite realizar la operación de crear en la tabla Tour """

    class Arguments:
        """ Define los argumentos para crear un Tour """
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        idZonaSalida = graphene.ID(required=True)
        idZonaLlegada = graphene.ID(required=True)
        slug = graphene.String()
        operator = graphene.String()
        type = graphene.String()
        img = graphene.String()
        pais = graphene.String()

    # El atributo usado para la respuesta de la mutación
    tour = graphene.Field(TourType)

    def mutate(self, info, name, description, idZonaSalida, idZonaLlegada,
               slug=None, operator=None, type=None, img=None, pais=None):
        """
        Se encarga de crear un nuevo Tour

        Los atributos obligatorios son:
        - nombre
        - descripcion
        - idZonaSalida
        - idZonaLlegada

        Los atributos opcionales son:
        - slug
        - operador
        - tipoDeTour
        - img
        - pais
        """
        zonaSalida = Zone.objects.get(pk=idZonaSalida)
        zonaLlegada = Zone.objects.get(pk=idZonaLlegada)
        tour = Tour(
            nombre=name,
            descripcion=description,
            zonaSalida=zonaSalida,
            zonaLlegada=zonaLlegada,
            slug=slug,
            operador=operator,
            type=type,
            img=img,
            pais=pais
        )
        tour.save()

        # Se regresa una instancia de esta mutación
        return CreateTour(tour=tour)


class UpdateTour(graphene.Mutation):
    """ Permite realizar la operación de modificar en la tabla Tour """

    class Arguments:
        """ Define los argumentos para modificar un Tour """
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        idZonaSalida = graphene.ID()
        idZonaLlegada = graphene.ID()
        slug = graphene.String()
        operator = graphene.String()
        type = graphene.String()
        img = graphene.String()
        pais = graphene.String()

    # El atributo usado para la respuesta de la mutación
    tour = graphene.Field(TourType)

    def mutate(self, info, id, name=None, description=None, idZonaSalida=None,
               idZonaLlegada=None, slug=None, operator=None, type=None,
               img=None, pais=None):
        """
        Se encarga de modificar un nuevo Tour

        Los atributos obligatorios son:
        - id

        Los atributos opcionales son:
        - nombre
        - descripcion
        - idZonaSalida
        - idZonaLlegada
        - slug
        - operador
        - tipoDeTour
        - img
        - pais
        """
        tour = Tour.objects.get(pk=id)
        if name is not None:
            tour.name = name
        if slug is not None:
            tour.slug = slug
        if idZonaSalida is not None:
            zonaSalida = Zone.objects.get(pk=idZonaSalida)
            tour.zonaSalida = zonaSalida
        if idZonaLlegada is not None:
            zonaLlegada = Zone.objects.get(pk=idZonaLlegada)
            tour.zonaLlegada = zonaLlegada
        if description is not None:
            tour.descripcion = description
        if operator is not None:
            tour.operator = operator
        if type is not None:
            tour.type = type
        if img is not None:
            tour.img = img
        if pais is not None:
            tour.pais = pais
        tour.save()

        # Se regresa una instancia de esta mutación
        return UpdateTour(tour=tour)


class DeleteTour(graphene.Mutation):
    """ Permite realizar la operación de eliminar en la tabla Tour """

    class Arguments:
        """ Define los argumentos para eliminar un Tour """
        id = graphene.ID(required=True)

    # El atributo usado para la respuesta de la mutación
    ok = graphene.Boolean()

    def mutate(self, info, id):
        """
        Se encarga de eliminar un Tour

        Los atributos obligatorios son:
        - id
        """
        try:
            # Si el Tour existe, se elimina
            tour = Tour.objects.get(pk=id)
            tour.delete()
            ok = True
        except Tour.DoesNotExist:
            ok = False

        # Se regresa el estado de la operación
        return DeleteTour(ok=ok)


class Mutation(graphene.ObjectType):
    create_zone = CreateZone.Field()
    delete_zone = DeleteZone.Field()
    update_zone = UpdateZone.Field()
    create_tour = CreateTour.Field()
    delete_tour = DeleteTour.Field()
    update_tour = UpdateTour.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
