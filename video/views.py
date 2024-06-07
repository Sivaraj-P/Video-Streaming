from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from .models import Video
from .serializers import VideoSerializer
import cv2
import threading

class VideoAPIView(APIView):
    def get(self,request,id=None):
        try:
            if id:
                # queryset=Video.objects.filter(created_by=request.user,id=id).first()
                queryset=Video.objects.filter(id=id).first()
                if not queryset:
                    return Response({"detail":"Invalid Video"},status=status.HTTP_406_NOT_ACCEPTABLE)
                data=VideoSerializer(queryset,context={"request":request}).data
            else:
                queryset=Video.objects.all()
                data=VideoSerializer(queryset,many=True,context={"request":request}).data
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            serializer=VideoSerializer(data=request.data,context={"request":request})
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self,request,id):
        try:
            queryset=Video.objects.filter(created_by=request.user,id=id).first()
            if not queryset:
                return Response({"detail":"Invalid video or you dont have permission"},status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer=VideoSerializer(instance=queryset,data=request.data,partial=True,context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id):
        try:
            queryset=Video.objects.filter(created_by=request.user,id=id).first()
            if not queryset:
                return Response({"detail":"Invalid video or you dont have permission"},status=status.HTTP_406_NOT_ACCEPTABLE)
            queryset.delete()
            return Response({'message':'Video deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return None

    def update(self):
        while True:
            if not self.video.isOpened():
                break

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            break


def stream_media(request, path):
    video = get_object_or_404(Video, file=path)
    camera = VideoCamera(video.file.path)
    return StreamingHttpResponse(gen(camera),content_type='multipart/x-mixed-replace; boundary=frame')
        