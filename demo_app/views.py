from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView

from .models import Student
from .serializers import Student_Serializer


# FUNCTION BASED VIEWS--------------------------------------------------------------------------------------------------
@api_view(['GET','POST'])
def student_list(request):
    if(request.method=="GET"):
        s = Student.objects.all()
        st = Student_Serializer(s,many=True)
        return Response(st.data,status=status.HTTP_200_OK)

    elif(request.method=="POST"):
        d = Student_Serializer(data=request.data)
        if(d.is_valid()):
            d.save()
            return Response(d.data,status=status.HTTP_201_CREATED)
    return Response(d.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def student_details(request,pk):
    try:
        s = Student.objects.get(id=pk)

    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method=="GET"):
        st = Student_Serializer(s)
        return Response(st.data,status=status.HTTP_200_OK)

    elif (request.method == "PUT"):
        d = Student_Serializer(s,data=request.data)
        if (d.is_valid()):
            d.save()
            return Response(d.data, status=status.HTTP_201_CREATED)

    elif (request.method=="DELETE"):
        s.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# CLASS BASED VIEWS-----------------------------------------------------------------------------------------------------
class student_list(APIView):
    def get(self,request):
        s = Student.objects.all()
        st = Student_Serializer(s, many=True)
        return Response(st.data, status=status.HTTP_200_OK)

    def post(self,request):
        d = Student_Serializer(data=request.data)
        if (d.is_valid()):
            d.save()
            return Response(d.data, status=status.HTTP_201_CREATED)
        return Response(d.errors,status=status.HTTP_400_BAD_REQUEST)


class student_details(APIView):

    def get_objects(self,pk):
        try:
            return Student.objects.get(id=pk)

        except Student.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        s = self.get_objects(pk)
        st = Student_Serializer(s)
        return Response(st.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        s = self.get_objects(pk)
        d = Student_Serializer(s, data=request.data)
        if (d.is_valid()):
            d.save()
            return Response(d.data, status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        s = self.get_objects(pk)
        s.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#CLASS BASED VIEWS with MIXINS-----------------------------------------------------------------------------------------

class student_list(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = Student_Serializer
    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)


class student_details(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = Student_Serializer

    def get(self,request,pk):
        return self.retrieve(request,pk)

    def put(self,request,pk):
        return self.update(request,pk)

    def delete(self,request,pk):
        return self.destroy(request,pk)


#CLASS BASED VIEWS with generics-----------------------------------------------------------------------------------------
class student_list(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = Student_Serializer


class student_details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = Student_Serializer

# CLASS BASED VIEWS with ViewSets-----------------------------------------------------------------------------------------
class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = Student_Serializer