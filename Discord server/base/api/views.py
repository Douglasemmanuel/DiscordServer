from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET/api'
        'GET/api/rooms',
        'GET/api/rooms/:id' ,
    ]
    return Response(routes)



#to enable people accesss our Room data Api
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)   #to serializer our  django model which is in python to JSON FORMAT,we use many=true to convert all to JSON FORMAT
    return Response(serializer.data)  #to access the sterializer we use the variable name.data



#to enable people accesss our Room data Api to open up a room using the Room Api end point
@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)   #to serializer our  django model which is in python to JSON FORMAT,we use many=false to convert all to JSON FORMAT only want the user to see a certain url
    return Response(serializer.data)  #to access the sterializer we use the variable name.data